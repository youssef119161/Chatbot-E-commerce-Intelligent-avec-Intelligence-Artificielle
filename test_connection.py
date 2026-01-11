#!/usr/bin/env python3
"""
Test de connexion API
"""

import requests
import json

def test_connection():
    print("🧪 Test de connexion API...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API Backend connectée !")
            print(f"Réponse: {response.json()}")
            
            # Test chat
            chat_response = requests.post(
                "http://localhost:8000/chat",
                json={"message": "Bonjour", "user_id": "test"},
                timeout=10
            )
            if chat_response.status_code == 200:
                print("✅ Chatbot fonctionne !")
                data = chat_response.json()
                print(f"Réponse chatbot: {data['response'][:100]}...")
            else:
                print(f"❌ Erreur chatbot: {chat_response.status_code}")
                
        else:
            print(f"❌ Erreur API: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend non accessible !")
        print("Démarrez le backend avec: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_connection()