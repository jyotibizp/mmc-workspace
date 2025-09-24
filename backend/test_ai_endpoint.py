#!/usr/bin/env python3
"""
Test script for new unified AI endpoint
Run with: python test_ai_endpoint.py
"""

import requests
import json
from datetime import datetime
import time

def test_analyze_opportunity():
    """Test the new unified AI analyze-opportunity endpoint"""

    # Create a unique post URL to avoid duplicates
    timestamp = int(time.time())
    test_post = {
        "post_url": f"https://www.linkedin.com/posts/test-ai_activity-{timestamp}",
        "author_profile_url": "https://www.linkedin.com/in/test-ai/",
        "content": "Looking for a senior React developer to join our fintech startup. Must have 5+ years experience with TypeScript, Node.js, and AWS. Remote work available. Budget: $80-100k. Need to start ASAP!",
        "scraped_at": datetime.now().isoformat()
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer demo_token"  # Demo mode
    }

    try:
        # Step 1: Try to get existing posts first
        print("📋 Checking for existing posts...")
        response = requests.get(
            "http://localhost:8000/api/linkedin/posts?limit=1",
            headers=headers
        )

        post_id = None
        if response.status_code == 200 and response.json():
            # Use existing post
            post_data = response.json()[0]
            post_id = post_data['id']
            print(f"✅ Using existing post with ID: {post_id}")
        else:
            # Create a new post
            print("📝 Creating new test post...")
            response = requests.post(
                "http://localhost:8000/api/linkedin/ingest",
                json=test_post,
                headers=headers
            )

            if response.status_code != 200:
                print(f"❌ Failed to create post: {response.text}")
                return

            post_data = response.json()
            post_id = post_data['id']
            print(f"✅ Created post with ID: {post_id}")

        # Step 2: Test the new AI analysis endpoint
        print(f"\n🤖 Analyzing opportunity for post {post_id}...")
        ai_request = {
            "post_id": post_id,
            "enable_cache": True
        }

        response = requests.post(
            "http://localhost:8000/api/ai/analyze-opportunity",
            json=ai_request,
            headers=headers
        )

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✅ AI Analysis successful!")
            print(f"🎯 Is Opportunity: {data.get('is_opportunity')}")
            print(f"📊 Confidence: {data.get('confidence', 0):.2f}")
            print(f"🏷️ Category: {data.get('category', 'N/A')}")
            print(f"⚡ Urgency: {data.get('urgency', 'N/A')}")

            # Show extracted fields
            extracted = data.get('extracted_fields', {})
            if extracted:
                print("\n📋 Extracted Fields:")
                for field, details in extracted.items():
                    if isinstance(details, dict) and 'value' in details:
                        print(f"  - {field}: {details['value']} (confidence: {details.get('confidence', 0):.2f})")
                    else:
                        print(f"  - {field}: {details}")

            # Show company suggestion
            company = data.get('company_suggestion')
            if company:
                print(f"\n🏢 Company Suggestion: {company.get('name')} (confidence: {company.get('confidence', 0):.2f})")

            # Show contact suggestion
            contact = data.get('contact_suggestion')
            if contact:
                print(f"👤 Contact Suggestion: {contact.get('name', 'N/A')} (confidence: {contact.get('confidence', 0):.2f})")

            # Show tags
            tags = data.get('tags', [])
            if tags:
                print(f"🏷️ Tags: {', '.join(tags)}")

            # Show budget and timeline
            budget = data.get('budget_range')
            timeline = data.get('timeline')
            if budget:
                print(f"💰 Budget: {budget}")
            if timeline:
                print(f"📅 Timeline: {timeline}")

        else:
            print(f"❌ AI analysis failed: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure backend is running on localhost:8000")
    except Exception as e:
        print(f"❌ Test failed: {e}")

def test_post_not_found():
    """Test error handling for non-existent post"""
    print("\n🧪 Testing error handling with non-existent post...")

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer demo_token"
    }

    ai_request = {
        "post_id": 99999,  # Non-existent post ID
        "enable_cache": True
    }

    try:
        response = requests.post(
            "http://localhost:8000/api/ai/analyze-opportunity",
            json=ai_request,
            headers=headers
        )

        print(f"Status Code: {response.status_code}")
        if response.status_code == 404:
            print("✅ Correctly returned 404 for non-existent post")
        else:
            print(f"❓ Unexpected response: {response.text}")

    except Exception as e:
        print(f"❌ Error test failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing unified AI analyze-opportunity endpoint...")
    test_analyze_opportunity()
    test_post_not_found()
    print("\n✨ Test complete!")