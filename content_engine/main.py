#!/usr/bin/env python3
"""
AI Content Engine CLI

Generate social media content ideas and posts.
"""

import argparse
import random
import sys
import os

# Add content_engine to path
sys.path.append(os.path.dirname(__file__))

from models import ContentIdea, ContentPost
from config import NICHES, TEMPLATE_TYPES
from sources.sports_ideas import SPORTS_TOPICS, SPORTS_KEYWORDS
from sources.motivation_ideas import MOTIVATION_TOPICS, MOTIVATION_KEYWORDS
from sources.business_ideas import BUSINESS_TOPICS, BUSINESS_KEYWORDS
from generators.hook_generator import generate_hook_for_idea
from generators.caption_generator import generate_caption_for_idea
from generators.description_generator import generate_description_for_idea
from generators.cta_generator import generate_cta_for_idea
from templates.hot_take import apply_hot_take_template
from templates.ranking import apply_ranking_template
from templates.controversial import apply_controversial_template
from templates.motivational import apply_motivational_template
from templates.business_lesson import apply_business_lesson_template
from exporters.export import export_to_markdown, export_to_csv

def load_ideas(niche: str):
    """Load content ideas for a niche."""
    if niche == 'sports':
        topics = SPORTS_TOPICS
        keywords = SPORTS_KEYWORDS
    elif niche == 'motivation':
        topics = MOTIVATION_TOPICS
        keywords = MOTIVATION_KEYWORDS
    elif niche == 'business':
        topics = BUSINESS_TOPICS
        keywords = BUSINESS_KEYWORDS
    else:
        return []

    ideas = []
    for topic in topics:
        template = random.choice(TEMPLATE_TYPES)
        idea = ContentIdea(
            niche=niche,
            topic=topic,
            template_type=template,
            keywords=random.sample(keywords, 3)
        )
        ideas.append(idea)
    return ideas

def generate_post(idea: ContentIdea) -> ContentPost:
    """Generate a complete content post from an idea."""
    hook = generate_hook_for_idea(idea)
    caption = generate_caption_for_idea(idea, hook)
    description = generate_description_for_idea(idea)
    cta = generate_cta_for_idea(idea)

    # Apply template
    if idea.template_type == 'hot_take':
        full_post = apply_hot_take_template(idea, hook, caption, description, cta)
    elif idea.template_type == 'ranking':
        full_post = apply_ranking_template(idea, hook, caption, description, cta)
    elif idea.template_type == 'controversial':
        full_post = apply_controversial_template(idea, hook, caption, description, cta)
    elif idea.template_type == 'motivational':
        full_post = apply_motivational_template(idea, hook, caption, description, cta)
    elif idea.template_type == 'business_lesson':
        full_post = apply_business_lesson_template(idea, hook, caption, description, cta)
    else:
        full_post = f"{hook}\n\n{caption}\n\n{description}\n\n{cta}"

    return ContentPost(
        idea=idea,
        hook=hook,
        caption=caption,
        description=description,
        cta=cta,
        full_post=full_post
    )

def generate_batch(niche: str, num_posts: int):
    """Generate a batch of content posts."""
    ideas = load_ideas(niche)
    if not ideas:
        print(f"No ideas found for niche: {niche}")
        return []

    # Randomly select ideas
    selected_ideas = random.sample(ideas, min(num_posts, len(ideas)))

    posts = []
    for idea in selected_ideas:
        post = generate_post(idea)
        posts.append(post)

    return posts

def main():
    parser = argparse.ArgumentParser(description="AI Content Engine")
    parser.add_argument('--niche', choices=NICHES, required=True, help="Content niche")
    parser.add_argument('--num', type=int, default=5, help="Number of posts to generate")
    parser.add_argument('--export', choices=['md', 'csv', 'both'], default='both', help="Export format")

    args = parser.parse_args()

    print(f"Generating {args.num} posts for {args.niche} niche...")

    posts = generate_batch(args.niche, args.num)

    if not posts:
        return

    print(f"Generated {len(posts)} posts.")

    # Export
    if args.export in ['md', 'both']:
        export_to_markdown(posts)
        print("Exported to content_plan.md")

    if args.export in ['csv', 'both']:
        export_to_csv(posts)
        print("Exported to content_plan.csv")

    # Print sample
    print("\nSample post:")
    print(posts[0].full_post)

if __name__ == "__main__":
    main()