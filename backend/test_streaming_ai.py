#!/usr/bin/env python3
"""
Test script for streaming AI endpoint
Run with: python test_streaming_ai.py
"""

import requests
import json
from datetime import datetime
import time

def test_streaming_analysis():
    """Test the streaming AI analyze-opportunity endpoint"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer demo_token"  # Demo mode
    }

    try:
        # Step 1: Get existing post first
        print("📋 Getting existing post...")
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
            print("❌ No existing posts found. Please create a post first using test_ai_endpoint.py")
            return

        # Step 2: Test streaming endpoint
        print(f"\n🌊 Starting streaming AI analysis for post {post_id}...")
        ai_request = {
            "post_id": post_id,
            "enable_cache": True
        }

        # Make streaming request
        with requests.post(
            "http://localhost:8000/api/ai/analyze-opportunity/stream",
            json=ai_request,
            headers=headers,
            stream=True
        ) as response:

            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                print("🌊 Streaming response:")
                print("-" * 50)

                for line in response.iter_lines():
                    if line:
                        try:
                            # Parse each streaming chunk
                            data = json.loads(line.decode('utf-8'))

                            status = data.get('status', 'unknown')
                            message = data.get('message', '')

                            if status == 'starting':
                                print(f"🏁 {message}")
                            elif status == 'analyzing':
                                print(f"🤖 {message}")
                            elif status == 'processing':
                                print(f"⚙️  {message}")
                            elif status == 'extracting_fields':
                                print(f"📊 {message}")
                            elif status == 'company_extracted':
                                print(f"🏢 {message}")
                            elif status == 'contact_extracted':
                                print(f"👤 {message}")
                            elif status == 'finalizing':
                                print(f"✨ {message}")
                            elif status == 'completed':
                                print(f"✅ Analysis completed!")

                                # Show final results
                                result = data.get('result', {})
                                print(f"\n📊 Final Results:")
                                print(f"🎯 Is Opportunity: {result.get('is_opportunity')}")
                                print(f"📈 Confidence: {result.get('confidence', 0):.2f}")
                                print(f"🏷️ Category: {result.get('category', 'N/A')}")
                                print(f"⚡ Urgency: {result.get('urgency', 'N/A')}")

                                # Show extracted fields
                                extracted = result.get('extracted_fields', {})
                                if extracted:
                                    print(f"\n📋 Extracted Fields:")
                                    for field, details in extracted.items():
                                        if isinstance(details, dict) and 'value' in details:
                                            print(f"  - {field}: {details['value']} (confidence: {details.get('confidence', 0):.2f})")
                                        else:
                                            print(f"  - {field}: {details}")

                                # Show company suggestion
                                company = result.get('company_suggestion')
                                if company:
                                    print(f"\n🏢 Company: {company.get('name')} (confidence: {company.get('confidence', 0):.2f})")

                                # Show contact suggestion
                                contact = result.get('contact_suggestion')
                                if contact:
                                    print(f"👤 Contact: {contact.get('name', 'N/A')} (confidence: {contact.get('confidence', 0):.2f})")

                                # Show tags, budget, timeline
                                tags = result.get('tags', [])
                                if tags:
                                    print(f"🏷️ Tags: {', '.join(tags)}")

                                budget = result.get('budget_range')
                                timeline = result.get('timeline')
                                if budget:
                                    print(f"💰 Budget: {budget}")
                                if timeline:
                                    print(f"📅 Timeline: {timeline}")

                            elif status == 'error':
                                print(f"❌ Error: {data.get('error')}")
                                break
                            else:
                                print(f"ℹ️  Status: {status} - {message}")

                        except json.JSONDecodeError as e:
                            print(f"⚠️  Could not parse streaming chunk: {line}")

                print("-" * 50)
                print("🎉 Streaming test completed!")
            else:
                print(f"❌ Streaming request failed: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure backend is running on localhost:8000")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    print("🌊 Testing streaming AI analyze-opportunity endpoint...")
    test_streaming_analysis()
    print("\n✨ Test complete!")