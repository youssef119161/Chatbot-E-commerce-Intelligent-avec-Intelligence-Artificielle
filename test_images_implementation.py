#!/usr/bin/env python3
"""
Test de l'implémentation des images réelles
"""

import requests
import json

def test_product_images():
    """Test que les produits retournent bien des URLs d'images"""
    
    try:
        # Test avec une requête de produits
        response = requests.post(
            "http://localhost:8000/chat",
            json={"message": "montrez-moi des casquettes rouges", "user_id": "test_images"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            
            print("🧪 Test des images de produits:")
            print("=" * 50)
            print(f"Nombre de produits: {len(products)}")
            
            for i, product in enumerate(products[:3], 1):
                print(f"\n{i}. {product.get('name', 'N/A')}")
                print(f"   Image URL: {product.get('image', 'N/A')}")
                print(f"   Catégorie: {product.get('category', 'N/A')}")
                print(f"   Prix: {product.get('price', 'N/A')} {product.get('currency', 'N/A')}")
                
                # Vérifier que l'URL d'image est valide
                image_url = product.get('image', '')
                if image_url.startswith('https://'):
                    print(f"   ✅ URL d'image valide")
                else:
                    print(f"   ❌ URL d'image invalide")
            
            # Test d'accès à une image
            if products and products[0].get('image'):
                test_image_url = products[0]['image']
                print(f"\n🔍 Test d'accès à l'image:")
                print(f"URL: {test_image_url}")
                
                try:
                    img_response = requests.head(test_image_url, timeout=5)
                    if img_response.status_code == 200:
                        print("✅ Image accessible")
                    else:
                        print(f"❌ Image non accessible (HTTP {img_response.status_code})")
                except Exception as e:
                    print(f"❌ Erreur d'accès à l'image: {e}")
            
            return len(products) > 0
            
        else:
            print(f"❌ Erreur API: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_all_products_images():
    """Test toutes les images de produits"""
    
    try:
        response = requests.get("http://localhost:8000/products", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            
            print(f"\n📊 Test de toutes les images ({len(products)} produits):")
            print("-" * 60)
            
            valid_images = 0
            invalid_images = 0
            
            for product in products:
                name = product.get('name', 'N/A')
                image_url = product.get('image', '')
                
                if image_url.startswith('https://'):
                    valid_images += 1
                    print(f"✅ {name[:30]:<30} | {image_url[:50]}...")
                else:
                    invalid_images += 1
                    print(f"❌ {name[:30]:<30} | {image_url}")
            
            print(f"\n📈 Résultats:")
            print(f"✅ Images valides: {valid_images}")
            print(f"❌ Images invalides: {invalid_images}")
            print(f"📊 Pourcentage de réussite: {valid_images/len(products)*100:.1f}%")
            
            return invalid_images == 0
            
        else:
            print(f"❌ Erreur API: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🖼️ TEST DES IMAGES RÉELLES")
    print("=" * 60)
    
    # Test des images dans les réponses du chatbot
    chatbot_test = test_product_images()
    
    # Test de toutes les images de produits
    all_images_test = test_all_products_images()
    
    print(f"\n🎯 RÉSULTAT FINAL:")
    print(f"Chatbot avec images: {'✅ OK' if chatbot_test else '❌ ÉCHEC'}")
    print(f"Toutes les images:   {'✅ OK' if all_images_test else '❌ ÉCHEC'}")
    
    if chatbot_test and all_images_test:
        print("\n🎉 SUCCÈS: Toutes les images sont correctement configurées!")
    else:
        print("\n⚠️ Des améliorations sont nécessaires.")