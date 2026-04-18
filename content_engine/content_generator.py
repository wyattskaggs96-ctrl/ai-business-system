import openai
from shared.utils import get_logger
from shared.master_config import Config

class ContentGenerator:
    def __init__(self):
        self.logger = get_logger(__name__)
        openai.api_key = Config.OPENAI_API_KEY

    def generate_blog_post(self, topic):
        """Generate a blog post on the given topic."""
        prompt = f"Write a 500-word blog post about {topic}."
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            content = response.choices[0].message.content.strip()
            self.logger.info(f"Generated content for topic: {topic}")
            return content
        except Exception as e:
            self.logger.error(f"Error generating content: {e}")
            return None