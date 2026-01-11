#!/usr/bin/env python3
"""
Script pour mettre à jour database.py avec des images locales
"""

import re

def update_database_with_local_images():
    """Met à jour database.py avec les chemins des images locales"""
    
    # Mapping des produits vers leurs images locales
    image_mapping = {
        1: "assets/images/accessoires/casquette-rouge.jpg",
        2: "assets/images/accessoires/casquette-bleue.jpg", 
        3: "assets/images/accessoires/sac-bleu.jpg",
        4: "assets/images/accessoires/montre-bleue.jpg",
        5: "assets/images/bijoux/bracelet-bleu.jpg",
        6: "assets/images/bijoux/collier-bleu.jpg",
        7: "assets/images/bijoux/bague-doree.jpg",
        8: "assets/images/vetements/tshirt-bleu.jpg",
        9: "assets/images/vetements/robe-rouge.jpg",
        10: "assets/images/vetements/pantalon-noir.jpg",
        11: "assets/images/jouets/peluche-licorne.jpg",
        12: "assets/images/jouets/voiture-rouge.jpg",
        13: "assets/images/maison/coussin-bleu.jpg",
        14: "assets/images/maison/vase-blanc.jpg",
        15: "assets/images/maison/lampe-noire.jpg",
        16: "assets/images/maison/tapis-rouge.jpg",
        17: "assets/images/sport/ballon-football.jpg",
        18: "assets/images/sport/raquette-tennis.jpg",
        19: "assets/images/sport/chaussures-sport.jpg",
        20: "assets/images/jardin/pot-fleurs.jpg",
        21: "assets/images/jardin/arrosoir-bleu.jpg",
        22: "assets/images/jardin/chaise-jardin.jpg",
        23: "assets/images/loisirs/livre-coloriage.jpg",
        24: "assets/images/loisirs/puzzle.jpg",
        25: "assets/images/electronique/ecouteurs-noirs.jpg",
        26: "assets/images/electronique/chargeur-blanc.jpg",
        27: "assets/images/cuisine/mug-rouge.jpg",
        28: "assets/images/cuisine/couteaux-noirs.jpg",
        29: "assets/images/beaute/parfum-rose.jpg",
        30: "assets/images/beaute/creme-blanche.jpg"
    }
    
    try:
        # Lire le fichier database.py
        with open("backend/database.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Remplacer les images pour chaque produit
        updated_count = 0
        
        for product_id, image_path in image_mapping.items():
            # Pattern pour trouver le produit et son image
            pattern = rf'("id": {product_id},.*?"image": ")[^"]*(")'
            
            def replace_image(match):
                nonlocal updated_count
                updated_count += 1
                return match.group(1) + image_path + match.group(2)
            
            content = re.sub(pattern, replace_image, content, flags=re.DOTALL)
        
        # Sauvegarder le fichier modifié
        with open("backend/database.py", "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ {updated_count} images mises à jour dans database.py")
        print("📁 Assurez-vous que vos images sont dans frontend/src/assets/images/")
        print("🔄 Redémarrez le backend pour appliquer les changements")
        
    except FileNotFoundError:
        print("❌ Fichier backend/database.py non trouvé")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def show_missing_images():
    """Affiche la liste des images à télécharger"""
    
    print("\n📋 LISTE DES IMAGES À TÉLÉCHARGER")
    print("=" * 60)
    
    images_needed = [
        "frontend/src/assets/images/accessoires/casquette-rouge.jpg",
        "frontend/src/assets/images/accessoires/casquette-bleue.jpg",
        "frontend/src/assets/images/accessoires/sac-bleu.jpg",
        "frontend/src/assets/images/accessoires/montre-bleue.jpg",
        "frontend/src/assets/images/bijoux/bracelet-bleu.jpg",
        "frontend/src/assets/images/bijoux/collier-bleu.jpg",
        "frontend/src/assets/images/bijoux/bague-doree.jpg",
        "frontend/src/assets/images/vetements/tshirt-bleu.jpg",
        "frontend/src/assets/images/vetements/robe-rouge.jpg",
        "frontend/src/assets/images/vetements/pantalon-noir.jpg",
        "frontend/src/assets/images/jouets/peluche-licorne.jpg",
        "frontend/src/assets/images/jouets/voiture-rouge.jpg",
        "frontend/src/assets/images/maison/coussin-bleu.jpg",
        "frontend/src/assets/images/maison/vase-blanc.jpg",
        "frontend/src/assets/images/maison/lampe-noire.jpg",
        "frontend/src/assets/images/maison/tapis-rouge.jpg",
        "frontend/src/assets/images/sport/ballon-football.jpg",
        "frontend/src/assets/images/sport/raquette-tennis.jpg",
        "frontend/src/assets/images/sport/chaussures-sport.jpg",
        "frontend/src/assets/images/jardin/pot-fleurs.jpg",
        "frontend/src/assets/images/jardin/arrosoir-bleu.jpg",
        "frontend/src/assets/images/jardin/chaise-jardin.jpg",
        "frontend/src/assets/images/loisirs/livre-coloriage.jpg",
        "frontend/src/assets/images/loisirs/puzzle.jpg",
        "frontend/src/assets/images/electronique/ecouteurs-noirs.jpg",
        "frontend/src/assets/images/electronique/chargeur-blanc.jpg",
        "frontend/src/assets/images/cuisine/mug-rouge.jpg",
        "frontend/src/assets/images/cuisine/couteaux-noirs.jpg",
        "frontend/src/assets/images/beaute/parfum-rose.jpg",
        "frontend/src/assets/images/beaute/creme-blanche.jpg"
    ]
    
    for i, image_path in enumerate(images_needed, 1):
        print(f"{i:2d}. {image_path}")

def main():
    """Menu principal"""
    
    print("📸 GESTIONNAIRE D'IMAGES LOCALES")
    print("=" * 50)
    
    while True:
        print("\nQue voulez-vous faire ?")
        print("1. 📋 Voir la liste des images à télécharger")
        print("2. 🔄 Mettre à jour database.py avec les images locales")
        print("3. 📖 Ouvrir le guide complet")
        print("4. ❌ Quitter")
        
        choice = input("\nVotre choix (1-4): ").strip()
        
        if choice == "1":
            show_missing_images()
        elif choice == "2":
            update_database_with_local_images()
        elif choice == "3":
            print("📖 Consultez le fichier: GUIDE_IMAGES_LOCALES.md")
        elif choice == "4":
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()