#!/usr/bin/env python3
"""
Quick API test for the Intelligent Chatbot System
"""

import requests
import json

def test_api():
    """Test the intelligent chatbot API"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Intelligent Chatbot API")
    print("=" * 40)
    
    # Test 1: Health check
    print("\n1. Health Check:")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Chat interaction
    print("\n2. Chat Interaction:")
    try:
        chat_data = {
            "message": "Bonjour, je cherche un cadeau pour ma fille de 8 ans",
            "user_id": "test_user_api"
        }
        response = requests.post(f"{base_url}/chat", json=chat_data)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {result['response'][:100]}...")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Intents: {result['detected_intents']}")
        print(f"   Products: {len(result['products'])}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Intent testing
    print("\n3. Intent Detection Test:")
    try:
        response = requests.get(f"{base_url}/intents/test", params={"message": "Je veux un sac rouge pas cher"})
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Primary Intent: {result['primary_intent']['intent']} ({result['primary_intent']['confidence']:.2f})")
        print(f"   Keywords: {result['primary_intent']['matched_keywords']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: System stats
    print("\n4. System Statistics:")
    try:
        response = requests.get(f"{base_url}/stats")
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Memory Users: {result['system_stats']['conversation_memory']['total_users']}")
        print(f"   Unknown Queries: {len(result['unknown_queries'])}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n✅ API Test Complete!")

if __name__ == "__main__":
    test_api()