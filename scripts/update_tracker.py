#!/usr/bin/env python3
"""
Business Tracker CLI Tool

Usage:
    python update_tracker.py add      # Add a new business
    python update_tracker.py update   # Update status of a business
    python update_tracker.py print    # Print all businesses
"""

import csv
import os
import sys
import argparse

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from shared.utils import get_logger

logger = get_logger(__name__)

CSV_FILE = 'analytics/business_tracker.csv'
HEADERS = [
    'business_name', 'category', 'status', 'date_started', 'date_launched',
    'estimated_time_to_launch', 'estimated_time_to_revenue', 'current_revenue',
    'automation_level', 'priority', 'notes'
]

def ensure_csv_exists():
    """Create CSV file with headers if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)
        logger.info("Created business_tracker.csv")

def load_businesses():
    """Load all businesses from CSV."""
    ensure_csv_exists()
    businesses = []
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            businesses.append(row)
    return businesses

def save_businesses(businesses):
    """Save businesses to CSV."""
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(businesses)

def add_business():
    """Add a new business interactively."""
    print("Adding a new business:")
    business = {}
    for header in HEADERS:
        value = input(f"{header}: ")
        business[header] = value

    businesses = load_businesses()
    businesses.append(business)
    save_businesses(businesses)
    logger.info(f"Added business: {business['business_name']}")

def update_status():
    """Update status of an existing business."""
    businesses = load_businesses()
    if not businesses:
        print("No businesses found.")
        return

    print("Available businesses:")
    for i, b in enumerate(businesses):
        print(f"{i+1}. {b['business_name']} - {b['status']}")

    try:
        choice = int(input("Select business number: ")) - 1
        if 0 <= choice < len(businesses):
            new_status = input("New status (idea/building/live/scaling/paused/killed): ")
            businesses[choice]['status'] = new_status
            save_businesses(businesses)
            logger.info(f"Updated status for {businesses[choice]['business_name']} to {new_status}")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

def print_businesses():
    """Print all businesses in a table format."""
    businesses = load_businesses()
    if not businesses:
        print("No businesses found.")
        return

    print(f"{'Business Name':<20} {'Category':<10} {'Status':<10} {'Priority':<8} {'Revenue':<8}")
    print("-" * 60)
    for b in businesses:
        print(f"{b['business_name']:<20} {b['category']:<10} {b['status']:<10} {b['priority']:<8} {b['current_revenue']:<8}")

def main():
    parser = argparse.ArgumentParser(description="Business Tracker CLI")
    parser.add_argument('command', choices=['add', 'update', 'print'], help="Command to run")

    args = parser.parse_args()

    if args.command == 'add':
        add_business()
    elif args.command == 'update':
        update_status()
    elif args.command == 'print':
        print_businesses()

if __name__ == "__main__":
    main()