# Websites

This module generates and manages websites, landing pages, and web dashboards.

## Features

- Landing page generation
- Video approval dashboard
- Flask-based web applications

## Usage

```python
from websites.site_builder import SiteBuilder

builder = SiteBuilder()
builder.create_landing_page("My Product", description)
```

## Approval Dashboard

Review and approve generated videos:

```bash
python websites/approval_dashboard.py
```

Open http://localhost:5000 in your browser to:
- View pending videos
- Watch video previews
- Approve or reject videos
- Regenerate videos