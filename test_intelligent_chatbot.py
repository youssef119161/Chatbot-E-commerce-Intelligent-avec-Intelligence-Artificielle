#!/usr/bin/env python3
"""
Comprehensive Test Suite for Intelligent Chatbot System
Tests intent scoring, conversation memory, and learning capabilities
"""

import sys
import os
import json
from datetime import datetime

# Add backend to path
sys.path.append(os.path.dirname(__file__))

from intelligent_chatbot import intelligent_chatbot
from intent_scorer import intent_scorer
from conversation_memory import conversation_memory


def test_intent_scoring():
    """Test the intent scoring system"""
    print("🧠 Testing Intent Scoring System")
    print("=" * 50)
    
    test_messages = [
        "Bonjour, comment allez-vous ?",
        "Je cherche un cadeau pour ma fille de 8 ans",
        "Avez-vous des casquettes rouges pas chères ?",
        "Mon budget est de 50 DT maximum",
        "Au revoir et merci",
        "Pouvez-vous m'aider à trouver quelque chose ?",
        "Je veux quelque chose de bleu pour un garçon",
        "C'est pour un anniversaire"
    ]
    
    for message in test_messages:
        print(f"\n📝 Message: '{message}'")
        
        # Test primary intent
        primary = intent_scorer.get_primary_intent(message)
        print(f"🎯 Primary Intent: {primary.intent} (confidence: {primary.confidence:.2f})")
        print(f"🔑 Keywords: {primary.matched_keywords}")
        print(f"📊 Context: {primary.context_data}")
        
        # Test all intents
        all_intents = intent_scorer.detect_intents(message, top_k=3)
        print(f"📈 Top Intents: {[(i.intent, f'{i.confidence:.2f}') for i in all_intents]}")
        print("-" * 30)


def test_conversation_memory():
    """Test the conversation memory system"""
    print("\n💾 Testing Conversation Memory System")
    print("=" * 50)
    
    user_id = "test_user_123"
    
    # Simulate a conversation
    conversation_flow = [
        "Bonjour",
        "Je cherche un cadeau",
        "Pour ma fille de 10 ans",
        "Budget 30 DT",
        "Elle aime le rose",
        "Montrez-moi des bijoux"
    ]
    
    print(f"👤 User ID: {user_id}")
    print("🔄 Simulating conversation flow...")
    
    for i, message in enumerate(conversation_flow, 1):
        print(f"\n{i}. User: {message}")
        
        # Process message
        response = intelligent_chatbot.process_message(user_id, message)
        
        print(f"   Bot: {response.message[:100]}...")
        print(f"   Confidence: {response.confidence:.2f}")
        print(f"   Intents: {response.detected_intents}")
        print(f"   Products: {len(response.products)}")
        
        # Show conversation context
        context = conversation_memory.get_conversation_context(user_id)
        print(f"   Context: {context}")
    
    # Show final conversation history
    print(f"\n📚 Final Conversation History:")
    history = conversation_memory.get_conversation_history(user_id)
    for turn in history:
        print(f"   {turn.timestamp.strftime('%H:%M:%S')} - {turn.intent} ({turn.confidence:.2f})")
    
    # Show user preferences
    preferences = conversation_memory.get_user_preferences(user_id)
    print(f"\n👤 User Preferences: {preferences}")


def test_learning_system():
    """Test the learning system with unknown queries"""
    print("\n🎓 Testing Learning System")
    print("=" * 50)
    
    unknown_messages = [
        "Avez-vous des produits écologiques ?",
        "Je veux quelque chose d'unique",
        "Pouvez-vous me recommander selon mes goûts ?",
        "Qu'est-ce qui est tendance en ce moment ?",
        "Avez-vous des promotions spéciales ?"
    ]
    
    for message in unknown_messages:
        print(f"\n❓ Unknown Query: '{message}'")
        
        # Test intent detection
        intent = intent_scorer.get_primary_intent(message)
        print(f"   Detected: {intent.intent} (confidence: {intent.confidence:.2f})")
        
        # If low confidence, it will be logged as unknown
        if intent.confidence < 0.3:
            conversation_memory.log_unknown_query(message)
            print("   ✅ Logged as unknown query for learning")
        
        # Process through chatbot
        response = intelligent_chatbot.process_message("learning_test_user", message)
        print(f"   Response: {response.message[:80]}...")
    
    # Show unknown queries
    print(f"\n📊 Unknown Queries Log:")
    unknown_queries = conversation_memory.get_unknown_queries(limit=10)
    for query in unknown_queries:
        print(f"   '{query['message']}' - Frequency: {query['frequency']}")


def test_multi_user_conversations():
    """Test multiple users with different conversation patterns"""
    print("\n👥 Testing Multi-User Conversations")
    print("=" * 50)
    
    users = {
        "alice": [
            "Salut",
            "Je veux un sac bleu",
            "Budget 40 DT",
            "Pour le travail"
        ],
        "bob": [
            "Bonjour",
            "Cadeau pour ma femme",
            "Elle aime les bijoux",
            "Pas plus de 60 DT"
        ],
        "charlie": [
            "Hello",
            "Jouet pour enfant",
            "Garçon de 5 ans",
            "Quelque chose d'éducatif"
        ]
    }
    
    for user_id, messages in users.items():
        print(f"\n👤 User: {user_id}")
        print("-" * 20)
        
        for message in messages:
            response = intelligent_chatbot.process_message(user_id, message)
            print(f"   {message} → {len(response.products)} products")
        
        # Show final context for each user
        context = conversation_memory.get_conversation_context(user_id)
        print(f"   Final context: {context}")
    
    # Show system statistics
    print(f"\n📊 System Statistics:")
    stats = conversation_memory.get_conversation_stats()
    print(f"   Total users: {stats['total_users']}")
    print(f"   Total conversations: {stats['total_conversations']}")
    print(f"   Average length: {stats['avg_conversation_length']:.1f}")
    print(f"   Intent distribution: {stats['intent_distribution']}")


def test_system_performance():
    """Test system performance and statistics"""
    print("\n⚡ Testing System Performance")
    print("=" * 50)
    
    # Get comprehensive stats
    system_stats = intelligent_chatbot.get_system_stats()
    
    print("🧠 Intent Scorer Stats:")
    for intent, stats in system_stats['intent_scorer'].items():
        print(f"   {intent}: {stats['keyword_count']} keywords, threshold {stats['threshold']}")
    
    print(f"\n💾 Memory Stats:")
    memory_stats = system_stats['conversation_memory']
    print(f"   Total users: {memory_stats['total_users']}")
    print(f"   Total conversations: {memory_stats['total_conversations']}")
    print(f"   Memory limit: {memory_stats['memory_limit']}")
    
    print(f"\n🤖 Chatbot Stats:")
    print(f"   Confidence threshold: {system_stats['confidence_threshold']}")
    print(f"   Unknown threshold: {system_stats['unknown_threshold']}")
    print(f"   Response templates: {system_stats['response_templates']}")


def run_comprehensive_test():
    """Run all tests in sequence"""
    print("🚀 Intelligent Chatbot System - Comprehensive Test Suite")
    print("=" * 60)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        test_intent_scoring()
        test_conversation_memory()
        test_learning_system()
        test_multi_user_conversations()
        test_system_performance()
        
        print(f"\n✅ All tests completed successfully!")
        print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_comprehensive_test()