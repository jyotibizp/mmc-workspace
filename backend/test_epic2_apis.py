#!/usr/bin/env python3
"""
Test script for Epic 2 APIs - Proposals and Campaign Notes
Run with: python test_epic2_apis.py
"""

import requests
import json
from datetime import datetime, timedelta
import time

def test_proposals_api():
    """Test the proposals CRUD and AI generation endpoints"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer demo_token"  # Demo mode
    }

    print("🗂️ Testing Proposals API...")

    try:
        # Step 1: Get existing opportunity to link proposal
        print("📋 Getting existing opportunity...")
        response = requests.get(
            "http://localhost:8000/api/opportunities?limit=1",
            headers=headers
        )

        opportunity_id = None
        if response.status_code == 200 and response.json():
            opportunity_data = response.json()[0]
            opportunity_id = opportunity_data['id']
            print(f"✅ Using existing opportunity with ID: {opportunity_id}")
        else:
            print("❌ No opportunities found. Please create one first.")
            return

        # Step 2: Test AI proposal generation
        print(f"\n🤖 Testing AI proposal generation for opportunity {opportunity_id}...")
        response = requests.post(
            f"http://localhost:8000/api/proposals/generate-ai?opportunity_id={opportunity_id}&additional_context=Test context",
            headers=headers
        )

        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            ai_data = response.json()
            print("✅ AI proposal generation successful!")
            print(f"📄 Generated proposal has {len(ai_data.get('suggested_sections', []))} sections")
            print(f"🎯 Content length: {len(ai_data.get('proposal_content', ''))}")
        else:
            print(f"❌ AI proposal generation failed: {response.text}")
            return

        # Step 3: Test proposal CRUD
        print(f"\n📝 Testing proposal creation...")
        proposal_data = {
            "opportunity_id": opportunity_id,
            "title": "Test Proposal - Epic 2 Validation",
            "content": ai_data.get('proposal_content', 'Test content'),
            "status": "draft"
        }

        response = requests.post(
            "http://localhost:8000/api/proposals/",
            json=proposal_data,
            headers=headers
        )

        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            proposal = response.json()
            proposal_id = proposal['id']
            print(f"✅ Proposal created with ID: {proposal_id}")
            print(f"📋 Title: {proposal['title']}")
        else:
            print(f"❌ Proposal creation failed: {response.text}")
            return

        # Step 4: Test export functionality
        print(f"\n📤 Testing proposal export...")
        response = requests.get(
            f"http://localhost:8000/api/proposals/{proposal_id}/export?format=markdown",
            headers=headers
        )

        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Proposal export successful!")
            print(f"📄 Export format: markdown")
        else:
            print(f"❌ Proposal export failed: {response.text}")

        # Step 5: Test proposals list
        print(f"\n📋 Testing proposals list...")
        response = requests.get(
            "http://localhost:8000/api/proposals/",
            headers=headers
        )

        if response.status_code == 200:
            proposals = response.json()
            print(f"✅ Found {len(proposals)} proposals")
        else:
            print(f"❌ Proposals list failed: {response.text}")

        print("🗂️ Proposals API testing complete!\n")

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure backend is running on localhost:8000")
    except Exception as e:
        print(f"❌ Proposals test failed: {e}")

def test_campaigns_api():
    """Test the campaigns and campaign notes CRUD endpoints"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer demo_token"  # Demo mode
    }

    print("📢 Testing Campaigns & Notes API...")

    try:
        # Step 1: Create a campaign
        print("📝 Testing campaign creation...")
        campaign_data = {
            "name": "Epic 2 Test Campaign",
            "description": "Testing campaign creation and notes functionality"
        }

        response = requests.post(
            "http://localhost:8000/api/campaigns/",
            json=campaign_data,
            headers=headers
        )

        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            campaign = response.json()
            campaign_id = campaign['id']
            print(f"✅ Campaign created with ID: {campaign_id}")
            print(f"📋 Name: {campaign['name']}")
        else:
            print(f"❌ Campaign creation failed: {response.text}")
            return

        # Step 2: Get existing opportunity for notes
        print("📋 Getting existing opportunity for notes...")
        response = requests.get(
            "http://localhost:8000/api/opportunities?limit=1",
            headers=headers
        )

        opportunity_id = None
        if response.status_code == 200 and response.json():
            opportunity_data = response.json()[0]
            opportunity_id = opportunity_data['id']
            print(f"✅ Using opportunity with ID: {opportunity_id}")
        else:
            print("❌ No opportunities found. Please create one first.")
            return

        # Step 3: Create campaign notes
        print(f"\n📝 Testing campaign note creation...")
        future_date = (datetime.now() + timedelta(days=3)).isoformat()

        note_data = {
            "campaign_id": campaign_id,
            "opportunity_id": opportunity_id,
            "note": "Initial outreach completed. Need to follow up next week.",
            "follow_up_at": future_date
        }

        response = requests.post(
            "http://localhost:8000/api/campaigns/notes",
            json=note_data,
            headers=headers
        )

        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            note = response.json()
            note_id = note['id']
            print(f"✅ Campaign note created with ID: {note_id}")
            print(f"📝 Note: {note['note'][:50]}...")
        else:
            print(f"❌ Campaign note creation failed: {response.text}")
            return

        # Step 4: Test getting campaign notes
        print(f"\n📋 Testing get campaign notes...")
        response = requests.get(
            f"http://localhost:8000/api/campaigns/{campaign_id}/notes",
            headers=headers
        )

        if response.status_code == 200:
            notes = response.json()
            print(f"✅ Found {len(notes)} notes for campaign {campaign_id}")
            for note in notes:
                print(f"  - Note {note['id']}: {note['note'][:30]}...")
        else:
            print(f"❌ Get campaign notes failed: {response.text}")

        # Step 5: Test updating note (mark as completed)
        print(f"\n✅ Testing note completion...")
        update_data = {
            "completed": True
        }

        response = requests.put(
            f"http://localhost:8000/api/campaigns/notes/{note_id}",
            json=update_data,
            headers=headers
        )

        if response.status_code == 200:
            updated_note = response.json()
            print(f"✅ Note marked as completed: {updated_note['completed']}")
        else:
            print(f"❌ Note update failed: {response.text}")

        # Step 6: Test overdue follow-ups
        print(f"\n⏰ Testing overdue follow-ups...")
        # Create an overdue note
        past_date = (datetime.now() - timedelta(days=1)).isoformat()
        overdue_note_data = {
            "campaign_id": campaign_id,
            "opportunity_id": opportunity_id,
            "note": "This follow-up is overdue for testing",
            "follow_up_at": past_date
        }

        requests.post(
            "http://localhost:8000/api/campaigns/notes",
            json=overdue_note_data,
            headers=headers
        )

        response = requests.get(
            "http://localhost:8000/api/campaigns/follow-ups/overdue",
            headers=headers
        )

        if response.status_code == 200:
            overdue_notes = response.json()
            print(f"✅ Found {len(overdue_notes)} overdue follow-ups")
        else:
            print(f"❌ Overdue follow-ups failed: {response.text}")

        # Step 7: Test notes by opportunity
        print(f"\n🎯 Testing notes by opportunity...")
        response = requests.get(
            f"http://localhost:8000/api/campaigns/notes/by-opportunity/{opportunity_id}",
            headers=headers
        )

        if response.status_code == 200:
            opportunity_notes = response.json()
            print(f"✅ Found {len(opportunity_notes)} notes for opportunity {opportunity_id}")
        else:
            print(f"❌ Notes by opportunity failed: {response.text}")

        print("📢 Campaigns & Notes API testing complete!\n")

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure backend is running on localhost:8000")
    except Exception as e:
        print(f"❌ Campaigns test failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing Epic 2 APIs - Proposals & Campaign Notes...")
    print("=" * 60)

    test_proposals_api()
    test_campaigns_api()

    print("=" * 60)
    print("✨ Epic 2 API testing complete!")