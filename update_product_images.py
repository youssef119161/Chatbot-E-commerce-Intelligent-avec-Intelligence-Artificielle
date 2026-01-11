#!/usr/bin/env python3
"""
Script pour mettre à jour toutes les images des produits avec des URLs réelles
"""

# Mapping des images avec des URLs Unsplash de haute qualité
image_urls = {
    "peluche_licorne_bleue.jpg": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop",
    "voiture_rouge.jpg": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=300&h=300&fit=crop",
    "coussin_bleu.jpg": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=300&h=300&fit=crop",
    "vase_blanc.jpg": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=300&fit=crop",
    "lampe_bureau.jpg": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop",
    "tapis_rouge.jpg": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=300&h=300&fit=crop",
    "ballon_football.jpg": "https://images.unsplash.com/photo-1614632537190-23e4146777db?w=300&h=300&fit=crop",
    "raquette_tennis.jpg": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=300&h=300&fit=crop",
    "chaussures_sport.jpg": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop",
    "pot_vert.jpg": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=300&h=300&fit=crop",
    "arrosoir_bleu.jpg": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=300&h=300&fit=crop",
    "chaise_jardin.jpg": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=300&h=300&fit=crop",
    "livre_coloriage_bleu.jpg": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=300&fit=crop",
    "puzzle_1000.jpg": "https://images.unsplash.com/photo-1606092195730-5d7b9af1efc5?w=300&h=300&fit=crop",
    "ecouteurs_bluetooth.jpg": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop",
    "chargeur_portable.jpg": "https://images.unsplash.com/photo-1609592806596-4d8b5b3c4b5b?w=300&h=300&fit=crop",
    "mug_rouge.jpg": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=300&h=300&fit=crop",
    "couteaux_noirs.jpg": "https://images.unsplash.com/photo-1593618998160-e34014e67546?w=300&h=300&fit=crop",
    "parfum_rose.jpg": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=300&h=300&fit=crop",
    "creme_blanche.jpg": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=300&h=300&fit=crop"
}

def update_database_file():
    """Met à jour le fichier database.py avec les nouvelles URLs"""
    
    with open('backend/database.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer chaque nom de fichier par son URL
    for filename, url in image_urls.items():
        old_line = f'"image": "{filename}",'
        new_line = f'"image": "{url}",'
        content = content.replace(old_line, new_line)
    
    with open('backend/database.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Base de données mise à jour avec les nouvelles URLs d'images")
    print(f"📸 {len(image_urls)} images mises à jour")

if __name__ == "__main__":
    update_database_file()