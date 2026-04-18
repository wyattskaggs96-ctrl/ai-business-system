#!/usr/bin/env python3
"""
Unified Content Workflow Runner

Runs the complete content generation and packaging workflow.
"""

import argparse
import csv
import os
import sys
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)

from shared.utils import get_logger
from shared.master_config import Config

# Import content engine modules
sys.path.append(os.path.join(project_root, 'content_engine'))
from content_engine.main import generate_batch
from content_engine.exporters.export import export_to_markdown, export_to_csv
from content_engine.exporters.platform_packager import package_for_platforms
from content_engine.video_renderer import render_videos_for_niche
from content_engine.approval_state import ApprovalState

logger = get_logger(__name__)

def log_workflow_run(niche, num_posts, status, error_msg=None):
    """Log the workflow run to CSV."""
    csv_file = os.path.join(project_root, 'analytics', 'workflow_runs.csv')

    # Create file with headers if it doesn't exist
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'niche', 'num_posts', 'status', 'error'])

    # Append the run
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            niche,
            num_posts,
            status,
            error_msg or ''
        ])

def run_content_workflow(niche, num_posts):
    """Run the complete content workflow."""
    print("🚀 Starting AI Business Content Workflow")
    print(f"📊 Niche: {niche}")
    print(f"📈 Number of posts: {num_posts}")
    print("-" * 50)

    try:
        # Step 1: Load config
        print("Step 1: Loading configuration...")
        config = Config()
        logger.info(f"Config loaded: OPENAI_API_KEY present: {bool(config.OPENAI_API_KEY)}")
        print("✅ Config loaded successfully")

        # Step 2: Generate content
        print("\nStep 2: Generating content...")
        posts = generate_batch(niche, num_posts)
        if not posts:
            raise ValueError(f"No posts generated for niche: {niche}")
        print(f"✅ Generated {len(posts)} content posts")

        # Step 3: Export content plan
        print("\nStep 3: Exporting content plan...")
        export_to_markdown(posts)
        export_to_csv(posts)
        print("✅ Exported to content_plan.md and content_plan.csv")

        # Step 4: Run platform packaging
        print("\nStep 4: Packaging for platforms...")
        package_for_platforms(posts)
        print("✅ Packaged for TikTok, Instagram, and YouTube")

        # Step 5: Render videos
        print("\nStep 5: Rendering videos...")
        rendered_videos = render_videos_for_niche(niche)
        print(f"✅ Rendered {len(rendered_videos)} videos")

        # Step 6: Add videos to approval queue
        print("\nStep 6: Adding videos to approval queue...")
        approval_state = ApprovalState()
        for video_data in rendered_videos:
            approval_state.add_video(video_data)
        print(f"✅ Added {len(rendered_videos)} videos to approval queue")

        # Step 7: Generate daily post queue (already done in packaging)
        print("\nStep 7: Daily post queue generated")
        print("✅ Created daily_post_queue.md")

        # Step 8: Log the run
        print("\nStep 8: Logging workflow run...")
        log_workflow_run(niche, num_posts, 'success')
        logger.info(f"Workflow completed successfully for {niche} with {num_posts} posts")
        print("✅ Workflow logged successfully")

        print("\n" + "=" * 50)
        print("🎉 Content workflow completed successfully!")
        print("📁 Check /content_engine/output/ for all generated files")
        print("🎬 Videos rendered and ready for approval")
        print("🌐 Run 'python websites/approval_dashboard.py' to review videos")
        print("=" * 50)

    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Error in workflow: {error_msg}")
        log_workflow_run(niche, num_posts, 'error', error_msg)
        logger.error(f"Workflow failed: {error_msg}")
        print("📝 Error logged to workflow_runs.csv")
        return False

    return True

def main():
    parser = argparse.ArgumentParser(description="Run complete content workflow")
    parser.add_argument('--niche', choices=['sports', 'motivation', 'business'], required=True,
                       help="Content niche")
    parser.add_argument('--num', type=int, default=5, help="Number of posts to generate")

    args = parser.parse_args()

    success = run_content_workflow(args.niche, args.num)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()