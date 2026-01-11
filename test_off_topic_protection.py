#!/usr/bin/env python3
"""
Test script for off-topic intent protection
Ensures chatbot NEVER returns products for non-shopping questions
"""

import requests
import json

# Test cases for off-topic questions
OFF_TOPIC_TESTS = [
    # General knowledge
    "Qui est Messi ?",
    "Quelle est la capitale de la France ?",
    "Comment faire 2+2 ?",
    "Parlez-moi de l'histoire de la Tunisie",
    "Quelle est la météo aujourd'hui ?",
    
    # Personal questions about chatbot
    "Quel est ton âge ?",
    "Comment tu t'appelles ?",
    "Qui es-tu ?",
    "Es-tu humain ?",
    "D'où viens-tu ?",
    
    # Non-shopping topics
    "Donne-moi une recette de couscous",
    "Où partir en vacances ?",
    "Comment soigner un rhume ?",
    "Quel travail choisir ?",
    "Recommande-moi un film",
    
    # Technical questions
    "Comment réparer mon ordinateur ?",
    "Quel est mon mot de passe wifi ?",
    "Comment installer Windows ?",
    
    # Philosophy/abstract
    "Quel est le sens de la vie ?",
    "Parle-moi de l'amour",
    "Que penses-tu de la religion ?"
]

# Test cases for shopping questions (should return products)
SHOPPING_TESTS = [
    "Je veux un cadeau pour ma fille",
    "Montrez-moi des casquettes rouges",
    "Cherche des bijoux pas chers",
    "Budget 30 DT pour un garçon de 8 ans",
    "Je veux acheter quelque chose de bleu"
]

def test_chatbot(message, expected_products=False):
    """Test a single message"""
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"message": message, "user_id": "test_user"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            has_products = len(data.get("products", [])) > 0
            intent = data.get("detected_intents", ["unknown"])[0]
            confidence = data.get("confidence", 0.0)
            
            # Check if result matches expectation
            success = (has_products == expected_products)
            
            print(f"✅ {'PASS' if success else '❌ FAIL'} | Intent: {intent:12} | Confidence: {confidence:.2f} | Products: {len(data.get('products', []))} | Message: {message[:50]}")
            
            if not success:
                print(f"   Expected products: {expected_products}, Got products: {has_products}")
                print(f"   Response: {data.get('response', '')[:100]}...")
            
            return success
        else:
            print(f"❌ ERROR | HTTP {response.status_code} | {message[:50]}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR | Exception: {e} | {message[:50]}")
        return False

def main():
    print("🧪 Testing Off-Topic Intent Protection")
    print("=" * 80)
    
    # Test off-topic questions (should NOT return products)
    print("\n🚫 Testing OFF-TOPIC questions (should return 0 products):")
    print("-" * 60)
    
    off_topic_results = []
    for message in OFF_TOPIC_TESTS:
        result = test_chatbot(message, expected_products=False)
        off_topic_results.append(result)
    
    # Test shopping questions (should return products)
    print("\n🛍️ Testing SHOPPING questions (should return products):")
    print("-" * 60)
    
    shopping_results = []
    for message in SHOPPING_TESTS:
        result = test_chatbot(message, expected_products=True)
        shopping_results.append(result)
    
    # Summary
    print("\n📊 SUMMARY:")
    print("=" * 80)
    
    off_topic_pass = sum(off_topic_results)
    off_topic_total = len(off_topic_results)
    shopping_pass = sum(shopping_results)
    shopping_total = len(shopping_results)
    
    print(f"🚫 Off-topic protection: {off_topic_pass}/{off_topic_total} ({off_topic_pass/off_topic_total*100:.1f}%)")
    print(f"🛍️ Shopping detection:   {shopping_pass}/{shopping_total} ({shopping_pass/shopping_total*100:.1f}%)")
    
    total_pass = off_topic_pass + shopping_pass
    total_tests = off_topic_total + shopping_total
    
    print(f"🎯 Overall success:      {total_pass}/{total_tests} ({total_pass/total_tests*100:.1f}%)")
    
    if total_pass == total_tests:
        print("\n🎉 ALL TESTS PASSED! Off-topic protection is working correctly!")
    else:
        print(f"\n⚠️ {total_tests - total_pass} tests failed. Review the implementation.")
    
    return total_pass == total_tests

if __name__ == "__main__":
    main()