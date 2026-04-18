import os
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')

def export_to_markdown(posts, filename="content_plan.md"):
    """Export posts to markdown file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w') as f:
        f.write("# Content Plan\n\n")
        for i, post in enumerate(posts, 1):
            f.write(f"## Post {i}\n\n")
            f.write(f"**Niche:** {post.idea.niche}\n")
            f.write(f"**Topic:** {post.idea.topic}\n")
            f.write(f"**Template:** {post.idea.template_type}\n\n")
            f.write("**Full Post:**\n")
            f.write(f"{post.full_post}\n\n")
            f.write("---\n\n")

def export_to_csv(posts, filename="content_plan.csv"):
    """Export posts to CSV file."""
    import csv
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Niche', 'Topic', 'Template', 'Hook', 'Caption', 'Description', 'CTA', 'Full Post'])
        for post in posts:
            writer.writerow([
                post.idea.niche,
                post.idea.topic,
                post.idea.template_type,
                post.hook,
                post.caption,
                post.description,
                post.cta,
                post.full_post.replace('\n', ' | ')
            ])