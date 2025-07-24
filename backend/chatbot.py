from typing import Dict, List, Optional
import re
from datetime import datetime
import json

class NorshelChatbot:
    def __init__(self):
        self.responses = {
            # Program Information
            "programs": {
                "keywords": ["program", "service", "what do you offer", "activities", "vocational", "recreational"],
                "response": "🏢 We offer several programs:\n\n• **Vocational Day Program** - Work skills and job training\n• **Recreational Program** - Social activities and community outings\n• **Work Experience Program** - Real workplace experience\n• **Individualized Programming** - Literacy, music therapy, and life skills\n\nWould you like details about any specific program?"
            },
            
            # Hours and Schedule
            "hours": {
                "keywords": ["hours", "time", "open", "close", "schedule", "when"],
                "response": "🕐 **Our Hours:**\n\n• **Monday - Thursday:** 8:00am - 3:30pm\n• **Friday:** 8:00am - 3:00pm\n• **Weekends:** Closed\n\nWe're here to support your loved ones during these hours with engaging programs and activities!"
            },
            
            # Contact Information
            "contact": {
                "keywords": ["contact", "phone", "call", "number", "reach", "location", "address"],
                "response": "📞 **Contact Us:**\n\n**Kernaghan Location:**\n• 📍 73-630 Kernaghan Avenue, Winnipeg, MB R2C 5G1\n• ☎️ (204) 654-6117\n\n**Scurfield Location:**\n• 📍 20-5 Scurfield Blvd, Winnipeg, MB R3Y 1G3\n• ☎️ (204) 452-9955\n\nFeel free to call us anytime during business hours!"
            },
            
            # Lunch and Meals
            "lunch": {
                "keywords": ["lunch", "food", "meal", "eat", "menu", "nutrition"],
                "response": "🍽️ **Lunch Information:**\n\nWe provide nutritious daily meals! Our weekly menu includes:\n• Rice & Beans\n• Pasta dishes\n• Chicken wraps\n• Fresh sandwiches\n• Pizza\n\nParents can view today's specific menu on their dashboard after logging in."
            },
            
            # Parent Login and Dashboard
            "parent": {
                "keywords": ["parent", "login", "dashboard", "portal", "account", "sign in"],
                "response": "👨‍👩‍👧‍👦 **Parent Portal:**\n\nOur secure parent portal lets you:\n• View your loved one's daily activities\n• Check today's lunch menu\n• See program schedules\n• Stay connected with their progress\n\n🔐 Login at the top right of our website to access your personalized dashboard!"
            },
            
            # Eligibility and Enrollment
            "eligibility": {
                "keywords": ["eligible", "qualify", "enroll", "join", "apply", "admission", "who can"],
                "response": "✅ **Who We Support:**\n\nWe support adults with:\n• Down Syndrome\n• Autism Spectrum Disorders\n• Cerebral Palsy\n• PDD (Pervasive Developmental Disorders)\n• Intellectual disabilities\n• And many other conditions\n\n📋 For enrollment information, please call us at (204) 654-6117 or (204) 452-9955."
            },
            
            # Activities and Daily Life
            "activities": {
                "keywords": ["activities", "daily", "what do they do", "day", "morning", "afternoon"],
                "response": "🎯 **Daily Activities:**\n\nOur clients enjoy varied daily programs:\n• **Morning Activities:** Art classes, music sessions, life skills training\n• **Afternoon Activities:** Community outings, recreational activities, work experience\n\nEach person has an individualized schedule based on their interests and goals. Parents can see specific daily activities on their dashboard!"
            },
            
            # Staff and Support
            "staff": {
                "keywords": ["staff", "worker", "support", "care", "team", "who works"],
                "response": "👥 **Our Team:**\n\nOur dedicated staff includes:\n• Qualified support workers\n• Program coordinators\n• Administrative team\n• Specialized therapists\n\nAll staff are trained in first aid, CPR, and NVCI (Non-Violent Crisis Intervention). We're committed to providing the best care for your loved ones!"
            },
            
            # Transportation
            "transportation": {
                "keywords": ["transport", "bus", "ride", "pickup", "drop off", "how to get"],
                "response": "🚌 **Transportation:**\n\nFor transportation information and arrangements, please contact our offices:\n• Kernaghan: (204) 654-6117\n• Scurfield: (204) 452-9955\n\nOur staff can discuss available transportation options and help coordinate pickup/drop-off arrangements."
            }
        }
        
        self.conversation_starters = [
            "Hi! I'm here to help you learn about Norshel programs and services. What would you like to know?",
            "Hello! I can help you with information about our programs, schedules, contact details, and more. How can I assist you?",
            "Welcome to Norshel! I'm here to answer questions about our day programs for adults with disabilities. What can I help you with?"
        ]
        
        self.fallback_responses = [
            "I'd be happy to help! You can ask me about our programs, hours, contact information, or parent portal access.",
            "I'm here to assist with information about Norshel services. Try asking about our programs, schedules, or how to contact us.",
            "For specific questions I can't answer, please call us at (204) 654-6117 (Kernaghan) or (204) 452-9955 (Scurfield)."
        ]
    
    def get_response(self, message: str, user_context: Optional[Dict] = None) -> str:
        """Get chatbot response based on user message and context"""
        message_lower = message.lower().strip()
        
        # Handle greetings
        if any(greeting in message_lower for greeting in ["hi", "hello", "hey", "good morning", "good afternoon"]):
            return "👋 Hello! Welcome to Norshel Inc. I'm here to help you with information about our programs and services. What would you like to know?"
        
        # Handle thanks
        if any(thanks in message_lower for thanks in ["thank", "thanks", "appreciate"]):
            return "You're very welcome! 😊 Is there anything else I can help you with about Norshel programs or services?"
        
        # Handle goodbye
        if any(bye in message_lower for bye in ["bye", "goodbye", "see you", "have a good"]):
            return "Goodbye! 👋 Feel free to reach out anytime if you have questions. Have a wonderful day!"
        
        # Search for matching responses
        for category, data in self.responses.items():
            for keyword in data["keywords"]:
                if keyword in message_lower:
                    response = data["response"]
                    
                    # Add context-specific information
                    if user_context:
                        response = self._add_context(response, user_context, category)
                    
                    return response
        
        # Handle specific questions with regex patterns
        if re.search(r"what.*time|when.*open|hours", message_lower):
            return self.responses["hours"]["response"]
        
        if re.search(r"how.*contact|phone.*number|call", message_lower):
            return self.responses["contact"]["response"]
        
        if re.search(r"who.*help|what.*condition|eligible", message_lower):
            return self.responses["eligibility"]["response"]
        
        # Fallback response
        return "I'm here to help! You can ask me about:\n\n🏢 Our programs and services\n🕐 Hours and schedules\n📞 Contact information\n👨‍👩‍👧‍👦 Parent portal access\n🍽️ Meals and activities\n✅ Eligibility and enrollment\n\nWhat would you like to know more about?"
    
    def _add_context(self, response: str, user_context: Dict, category: str) -> str:
        """Add context-specific information to responses"""
        page = user_context.get("page", "")
        is_logged_in = user_context.get("logged_in", False)
        
        # Add page-specific context
        if category == "lunch" and page == "dashboard" and is_logged_in:
            response += "\n\n💡 Since you're on your dashboard, you can see today's specific menu displayed below your client's information!"
        
        if category == "activities" and page == "dashboard" and is_logged_in:
            response += "\n\n📱 Your dashboard shows your loved one's specific activities for today - check the cards below!"
        
        if category == "parent" and is_logged_in:
            response = "🎉 You're already logged in! Your personalized dashboard shows your loved one's daily activities, today's lunch menu, and program information."
        
        return response
    
    def get_conversation_starter(self) -> str:
        """Get a random conversation starter"""
        import random
        return random.choice(self.conversation_starters)

class ChatSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: List[Dict] = []
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
    
    def add_message(self, message: str, is_user: bool = True):
        """Add a message to the conversation history"""
        self.messages.append({
            "message": message,
            "is_user": is_user,
            "timestamp": datetime.now().isoformat()
        })
        self.last_activity = datetime.now()
    
    def get_recent_messages(self, count: int = 5) -> List[Dict]:
        """Get recent messages for context"""
        return self.messages[-count:] if self.messages else [] 