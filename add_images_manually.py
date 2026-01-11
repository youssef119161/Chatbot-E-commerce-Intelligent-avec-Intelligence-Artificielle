"""
Script d'aide pour ajouter manuellement des images aux produits
"""

import json
import requests

def show_all_products():
    """Affiche tous les produits avec leurs IDs pour faciliter la sélection"""
    
    print("📦 LISTE DE TOUS LES PRODUITS")
    print("=" * 60)
    
    try:
        response = requests.get("http://localhost:8000/products", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            
            for product in products:
                print(f"ID: {product['id']:2d} | {product['name']}")
                print(f"     🎨 {product['color']} | 📂 {product['category']}")
                print(f"     🖼️  Actuel: {product['image']}")
                print("-" * 50)
                
        else:
            print(f"❌ Erreur API: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def create_image_template():
    """Crée un template pour ajouter les images"""
    
    print("\n📝 TEMPLATE POUR AJOUTER LES IMAGES")
    print("=" * 60)
    
    template = """
# INSTRUCTIONS POUR AJOUTER DES IMAGES MANUELLEMENT

## Méthode 1: Modifier directement backend/database.py

1. Ouvrir le fichier: backend/database.py
2. Trouver le produit par son ID
3. Remplacer l'emoji par l'URL de l'image

Exemple:
```python
{
    "id": 1,
    "name": "Casquette Rouge Classique",
    # ... autres propriétés ...
    "image": "https://votre-site.com/images/casquette-rouge.jpg",  # ← Remplacer ici
    "stock": 15
}
```

## Méthode 2: Sources d'images recommandées

### Images gratuites:
- Unsplash: https://unsplash.com/
- Pexels: https://www.pexels.com/
- Pixabay: https://pixabay.com/

### Format d'URL Unsplash optimisé:
https://images.unsplash.com/photo-[ID]?w=300&h=300&fit=crop

### Images locales:
- Créer un dossier: frontend/src/assets/images/
- Ajouter vos images dans ce dossier
- URL: "assets/images/nom-image.jpg"

## Méthode 3: Script automatique (si vous avez une liste d'URLs)

Créer un fichier images_urls.json:
```json
{
    "1": "https://example.com/casquette-rouge.jpg",
    "2": "https://example.com/casquette-bleue.jpg",
    "3": "https://example.com/sac-bleu.jpg"
}
```

Puis utiliser le script update_images_from_json.py
"""
    
    print(template)
    
    # Sauvegarder le template
    with open("GUIDE_AJOUT_IMAGES.md", "w", encoding="utf-8") as f:
        f.write(template)
    
    print("✅ Guide sauvegardé dans: GUIDE_AJOUT_IMAGES.md")

def create_update_script():
    """Crée un script pour mettre à jour les images depuis un fichier JSON"""
    
    script_content = '''#!/usr/bin/env python3
"""
Script pour mettre à jour les images depuis un fichier JSON
"""

import json
import re

def update_images_from_json():
    """Met à jour les images dans database.py depuis images_urls.json"""
    
    # Charger les URLs d'images
    try:
        with open("images_urls.json", "r", encoding="utf-8") as f:
            image_urls = json.load(f)
    except FileNotFoundError:
        print("❌ Fichier images_urls.json non trouvé")
        print("Créez ce fichier avec le format:")
        print('{"1": "url_image_1", "2": "url_image_2", ...}')
        return
    
    # Lire le fichier database.py
    try:
        with open("backend/database.py", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ Fichier backend/database.py non trouvé")
        return
    
    # Remplacer les images
    updated_count = 0
    for product_id, image_url in image_urls.items():
        # Pattern pour trouver l'image du produit
        pattern = rf'"id": {product_id},.*?"image": "[^"]*"'
        
        def replace_image(match):
            nonlocal updated_count
            updated_count += 1
            return match.group(0).rsplit('"image": "', 1)[0] + f'"image": "{image_url}"'
        
        content = re.sub(pattern, replace_image, content, flags=re.DOTALL)
    
    # Sauvegarder le fichier modifié
    with open("backend/database.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ {updated_count} images mises à jour dans database.py")
    print("🔄 Redémarrez le backend pour appliquer les changements")

if __name__ == "__main__":
    update_images_from_json()
'''
    
    with open("update_images_from_json.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ Script créé: update_images_from_json.py")

def create_example_json():
    """Crée un exemple de fichier JSON pour les URLs d'images"""
    
    example = {
        "1": "https://images.unsplash.com/photo-1521369909029-2afed882baee?w=300&h=300&fit=crop",
        "2": "https://images.unsplash.com/photo-1575428652377-a2d80e2277fc?w=300&h=300&fit=crop",
        "3": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop",
        "4": "https://images.unsplash.com/photo-1434056886845-dac89ffe9b56?w=300&h=300&fit=crop",
        "5": "https://images.unsplash.com/photo-1611652022419-a9419f74343d?w=300&h=300&fit=crop"
    }
    
    with open("images_urls_example.json", "w", encoding="utf-8") as f:
        json.dump(example, f, indent=2, ensure_ascii=False)
    
    print("✅ Exemple créé: images_urls_example.json")

def main():
    """Menu principal"""
    
    print("🖼️ ASSISTANT POUR AJOUTER DES IMAGES MANUELLEMENT")
    print("=" * 70)
    
    while True:
        print("\nQue voulez-vous faire ?")
        print("1. 📦 Voir tous les produits")
        print("2. 📝 Créer le guide d'ajout d'images")
        print("3. 🔧 Créer le script de mise à jour automatique")
        print("4. 📄 Créer un exemple de fichier JSON")
        print("5. ❌ Quitter")
        
        choice = input("\nVotre choix (1-5): ").strip()
        
        if choice == "1":
            show_all_products()
        elif choice == "2":
            create_image_template()
        elif choice == "3":
            create_update_script()
        elif choice == "4":
            create_example_json()
        elif choice == "5":
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()