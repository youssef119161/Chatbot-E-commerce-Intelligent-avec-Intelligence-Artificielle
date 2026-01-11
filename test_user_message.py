#!/usr/bin/env python3
"""
Test the specific user message to see the improved response
"""

import requests
import json

def test_user_message():
    """Test the specific user message"""
    
    message = "je cherche un produit comme un cadeau a ma femme , je veux que le produit soit rouge et ne depasse pas le prix 50 dt"
    
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"message": message, "user_id": "test_user_fix"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("🧪 Test du message utilisateur:")
            print("=" * 60)
            print(f"Message: {message}")
            print(f"Intent: {data.get('detected_intents', ['unknown'])[0]}")
            print(f"Confidence: {data.get('confidence', 0.0):.2f}")
            print(f"Produits trouvés: {len(data.get('products', []))}")
            print(f"Contexte utilisé: {data.get('context_used', {})}")
            print("\nRéponse du chatbot:")
            print("-" * 40)
            print(data.get('response', ''))
            
            if data.get('products'):
                print(f"\n🛍️ Produits affichés:")
                for i, product in enumerate(data.get('products', [])[:3], 1):
                    print(f"{i}. {product.get('name', 'N/A')} - {product.get('price', 'N/A')} DT - {product.get('color', 'N/A')}")
            
            # Check if response is positive
            response_text = data.get('response', '').lower()
            is_positive = any(word in response_text for word in ['parfait', 'excellente', 'super', 'génial', 'trouvé'])
            
            print(f"\n✅ Réponse positive: {'Oui' if is_positive else 'Non'}")
            print(f"✅ Produits affichés: {'Oui' if data.get('products') else 'Non'}")
            
            return is_positive and bool(data.get('products'))
            
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = test_user_message()
    print(f"\n🎯 Résultat: {'✅ SUCCÈS' if success else '❌ ÉCHEC'}")