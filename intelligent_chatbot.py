"""
Intelligent Chatbot System
Integrates intent scoring, conversation memory, and learning capabilities
"""

import random
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from intent_scorer import intent_scorer, IntentScore
from conversation_memory import conversation_memory, ConversationTurn
from database import product_db


@dataclass
class ChatbotResponse:
    """Structured chatbot response"""
    message: str
    products: List[Dict[str, Any]]
    confidence: float
    detected_intents: List[str]
    context_used: Dict[str, Any]
    needs_clarification: bool
    suggested_questions: List[str]


class IntelligentChatbot:
    """
    Advanced chatbot using intent scoring and conversation memory
    Academic approach with learning capabilities
    """
    
    def __init__(self):
        self.confidence_threshold = 0.4  # Lowered from 0.6 for better shopping detection
        self.unknown_threshold = 0.2     # Lowered from 0.3
        
        # Response templates organized by intent
        self.response_templates = {
            "greeting": [
                "🛍️ Bonjour ! Je suis votre assistant shopping intelligent. Comment puis-je vous aider aujourd'hui ?",
                "✨ Salut ! Ravi de vous revoir ! Que recherchez-vous ?",
                "🌟 Hello ! Prêt pour une expérience shopping personnalisée ?",
                "🎉 Bonjour ! J'ai hâte de vous aider à trouver le produit parfait !"
            ],
            
            "farewell": [
                "🛒 Merci pour votre visite ! À bientôt !",
                "✨ Au revoir ! J'espère vous avoir aidé !",
                "💫 À plus tard ! Revenez quand vous voulez !",
                "🎁 Merci ! N'hésitez pas à revenir !"
            ],
            
            "help_request": [
                "🤝 Bien sûr ! Je peux vous aider à trouver des produits selon vos critères.",
                "💡 Avec plaisir ! Décrivez-moi ce que vous cherchez.",
                "🎯 Je suis là pour ça ! Parlez-moi de vos besoins.",
                "✨ Parfait ! Plus vous me donnez d'infos, mieux je peux vous conseiller !"
            ],
            
            "product_search": [
                "🔍 Excellente idée ! Laissez-moi chercher ça pour vous.",
                "🛍️ Parfait ! Je vais vous trouver exactement ce qu'il vous faut.",
                "⭐ Super ! J'ai plusieurs options intéressantes à vous proposer.",
                "🎯 Génial ! Voici ce que j'ai trouvé pour vous."
            ],
            
            "unknown": [
                "🤔 Je ne suis pas sûr de bien comprendre. Pouvez-vous reformuler ?",
                "💭 Hmm, pouvez-vous être plus précis sur ce que vous cherchez ?",
                "🔄 Je n'ai pas bien saisi. Essayez de me donner plus de détails.",
                "❓ Pouvez-vous m'expliquer différemment ce que vous voulez ?"
            ]
        }
        
        # Clarification questions by missing context
        self.clarification_questions = {
            "recipient": [
                "👥 C'est pour qui exactement ?",
                "🎯 Le produit est destiné à quelle personne ?",
                "👤 Pour qui cherchez-vous ce produit ?"
            ],
            "budget": [
                "💰 Quel est votre budget ?",
                "💵 Combien souhaitez-vous dépenser ?",
                "🏷️ Avez-vous une fourchette de prix en tête ?"
            ],
            "occasion": [
                "🎁 C'est pour quelle occasion ?",
                "🎉 Dans quel contexte sera utilisé ce produit ?",
                "📅 Pour quel événement ?"
            ],
            "age": [
                "🎂 Quel âge a cette personne ?",
                "👶 Pouvez-vous me dire l'âge ?",
                "📏 Quelle tranche d'âge ?"
            ]
        }
    
    def process_message(self, user_id: str, message: str) -> ChatbotResponse:
        """
        Main message processing pipeline
        """
        # Step 1: Detect intents using scoring system
        primary_intent = intent_scorer.get_primary_intent(message)
        all_intents = intent_scorer.detect_intents(message, top_k=3)
        
        # Step 2: Get conversation context
        conversation_context = conversation_memory.get_conversation_context(user_id)
        user_preferences = conversation_memory.get_user_preferences(user_id)
        
        # Step 3: Merge context from intent detection and conversation history
        merged_context = self.merge_contexts(
            primary_intent.context_data,
            conversation_context,
            user_preferences
        )
        
        # Step 4: Generate response based on intent and context
        if primary_intent.confidence >= self.confidence_threshold:
            response = self.generate_confident_response(
                primary_intent, all_intents, merged_context, user_id
            )
        elif primary_intent.confidence >= self.unknown_threshold:
            response = self.generate_uncertain_response(
                primary_intent, merged_context, user_id
            )
        else:
            # Log unknown query for learning
            conversation_memory.log_unknown_query(message)
            response = self.generate_unknown_response(merged_context, user_id)
        
        # Step 5: Save conversation turn
        turn = ConversationTurn(
            user_id=user_id,
            message=message,
            intent=primary_intent.intent,
            confidence=primary_intent.confidence,
            context_data=primary_intent.context_data,
            response=response.message,
            timestamp=datetime.now()
        )
        conversation_memory.add_conversation_turn(turn)
        
        return response
    
    def merge_contexts(self, intent_context: Dict[str, Any], 
                      conversation_context: Dict[str, Any],
                      user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Intelligently merge different context sources
        Priority: intent_context > conversation_context > user_preferences
        """
        merged = {}
        
        # Start with user preferences (lowest priority)
        for key, pref_data in user_preferences.items():
            if isinstance(pref_data, dict) and 'value' in pref_data:
                merged[key] = pref_data['value']
        
        # Add conversation context (medium priority)
        for key, value in conversation_context.items():
            if value is not None:
                merged[key] = value
        
        # Add intent context (highest priority)
        for key, value in intent_context.items():
            if value is not None:
                merged[key] = value
        
        return merged
    
    def generate_confident_response(self, primary_intent: IntentScore, 
                                  all_intents: List[IntentScore],
                                  context: Dict[str, Any],
                                  user_id: str) -> ChatbotResponse:
        """Generate response when we're confident about the intent"""
        
        intent_name = primary_intent.intent
        
        # Handle different intents
        if intent_name == "off_topic":
            return self.handle_off_topic(context)
        
        elif intent_name == "personal_question":
            return self.handle_personal_question(context)
        
        elif intent_name == "greeting":
            return self.handle_greeting(context, user_id)
        
        elif intent_name == "farewell":
            return self.handle_farewell(context)
        
        elif intent_name == "help_request":
            return self.handle_help_request(context)
        
        elif intent_name in ["product_search", "gift_intent", "category_preference"]:
            return self.handle_product_search(context, all_intents)
        
        elif intent_name in ["recipient_info", "budget_info", "color_preference", "age_info"]:
            return self.handle_context_update(context, intent_name)
        
        else:
            return self.handle_general_response(primary_intent, context)
    
    def generate_uncertain_response(self, primary_intent: IntentScore,
                                  context: Dict[str, Any],
                                  user_id: str) -> ChatbotResponse:
        """
        Generate response when we're uncertain about the intent
        CRITICAL: Return products for shopping intents, but NOT for off-topic/personal
        """
        
        # Check if this is a shopping-related intent even with low confidence
        shopping_intents = ["product_search", "gift_intent", "category_preference", "budget_info", "recipient_info"]
        is_shopping_intent = primary_intent.intent in shopping_intents
        
        if is_shopping_intent:
            # Shopping intent with low confidence - be more positive
            clarification_msg = random.choice([
                "🛍️ Parfait ! Je vois que vous cherchez quelque chose de spécial.",
                "✨ Excellente idée ! Laissez-moi vous aider à trouver ce qu'il vous faut.",
                "🎯 Super ! J'ai quelques suggestions qui pourraient vous intéresser.",
                "💡 Génial ! Voici ce que j'ai trouvé selon vos critères."
            ])
            
            # Suggest what we detected
            suggestions = []
            if primary_intent.matched_keywords:
                suggestions.append(f"✅ J'ai compris: {', '.join(primary_intent.matched_keywords)}")
            
            # Show products and ask for more details if needed
            products = self.search_products_with_context(context)[:6]
            shopping_guidance = f"\n\n🔍 J'ai trouvé {len(products)} produit(s) correspondant !"
            
            if len(context) < 3:
                shopping_guidance += "\n\n💬 Pour affiner la recherche, précisez-moi:\n• La couleur souhaitée\n• Votre budget maximum\n• L'occasion ou le style"
            
        else:
            # Non-shopping intent - ask for clarification
            clarification_msg = random.choice([
                "🤔 Je pense comprendre, mais pouvez-vous être plus précis ?",
                "💭 J'ai une idée de ce que vous cherchez, mais aidez-moi à mieux comprendre.",
                "🔍 Je vois plusieurs possibilités. Pouvez-vous me donner plus de détails ?"
            ])
            
            suggestions = []
            if primary_intent.matched_keywords:
                suggestions.append(f"Vous parlez de: {', '.join(primary_intent.matched_keywords)}")
            
            products = []
            shopping_guidance = "\n\n💡 Pour mieux vous aider, précisez:\n• Ce que vous cherchez exactement\n• Votre budget\n• Pour qui c'est destiné"
        
        return ChatbotResponse(
            message=f"{clarification_msg}\n\n" + "\n".join(suggestions) + shopping_guidance,
            products=products,
            confidence=primary_intent.confidence,
            detected_intents=[primary_intent.intent],
            context_used=context,
            needs_clarification=True,
            suggested_questions=self.generate_clarification_questions(context)
        )
    
    def generate_unknown_response(self, context: Dict[str, Any],
                                user_id: str) -> ChatbotResponse:
        """
        Generate response for unknown intents
        CRITICAL: Be very strict - only return products for EXPLICIT shopping context
        """
        
        unknown_msg = random.choice(self.response_templates["unknown"])
        
        # STRICT CHECK: Only allow products if there's EXPLICIT shopping context from CURRENT message
        # Do NOT use conversation history context for unknown intents
        current_message_context = {k: v for k, v in context.items() 
                                 if k in ["recipient", "max_price", "color", "age", "category"] 
                                 and v is not None}
        
        # VERY STRICT: Only show products if we have MULTIPLE shopping indicators
        has_strong_shopping_context = (
            len(current_message_context) >= 2 or  # Multiple shopping criteria
            context.get("category") is not None or  # Explicit category mentioned
            context.get("max_price") is not None    # Explicit price mentioned
        )
        
        if has_strong_shopping_context:
            # Strong shopping context - provide products
            help_msg = "\n\n💡 Basé sur vos critères, voici quelques suggestions:"
            products = self.search_products_with_context(current_message_context)[:4]
        else:
            # Weak or no shopping context - redirect to shopping without products
            help_msg = "\n\n💡 Je suis un assistant e-commerce. Je peux vous aider à:\n• Trouver des produits par catégorie\n• Suggérer des cadeaux personnalisés\n• Filtrer par budget et couleur"
            products = []
        
        # Add shopping suggestions for unclear requests
        suggestions_msg = "\n\n👉 Soyez plus précis:\n• 'Je cherche un cadeau pour ma fille de 8 ans'\n• 'Montrez-moi des casquettes rouges'\n• 'Budget maximum 30 DT'"
        
        return ChatbotResponse(
            message=unknown_msg + help_msg + suggestions_msg,
            products=products,
            confidence=0.0,
            detected_intents=["unknown"],
            context_used=current_message_context,  # Only use current message context
            needs_clarification=True,
            suggested_questions=[
                "🛍️ Que recherchez-vous exactement ?",
                "🎯 Pouvez-vous me décrire ce que vous voulez acheter ?",
                "💡 Avez-vous une catégorie de produit en tête ?"
            ]
        )
    
    def handle_personal_question(self, context: Dict[str, Any]) -> ChatbotResponse:
        """
        Handle personal questions about the chatbot - NEVER return products
        CRITICAL: Completely ignore any shopping context
        """
        
        personal_responses = [
            "Je suis un assistant e-commerce et je ne peux pas répondre aux questions personnelles ou générales.",
            "Je suis conçu uniquement pour vous aider avec vos achats. Je ne peux pas discuter de sujets personnels.",
            "Mon rôle est de vous assister dans vos recherches de produits. Je ne réponds qu'aux questions liées au shopping.",
            "Je suis spécialisé dans l'e-commerce. Pour les questions personnelles, consultez d'autres sources."
        ]
        
        shopping_redirect = [
            "👉 Posez-moi une question liée aux produits ou aux cadeaux.",
            "💡 Demandez-moi plutôt ce que vous souhaitez acheter.",
            "🛍️ Je peux vous aider à trouver des produits ou des cadeaux.",
            "🎯 Parlez-moi de vos besoins d'achat."
        ]
        
        # Select random responses
        main_response = random.choice(personal_responses)
        redirect = random.choice(shopping_redirect)
        
        full_message = f"{main_response}\n\n{redirect}"
        
        return ChatbotResponse(
            message=full_message,
            products=[],  # NEVER return products for personal questions
            confidence=1.0,
            detected_intents=["personal_question"],
            context_used={},  # IGNORE all context for personal questions
            needs_clarification=False,
            suggested_questions=[
                "🛍️ Que souhaitez-vous acheter ?",
                "🎁 Cherchez-vous un cadeau ?",
                "💰 Avez-vous un budget en tête ?"
            ]
        )
    
    def handle_off_topic(self, context: Dict[str, Any]) -> ChatbotResponse:
        """
        Handle off-topic intents - NEVER return products
        CRITICAL: Completely ignore any shopping context
        """
        
        off_topic_responses = [
            "Je suis un assistant e-commerce et je ne peux pas répondre aux questions générales ou non liées au shopping.",
            "Je suis spécialisé dans l'aide à l'achat. Je ne peux répondre qu'aux questions sur les produits et le shopping.",
            "Mon domaine d'expertise est l'e-commerce. Je peux vous aider à trouver des articles, des cadeaux ou des produits.",
            "Je suis conçu pour vous assister dans vos achats en ligne. Pour d'autres sujets, consultez d'autres sources."
        ]
        
        shopping_suggestions = [
            "👉 Par exemple : 'Je cherche un cadeau pour ma sœur'",
            "💡 Essayez : 'Montrez-moi des produits bleus'",
            "🎁 Ou demandez : 'Quel cadeau pour un budget de 50 DT ?'",
            "🛒 Vous pouvez dire : 'Je veux acheter une casquette'"
        ]
        
        # Select random responses
        main_response = random.choice(off_topic_responses)
        suggestion = random.choice(shopping_suggestions)
        
        full_message = f"{main_response}\n\n{suggestion}"
        
        return ChatbotResponse(
            message=full_message,
            products=[],  # NEVER return products for off-topic
            confidence=1.0,
            detected_intents=["off_topic"],
            context_used={},  # IGNORE all context for off-topic questions
            needs_clarification=False,
            suggested_questions=[
                "🛍️ Que souhaitez-vous acheter ?",
                "🎁 Cherchez-vous un cadeau ?",
                "💰 Avez-vous un budget en tête ?"
            ]
        )
    
    def handle_greeting(self, context: Dict[str, Any], user_id: str) -> ChatbotResponse:
        """Handle greeting intents"""
        
        # Personalize greeting based on conversation history
        history = conversation_memory.get_conversation_history(user_id)
        
        if len(history) > 1:  # Returning user
            greeting = random.choice([
                "✨ Ravi de vous revoir ! Comment puis-je vous aider aujourd'hui ?",
                "🌟 Hello ! Que puis-je faire pour vous cette fois ?",
                "🎉 Salut ! Prêt pour une nouvelle session shopping ?"
            ])
        else:  # New user
            greeting = random.choice(self.response_templates["greeting"])
        
        # Add personalized suggestions based on preferences
        suggestions = []
        user_prefs = conversation_memory.get_user_preferences(user_id)
        if user_prefs:
            suggestions.append("💡 Basé sur vos préférences, je peux vous proposer des suggestions personnalisées !")
        
        return ChatbotResponse(
            message=greeting + ("\n\n" + "\n".join(suggestions) if suggestions else ""),
            products=[],
            confidence=1.0,
            detected_intents=["greeting"],
            context_used=context,
            needs_clarification=False,
            suggested_questions=[
                "🛍️ Que recherchez-vous aujourd'hui ?",
                "🎁 Cherchez-vous un cadeau ?",
                "💰 Avez-vous un budget en tête ?"
            ]
        )
    
    def handle_farewell(self, context: Dict[str, Any]) -> ChatbotResponse:
        """Handle farewell intents"""
        
        farewell_msg = random.choice(self.response_templates["farewell"])
        
        return ChatbotResponse(
            message=farewell_msg,
            products=[],
            confidence=1.0,
            detected_intents=["farewell"],
            context_used=context,
            needs_clarification=False,
            suggested_questions=[]
        )
    
    def handle_help_request(self, context: Dict[str, Any]) -> ChatbotResponse:
        """Handle help request intents"""
        
        help_msg = random.choice(self.response_templates["help_request"])
        
        # Add specific help based on context
        help_details = [
            "🔍 Recherche de produits par catégorie",
            "🎁 Suggestions de cadeaux personnalisés",
            "💰 Filtrage par budget",
            "🌈 Recherche par couleur",
            "👥 Recommandations selon l'âge/genre"
        ]
        
        full_message = f"{help_msg}\n\n💡 Voici ce que je peux faire:\n" + "\n".join(f"• {detail}" for detail in help_details)
        
        return ChatbotResponse(
            message=full_message,
            products=[],
            confidence=1.0,
            detected_intents=["help_request"],
            context_used=context,
            needs_clarification=False,
            suggested_questions=[
                "🛍️ Que voulez-vous acheter ?",
                "🎯 Avez-vous une catégorie en tête ?",
                "💰 Quel est votre budget ?"
            ]
        )
    
    def handle_product_search(self, context: Dict[str, Any], 
                            all_intents: List[IntentScore]) -> ChatbotResponse:
        """Handle product search intents"""
        
        # Search for products using context
        products = self.search_products_with_context(context)
        
        # Generate response based on results
        if products:
            response_msg = random.choice(self.response_templates["product_search"])
            
            # Add context-specific information
            context_info = []
            if context.get("recipient"):
                context_info.append(f"pour {context['recipient']}")
            if context.get("max_price"):
                context_info.append(f"budget {context['max_price']} DT")
            if context.get("color"):
                context_info.append(f"couleur {context['color']}")
            
            if context_info:
                response_msg += f"\n\n📋 Critères: {', '.join(context_info)}"
            
            response_msg += f"\n\n✨ J'ai trouvé {len(products)} produit(s) correspondant !"
            
            needs_clarification = len(context) < 3  # Need more context
            
        else:
            response_msg = "🤔 Je n'ai pas trouvé de produits correspondant exactement à vos critères."
            response_msg += "\n\n💡 Essayons avec des critères différents ou regardez ces alternatives :"
            
            # Get alternative products
            products = product_db.get_all_products()[:6]
            needs_clarification = True
        
        return ChatbotResponse(
            message=response_msg,
            products=products[:6],
            confidence=0.9,
            detected_intents=[intent.intent for intent in all_intents],
            context_used=context,
            needs_clarification=needs_clarification,
            suggested_questions=self.generate_clarification_questions(context) if needs_clarification else []
        )
    
    def handle_context_update(self, context: Dict[str, Any], 
                            intent_name: str) -> ChatbotResponse:
        """Handle context information updates"""
        
        acknowledgments = {
            "recipient_info": "👥 Parfait ! J'ai noté le destinataire.",
            "budget_info": "💰 Très bien ! Budget enregistré.",
            "color_preference": "🌈 Excellent ! Couleur notée.",
            "age_info": "🎂 Parfait ! Âge pris en compte."
        }
        
        ack_msg = acknowledgments.get(intent_name, "✅ Information enregistrée !")
        
        # Search for products with updated context
        products = self.search_products_with_context(context)
        
        if products:
            ack_msg += f"\n\n🔍 Avec ces informations, j'ai trouvé {len(products)} produit(s) !"
        else:
            ack_msg += "\n\n🤔 J'ai besoin de quelques détails supplémentaires pour vous proposer des produits."
        
        return ChatbotResponse(
            message=ack_msg,
            products=products[:6],
            confidence=0.8,
            detected_intents=[intent_name],
            context_used=context,
            needs_clarification=len(context) < 3,
            suggested_questions=self.generate_clarification_questions(context)
        )
    
    def handle_general_response(self, intent: IntentScore, 
                              context: Dict[str, Any]) -> ChatbotResponse:
        """Handle general/other intents"""
        
        general_msg = f"🤖 J'ai détecté votre intention ({intent.intent}) avec {intent.confidence:.1%} de confiance."
        general_msg += "\n\n💡 Comment puis-je vous aider concrètement ?"
        
        return ChatbotResponse(
            message=general_msg,
            products=[],
            confidence=intent.confidence,
            detected_intents=[intent.intent],
            context_used=context,
            needs_clarification=True,
            suggested_questions=[
                "🛍️ Que recherchez-vous ?",
                "🎯 Puis-je vous aider à trouver un produit ?",
                "💡 Avez-vous une question spécifique ?"
            ]
        )
    
    def search_products_with_context(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search products using available context"""
        
        # Build search criteria from context
        criteria = {}
        
        # Map context to database criteria
        if context.get("color"):
            criteria["color"] = context["color"]
        
        if context.get("max_price"):
            criteria["max_price"] = context["max_price"]
        
        if context.get("recipient"):
            recipient = context["recipient"]
            if recipient in ["fille", "garçon"]:
                criteria["gender"] = recipient
                criteria["age_group"] = "enfant"
            elif recipient in ["femme", "homme"]:
                criteria["gender"] = recipient
                criteria["age_group"] = "adulte"
            elif recipient == "enfant":
                criteria["age_group"] = "enfant"
        
        if context.get("age"):
            age = context["age"]
            if isinstance(age, int):
                if age < 3:
                    criteria["age_group"] = "bébé"
                elif 3 <= age <= 12:
                    criteria["age_group"] = "enfant"
                elif 13 <= age <= 17:
                    criteria["age_group"] = "ado"
                else:
                    criteria["age_group"] = "adulte"
        
        # Add category if available
        if context.get("category"):
            criteria["category"] = context["category"]
        
        # Search with criteria
        if criteria:
            products = product_db.complex_search(**criteria)
            
            # If no results, try with fewer criteria
            if not products and len(criteria) > 1:
                # Remove least important criteria and try again
                for key_to_remove in ["color", "category", "age_group"]:
                    if key_to_remove in criteria:
                        reduced_criteria = {k: v for k, v in criteria.items() if k != key_to_remove}
                        products = product_db.complex_search(**reduced_criteria)
                        if products:
                            break
            
            return products
        else:
            # No specific criteria, return popular products
            return product_db.get_all_products()[:8]
    
    def generate_clarification_questions(self, context: Dict[str, Any]) -> List[str]:
        """Generate clarification questions based on missing context"""
        
        questions = []
        
        # Check what's missing and suggest questions
        if not context.get("recipient"):
            questions.extend(random.sample(self.clarification_questions["recipient"], 1))
        
        if not context.get("max_price"):
            questions.extend(random.sample(self.clarification_questions["budget"], 1))
        
        if not context.get("occasion"):
            questions.extend(random.sample(self.clarification_questions["occasion"], 1))
        
        if context.get("recipient") in ["fille", "garçon", "enfant"] and not context.get("age"):
            questions.extend(random.sample(self.clarification_questions["age"], 1))
        
        # Limit to 3 questions max
        return questions[:3]
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        
        return {
            "intent_scorer": intent_scorer.get_intent_stats(),
            "conversation_memory": conversation_memory.get_conversation_stats(),
            "confidence_threshold": self.confidence_threshold,
            "unknown_threshold": self.unknown_threshold,
            "response_templates": {k: len(v) for k, v in self.response_templates.items()}
        }


# Global instance
intelligent_chatbot = IntelligentChatbot()