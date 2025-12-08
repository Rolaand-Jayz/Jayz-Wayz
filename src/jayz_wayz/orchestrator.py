"""CLI orchestrator with demo, checkpoints list, and rollback commands."""

import asyncio
import argparse
import sys
from typing import Optional

from .supervisor import Supervisor
from .state import GraphState


def create_cli_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser.
    
    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        prog="jayz-wayz",
        description="Jayz Wayz - LangGraph supervisor with checkpointing and policy enforcement"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run a demo conversation")
    demo_parser.add_argument(
        "--conversation-id",
        type=str,
        default="demo-conversation",
        help="Conversation ID for the demo"
    )
    demo_parser.add_argument(
        "--checkpoint-dir",
        type=str,
        default="checkpoints",
        help="Directory for checkpoints"
    )
    demo_parser.add_argument(
        "--enable-opa",
        action="store_true",
        help="Enable OPA HTTP policy enforcer"
    )
    demo_parser.add_argument(
        "--opa-url",
        type=str,
        default="http://localhost:8181",
        help="OPA server URL"
    )
    
    # Checkpoints subcommand group
    checkpoints_parser = subparsers.add_parser("checkpoints", help="Checkpoint operations")
    checkpoints_sub = checkpoints_parser.add_subparsers(dest="checkpoint_command")
    
    # List checkpoints
    list_parser = checkpoints_sub.add_parser("list", help="List all checkpoints")
    list_parser.add_argument(
        "--conversation-id",
        type=str,
        help="Filter by conversation ID"
    )
    list_parser.add_argument(
        "--checkpoint-dir",
        type=str,
        default="checkpoints",
        help="Directory for checkpoints"
    )
    
    # Rollback checkpoint
    rollback_parser = checkpoints_sub.add_parser("rollback", help="Rollback to a checkpoint")
    rollback_parser.add_argument(
        "checkpoint_id",
        type=str,
        nargs="?",
        help="Checkpoint ID to rollback to (interactive if not provided)"
    )
    rollback_parser.add_argument(
        "--checkpoint-dir",
        type=str,
        default="checkpoints",
        help="Directory for checkpoints"
    )
    
    return parser


async def run_demo(args: argparse.Namespace) -> int:
    """Run a demo conversation.
    
    Args:
        args: CLI arguments
        
    Returns:
        Exit code
    """
    print(f"🚀 Starting Jayz Wayz demo conversation: {args.conversation_id}")
    print(f"📁 Checkpoint directory: {args.checkpoint_dir}")
    
    if args.enable_opa:
        print(f"🔒 OPA policy enforcement enabled: {args.opa_url}")
    else:
        print("🔒 Using local deny policy enforcer (safe default)")
    
    supervisor = Supervisor(
        checkpoint_dir=args.checkpoint_dir,
        enable_opa=args.enable_opa,
        opa_url=args.opa_url
    )
    
    try:
        # Run the conversation
        final_state = await supervisor.run_conversation(
            conversation_id=args.conversation_id,
            auto_checkpoint=True
        )
        
        # Display results
        print("\n" + "="*60)
        print("📊 Conversation Results")
        print("="*60)
        print(f"Conversation ID: {final_state.conversation_id}")
        print(f"Final Step: {final_state.current_step}")
        print(f"Messages: {len(final_state.messages)}")
        print(f"Checkpoints: {len(final_state.checkpoints)}")
        
        if final_state.error:
            print(f"❌ Error: {final_state.error}")
            return 1
        
        print("\n💬 Messages:")
        for i, msg in enumerate(final_state.messages, 1):
            sender = msg.get("sender", "unknown")
            content = msg.get("content", {})
            text = content.get("text", str(content))
            print(f"  {i}. [{sender}] {text}")
        
        if final_state.checkpoints:
            print(f"\n💾 Latest checkpoint: {final_state.checkpoints[-1]}")
        
        print("\n✅ Demo completed successfully!")
        return 0
        
    finally:
        await supervisor.close()


def list_checkpoints_command(args: argparse.Namespace) -> int:
    """List all checkpoints.
    
    Args:
        args: CLI arguments
        
    Returns:
        Exit code
    """
    from .checkpoint import CheckpointStore
    
    store = CheckpointStore(args.checkpoint_dir)
    checkpoints = store.list_checkpoints(args.conversation_id)
    
    if not checkpoints:
        print("No checkpoints found.")
        return 0
    
    print(f"📋 Checkpoints in {args.checkpoint_dir}:")
    print("="*80)
    
    for cp in checkpoints:
        print(f"ID: {cp['checkpoint_id']}")
        print(f"  Time: {cp['timestamp']}")
        print(f"  Conversation: {cp['conversation_id']}")
        print(f"  Step: {cp['current_step']}")
        print()
    
    print(f"Total: {len(checkpoints)} checkpoint(s)")
    return 0


def rollback_checkpoint_command(args: argparse.Namespace) -> int:
    """Rollback to a checkpoint.
    
    Args:
        args: CLI arguments
        
    Returns:
        Exit code
    """
    from .checkpoint import CheckpointStore
    
    store = CheckpointStore(args.checkpoint_dir)
    
    # If no checkpoint ID provided, show list and prompt
    if not args.checkpoint_id:
        checkpoints = store.list_checkpoints()
        if not checkpoints:
            print("No checkpoints available for rollback.")
            return 1
        
        print("Available checkpoints:")
        for i, cp in enumerate(checkpoints, 1):
            print(f"{i}. {cp['checkpoint_id']} (Time: {cp['timestamp']}, Step: {cp['current_step']})")
        
        try:
            choice = input("\nEnter checkpoint number to rollback (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                print("Cancelled.")
                return 0
            
            idx = int(choice) - 1
            if idx < 0 or idx >= len(checkpoints):
                print("Invalid choice.")
                return 1
            
            checkpoint_id = checkpoints[idx]['checkpoint_id']
        except (ValueError, KeyboardInterrupt):
            print("\nCancelled.")
            return 1
    else:
        checkpoint_id = args.checkpoint_id
    
    # Perform rollback
    state_dict = store.rollback(checkpoint_id)
    
    if not state_dict:
        print(f"❌ Checkpoint '{checkpoint_id}' not found.")
        return 1
    
    restored_state = GraphState.from_dict(state_dict)
    
    print(f"✅ Rolled back to checkpoint: {checkpoint_id}")
    print(f"   Conversation ID: {restored_state.conversation_id}")
    print(f"   Step: {restored_state.current_step}")
    print(f"   Messages: {len(restored_state.messages)}")
    
    return 0


async def async_main() -> int:
    """Async main entry point.
    
    Returns:
        Exit code
    """
    parser = create_cli_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == "demo":
            return await run_demo(args)
        elif args.command == "checkpoints":
            if not args.checkpoint_command:
                print("Error: checkpoints command requires subcommand (list or rollback)")
                return 1
            
            if args.checkpoint_command == "list":
                return list_checkpoints_command(args)
            elif args.checkpoint_command == "rollback":
                return rollback_checkpoint_command(args)
            else:
                print(f"Unknown checkpoint command: {args.checkpoint_command}")
                return 1
        else:
            print(f"Unknown command: {args.command}")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        return 130
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def main() -> None:
    """Main entry point for CLI."""
    exit_code = asyncio.run(async_main())
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
