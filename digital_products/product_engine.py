from dataclasses import dataclass
import random
import os

@dataclass
class DigitalProduct:
    """Represents a digital product for sale."""
    title: str
    description: str
    price: float
    file_path: str

# Starter products
PRODUCTS = [
    DigitalProduct(
        title="AI Side Hustle Starter Guide",
        description="Complete guide to building AI-powered side hustles. Includes templates, strategies, and real case studies.",
        price=47.00,
        file_path="products/ai_side_hustle_guide.pdf"
    ),
    DigitalProduct(
        title="TikTok Growth Blueprint",
        description="Step-by-step system for growing your TikTok from 0 to 10K followers. Viral content strategies included.",
        price=67.00,
        file_path="products/tiktok_growth_blueprint.pdf"
    ),
    DigitalProduct(
        title="Content Automation System Guide",
        description="Automate your content creation with AI. Save 10+ hours per week while scaling your business.",
        price=97.00,
        file_path="products/content_automation_guide.pdf"
    )
]

def get_random_product():
    """Get a random product for promotion."""
    return random.choice(PRODUCTS)

def generate_sales_page(product: DigitalProduct) -> str:
    """Generate a markdown sales page for a product."""
    return f"""# {product.title}

## Description
{product.description}

## Price
**${product.price:.2f}**

## What You'll Get
- Instant digital download
- Lifetime access
- Email support for 30 days
- Regular updates

## Why Buy Now?
- Proven strategies that work
- Save time and money
- Join 100+ successful entrepreneurs
- 30-day money-back guarantee

## Get Started
[Buy Now - ${product.price:.2f}](https://yourstore.com/buy/{product.title.lower().replace(' ', '-')})

---
*This product is for educational purposes. Results may vary.*
"""

def inject_product_promotion(content: str) -> str:
    """Inject product promotion into content."""
    product = get_random_product()

    promotion = f"""

🚀 **Want to take your {product.title.split()[1]} game to the next level?**

Check out my **{product.title}** - {product.description[:100]}...

👉 [Get it now for ${product.price:.2f}](https://yourstore.com/buy/{product.title.lower().replace(' ', '-')})

#Entrepreneurship #SideHustle #AI
"""

    return content + promotion

def should_promote() -> bool:
    """Randomly decide if content should include promotion (30% chance)."""
    return random.random() < 0.3