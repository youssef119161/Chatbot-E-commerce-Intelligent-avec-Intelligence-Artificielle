"""
Conversation Memory System
Manages user conversation history and context for personalized responses
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import deque


@dataclass
class ConversationTurn:
    """Represents a single conversation turn"""
    user_id: str
    message: str
    intent: str
    confidence: float
    context_data: Dict[str, Any]
    response: str
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationTurn':
        """Create from dictionary"""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


class ConversationMemory:
    """
    Manages conversation history and user context
    Supports both in-memory and persistent SQLite storage
    """
    
    def __init__(self, db_path: Optional[str] = None, memory_limit: int = 5):
        self.memory_limit = memory_limit
        self.db_path = db_path
        
        # In-memory storage (fast access)
        self.user_conversations: Dict[str, deque] = {}
        self.user_preferences: Dict[str, Dict[str, Any]] = {}
        
        # Initialize database if path provided
        if db_path:
            self.init_database()
            self.load_recent_conversations()
    
    def init_database(self):
        """Initialize SQLite database tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    message TEXT NOT NULL,
                    intent TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    context_data TEXT NOT NULL,
                    response TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    user_id TEXT PRIMARY KEY,
                    preferences TEXT NOT NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS unknown_queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message TEXT NOT NULL,
                    frequency INTEGER DEFAULT 1,
                    first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(message)
                )
            """)
            
            # Create indexes for better performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp)")
            conn.commit()
    
    def load_recent_conversations(self, days: int = 7):
        """Load recent conversations from database into memory"""
        if not self.db_path:
            return
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT user_id, message, intent, confidence, context_data, response, timestamp
                FROM conversations 
                WHERE timestamp > ?
                ORDER BY user_id, timestamp
            """, (cutoff_date,))
            
            for row in cursor:
                user_id = row['user_id']
                turn = ConversationTurn(
                    user_id=user_id,
                    message=row['message'],
                    intent=row['intent'],
                    confidence=row['confidence'],
                    context_data=json.loads(row['context_data']),
                    response=row['response'],
                    timestamp=datetime.fromisoformat(row['timestamp'])
                )
                
                if user_id not in self.user_conversations:
                    self.user_conversations[user_id] = deque(maxlen=self.memory_limit)
                
                self.user_conversations[user_id].append(turn)
    
    def add_conversation_turn(self, turn: ConversationTurn):
        """Add a conversation turn to memory and optionally to database"""
        user_id = turn.user_id
        
        # Add to in-memory storage
        if user_id not in self.user_conversations:
            self.user_conversations[user_id] = deque(maxlen=self.memory_limit)
        
        self.user_conversations[user_id].append(turn)
        
        # Persist to database if available
        if self.db_path:
            self.save_conversation_turn(turn)
        
        # Update user preferences based on context
        self.update_user_preferences(user_id, turn.context_data)
    
    def save_conversation_turn(self, turn: ConversationTurn):
        """Save conversation turn to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO conversations 
                (user_id, message, intent, confidence, context_data, response, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                turn.user_id,
                turn.message,
                turn.intent,
                turn.confidence,
                json.dumps(turn.context_data),
                turn.response,
                turn.timestamp.isoformat()
            ))
            conn.commit()
    
    def get_conversation_history(self, user_id: str, limit: Optional[int] = None) -> List[ConversationTurn]:
        """Get conversation history for a user"""
        if user_id not in self.user_conversations:
            return []
        
        history = list(self.user_conversations[user_id])
        
        if limit:
            return history[-limit:]
        
        return history
    
    def get_conversation_context(self, user_id: str) -> Dict[str, Any]:
        """Get aggregated context from recent conversations"""
        history = self.get_conversation_history(user_id)
        
        if not history:
            return {}
        
        # Aggregate context from recent turns
        context = {}
        
        # Get most recent values for each context key
        for turn in reversed(history):
            for key, value in turn.context_data.items():
                if key not in context and value is not None:
                    context[key] = value
        
        # Add conversation state information
        context['conversation_length'] = len(history)
        context['last_intent'] = history[-1].intent if history else None
        context['avg_confidence'] = sum(turn.confidence for turn in history) / len(history) if history else 0.0
        
        return context
    
    def update_user_preferences(self, user_id: str, context_data: Dict[str, Any]):
        """Update user preferences based on conversation context"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        
        preferences = self.user_preferences[user_id]
        
        # Update preferences with new context data
        for key, value in context_data.items():
            if value is not None:
                if key in preferences:
                    # Keep track of frequency for repeated preferences
                    if isinstance(preferences[key], dict) and 'value' in preferences[key]:
                        if preferences[key]['value'] == value:
                            preferences[key]['frequency'] = preferences[key].get('frequency', 1) + 1
                        else:
                            # New value, reset frequency
                            preferences[key] = {'value': value, 'frequency': 1}
                    else:
                        # Convert to frequency tracking
                        preferences[key] = {'value': value, 'frequency': 1}
                else:
                    preferences[key] = {'value': value, 'frequency': 1}
        
        # Save to database if available
        if self.db_path:
            self.save_user_preferences(user_id)
    
    def save_user_preferences(self, user_id: str):
        """Save user preferences to database"""
        if user_id not in self.user_preferences:
            return
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO user_preferences (user_id, preferences, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (user_id, json.dumps(self.user_preferences[user_id])))
            conn.commit()
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences"""
        return self.user_preferences.get(user_id, {})
    
    def log_unknown_query(self, message: str):
        """Log an unknown query for analysis"""
        if not self.db_path:
            return
        
        with sqlite3.connect(self.db_path) as conn:
            # Try to increment frequency if exists, otherwise insert new
            conn.execute("""
                INSERT INTO unknown_queries (message, frequency, first_seen, last_seen)
                VALUES (?, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ON CONFLICT(message) DO UPDATE SET
                    frequency = frequency + 1,
                    last_seen = CURRENT_TIMESTAMP
            """, (message,))
            conn.commit()
    
    def get_unknown_queries(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get most frequent unknown queries for analysis"""
        if not self.db_path:
            return []
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT message, frequency, first_seen, last_seen
                FROM unknown_queries
                ORDER BY frequency DESC, last_seen DESC
                LIMIT ?
            """, (limit,))
            
            return [dict(row) for row in cursor]
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get conversation statistics"""
        total_users = len(self.user_conversations)
        total_conversations = sum(len(conv) for conv in self.user_conversations.values())
        
        # Calculate average conversation length
        avg_length = total_conversations / total_users if total_users > 0 else 0
        
        # Get intent distribution
        intent_counts = {}
        for conversations in self.user_conversations.values():
            for turn in conversations:
                intent_counts[turn.intent] = intent_counts.get(turn.intent, 0) + 1
        
        return {
            "total_users": total_users,
            "total_conversations": total_conversations,
            "avg_conversation_length": avg_length,
            "intent_distribution": intent_counts,
            "memory_limit": self.memory_limit
        }
    
    def clear_user_data(self, user_id: str):
        """Clear all data for a specific user (GDPR compliance)"""
        # Clear from memory
        if user_id in self.user_conversations:
            del self.user_conversations[user_id]
        
        if user_id in self.user_preferences:
            del self.user_preferences[user_id]
        
        # Clear from database
        if self.db_path:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
                conn.execute("DELETE FROM user_preferences WHERE user_id = ?", (user_id,))
                conn.commit()


# Global instance (can be configured with database path)
conversation_memory = ConversationMemory(
    db_path="chatbot_memory.db",  # Enable persistence in current directory
    memory_limit=5
)