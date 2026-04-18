import random

# Description starters
DESCRIPTION_STARTERS = [
    "In this post, we explore",
    "Let's dive into",
    "Today we're talking about",
    "Here's what you need to know about",
    "Breaking down the concept of"
]

DESCRIPTION_ENDERS = [
    "This could change how you think about it.",
    "What are your thoughts on this approach?",
    "How has this impacted your life?",
    "Share your experiences in the comments!",
    "Let me know if you've tried this before."
]

def generate_description(topic: str) -> str:
    """Generate a short description for the topic."""
    starter = random.choice(DESCRIPTION_STARTERS)
    ender = random.choice(DESCRIPTION_ENDERS)
    return f"{starter} {topic.lower()}. {ender}"

def generate_description_for_idea(idea) -> str:
    """Generate description for content idea."""
    return generate_description(idea.topic)