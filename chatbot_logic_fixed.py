"""
Logique du Chatbot E-commerce - Assistant Commercial Intelligent avec Gestion de Session
Analyse les demandes clients, motive les achats et propose des alternatives
"""

import random
import re
from typing import Dict, List, Any, Optional
from database import product_db


class SmartSalesAssistant:
    """
    Assistant commercial intelligent pour boutique e-commerce
    Motive les clients, pose des questions et propose des alternatives
    """
    
    def __init__(self):
        # Stockage des sessions utilisateur (contexte persistant)
        self.user_sessions = {}
        
        # Réponses motivantes par catégories
        self.responses = {
            "salutations": [
                "🛍️ Bonjour et bienvenue dans notre boutique ! Je suis ravi de vous aider à trouver le produit parfait !",
                "✨ Salut ! Quelle excellente idée de faire du shopping ! Je suis votre conseiller personnel.",
                "🎉 Hello ! Vous tombez bien, nous avons de superbes nouveautés !",
                "🌟 Bonjour ! Prêt(e) pour une session shopping réussie ?"
            ],
            "au_revoir": [
                "🛒 Merci pour votre visite ! N'hésitez pas à revenir !",
                "✨ À bientôt ! J'espère vous avoir aidé à trouver votre bonheur.",
                "🎁 Au revoir ! Si vous changez d'avis sur un produit, je serai là !",
                "💫 À plus tard ! Le shopping, c'est encore mieux avec de bons conseils !"
            ],
            "aide": [
                "🤝 Bien sûr, je suis là pour ça ! Décrivez-moi ce que vous cherchez.",
                "💡 Parfait ! Dites-moi tout : couleur préférée, occasion, budget...",
                "🎯 Excellente question ! Parlez-moi de vos besoins.",
                "✨ Avec plaisir ! Plus j'en sais, mieux je peux vous conseiller !"
            ]
        }
        
        # Patterns pour l'analyse
        self.color_patterns = {
            "rouge": r"\b(rouge|red|bordeaux|cerise)\b",
            "bleu": r"\b(bleu|bleue|blue|marine|turquoise|cyan)\b",
            "vert": r"\b(vert|verte|green|kaki|olive)\b",
            "noir": r"\b(noir|noire|black|sombre)\b",
            "blanc": r"\b(blanc|blanche|white|crème|ivoire)\b",
            "rose": r"\b(rose|pink|fuchsia)\b",
            "jaune": r"\b(jaune|yellow|doré|or)\b"
        }
        
        self.category_patterns = {
            "casquette": r"\b(casquette|cap|chapeau|couvre-chef)\b",
            "bijoux": r"\b(bijou|bijoux|bracelet|collier|bague|pendentif|chaîne)\b",
            "sac": r"\b(sac|bag|pochette|besace|cartable)\b",
            "vêtement": r"\b(vêtement|t-shirt|tshirt|pull|pantalon|robe|chemise)\b",
            "jouet": r"\b(jouet|peluche|jeu|poupée|figurine|voiture|ballon)\b",
            "livre": r"\b(livre|book|coloriage|lecture|bd|manga|puzzle)\b",
            "montre": r"\b(montre|watch|bracelet-montre)\b"
        }
        
        self.price_patterns = {
            "budget": r"\b(?:budget|prix|coût|coute)\s*(?:de|:)?\s*(\d+)\s*(?:dt|dinar|€|euro)?\b",
            "max_price": r"\b(?:maximum|max|pas plus de|moins de|jusqu'à)\s*(\d+)\s*(?:dt|dinar|€|euro)?\b",
            "cheap": r"\b(pas cher|économique|abordable|petit prix|bon marché)\b"
        }
        
        self.recipient_patterns = {
            "fille": r"\b(fille|daughter|girl|petite fille|fillette|pour elle|pour ma fille)\b",
            "garçon": r"\b(garçon|fils|boy|son|petit garçon|pour lui|pour mon fils)\b",
            "femme": r"\b(femme|woman|maman|mère|épouse|copine|amie|pour ma femme)\b",
            "homme": r"\b(homme|man|papa|père|mari|copain|ami|pour mon mari)\b",
            "enfant": r"\b(enfant|child|kid|petit|petite|bébé|pour un enfant)\b"
        }
        
        self.age_patterns = {
            "age_specific": r"\b(\d+)\s*(?:ans?|years?|year old)\b",
            "age_range": r"\b(?:entre|from)\s*(\d+)\s*(?:et|and|to)\s*(\d+)\s*ans?\b"
        }
        
        self.occasion_patterns = {
            "cadeau": r"\b(cadeau|gift|offrir|surprise|anniversaire|fête|noël)\b",
            "travail": r"\b(travail|bureau|professionnel|boulot)\b",
            "sport": r"\b(sport|gym|fitness|course|jogging)\b",
            "quotidien": r"\b(quotidien|tous les jours|casual|décontracté)\b"
        }
    
    def get_or_create_session(self, session_id: str = "default") -> Dict[str, Any]:
        """Récupère ou crée une session utilisateur"""
        if session_id not in self.user_sessions:
            self.user_sessions[session_id] = {
                "context": {
                    "color": None,
                    "category": None,
                    "max_price": None,
                    "recipient": None,
                    "age": None,
                    "occasion": None,
                    "sentiment": "neutral"
                },
                "conversation_history": [],
                "last_questions": []
            }
        return self.user_sessions[session_id]
    
    def update_session_context(self, session_id: str, new_context: Dict[str, Any]):
        """Met à jour le contexte de la session avec les nouvelles informations"""
        session = self.get_or_create_session(session_id)
        
        # Fusionner les contextes (les nouvelles infos écrasent les anciennes)
        for key, value in new_context.items():
            if value is not None and key in session["context"]:
                session["context"][key] = value
    
    def detect_intent_and_context(self, message: str, session_id: str = "default") -> Dict[str, Any]:
        """Analyse complète du message pour comprendre l'intention et le contexte"""
        message_lower = message.lower()
        
        # Récupérer le contexte existant de la session
        session = self.get_or_create_session(session_id)
        existing_context = session["context"].copy()
        
        # Nouveau contexte détecté dans ce message
        new_context = {
            "intent": "product_search",
            "color": None,
            "category": None,
            "max_price": None,
            "recipient": None,
            "age": None,
            "occasion": None,
            "sentiment": "neutral",
            "needs_clarification": False
        }
        
        # Détection d'intention principale
        if re.search(r"\b(bonjour|salut|hello|hi|hey|bonsoir)\b", message_lower):
            new_context["intent"] = "salutations"
        elif re.search(r"\b(au revoir|bye|à bientôt|merci)\b", message_lower):
            new_context["intent"] = "au_revoir"
        elif re.search(r"\b(aide|help|comment|que faire)\b", message_lower):
            new_context["intent"] = "aide"
        
        # Extraction des critères du message actuel
        for color, pattern in self.color_patterns.items():
            if re.search(pattern, message_lower):
                new_context["color"] = color
                break
        
        for category, pattern in self.category_patterns.items():
            if re.search(pattern, message_lower):
                new_context["category"] = category
                break
        
        # Prix et budget
        for price_type, pattern in self.price_patterns.items():
            match = re.search(pattern, message_lower)
            if match and price_type in ["budget", "max_price"]:
                new_context["max_price"] = float(match.group(1))
                break
            elif re.search(pattern, message_lower) and price_type == "cheap":
                new_context["max_price"] = 30.0
        
        # Destinataire
        for recipient, pattern in self.recipient_patterns.items():
            if re.search(pattern, message_lower):
                new_context["recipient"] = recipient
                break
        
        # Détection de l'âge
        for age_type, pattern in self.age_patterns.items():
            match = re.search(pattern, message_lower)
            if match:
                if age_type == "age_specific":
                    new_context["age"] = int(match.group(1))
                elif age_type == "age_range":
                    age1, age2 = int(match.group(1)), int(match.group(2))
                    new_context["age"] = (age1 + age2) // 2
                break
        
        # Occasion
        for occasion, pattern in self.occasion_patterns.items():
            if re.search(pattern, message_lower):
                new_context["occasion"] = occasion
                break
        
        # Fusionner avec le contexte existant (priorité aux nouvelles infos)
        combined_context = existing_context.copy()
        for key, value in new_context.items():
            if value is not None:
                combined_context[key] = value
        
        # Mettre à jour la session
        self.update_session_context(session_id, new_context)
        
        return combined_context
    
    def search_products_smart(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recherche intelligente avec alternatives"""
        criteria = {}
        
        if context["color"]:
            criteria["color"] = context["color"]
        if context["category"]:
            criteria["category"] = context["category"]
        if context["max_price"]:
            criteria["max_price"] = context["max_price"]
        
        # Mapping recipient vers gender/age
        if context["recipient"]:
            if context["recipient"] in ["fille", "garçon"]:
                criteria["gender"] = context["recipient"]
                criteria["age_group"] = "enfant"
            elif context["recipient"] in ["femme", "homme"]:
                criteria["gender"] = context["recipient"]
                criteria["age_group"] = "adulte"
            elif context["recipient"] == "enfant":
                criteria["age_group"] = "enfant"
        
        # Gestion de l'âge spécifique
        if context["age"] and isinstance(context["age"], int):
            if context["age"] < 3:
                criteria["age_group"] = "bébé"
            elif 3 <= context["age"] <= 12:
                criteria["age_group"] = "enfant"
            elif 13 <= context["age"] <= 17:
                criteria["age_group"] = "ado"
            else:
                criteria["age_group"] = "adulte"
        
        # Tags selon l'occasion
        tags = []
        if context["occasion"] == "cadeau":
            tags.append("cadeau")
        if context["occasion"] == "sport":
            tags.append("sport")
        
        if tags:
            criteria["tags"] = tags
        
        # Recherche principale
        products = product_db.complex_search(**criteria)
        
        # Si pas de résultats, chercher des alternatives
        if not products and context["category"]:
            alt_criteria = {k: v for k, v in criteria.items() if k != "category"}
            if alt_criteria:
                products = product_db.complex_search(**alt_criteria)
        
        return products
    
    def generate_clarification_questions(self, context: Dict[str, Any], products: List[Dict], session_id: str = "default") -> List[str]:
        """Génère des questions de clarification intelligentes et proactives"""
        questions = []
        session = self.get_or_create_session(session_id)
        
        # Compter les critères déjà fournis
        criteria_count = sum([1 for key in ["color", "category", "max_price", "recipient", "age", "occasion"] 
                             if context[key] is not None])
        
        # Éviter de reposer les mêmes questions
        already_asked = set()
        for prev_q in session["last_questions"]:
            if "pour qui" in prev_q.lower():
                already_asked.add("recipient")
            if "budget" in prev_q.lower():
                already_asked.add("budget")
            if "couleur" in prev_q.lower():
                already_asked.add("color")
            if "âge" in prev_q.lower() or "age" in prev_q.lower():
                already_asked.add("age")
        
        # Poser des questions si moins de 3 critères
        if criteria_count < 3:
            # Questions sur le destinataire
            if not context["recipient"] and "recipient" not in already_asked:
                questions.append("👥 C'est pour qui exactement ? (fille, garçon, femme, homme)")
            
            # Questions sur l'âge
            if context["recipient"] and not context["age"] and "age" not in already_asked:
                if context["recipient"] in ["fille", "garçon", "enfant"]:
                    questions.append("🎂 Quel âge a cet enfant ?")
                elif context["recipient"] in ["femme", "homme"]:
                    questions.append("👤 Quel âge approximatif ?")
            
            # Questions sur le budget
            if not context["max_price"] and "budget" not in already_asked:
                questions.append("💰 Quel est votre budget maximum ? (ex: 20 DT, 50 DT, 100 DT)")
            
            # Questions sur les couleurs
            if not context["color"] and "color" not in already_asked:
                questions.append("🌈 Quelle couleur préférez-vous ?")
            
            # Questions sur l'occasion
            if not context["occasion"]:
                questions.append("🎁 C'est pour quelle occasion ?")
            
            # Questions sur la catégorie
            if not context["category"]:
                questions.append("🛍️ Quel type de produit vous intéresse ?")
        
        # Questions spécifiques selon l'âge
        if context["age"] and isinstance(context["age"], int):
            if 5 <= context["age"] <= 12:
                questions.append("🎮 Quels sont ses centres d'intérêt ? (sport, lecture, jeux, art)")
            elif 13 <= context["age"] <= 17:
                questions.append("😎 Quel style préfère-t-il/elle ?")
        
        # Limiter à 3 questions maximum
        final_questions = questions[:3]
        
        # Sauvegarder les questions posées
        session["last_questions"] = final_questions
        
        return final_questions
    
    def build_questions_response(self, context: Dict[str, Any], questions: List[str], session_id: str = "default") -> Dict[str, Any]:
        """Construit une réponse avec des questions de clarification"""
        intro_phrases = [
            "🤔 Pour vous proposer exactement ce qu'il vous faut, j'ai quelques questions :",
            "💡 Aidez-moi à mieux vous conseiller :",
            "🎯 Pour affiner ma recherche :",
            "✨ Quelques détails m'aideraient :"
        ]
        
        intro = random.choice(intro_phrases)
        questions_text = "\n".join([f"• {q}" for q in questions])
        
        response = f"{intro}\n\n{questions_text}\n\n💬 Répondez simplement, je m'occupe du reste !"
        
        return {"text": response}
    
    def build_success_response(self, products: List[Dict], context: Dict) -> Dict[str, Any]:
        """Construit une réponse motivante quand des produits sont trouvés"""
        response = f"🔥 Parfait ! J'ai trouvé {len(products)} produit(s) qui correspondent à vos critères !\n\n"
        
        # Ajout de conseils personnalisés
        if context["occasion"] == "cadeau":
            response += "🎁 Ces produits feront des cadeaux formidables !\n"
        if context["max_price"]:
            response += f"💰 Tous respectent votre budget de {context['max_price']} DT !\n"
        
        response += "\n✨ Excellent choix ! Cliquez sur 🛒 pour ajouter au panier !"
        
        return {"text": response}
    
    def build_no_results_response(self, context: Dict) -> Dict[str, Any]:
        """Construit une réponse alternative quand aucun produit n'est trouvé"""
        response = "🤔 Je n'ai pas trouvé exactement ce que vous cherchez, mais regardez ces alternatives :\n\n"
        response += "💡 N'hésitez pas à me donner plus de détails pour que je vous trouve le produit parfait !"
        
        return {"text": response}
    
    def generate_smart_response(self, user_message: str, session_id: str = "default") -> Dict[str, Any]:
        """Génère une réponse commerciale intelligente avec questions de clarification"""
        context = self.detect_intent_and_context(user_message, session_id)
        session = self.get_or_create_session(session_id)
        
        # Ajouter le message à l'historique
        session["conversation_history"].append({
            "user": user_message,
            "context": context.copy()
        })
        
        # Réponses avec questions proactives pour les salutations
        if context["intent"] == "salutations":
            greeting = random.choice(self.responses["salutations"])
            proactive_questions = [
                "🎯 Pour commencer, dites-moi : c'est pour qui ?",
                "💰 Quel est votre budget approximatif ?",
                "🌈 Avez-vous une couleur préférée ?"
            ]
            
            response_text = f"{greeting}\n\n💡 Pour vous proposer exactement ce qu'il vous faut :\n"
            response_text += "\n".join([f"• {q}" for q in proactive_questions])
            response_text += "\n\n✨ Plus vous me donnez d'infos, mieux je peux vous conseiller !"
            
            session["last_questions"] = proactive_questions
            
            return {
                "response": response_text,
                "products": [],
                "criteria": context,
                "follow_up": "awaiting_details",
                "questions": proactive_questions
            }
        
        # Autres réponses simples
        if context["intent"] in ["au_revoir", "aide"]:
            return {
                "response": random.choice(self.responses[context["intent"]]),
                "products": [],
                "criteria": context,
                "follow_up": None,
                "questions": []
            }
        
        # Recherche de produits
        products = self.search_products_smart(context)
        
        # Vérifier si on a besoin de poser des questions
        questions = self.generate_clarification_questions(context, products, session_id)
        
        # Construction de la réponse
        if products and len(products) > 0 and len(questions) == 0:
            response = self.build_success_response(products, context)
        elif questions:
            response = self.build_questions_response(context, questions, session_id)
        else:
            response = self.build_no_results_response(context)
        
        return {
            "response": response["text"],
            "products": products[:6] if products else [],
            "criteria": context,
            "follow_up": response.get("follow_up"),
            "questions": questions
        }
    
    def get_stats(self) -> Dict:
        """Statistiques du chatbot commercial"""
        total_products = len(product_db.get_all_products())
        categories = set(p["category"] for p in product_db.get_all_products())
        
        return {
            "total_products": total_products,
            "categories": list(categories),
            "sessions": len(self.user_sessions),
            "type": "Smart Sales Assistant with Session Management"
        }


# Instance globale du chatbot commercial intelligent
ecommerce_chatbot = SmartSalesAssistant()