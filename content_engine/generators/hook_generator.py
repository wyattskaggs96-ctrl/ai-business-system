import random

# Predefined hooks for different niches
HOOKS = {
    'sports': [
        "What if I told you the greatest athlete never won a championship?",
        "This one play changed the entire game forever",
        "The secret behind every champion's success",
        "Why most athletes fail before they succeed",
        "The untold story that shocked the sports world"
    ],
    'motivation': [
        "What successful people do differently",
        "The one habit that changed my life",
        "Why most people never achieve their dreams",
        "The mindset shift that leads to success",
        "How to turn failure into your greatest strength"
    ],
    'business': [
        "How I built a 7-figure business from scratch",
        "The pricing mistake that almost killed my business",
        "Why most businesses fail in the first year",
        "The marketing strategy that exploded my growth",
        "How to scale without losing your soul"
    ]
}

def generate_hook(niche: str) -> str:
    """Generate a hook for the given niche."""
    return random.choice(HOOKS.get(niche, ["Default hook"]))

def generate_hook_for_idea(idea) -> str:
    """Generate hook based on content idea."""
    return generate_hook(idea.niche)