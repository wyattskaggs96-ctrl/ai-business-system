# Master Business Tracker

This document outlines the AI Business Tracking System used to monitor all business ideas, projects, and progress within the AI Business Operating System.

## Overview

The tracking system uses a CSV file (`/analytics/business_tracker.csv`) to store business data. The `update_tracker.py` script provides a command-line interface to manage the tracker.

## Columns

- **business_name**: Name of the business or project
- **category**: Category (e.g., content, product, automation, website, analytics)
- **status**: Current status (idea, building, live, scaling, paused, killed)
- **date_started**: Date when work began (YYYY-MM-DD)
- **date_launched**: Date when business went live (YYYY-MM-DD or empty)
- **estimated_time_to_launch**: Estimated days to launch
- **estimated_time_to_revenue**: Estimated days to first revenue
- **current_revenue**: Current monthly revenue ($)
- **automation_level**: Level of automation (low, medium, high)
- **priority**: Priority level (low, medium, high)
- **notes**: Additional notes

## Usage

Use the `update_tracker.py` script to manage businesses:

```bash
# Add a new business
python scripts/update_tracker.py add

# Update status of a business
python scripts/update_tracker.py update

# Print all businesses
python scripts/update_tracker.py print
```

## Status Definitions

- **idea**: Initial concept phase
- **building**: Actively developing
- **live**: Launched and operational
- **scaling**: Growing and optimizing
- **paused**: Temporarily on hold
- **killed**: Discontinued

## Maintenance

Regularly review and update the tracker to track progress and make data-driven decisions.