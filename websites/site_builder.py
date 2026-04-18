from flask import Flask
from shared.utils import get_logger

class SiteBuilder:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.app = Flask(__name__)

    def create_landing_page(self, title, description):
        """Create a simple landing page."""
        @self.app.route('/')
        def home():
            return f"<h1>{title}</h1><p>{description}</p>"

        self.logger.info(f"Created landing page for: {title}")

    def run_server(self):
        """Run the Flask server."""
        self.app.run(debug=True)