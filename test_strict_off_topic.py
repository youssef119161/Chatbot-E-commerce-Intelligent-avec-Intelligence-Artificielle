#!/usr/bin/env python3
"""
STRICT Off-Topic Protection Test
Tests the critical requirement that chatbot NEVER returns products for off-topic questions,
even when previous shopping context exists.
"""

import requests
import json

def test_chatbot_with_context(messages, expected_results):
    """Test a sequence of messages to verify context handling"""
    user_id = "test_strict_user"
    
    print(f"\n🧪 Testing conversation sequence:")
    print("-" * 60)
    
    all_passed = True
    
    for i, (message, expected_products) in enumerate(zip(messages, expected_results)):
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"message": message, "user_id": user_id},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                has_products = len(data.get("products", [])) > 0
                intent = data.get("detected_intents", ["unknown"])[0]
                confidence = data.get("confidence", 0.0)
                
                # Check if result matches expectation
                success = (has_products == expected_products)
                
                status = "✅ PASS" if success else "❌ FAIL"
                print(f"{i+1}. {status} | Intent: {intent:15} | Products: {len(data.get('products', []))} | {message}")
                
                if not success:
                    print(f"   Expected products: {expected_products}, Got products: {has_products}")
                    print(f"   Response: {data.get('response', '')[:80]}...")
                    all_passed = False
                
            else:
                print(f"{i+1}. ❌ ERROR | HTTP {response.status_code} | {message}")
                all_passed = False
                
        except Exception as e:
            print(f"{i+1}. ❌ ERROR | Exception: {e} | {message}")
            all_passed = False
    
    return all_passed

def test_critical_scenarios():
    """Test critical scenarios where off-topic protection must work"""
    
    print("🚨 CRITICAL TEST: Off-topic questions after shopping context")
    print("=" * 80)
    
    # Scenario 1: Shopping conversation followed by off-topic question
    scenario1_messages = [
        "Je veux un cadeau pour ma fille",  # Shopping context established
        "Budget 50 DT",                     # More shopping context
        "Qui est Messi ?"                   # OFF-TOPIC - must NOT return products
    ]
    scenario1_expected = [True, True, False]  # Last one must be False
    
    result1 = test_chatbot_with_context(scenario1_messages, scenario1_expected)
    
    # Scenario 2: Shopping conversation followed by personal question
    scenario2_messages = [
        "Montrez-moi des casquettes rouges", # Shopping context
        "Quel est ton âge ?"                 # PERSONAL - must NOT return products
    ]
    scenario2_expected = [True, False]  # Last one must be False
    
    result2 = test_chatbot_with_context(scenario2_messages, scenario2_expected)
    
    # Scenario 3: Multiple off-topic questions
    scenario3_messages = [
        "Je cherche des bijoux bleus",       # Shopping context
        "Comment réparer mon ordinateur ?",  # OFF-TOPIC - must NOT return products
        "Quelle est la météo ?",             # OFF-TOPIC - must NOT return products
        "Parle-moi du réveillon"             # OFF-TOPIC - must NOT return products
    ]
    scenario3_expected = [True, False, False, False]
    
    result3 = test_chatbot_with_context(scenario3_messages, scenario3_expected)
    
    return result1 and result2 and result3

def test_individual_off_topic():
    """Test individual off-topic questions"""
    
    print("\n🚫 Individual Off-Topic Tests:")
    print("-" * 60)
    
    off_topic_tests = [
        # General knowledge
        ("Qui est Messi ?", False),
        ("Quelle est la capitale de la France ?", False),
        ("Comment faire 2+2 ?", False),
        ("Parlez-moi de l'histoire", False),
        ("Quelle est la météo ?", False),
        ("Parle-moi du réveillon", False),
        
        # Personal questions
        ("Quel est ton âge ?", False),
        ("Comment tu t'appelles ?", False),
        ("Qui es-tu ?", False),
        ("Es-tu humain ?", False),
        
        # Technical questions
        ("Comment réparer mon ordinateur ?", False),
        ("Quel est mon mot de passe wifi ?", False),
        
        # Shopping questions (should return products)
        ("Je veux un cadeau", True),
        ("Montrez-moi des casquettes", True),
        ("Budget 30 DT", True)
    ]
    
    all_passed = True
    
    for message, expected_products in off_topic_tests:
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"message": message, "user_id": "test_individual"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                has_products = len(data.get("products", [])) > 0
                intent = data.get("detected_intents", ["unknown"])[0]
                
                success = (has_products == expected_products)
                status = "✅ PASS" if success else "❌ FAIL"
                
                print(f"{status} | Intent: {intent:15} | Products: {len(data.get('products', []))} | {message}")
                
                if not success:
                    all_passed = False
                    
            else:
                print(f"❌ ERROR | HTTP {response.status_code} | {message}")
                all_passed = False
                
        except Exception as e:
            print(f"❌ ERROR | Exception: {e} | {message}")
            all_passed = False
    
    return all_passed

def main():
    print("🚨 STRICT OFF-TOPIC PROTECTION TEST")
    print("=" * 80)
    print("CRITICAL REQUIREMENT: Chatbot must NEVER return products for off-topic questions,")
    print("even when previous shopping context exists in conversation memory.")
    print("=" * 80)
    
    # Test critical scenarios
    critical_passed = test_critical_scenarios()
    
    # Test individual cases
    individual_passed = test_individual_off_topic()
    
    # Summary
    print("\n📊 FINAL RESULTS:")
    print("=" * 80)
    print(f"Critical Scenarios: {'✅ PASSED' if critical_passed else '❌ FAILED'}")
    print(f"Individual Tests:   {'✅ PASSED' if individual_passed else '❌ FAILED'}")
    
    overall_success = critical_passed and individual_passed
    
    if overall_success:
        print("\n🎉 SUCCESS: Strict off-topic protection is working correctly!")
        print("✅ Chatbot NEVER returns products for off-topic questions")
        print("✅ Previous shopping context is properly ignored for off-topic queries")
    else:
        print("\n🚨 FAILURE: Off-topic protection has critical issues!")
        print("❌ Chatbot is still returning products for off-topic questions")
        print("❌ This violates the core requirement and must be fixed immediately")
    
    return overall_success

if __name__ == "__main__":
    main()