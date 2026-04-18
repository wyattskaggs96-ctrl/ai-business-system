import random

# CTA options
CTAS = [
    "Comment below what you think!",
    "Drop a 🔥 if you agree",
    "Share this with someone who needs to hear it",
    "What's your take? Reply below",
    "Tag a friend who needs this",
    "Save this for later!",
    "Follow for more insights",
    "What would you do differently?"
]

def generate_cta() -> str:
    """Generate a random call to action."""
    return random.choice(CTAS)

def generate_cta_for_idea(idea) -> str:
    """Generate CTA for content idea."""
    return generate_cta()