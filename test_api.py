#!/usr/bin/env python3
"""
Test rapide de l'API Backend
"""

import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("🧪 Test de l'API Backend...")
    
    try:
        # Test health
        print("📡 Test /health...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend connecté !")
            print(f"   Réponse: {response.json()}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            return False
            
        # Test root
        print("📡 Test /...")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Endpoint racine OK !")
        else:
            print(f"❌ Erreur: {response.status_code}")
            
        # Test chat
        print("📡 Test /chat...")
        payload = {"message": "Bonjour", "user_id": "test"}
        response = requests.post(f"{base_url}/chat", json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Chatbot répond !")
            data = response.json()
            print(f"   Réponse: {data['response'][:50]}...")
        else:
            print(f"❌ Erreur chat: {response.status_code}")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au backend !")
        print("💡 Vérifiez que le serveur est démarré avec:")
        print("   cd backend")
        print("   uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    test_api()