#!/usr/bin/env python3
"""
Complete system test for the intelligent e-commerce chatbot
Tests both backend API and off-topic protection
"""

import requests
import json

def test_backend_health():
    """Test backend health"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Health: {data['status']}")
            print(f"   Chatbot: {data['chatbot']}")
            print(f"   Database: {data['database']}")
            print(f"   Memory: {data['memory']}")
            return True
        else:
            print(f"❌ Backend Health Check Failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend Health Check Error: {e}")
        return False

def test_off_topic_protection():
    """Test off-topic protection"""
    off_topic_tests = [
        "Qui est Messi ?",
        "Quel est ton âge ?",
        "Comment réparer mon ordinateur ?",
        "Donne-moi une recette"
    ]
    
    print("\n🚫 Testing Off-Topic Protection:")
    all_passed = True
    
    for message in off_topic_tests:
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"message": message, "user_id": "test_system"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                has_products = len(data.get("products", [])) > 0
                intent = data.get("detected_intents", ["unknown"])[0]
                
                if not has_products and intent in ["off_topic", "personal_question"]:
                    print(f"   ✅ PASS: '{message}' -> No products, {intent} intent")
                else:
                    print(f"   ❌ FAIL: '{message}' -> {len(data.get('products', []))} products, {intent} intent")
                    all_passed = False
            else:
                print(f"   ❌ ERROR: HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            all_passed = False
    
    return all_passed

def test_shopping_functionality():
    """Test shopping functionality"""
    shopping_tests = [
        "Je veux un cadeau pour ma fille",
        "Montrez-moi des casquettes rouges",
        "Budget 50 DT"
    ]
    
    print("\n🛍️ Testing Shopping Functionality:")
    all_passed = True
    
    for message in shopping_tests:
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"message": message, "user_id": "test_system"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                has_products = len(data.get("products", [])) > 0
                intent = data.get("detected_intents", ["unknown"])[0]
                
                if has_products:
                    print(f"   ✅ PASS: '{message}' -> {len(data.get('products', []))} products, {intent} intent")
                else:
                    print(f"   ❌ FAIL: '{message}' -> No products, {intent} intent")
                    all_passed = False
            else:
                print(f"   ❌ ERROR: HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            all_passed = False
    
    return all_passed

def test_frontend_accessibility():
    """Test if frontend is accessible"""
    try:
        response = requests.get("http://localhost:4201", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend: Accessible on http://localhost:4201")
            return True
        else:
            print(f"❌ Frontend: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend: {e}")
        return False

def main():
    print("🧪 Complete System Test")
    print("=" * 50)
    
    # Test backend health
    backend_ok = test_backend_health()
    
    # Test off-topic protection
    off_topic_ok = test_off_topic_protection()
    
    # Test shopping functionality
    shopping_ok = test_shopping_functionality()
    
    # Test frontend
    print("\n🌐 Testing Frontend:")
    frontend_ok = test_frontend_accessibility()
    
    # Summary
    print("\n📊 SYSTEM STATUS:")
    print("=" * 50)
    print(f"Backend API:        {'✅ OK' if backend_ok else '❌ FAIL'}")
    print(f"Off-topic Protection: {'✅ OK' if off_topic_ok else '❌ FAIL'}")
    print(f"Shopping Features:  {'✅ OK' if shopping_ok else '❌ FAIL'}")
    print(f"Frontend Access:    {'✅ OK' if frontend_ok else '❌ FAIL'}")
    
    all_ok = backend_ok and off_topic_ok and shopping_ok and frontend_ok
    
    if all_ok:
        print("\n🎉 SYSTEM FULLY OPERATIONAL!")
        print("🔗 Backend API: http://localhost:8000")
        print("🔗 Frontend App: http://localhost:4201")
        print("📚 API Docs: http://localhost:8000/docs")
    else:
        print("\n⚠️ Some components have issues. Check the logs above.")
    
    return all_ok

if __name__ == "__main__":
    main()