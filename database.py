"""
Base de données simulée pour la boutique e-commerce
Contient les produits avec leurs caractéristiques
"""

from typing import List, Dict, Any
import json

class ProductDatabase:
    """
    Base de données des produits de la boutique
    """
    
    def __init__(self):
        self.products = [
            # ACCESSOIRES
            {
                "id": 1,
                "name": "Casquette Rouge Classique",
                "category": "accessoires",
                "subcategory": "casquettes",
                "color": "rouge",
                "price": 25.0,
                "currency": "DT",
                "description": "Casquette rouge en coton, style classique",
                "tags": ["sport", "casual", "unisexe"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "assets/images/vetements/casquette-rouge.jpg",
                "stock": 15
            },
            {
                "id": 2,
                "name": "Casquette Bleue Marine",
                "category": "accessoires",
                "subcategory": "casquettes",
                "color": "bleu",
                "price": 32.0,
                "currency": "DT",
                "description": "Casquette bleu marine style marin",
                "tags": ["marin", "style", "unisexe"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "assets/images/vetements/casquette-bleu.jpg",
                "stock": 7
            },
            {
                "id": 3,
                "name": "Sac à Main Bleu Élégant",
                "category": "accessoires",
                "subcategory": "sacs",
                "color": "bleu",
                "price": 45.0,
                "currency": "DT",
                "description": "Sac à main bleu en cuir synthétique",
                "tags": ["élégant", "pratique", "femme"],
                "age_group": "adulte",
                "gender": "femme",
                "image": "assets/images/vetements/Sac_a_main_bleu.jpg",
                "stock": 4
            },
            {
                "id": 4,
                "name": "Montre Digitale Bleue",
                "category": "accessoires",
                "subcategory": "montres",
                "color": "bleu",
                "price": 55.0,
                "currency": "DT",
                "description": "Montre digitale bleue étanche",
                "tags": ["moderne", "sport", "étanche"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "⌚",
                "stock": 3
            },
            
            # BIJOUX
            {
                "id": 5,
                "name": "Bracelet Bleu Élégant",
                "category": "bijoux",
                "subcategory": "bracelets",
                "color": "bleu",
                "price": 30.0,
                "currency": "DT",
                "description": "Bracelet bleu élégant pour femme",
                "tags": ["élégant", "cadeau", "femme"],
                "age_group": "adulte",
                "gender": "femme",
                "image": "📿",
                "stock": 12
            },
            {
                "id": 6,
                "name": "Collier Bleu Princesse",
                "category": "bijoux",
                "subcategory": "colliers",
                "color": "bleu",
                "price": 38.0,
                "currency": "DT",
                "description": "Collier bleu pour petite fille, style princesse",
                "tags": ["princesse", "cadeau", "fille", "enfant"],
                "age_group": "enfant",
                "gender": "fille",
                "image": "📿",
                "stock": 6
            },
            {
                "id": 7,
                "name": "Bague Dorée Femme",
                "category": "bijoux",
                "subcategory": "bagues",
                "color": "jaune",
                "price": 42.0,
                "currency": "DT",
                "description": "Bague dorée élégante pour femme",
                "tags": ["élégant", "mariage", "femme"],
                "age_group": "adulte",
                "gender": "femme",
                "image": "💍",
                "stock": 8
            },
            
            # VÊTEMENTS
            {
                "id": 8,
                "name": "T-shirt Bleu Enfant",
                "category": "vêtements",
                "subcategory": "t-shirts",
                "color": "bleu",
                "price": 22.0,
                "currency": "DT",
                "description": "T-shirt bleu confortable pour enfant",
                "tags": ["confortable", "casual", "enfant"],
                "age_group": "enfant",
                "gender": "unisexe",
                "image": "👕",
                "stock": 20
            },
            {
                "id": 9,
                "name": "Robe Rouge Élégante",
                "category": "vêtements",
                "subcategory": "robes",
                "color": "rouge",
                "price": 65.0,
                "currency": "DT",
                "description": "Robe rouge élégante pour soirée",
                "tags": ["élégant", "soirée", "femme"],
                "age_group": "adulte",
                "gender": "femme",
                "image": "👗",
                "stock": 5
            },
            {
                "id": 10,
                "name": "Pantalon Noir Homme",
                "category": "vêtements",
                "subcategory": "pantalons",
                "color": "noir",
                "price": 48.0,
                "currency": "DT",
                "description": "Pantalon noir classique pour homme",
                "tags": ["classique", "travail", "homme"],
                "age_group": "adulte",
                "gender": "homme",
                "image": "👖",
                "stock": 12
            },
            
            # JOUETS
            {
                "id": 11,
                "name": "Peluche Licorne Bleue",
                "category": "jouets",
                "subcategory": "peluches",
                "color": "bleu",
                "price": 28.0,
                "currency": "DT",
                "description": "Peluche licorne bleue douce et câline",
                "tags": ["cadeau", "enfant", "fille", "doux"],
                "age_group": "enfant",
                "gender": "fille",
                "image": "🦄",
                "stock": 10
            },
            {
                "id": 12,
                "name": "Voiture Télécommandée Rouge",
                "category": "jouets",
                "subcategory": "véhicules",
                "color": "rouge",
                "price": 35.0,
                "currency": "DT",
                "description": "Voiture télécommandée rouge rapide",
                "tags": ["cadeau", "enfant", "garçon", "électronique"],
                "age_group": "enfant",
                "gender": "garçon",
                "image": "🚗",
                "stock": 8
            },
            
            # MAISON & DÉCORATION
            {
                "id": 13,
                "name": "Coussin Décoratif Bleu",
                "category": "maison",
                "subcategory": "décoration",
                "color": "bleu",
                "price": 18.0,
                "currency": "DT",
                "description": "Coussin décoratif bleu pour salon",
                "tags": ["décoration", "confort", "maison"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "🛏️",
                "stock": 15
            },
            {
                "id": 14,
                "name": "Vase Blanc Moderne",
                "category": "maison",
                "subcategory": "décoration",
                "color": "blanc",
                "price": 32.0,
                "currency": "DT",
                "description": "Vase blanc design moderne",
                "tags": ["décoration", "moderne", "élégant"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "🏺",
                "stock": 6
            },
            {
                "id": 15,
                "name": "Lampe de Bureau Noire",
                "category": "maison",
                "subcategory": "éclairage",
                "color": "noir",
                "price": 45.0,
                "currency": "DT",
                "description": "Lampe de bureau noire LED",
                "tags": ["bureau", "travail", "moderne"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "💡",
                "stock": 9
            },
            {
                "id": 16,
                "name": "Tapis Rouge Salon",
                "category": "maison",
                "subcategory": "textiles",
                "color": "rouge",
                "price": 75.0,
                "currency": "DT",
                "description": "Tapis rouge pour salon 120x180cm",
                "tags": ["décoration", "confort", "salon"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "🏠",
                "stock": 4
            },
            
            # SPORT & FITNESS
            {
                "id": 17,
                "name": "Ballon de Football Blanc",
                "category": "sport",
                "subcategory": "ballons",
                "color": "blanc",
                "price": 25.0,
                "currency": "DT",
                "description": "Ballon de football officiel blanc",
                "tags": ["sport", "football", "extérieur"],
                "age_group": "enfant",
                "gender": "unisexe",
                "image": "⚽",
                "stock": 12
            },
            {
                "id": 18,
                "name": "Raquette de Tennis Rouge",
                "category": "sport",
                "subcategory": "raquettes",
                "color": "rouge",
                "price": 85.0,
                "currency": "DT",
                "description": "Raquette de tennis professionnelle rouge",
                "tags": ["sport", "tennis", "professionnel"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "🎾",
                "stock": 5
            },
            {
                "id": 19,
                "name": "Chaussures de Sport Noires",
                "category": "sport",
                "subcategory": "chaussures",
                "color": "noir",
                "price": 95.0,
                "currency": "DT",
                "description": "Chaussures de sport noires confortables",
                "tags": ["sport", "running", "confort"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "👟",
                "stock": 8
            },
            
            # JARDIN & EXTÉRIEUR
            {
                "id": 20,
                "name": "Pot de Fleurs Vert",
                "category": "jardin",
                "subcategory": "pots",
                "color": "vert",
                "price": 15.0,
                "currency": "DT",
                "description": "Pot de fleurs vert en céramique",
                "tags": ["jardin", "plantes", "décoration"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "🪴",
                "stock": 20
            },
            {
                "id": 21,
                "name": "Arrosoir Bleu",
                "category": "jardin",
                "subcategory": "outils",
                "color": "bleu",
                "price": 22.0,
                "currency": "DT",
                "description": "Arrosoir bleu 5 litres",
                "tags": ["jardin", "arrosage", "pratique"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "🚿",
                "stock": 10
            },
            {
                "id": 22,
                "name": "Chaise de Jardin Blanche",
                "category": "jardin",
                "subcategory": "mobilier",
                "color": "blanc",
                "price": 65.0,
                "currency": "DT",
                "description": "Chaise de jardin blanche en plastique",
                "tags": ["jardin", "mobilier", "extérieur"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "🪑",
                "stock": 6
            },
            
            # LIVRES & LOISIRS
            {
                "id": 23,
                "name": "Livre de Coloriage Bleu",
                "category": "loisirs",
                "subcategory": "livres",
                "color": "bleu",
                "price": 15.0,
                "currency": "DT",
                "description": "Livre de coloriage avec couverture bleue",
                "tags": ["éducatif", "cadeau", "enfant", "créatif"],
                "age_group": "enfant",
                "gender": "unisexe",
                "image": "📚",
                "stock": 25
            },
            {
                "id": 24,
                "name": "Puzzle 1000 Pièces",
                "category": "loisirs",
                "subcategory": "puzzles",
                "color": "multicolore",
                "price": 28.0,
                "currency": "DT",
                "description": "Puzzle 1000 pièces paysage",
                "tags": ["loisir", "famille", "patience"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "🧩",
                "stock": 8
            },
            
            # ÉLECTRONIQUE
            {
                "id": 25,
                "name": "Écouteurs Bluetooth Noirs",
                "category": "électronique",
                "subcategory": "audio",
                "color": "noir",
                "price": 75.0,
                "currency": "DT",
                "description": "Écouteurs Bluetooth sans fil noirs",
                "tags": ["technologie", "musique", "moderne"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "🎧",
                "stock": 12
            },
            {
                "id": 26,
                "name": "Chargeur Portable Blanc",
                "category": "électronique",
                "subcategory": "accessoires",
                "color": "blanc",
                "price": 35.0,
                "currency": "DT",
                "description": "Chargeur portable 10000mAh blanc",
                "tags": ["technologie", "pratique", "voyage"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "🔋",
                "stock": 15
            },
            
            # CUISINE
            {
                "id": 27,
                "name": "Mug Rouge Personnalisé",
                "category": "cuisine",
                "subcategory": "vaisselle",
                "color": "rouge",
                "price": 12.0,
                "currency": "DT",
                "description": "Mug rouge en céramique",
                "tags": ["cuisine", "cadeau", "personnalisé"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "☕",
                "stock": 30
            },
            {
                "id": 28,
                "name": "Set de Couteaux Noirs",
                "category": "cuisine",
                "subcategory": "ustensiles",
                "color": "noir",
                "price": 55.0,
                "currency": "DT",
                "description": "Set de 3 couteaux de cuisine noirs",
                "tags": ["cuisine", "professionnel", "qualité"],
                "age_group": "adulte",
                "gender": "unisexe",
                "image": "🔪",
                "stock": 7
            },
            
            # BEAUTÉ & SOINS
            {
                "id": 29,
                "name": "Parfum Femme Rose",
                "category": "beauté",
                "subcategory": "parfums",
                "color": "rose",
                "price": 85.0,
                "currency": "DT",
                "description": "Parfum femme aux notes florales roses",
                "tags": ["beauté", "femme", "élégant"],
                "age_group": "adulte",
                "gender": "femme",
                "image": "🌸",
                "stock": 6
            },
            {
                "id": 30,
                "name": "Crème Hydratante Blanche",
                "category": "beauté",
                "subcategory": "soins",
                "color": "blanc",
                "price": 25.0,
                "currency": "DT",
                "description": "Crème hydratante visage blanche",
                "tags": ["beauté", "soins", "hydratant"],
                "age_group": "adulte",
                "gender": "femme",
                "image": "🧴",
                "stock": 18
            }
        ]
    
    def get_all_products(self) -> List[Dict[str, Any]]:
        """Retourne tous les produits"""
        return self.products
    
    def search_by_color(self, color: str) -> List[Dict[str, Any]]:
        """Recherche par couleur"""
        color_lower = color.lower()
        return [p for p in self.products if color_lower in p["color"].lower()]
    
    def search_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Recherche par catégorie"""
        category_lower = category.lower()
        return [p for p in self.products if category_lower in p["category"].lower() or 
                category_lower in p["subcategory"].lower()]
    
    def search_by_price_range(self, max_price: float, min_price: float = 0) -> List[Dict[str, Any]]:
        """Recherche par gamme de prix"""
        return [p for p in self.products if min_price <= p["price"] <= max_price]
    
    def search_by_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        """Recherche par tags"""
        results = []
        for product in self.products:
            for tag in tags:
                if any(tag.lower() in product_tag.lower() for product_tag in product["tags"]):
                    if product not in results:
                        results.append(product)
        return results
    
    def search_by_gender_and_age(self, gender: str = None, age_group: str = None) -> List[Dict[str, Any]]:
        """Recherche par genre et groupe d'âge"""
        results = self.products.copy()
        
        if gender:
            gender_lower = gender.lower()
            results = [p for p in results if 
                      gender_lower in p["gender"].lower() or p["gender"].lower() == "unisexe"]
        
        if age_group:
            age_lower = age_group.lower()
            results = [p for p in results if age_lower in p["age_group"].lower()]
        
        return results
    
    def complex_search(self, **criteria) -> List[Dict[str, Any]]:
        """Recherche complexe avec plusieurs critères"""
        results = self.products.copy()
        
        if "color" in criteria and criteria["color"]:
            color_results = self.search_by_color(criteria["color"])
            results = [p for p in results if p in color_results]
        
        if "category" in criteria and criteria["category"]:
            category_results = self.search_by_category(criteria["category"])
            results = [p for p in results if p in category_results]
        
        if "max_price" in criteria and criteria["max_price"]:
            price_results = self.search_by_price_range(criteria["max_price"])
            results = [p for p in results if p in price_results]
        
        if "tags" in criteria and criteria["tags"]:
            tag_results = self.search_by_tags(criteria["tags"])
            results = [p for p in results if p in tag_results]
        
        if "gender" in criteria or "age_group" in criteria:
            gender_age_results = self.search_by_gender_and_age(
                criteria.get("gender"), criteria.get("age_group")
            )
            results = [p for p in results if p in gender_age_results]
        
        return results

# Instance globale de la base de données
product_db = ProductDatabase()