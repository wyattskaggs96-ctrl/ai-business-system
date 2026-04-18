# AI Business Operating System

A modular Python-based system designed for solo entrepreneurs to automate and scale their AI-powered businesses. This system supports content generation, digital product creation, automation workflows, website building, and analytics tracking.

## Features

- **Content Engine**: Generate high-quality content using AI
- **Video Rendering**: Automatically render TikTok-style videos from content
- **Approval Dashboard**: Review and approve generated videos
- **Digital Products**: Create and manage digital products
- **Automations**: Build and run automated workflows
- **Websites**: Generate landing pages and websites
- **Analytics**: Track performance and user engagement
- **Shared Utilities**: Common configurations and utilities

## Project Structure

```
ai_business_system/
├── README.md
├── requirements.txt
├── .env.example
├── content_engine/
│   ├── README.md
│   └── content_generator.py
├── digital_products/
│   ├── README.md
│   └── product_creator.py
├── automations/
│   ├── README.md
│   └── workflow_runner.py
├── websites/
│   ├── README.md
│   └── site_builder.py
├── analytics/
│   ├── README.md
│   └── tracker.py
├── shared/
│   ├── README.md
│   ├── master_config.py
│   └── utils.py
├── docs/
│   └── README.md
└── scripts/
    ├── README.md
    └── run_system.py
```

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your API keys
4. Run the system: `python scripts/run_system.py`

## Usage

Each module can be used independently or integrated into larger workflows. See individual READMEs in each folder for details.

## Contributing

This is a solo-operated system, but feel free to fork and adapt for your needs.
