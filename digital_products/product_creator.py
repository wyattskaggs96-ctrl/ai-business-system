from shared.utils import get_logger

class ProductCreator:
    def __init__(self):
        self.logger = get_logger(__name__)

    def create_ebook(self, title, content):
        """Create an e-book from content."""
        # Simple implementation: save to file
        filename = f"{title.replace(' ', '_')}.txt"
        with open(filename, 'w') as f:
            f.write(content)
        self.logger.info(f"Created e-book: {filename}")
        return filename