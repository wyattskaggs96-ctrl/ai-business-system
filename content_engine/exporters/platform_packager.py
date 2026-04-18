import os
from models import ContentPost

# Platform configurations
PLATFORM_CONFIGS = {
    'tiktok': {
        'max_title_length': 60,
        'max_caption_length': 150,
        'hashtags': ['#TikTok', '#Viral', '#Shorts'],
        'posting_notes': 'Post during peak hours (6-9 PM). Use trending sounds. Keep video under 60 seconds.'
    },
    'instagram': {
        'max_title_length': 50,
        'max_caption_length': 200,
        'hashtags': ['#Instagram', '#Reels', '#Content'],
        'posting_notes': 'Post as Reel. Use engaging thumbnail. Add location tag. Engage with comments.'
    },
    'youtube': {
        'max_title_length': 70,
        'max_caption_length': 5000,
        'hashtags': ['#YouTube', '#Shorts', '#Education'],
        'posting_notes': 'Upload as YouTube Short. Add end screen. Enable comments. Use custom thumbnail.'
    }
}

def generate_title(post: ContentPost, platform: str) -> str:
    """Generate platform-specific title."""
    config = PLATFORM_CONFIGS[platform]
    base_title = f"{post.idea.topic} - {post.idea.template_type.replace('_', ' ').title()}"
    return base_title[:config['max_title_length']]

def generate_hook_text(post: ContentPost, platform: str) -> str:
    """Generate hook text for platform."""
    if platform == 'tiktok':
        return f"⚡ {post.hook} ⚡"
    elif platform == 'instagram':
        return f"🔥 {post.hook} 🔥"
    elif platform == 'youtube':
        return f"🚀 {post.hook} 🚀"
    return post.hook

def generate_caption(post: ContentPost, platform: str) -> str:
    """Generate caption for platform."""
    config = PLATFORM_CONFIGS[platform]
    base_caption = f"{post.caption}\n\n{post.description}\n\n{post.cta}"
    return base_caption[:config['max_caption_length']]

def generate_hashtags(post: ContentPost, platform: str) -> str:
    """Generate hashtags for platform."""
    config = PLATFORM_CONFIGS[platform]
    niche_hashtags = [f"#{tag.capitalize()}" for tag in post.idea.keywords]
    return ' '.join(config['hashtags'] + niche_hashtags[:3])

def generate_filename(post: ContentPost, platform: str, index: int) -> str:
    """Generate suggested filename."""
    safe_topic = post.idea.topic.replace(' ', '_').replace('?', '').lower()
    return f"{platform}_{index:02d}_{safe_topic}.txt"

def package_post_for_platform(post: ContentPost, platform: str, index: int):
    """Package a single post for a specific platform."""
    title = generate_title(post, platform)
    hook_text = generate_hook_text(post, platform)
    caption = generate_caption(post, platform)
    hashtags = generate_hashtags(post, platform)
    filename = generate_filename(post, platform, index)
    posting_notes = PLATFORM_CONFIGS[platform]['posting_notes']

    content = f"""TITLE: {title}

HOOK: {hook_text}

CAPTION:
{caption}

HASHTAGS: {hashtags}

CTA: {post.cta}

POSTING NOTES: {posting_notes}

ORIGINAL TOPIC: {post.idea.topic}
TEMPLATE: {post.idea.template_type}
NICHE: {post.idea.niche}
"""

    # Save to file
    output_dir = f"output/{platform}"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        f.write(content)

    return {
        'platform': platform,
        'title': title,
        'filename': filename,
        'topic': post.idea.topic
    }

def package_for_platforms(posts):
    """Package posts for all platforms and create daily queue."""
    packaged_posts = []

    for i, post in enumerate(posts, 1):
        for platform in ['tiktok', 'instagram', 'youtube']:
            packaged = package_post_for_platform(post, platform, i)
            packaged_posts.append(packaged)

    # Create daily post queue
    create_daily_queue(packaged_posts)

def create_daily_queue(packaged_posts):
    """Create daily_post_queue.md with posting schedule."""
    # Simple rotation: TikTok, Instagram, YouTube, repeat
    platforms = ['tiktok', 'instagram', 'youtube']
    queue_content = "# Daily Post Queue\n\n"
    queue_content += "Suggested posting order for maximum reach:\n\n"

    for i, post in enumerate(packaged_posts):
        platform_order = platforms[i % 3]
        if post['platform'] == platform_order:
            queue_content += f"## Post {i//3 + 1}: {post['platform'].title()}\n"
            queue_content += f"- **Title:** {post['title']}\n"
            queue_content += f"- **Topic:** {post['topic']}\n"
            queue_content += f"- **File:** {post['filename']}\n"
            queue_content += f"- **Platform:** {post['platform']}\n\n"

    # Save queue
    filepath = "output/daily_post_queue.md"
    with open(filepath, 'w') as f:
        f.write(queue_content)