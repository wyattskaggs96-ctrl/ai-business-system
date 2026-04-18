# Ranking template

def apply_ranking_template(idea, hook, caption, description, cta):
    """Apply ranking template to generate full post."""
    return f"""📊 TOP 5: {idea.topic.upper()}

{hook}

{caption}

{description}

{cta}

#Ranking #{idea.niche.capitalize()} #Top5"""