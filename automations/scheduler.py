#!/usr/bin/env python3
"""
Content Workflow Scheduler

Automatically runs the content workflow on a schedule.
"""

import argparse
import time
import schedule
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)

from automations.run_content_workflow import run_content_workflow

def run_scheduled_workflow(niche, num_posts):
    """Wrapper for scheduled runs."""
    print(f"\n🕐 Running scheduled workflow: {niche} - {num_posts} posts")
    success = run_content_workflow(niche, num_posts)
    if success:
        print("✅ Scheduled run completed successfully")
    else:
        print("❌ Scheduled run failed")
    return success

def start_scheduler(niche, num_posts, run_time):
    """Start the daily scheduler."""
    print("🚀 Starting Content Workflow Scheduler")
    print(f"📅 Schedule: Daily at {run_time}")
    print(f"📊 Config: {niche} niche, {num_posts} posts")
    print("Press Ctrl+C to stop\n")

    # Schedule the job
    schedule.every().day.at(run_time).do(run_scheduled_workflow, niche=niche, num_posts=num_posts)

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Content Workflow Scheduler")
    parser.add_argument('--niche', choices=['sports', 'motivation', 'business'],
                       default='motivation', help="Content niche (default: motivation)")
    parser.add_argument('--num', type=int, default=5,
                       help="Number of posts to generate (default: 5)")
    parser.add_argument('--time', default='09:00',
                       help="Daily run time in HH:MM format (default: 09:00)")
    parser.add_argument('--run-now', action='store_true',
                       help="Run workflow immediately and exit")

    args = parser.parse_args()

    if args.run_now:
        print("⚡ Running workflow now...")
        success = run_content_workflow(args.niche, args.num)
        sys.exit(0 if success else 1)
    else:
        start_scheduler(args.niche, args.num, args.time)

if __name__ == "__main__":
    main()