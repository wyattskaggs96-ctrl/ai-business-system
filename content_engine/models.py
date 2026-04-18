from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ContentIdea:
    """Represents a basic content idea."""
    niche: str
    topic: str
    template_type: str
    keywords: List[str]

@dataclass
class ContentPost:
    """Represents a generated content post."""
    idea: ContentIdea
    hook: str
    caption: str
    description: str
    cta: str
    full_post: str