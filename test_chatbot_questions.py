#!/usr/bin/env python3
"""
Test du chatbot avec logique simplifiée : MAX 2-3 questions puis produits
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from chatbot_logic import ecommerce_chatbot

def test_max_questions_then_products():
    """Test : Maximum 2-3 questions puis produits obligatoires"""
    
    print("🤖 Test du Chatbot : MAX 2-3 Questions puis Produits")
    print("=" * 60)
    
    session_id = "test_max_questions"
    
    # Conversation simulée
    messages = [
        "Bonjour",
        "je veux un cadeau", 
        "pour une fille",
        "budget 30 DT",
        "elle aime le bleu"
    ]
    
    print(f"\n📱 Session ID: {session_id}")
    print("-" * 40)
    
    for i, message in enumerate(messages, 1):
        print(f"\n{i}️⃣ Utilisateur: {message}")
        response = ecommerce_chatbot.generate_smart_response(message, session_id)
        
        print(f"🤖 Chatbot: {response['response'][:250]}...")
        print(f"📊 Contexte: {response['criteria']}")
        print(f"❓ Questions: {len(response['questions'])} question(s)")
        print(f"🛍️ Produits: {len(response['products'])} produit(s)")
        
        # Vérifier si on doit montrer les produits
        should_show = ecommerce_chatbot.should_show_products(response['criteria'], session_id)
        print(f"✅ Doit montrer produits: {should_show}")
        
        # Compter les échanges
        session = ecommerce_chatbot.get_or_create_session(session_id)
        exchanges = len(session["conversation_history"])
        print(f"💬 Échanges: {exchanges}")
        print("-" * 40)

if __name__ == "__main__":
    test_max_questions_then_products()