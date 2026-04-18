import pandas as pd
from shared.utils import get_logger

class AnalyticsTracker:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.data = []

    def track_event(self, event_type, data):
        """Track an event."""
        self.data.append({"event": event_type, **data})
        self.logger.info(f"Tracked event: {event_type}")

    def get_report(self):
        """Generate a simple report."""
        df = pd.DataFrame(self.data)
        return df.describe()