# Content Engine

This module handles AI-powered content generation for blogs, social media, emails, and more. It also includes automatic video rendering for TikTok-style content.

## Features

- AI-powered content generation
- Multiple content templates (hot takes, rankings, etc.)
- Platform-specific packaging
- Automatic video rendering
- Approval state management

## Usage

```python
from content_engine.content_generator import ContentGenerator

generator = ContentGenerator()
content = generator.generate_blog_post("AI in Business")
```

## Video Rendering

The system can automatically render vertical videos from generated TikTok content:

```python
from content_engine.video_renderer import render_videos_for_niche

# Render videos for all generated TikTok content
videos = render_videos_for_niche('business')
```

## Approval Dashboard

Review generated videos in a web interface:

```bash
python websites/approval_dashboard.py
```

Then open http://localhost:5000 to approve/reject/regenerate videos.