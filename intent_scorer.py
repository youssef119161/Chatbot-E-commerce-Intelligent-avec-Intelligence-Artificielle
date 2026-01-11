"""
Intent Detection System with Keyword Scoring
Academic approach to natural language understanding for e-commerce chatbot
"""

import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class IntentScore:
    """Represents an intent detection result with confidence score"""
    intent: str
    confidence: float
    matched_keywords: List[str]
    context_data: Dict[str, Any]


class IntentScorer:
    """
    Intent detection using weighted keyword scoring system
    More flexible than regex patterns, handles variations better
    """
    
    def __init__(self):
        # Intent definitions with weighted keywords
        self.intent_definitions = {
            # HIGHEST PRIORITY: Off-topic detection (must be first)
            "off_topic": {
                "keywords": {
                    # General knowledge questions
                    "messi": 1.0, "football": 0.8, "sport": 0.6, "équipe": 0.7,
                    "histoire": 1.0, "géographie": 1.0, "mathématiques": 1.0, "math": 1.0,
                    "science": 1.0, "physique": 1.0, "chimie": 1.0, "biologie": 1.0,
                    "politique": 1.0, "président": 0.9, "gouvernement": 0.9,
                    "météo": 1.0, "temps": 0.7, "température": 0.9,
                    "actualité": 1.0, "news": 1.0, "nouvelles": 1.0,
                    "capitale": 1.0, "pays": 0.8, "ville": 0.7, "france": 0.9,
                    "tunisie": 0.9, "calcul": 1.0, "2+2": 1.0,
                    "réveillon": 1.0, "nouvel an": 1.0, "événement": 0.8,
                    
                    # Non-shopping topics
                    "recette": 1.0, "cuisine": 0.6, "cuisinier": 0.8, "plat": 0.8,
                    "couscous": 1.0, "manger": 0.7, "nourriture": 0.8,
                    "voyage": 1.0, "vacances": 0.9, "tourisme": 0.9, "hôtel": 0.8,
                    "partir": 0.7, "destination": 0.8,
                    "santé": 1.0, "médecin": 1.0, "maladie": 1.0, "symptôme": 1.0,
                    "rhume": 1.0, "soigner": 1.0, "guérir": 0.9, "traitement": 0.9,
                    "travail": 0.7, "emploi": 0.8, "job": 0.8, "carrière": 0.8,
                    "choisir": 0.6, "métier": 0.8,
                    "école": 0.9, "université": 0.9, "étudiant": 0.8, "cours": 0.8,
                    
                    # Technical/IT questions
                    "ordinateur": 0.8, "internet": 0.9, "wifi": 1.0, "password": 1.0,
                    "mot de passe": 1.0, "réparer": 1.0, "installer": 1.0,
                    "logiciel": 0.9, "application": 0.7, "téléphone": 0.7,
                    "windows": 1.0, "système": 0.8,
                    
                    # Entertainment
                    "film": 0.9, "cinéma": 0.9, "série": 0.9, "musique": 0.9,
                    "chanson": 0.9, "artiste": 0.8, "concert": 0.8,
                    "recommande": 0.7, "recommandation": 0.7,
                    
                    # Philosophy/abstract
                    "sens de la vie": 1.0, "bonheur": 0.8, "amour": 0.8,
                    "philosophie": 1.0, "religion": 1.0, "dieu": 1.0,
                    "penses-tu": 0.9, "opinion": 0.8, "crois-tu": 0.9,
                    
                    # Question words that often indicate off-topic
                    "pourquoi": 0.5, "comment faire": 0.7, "expliquer": 0.6,
                    "parlez-moi": 0.8, "parle-moi": 0.8, "donne-moi": 0.7,
                    "quelle est": 0.6, "quel est": 0.6, "qu'est-ce": 0.6
                },
                "threshold": 0.3  # Very low threshold for aggressive detection
            },
            
            # SECOND HIGHEST PRIORITY: Personal questions about chatbot
            "personal_question": {
                "keywords": {
                    # Personal questions about chatbot identity
                    "ton âge": 1.0, "votre âge": 1.0, "quel âge": 0.8,
                    "ton nom": 1.0, "votre nom": 1.0, "comment tu t'appelles": 1.0,
                    "qui es-tu": 1.0, "qui êtes-vous": 1.0, "que fais-tu": 0.9,
                    "d'où viens-tu": 1.0, "où habites-tu": 1.0,
                    "es-tu humain": 1.0, "êtes-vous humain": 1.0, "robot": 0.8,
                    "intelligence artificielle": 0.9, "ia": 0.8,
                    "comment ça va": 0.9, "ça va": 0.7, "comment allez-vous": 0.9,
                    "tu fais quoi": 0.9, "que faites-vous": 0.9
                },
                "threshold": 0.4
            },
            
            "greeting": {
                "keywords": {
                    "bonjour": 1.0, "salut": 1.0, "hello": 1.0, "hi": 0.9,
                    "bonsoir": 0.9, "hey": 0.8, "coucou": 0.8
                },
                "threshold": 0.7
            },
            
            "farewell": {
                "keywords": {
                    "au revoir": 1.0, "bye": 1.0, "à bientôt": 0.9,
                    "merci": 0.8, "tchao": 0.8, "salut": 0.6
                },
                "threshold": 0.7
            },
            
            "product_search": {
                "keywords": {
                    "cherche": 1.0, "veux": 1.0, "besoin": 1.0, "trouve": 0.9,
                    "acheter": 0.9, "commander": 0.8, "voir": 0.7, "montrer": 0.7,
                    "produit": 1.0, "article": 0.7, "quelque chose": 0.8,
                    "je veux": 1.0, "je cherche": 1.0, "j'ai besoin": 1.0,
                    "je veux un": 1.0, "je veux une": 1.0, "je cherche un": 1.0, "je cherche une": 1.0,
                    "comme un": 0.8, "comme une": 0.8, "un produit": 1.0, "une produit": 1.0
                },
                "threshold": 0.3  # Even lower threshold for better detection
            },
            
            "gift_intent": {
                "keywords": {
                    "cadeau": 1.0, "offrir": 1.0, "gift": 1.0, "surprise": 0.9,
                    "anniversaire": 0.8, "fête": 0.8, "noël": 0.8,
                    "pour ma": 0.9, "pour mon": 0.9, "pour une": 0.9, "pour un": 0.9,
                    "pour sa": 0.8, "pour son": 0.8, "pour leur": 0.8,
                    "je veux un cadeau": 1.0, "je cherche un cadeau": 1.0,
                    "cadeau a": 1.0, "cadeau à": 1.0, "comme un cadeau": 1.0
                },
                "threshold": 0.4  # Lower threshold for better detection
            },
            
            "recipient_info": {
                "keywords": {
                    "fille": 1.0, "garçon": 1.0, "femme": 1.0, "homme": 1.0,
                    "enfant": 0.9, "bébé": 0.9, "ado": 0.8, "adulte": 0.8,
                    "maman": 0.8, "papa": 0.8, "copain": 0.7, "copine": 0.7
                },
                "threshold": 0.8
            },
            
            "budget_info": {
                "keywords": {
                    "budget": 1.0, "prix": 1.0, "coût": 0.9, "dépenser": 0.9,
                    "maximum": 0.8, "pas cher": 0.8, "abordable": 0.7,
                    "dt": 0.6, "dinar": 0.6, "euro": 0.5
                },
                "threshold": 0.6
            },
            
            "color_preference": {
                "keywords": {
                    "rouge": 1.0, "bleu": 1.0, "vert": 1.0, "noir": 1.0,
                    "blanc": 1.0, "rose": 1.0, "jaune": 1.0, "violet": 0.9,
                    "orange": 0.9, "couleur": 0.8, "coloré": 0.7
                },
                "threshold": 0.8
            },
            
            "age_info": {
                "keywords": {
                    "ans": 1.0, "âge": 1.0, "vieux": 0.8, "jeune": 0.8,
                    "petit": 0.7, "grand": 0.7, "year": 0.9, "old": 0.8
                },
                "threshold": 0.7
            },
            
            "help_request": {
                "keywords": {
                    "aide": 1.0, "help": 1.0, "comment": 0.9, "expliquer": 0.8,
                    "comprendre": 0.8, "savoir": 0.7, "question": 0.7
                },
                "threshold": 0.7
            },
            
            "category_preference": {
                "keywords": {
                    "casquette": 1.0, "bijoux": 1.0, "sac": 1.0, "vêtement": 1.0,
                    "jouet": 1.0, "livre": 1.0, "montre": 1.0, "accessoire": 0.9,
                    "décoration": 0.8, "sport": 0.8, "cuisine": 0.8,
                    "pas cher": 0.8, "abordable": 0.7, "bon marché": 0.8
                },
                "threshold": 0.6
            }
        }
        
        # Patterns for extracting specific data
        self.data_extractors = {
            "age": r"\b(\d+)\s*(?:ans?|years?)\b",
            "price": r"\b(\d+)\s*(?:dt|dinar|euro|€)\b",
            "color": r"\b(rouge|bleu|vert|noir|blanc|rose|jaune|violet|orange)\b",
            "recipient": r"\b(fille|garçon|femme|homme|enfant|bébé)\b"
        }
    
    def normalize_message(self, message: str) -> str:
        """Normalize message for better matching"""
        # Convert to lowercase and remove extra spaces
        normalized = re.sub(r'\s+', ' ', message.lower().strip())
        
        # Handle common variations and contractions
        replacements = {
            "j'ai besoin": "besoin",
            "je veux": "veux",
            "je cherche": "cherche",
            "pour ma": "pour",
            "pour mon": "pour",
            "cadeau a": "cadeau",
            "cadeau à": "cadeau",
            "comme un cadeau": "cadeau",
            "comme une cadeau": "cadeau",
            "un produit": "produit",
            "une produit": "produit",
            "le produit": "produit",
            "des produits": "produit",
            "ne depasse pas": "maximum",
            "ne dépasse pas": "maximum",
            "pas plus de": "maximum",
            "maximum de": "maximum"
        }
        
        for old, new in replacements.items():
            normalized = normalized.replace(old, new)
        
        return normalized
    
    def score_intent(self, message: str, intent: str) -> IntentScore:
        """Score a message against a specific intent"""
        normalized_msg = self.normalize_message(message)
        intent_def = self.intent_definitions[intent]
        
        total_score = 0.0
        matched_keywords = []
        word_count = len(normalized_msg.split())
        
        # Score based on keyword matches
        for keyword, weight in intent_def["keywords"].items():
            if keyword in normalized_msg:
                # Boost score for exact matches
                if f" {keyword} " in f" {normalized_msg} ":
                    score_boost = weight * 1.2
                else:
                    score_boost = weight
                
                total_score += score_boost
                matched_keywords.append(keyword)
        
        # Normalize score by message length (prevent long messages from dominating)
        if word_count > 0:
            confidence = min(total_score / max(word_count * 0.5, 1.0), 1.0)
        else:
            confidence = 0.0
        
        # Extract context data
        context_data = self.extract_context_data(normalized_msg)
        
        return IntentScore(
            intent=intent,
            confidence=confidence,
            matched_keywords=matched_keywords,
            context_data=context_data
        )
    
    def extract_context_data(self, message: str) -> Dict[str, Any]:
        """Extract specific data from message using patterns"""
        context = {}
        
        for data_type, pattern in self.data_extractors.items():
            matches = re.findall(pattern, message)
            if matches:
                if data_type == "age":
                    context["age"] = int(matches[0])
                elif data_type == "price":
                    context["max_price"] = float(matches[0])
                elif data_type in ["color", "recipient"]:
                    context[data_type] = matches[0]
        
        return context
    
    def detect_intents(self, message: str, top_k: int = 3) -> List[IntentScore]:
        """
        Detect multiple intents in a message, return top K by confidence
        OFF-TOPIC and PERSONAL_QUESTION have HIGHEST PRIORITY and override others
        """
        if not message or not message.strip():
            return []
        
        intent_scores = []
        
        # FIRST: Check for off-topic intent with highest priority
        off_topic_score = self.score_intent(message, "off_topic")
        if off_topic_score.confidence >= self.intent_definitions["off_topic"]["threshold"]:
            # OFF-TOPIC DETECTED - Return only this intent, ignore others
            return [off_topic_score]
        
        # SECOND: Check for personal questions with second highest priority
        if "personal_question" in self.intent_definitions:
            personal_score = self.score_intent(message, "personal_question")
            if personal_score.confidence >= self.intent_definitions["personal_question"]["threshold"]:
                # PERSONAL QUESTION DETECTED - Return only this intent, ignore others
                return [personal_score]
        
        # THIRD: Score against all other intents (excluding off_topic and personal_question)
        for intent_name in self.intent_definitions:
            if intent_name in ["off_topic", "personal_question"]:
                continue  # Already checked above
                
            score = self.score_intent(message, intent_name)
            
            # Only include intents above threshold
            if score.confidence >= self.intent_definitions[intent_name]["threshold"]:
                intent_scores.append(score)
        
        # Sort by confidence and return top K
        intent_scores.sort(key=lambda x: x.confidence, reverse=True)
        return intent_scores[:top_k]
    
    def get_primary_intent(self, message: str) -> IntentScore:
        """Get the highest confidence intent"""
        intents = self.detect_intents(message, top_k=1)
        
        if intents:
            return intents[0]
        else:
            # Return unknown intent with low confidence
            return IntentScore(
                intent="unknown",
                confidence=0.0,
                matched_keywords=[],
                context_data=self.extract_context_data(self.normalize_message(message))
            )
    
    def add_intent_keywords(self, intent: str, keywords: Dict[str, float]):
        """Dynamically add keywords to an intent (for learning)"""
        if intent in self.intent_definitions:
            self.intent_definitions[intent]["keywords"].update(keywords)
        else:
            # Create new intent
            self.intent_definitions[intent] = {
                "keywords": keywords,
                "threshold": 0.6
            }
    
    def get_intent_stats(self) -> Dict[str, Any]:
        """Get statistics about intent definitions"""
        stats = {}
        for intent, definition in self.intent_definitions.items():
            stats[intent] = {
                "keyword_count": len(definition["keywords"]),
                "threshold": definition["threshold"],
                "avg_weight": sum(definition["keywords"].values()) / len(definition["keywords"])
            }
        return stats


# Global instance
intent_scorer = IntentScorer()