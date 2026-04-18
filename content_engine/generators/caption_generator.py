import random

# Caption templates
CAPTION_TEMPLATES = [
    "{hook}\n\n{topic}\n\nWhat do you think?",
    "Breaking down: {topic}\n\n{hook}\n\nShare your thoughts!",
    "{hook}\n\nHere's why {topic} matters.\n\nYour take?",
    "The truth about {topic}:\n\n{hook}\n\nAgree or disagree?"
]

def generate_caption(hook: str, topic: str) -> str:
    """Generate a caption using hook and topic."""
    template = random.choice(CAPTION_TEMPLATES)
    return template.format(hook=hook, topic=topic)

def generate_caption_for_idea(idea, hook: str) -> str:
    """Generate caption for content idea."""
    return generate_caption(hook, idea.topic)