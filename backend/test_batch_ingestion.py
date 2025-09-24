#!/usr/bin/env python3
"""
Quick test script for batch ingestion API
Run with: python test_batch_ingestion.py
"""

import requests
import json
from datetime import datetime

# Test data
test_posts = [
    {
        "post_url": "https://www.linkedin.com/posts/test-user-1_activity-123456789",
        "author_profile_url": "https://www.linkedin.com/in/test-user-1/",
        "content": "Looking for a Python developer for our startup. Remote work available!",
        "scraped_at": datetime.now().isoformat()
    },
    {
        "post_url": "https://www.linkedin.com/posts/test-user-2_activity-987654321",
        "author_profile_url": "https://www.linkedin.com/in/test-user-2/",
        "content": "Need help with React frontend development. Urgent project.",
        "scraped_at": datetime.now().isoformat()
    },
    {
        "post_url": "https://www.linkedin.com/posts/test-user-1_activity-123456789",  # Duplicate
        "author_profile_url": "https://www.linkedin.com/in/test-user-1/",
        "content": "Looking for a Python developer for our startup. Remote work available!",
        "scraped_at": datetime.now().isoformat()
    }
]

def test_batch_ingestion():
    """Test the batch ingestion endpoint"""
    url = "http://localhost:8000/api/linkedin/ingest/batch"

    payload = {
        "posts": test_posts
    }

    headers = {
        "Content-Type": "application/json",
        # Note: In real usage, you'd need proper Auth0 JWT token
        "Authorization": "Bearer demo_token"  # Demo mode
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Batch ingestion successful!")
            print(f"Total: {data['total']}")
            print(f"Successful: {data['successful']}")
            print(f"Duplicates: {data['duplicates']}")
            print(f"Failed: {data['failed']}")

            print("\nResults:")
            for result in data['results']:
                status_emoji = {"success": "✅", "duplicate": "🔁", "failed": "❌"}.get(result['status'], "❓")
                print(f"{status_emoji} {result['post_url']}: {result['status']}")
                if result.get('error'):
                    print(f"   Error: {result['error']}")
        else:
            print(f"❌ Request failed: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure backend is running on localhost:8000")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing batch ingestion API...")
    test_batch_ingestion()