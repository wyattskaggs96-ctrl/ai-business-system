#!/usr/bin/env python3
"""
Approval State Management

Manages the approval status of generated videos.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

class ApprovalState:
    """Manages approval states for videos."""

    def __init__(self, state_file: str = None):
        if state_file is None:
            # Default to content_engine/output/approval_state.json
            self.state_file = os.path.join(
                os.path.dirname(__file__),
                'output', 'approval_state.json'
            )
        else:
            self.state_file = state_file

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)

        # Load existing state
        self.state = self._load_state()

        # Load existing state
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        """Load state from file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_state(self):
        """Save state to file."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2, default=str)

    def add_video(self, video_data: Dict[str, Any]):
        """Add a new video to the approval queue."""
        content_id = video_data['content_id']

        self.state[content_id] = {
            'content_id': content_id,
            'niche': video_data.get('niche', ''),
            'video_path': video_data.get('video_path', ''),
            'title': video_data.get('title', ''),
            'hook': video_data.get('hook', ''),
            'caption': video_data.get('caption', ''),
            'hashtags': video_data.get('hashtags', ''),
            'filename': video_data.get('filename', ''),  # Add filename
            'status': 'pending_review',
            'created_at': datetime.now(),
            'approved_at': None,
            'rejected_at': None
        }

        self._save_state()

    def update_status(self, content_id: str, status: str):
        """Update the status of a video."""
        if content_id in self.state:
            self.state[content_id]['status'] = status

            if status == 'approved':
                self.state[content_id]['approved_at'] = datetime.now()
            elif status == 'rejected':
                self.state[content_id]['rejected_at'] = datetime.now()

            self._save_state()

    def get_pending_videos(self) -> List[Dict[str, Any]]:
        """Get all videos pending review."""
        return [
            video for video in self.state.values()
            if video['status'] == 'pending_review'
        ]

    def get_approved_videos(self) -> List[Dict[str, Any]]:
        """Get all approved videos."""
        return [
            video for video in self.state.values()
            if video['status'] == 'approved'
        ]

    def get_video(self, content_id: str) -> Dict[str, Any]:
        """Get a specific video by content ID."""
        return self.state.get(content_id, {})

    def regenerate_video(self, content_id: str) -> bool:
        """Mark video for regeneration."""
        if content_id in self.state:
            self.state[content_id]['status'] = 'generated'  # Reset to generated
            self.state[content_id]['approved_at'] = None
            self.state[content_id]['rejected_at'] = None
            self._save_state()
            return True
        return False