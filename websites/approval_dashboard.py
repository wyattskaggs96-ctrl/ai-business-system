#!/usr/bin/env python3
"""
Video Approval Dashboard

A simple web interface for approving/rejecting generated videos.
"""

import os
import sys
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

# Add project root to path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)

# Import approval state management
sys.path.append(os.path.join(project_root, 'content_engine'))
from content_engine.approval_state import ApprovalState
from content_engine.video_renderer import VideoRenderer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-change-in-production'

# Initialize approval state
approval_state = ApprovalState()

@app.route('/videos/<filename>')
def serve_video(filename):
    """Serve video files from the videos directory."""
    videos_dir = os.path.join(project_root, 'content_engine', 'output', 'videos')
    return send_from_directory(videos_dir, filename)

@app.route('/')
def dashboard():
    """Main dashboard showing pending videos."""
    pending_videos = approval_state.get_pending_videos()
    approved_count = len(approval_state.get_approved_videos())

    return render_template('dashboard.html',
                         pending_videos=pending_videos,
                         approved_count=approved_count)

@app.route('/approve/<content_id>', methods=['POST'])
def approve_video(content_id):
    """Approve a video."""
    approval_state.update_status(content_id, 'approved')
    return redirect(url_for('dashboard'))

@app.route('/reject/<content_id>', methods=['POST'])
def reject_video(content_id):
    """Reject a video."""
    approval_state.update_status(content_id, 'rejected')
    return redirect(url_for('dashboard'))

@app.route('/regenerate/<content_id>', methods=['POST'])
def regenerate_video(content_id):
    """Mark video for regeneration and re-render."""
    video = approval_state.get_video(content_id)
    if video and video.get('filename'):
        # Re-render the video
        renderer = VideoRenderer()
        tiktok_file = os.path.join(
            project_root, 'content_engine', 'output', 'tiktok', video['filename']
        )
        if os.path.exists(tiktok_file):
            try:
                new_video_data = renderer.render_from_tiktok_file(tiktok_file)
                # Update the video data
                approval_state.state[content_id].update({
                    'video_path': new_video_data['video_path'],
                    'status': 'pending_review',
                    'approved_at': None,
                    'rejected_at': None
                })
                approval_state._save_state()
            except Exception as e:
                print(f"Failed to regenerate video {content_id}: {e}")

    return redirect(url_for('dashboard'))

@app.route('/video/<content_id>')
def view_video(content_id):
    """View a specific video."""
    video = approval_state.get_video(content_id)
    if not video:
        return "Video not found", 404

    return render_template('video_detail.html', video=video)

if __name__ == '__main__':
    print("🚀 Starting Video Approval Dashboard")
    print("📱 Open http://localhost:5000 in your browser")
    print("Press Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=5000)