#!/usr/bin/env python3
"""
Video Renderer for AI Content System

Renders TikTok-style videos from generated content posts.
"""

import os
import re
import hashlib
from typing import List, Dict, Any
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from moviepy.config import change_settings

# Set ImageMagick path if needed (for text rendering)
# change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

class VideoRenderer:
    """Handles rendering of TikTok-style videos from content posts."""

    def __init__(self, output_dir: str = None):
        if output_dir is None:
            # Default to content_engine/output/videos/
            self.output_dir = os.path.join(
                os.path.dirname(__file__),
                'output', 'videos'
            )
        else:
            self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

    def generate_content_id(self, platform_file: str) -> str:
        """Generate a deterministic content ID from the platform file."""
        # Use filename hash for deterministic ID
        return hashlib.md5(platform_file.encode()).hexdigest()[:8]

    def parse_tiktok_content(self, filepath: str) -> Dict[str, Any]:
        """Parse TikTok content file and extract video components."""
        with open(filepath, 'r') as f:
            content = f.read()

        # Extract components using regex
        title_match = re.search(r'TITLE: (.+)', content)
        hook_match = re.search(r'HOOK: (.+)', content)
        caption_match = re.search(r'CAPTION:\s*\n(.+?)\n\nHASHTAGS:', content, re.DOTALL)
        hashtags_match = re.search(r'HASHTAGS: (.+)', content)
        niche_match = re.search(r'NICHE: (.+)', content)

        return {
            'title': title_match.group(1) if title_match else '',
            'hook': hook_match.group(1) if hook_match else '',
            'caption': caption_match.group(1).strip() if caption_match else '',
            'hashtags': hashtags_match.group(1) if hashtags_match else '',
            'niche': niche_match.group(1) if niche_match else '',
            'filename': os.path.basename(filepath)
        }

    def split_text_into_lines(self, text: str) -> List[str]:
        """Split text into displayable lines for video."""
        # Split by sentences first
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())

        lines = []
        for sentence in sentences:
            # If sentence is too long, split by commas or words
            if len(sentence) > 50:
                # Split by commas
                parts = sentence.split(',')
                for part in parts:
                    part = part.strip()
                    if part:
                        lines.append(part)
            else:
                lines.append(sentence.strip())

        # Limit to reasonable number of lines for 15-second video
        # Each line 1.5-2 seconds, max 10 lines = 15-20 seconds
        return lines[:10]

    def create_text_clip(self, text: str, duration: float, start_time: float) -> TextClip:
        """Create a text clip with white bold text on black background."""
        return TextClip(
            text,
            fontsize=70,
            color='white',
            font='DejaVuSans-Bold',
            size=(720, 1280),  # 9:16 aspect ratio
            method='label',  # Use PIL instead of ImageMagick
            align='center'
        ).set_position('center').set_duration(duration).set_start(start_time)

    def render_video(self, content_data: Dict[str, Any]) -> str:
        """Render video from content data."""
        content_id = self.generate_content_id(content_data['filename'])

        # Prepare text lines
        all_lines = []

        # Start with hook
        if content_data['hook']:
            all_lines.append(content_data['hook'])

        # Add caption lines
        if content_data['caption']:
            caption_lines = self.split_text_into_lines(content_data['caption'])
            all_lines.extend(caption_lines)

        # Create video clips
        clips = []
        current_time = 0.0

        # Black background
        background = ColorClip(size=(720, 1280), color=(0, 0, 0)).set_duration(15)

        text_clips = []

        for line in all_lines:
            if not line.strip():
                continue

            # Random duration between 1.5-2.0 seconds
            duration = 1.5 + (hash(line) % 50) / 100.0  # Pseudo-random but deterministic

            text_clip = self.create_text_clip(line, duration, current_time)
            text_clips.append(text_clip)

            current_time += duration

            # Stop if we exceed 15 seconds
            if current_time >= 15:
                break

        # Composite video
        if text_clips:
            video = CompositeVideoClip([background] + text_clips)
            # Trim to actual duration
            video = video.set_duration(min(current_time, 15))
        else:
            video = background.set_duration(5)  # Fallback

        # Output path
        output_path = os.path.join(self.output_dir, f"{content_id}.mp4")

        # Render video
        video.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio=False,  # No audio for now
            verbose=False,
            logger=None
        )

        return output_path

    def render_from_tiktok_file(self, tiktok_file: str) -> Dict[str, Any]:
        """Render video from a TikTok content file."""
        content_data = self.parse_tiktok_content(tiktok_file)
        video_path = self.render_video(content_data)

        return {
            'content_id': self.generate_content_id(content_data['filename']),
            'niche': content_data['niche'],
            'video_path': video_path,
            'title': content_data['title'],
            'hook': content_data['hook'],
            'caption': content_data['caption'],
            'hashtags': content_data['hashtags'],
            'filename': content_data['filename'],
            'status': 'generated'
        }

def render_videos_for_niche(niche: str):
    """Render videos for all TikTok files in the output directory."""
    renderer = VideoRenderer()

    tiktok_dir = os.path.join(
        os.path.dirname(__file__),
        'output', 'tiktok'
    )

    rendered_videos = []

    if os.path.exists(tiktok_dir):
        for filename in os.listdir(tiktok_dir):
            if filename.startswith('tiktok_') and filename.endswith('.txt'):
                filepath = os.path.join(tiktok_dir, filename)
                try:
                    video_data = renderer.render_from_tiktok_file(filepath)
                    rendered_videos.append(video_data)
                    print(f"✅ Rendered video: {video_data['content_id']}")
                except Exception as e:
                    print(f"❌ Failed to render {filename}: {e}")

    return rendered_videos

if __name__ == "__main__":
    # Test rendering
    videos = render_videos_for_niche('test')
    print(f"Rendered {len(videos)} videos")