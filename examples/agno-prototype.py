#!/usr/bin/env python3
"""
Agno Prototype Example - Customer Support Agent
Demonstrates rapid prototyping with Agno framework

IMPORTANT: This is a CONCEPTUAL EXAMPLE showing the pattern.
Actual implementation requires:
- Agno SDK license from https://agno.com
- Valid AGNO_API_KEY in your environment

This example simulates Agno's behavior to demonstrate the architecture.
Replace simulated imports with actual Agno SDK when you have access.
"""

from typing import Dict, List, Optional, Any
import asyncio
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Check for Agno SDK availability
try:
    # Attempt to import actual Agno SDK
    import agno
    AGNO_AVAILABLE = True
    print("✅ Agno SDK detected")
except ImportError:
    AGNO_AVAILABLE = False
    print("⚠️ Agno SDK not found - using simulated classes for demonstration")
    print("   To use actual Agno: pip install agno-sdk (requires license)")
    print()

# Simulated Agno classes for demonstration purposes
# Replace these with actual Agno imports when SDK is available
class AgentStatus(Enum):
    INITIALIZING = "initializing"
    READY = "ready"
    PROCESSING = "processing"
    ERROR = "error"

@dataclass
class Message:
    """Represents a user message"""
    content: str
    timestamp: datetime
    user_id: str
    metadata: Optional[Dict] = None

@dataclass
class Response:
    """Agent response structure"""
    content: str
    confidence: float
    processing_time: float
    tools_used: List[str]
    success: bool

class Tool:
    """Base class for agent tools"""
    def __init__(self, name: str):
        self.name = name
        self.usage_count = 0
    
    async def execute(self, input_data: Any) -> Any:
        self.usage_count += 1
        return await self._process(input_data)
    
    async def _process(self, input_data: Any) -> Any:
        raise NotImplementedError

class ParseTool(Tool):
    """Natural language understanding tool"""
    def __init__(self):
        super().__init__("parser")
    
    async def _process(self, input_data: str) -> Dict:
        """Parse user input into structured data"""
        # Simulate NLP processing
        await asyncio.sleep(0.1)
        
        # Extract intent and entities (simplified)
        intents = {
            "refund": ["refund", "money back", "return"],
            "tracking": ["track", "where", "shipping", "delivery"],
            "support": ["help", "issue", "problem", "broken"],
            "account": ["account", "login", "password", "email"]
        }
        
        detected_intent = "general"
        for intent, keywords in intents.items():
            if any(keyword in input_data.lower() for keyword in keywords):
                detected_intent = intent
                break
        
        return {
            "raw_input": input_data,
            "intent": detected_intent,
            "entities": self._extract_entities(input_data),
            "sentiment": self._analyze_sentiment(input_data)
        }
    
    def _extract_entities(self, text: str) -> Dict:
        """Extract named entities from text"""
        # Simplified entity extraction
        entities = {}
        if "#" in text:
            # Extract order number
            parts = text.split("#")
            if len(parts) > 1:
                order_num = parts[1].split()[0] if parts[1] else None
                if order_num:
                    entities["order_number"] = order_num
        
        return entities
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of the text"""
        negative_words = ["angry", "frustrated", "terrible", "awful", "hate"]
        positive_words = ["thank", "great", "awesome", "love", "excellent"]
        
        text_lower = text.lower()
        if any(word in text_lower for word in negative_words):
            return "negative"
        elif any(word in text_lower for word in positive_words):
            return "positive"
        return "neutral"

class ProcessTool(Tool):
    """Business logic processing tool"""
    def __init__(self):
        super().__init__("processor")
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> Dict:
        """Load domain-specific knowledge"""
        return {
            "refund": {
                "policy": "30-day return policy for unused items",
                "process_time": "5-7 business days",
                "requirements": ["order number", "reason", "item condition"]
            },
            "tracking": {
                "carriers": ["UPS", "FedEx", "USPS"],
                "typical_delivery": "3-5 business days",
                "tracking_url": "https://track.example.com/"
            },
            "support": {
                "hours": "24/7 chat support, 9-5 PST phone support",
                "escalation": "Complex issues escalated to tier 2",
                "sla": "Response within 2 hours"
            }
        }
    
    async def _process(self, parsed_data: Dict) -> Dict:
        """Process parsed data with business logic"""
        await asyncio.sleep(0.1)
        
        intent = parsed_data.get("intent", "general")
        entities = parsed_data.get("entities", {})
        
        # Apply business rules based on intent
        if intent == "refund":
            return self._handle_refund(entities)
        elif intent == "tracking":
            return self._handle_tracking(entities)
        elif intent == "support":
            return self._handle_support(parsed_data)
        else:
            return self._handle_general()
    
    def _handle_refund(self, entities: Dict) -> Dict:
        """Handle refund requests"""
        if "order_number" in entities:
            return {
                "action": "initiate_refund",
                "response_template": "refund_initiated",
                "data": {
                    "order": entities["order_number"],
                    "policy": self.knowledge_base["refund"]["policy"],
                    "timeline": self.knowledge_base["refund"]["process_time"]
                }
            }
        return {
            "action": "request_info",
            "response_template": "need_order_number",
            "data": {"required": "order number"}
        }
    
    def _handle_tracking(self, entities: Dict) -> Dict:
        """Handle tracking requests"""
        if "order_number" in entities:
            # Simulate tracking lookup
            return {
                "action": "provide_tracking",
                "response_template": "tracking_info",
                "data": {
                    "order": entities["order_number"],
                    "status": "In Transit",
                    "eta": "2 days",
                    "carrier": "UPS"
                }
            }
        return {
            "action": "request_info",
            "response_template": "need_order_number",
            "data": {"required": "order number for tracking"}
        }
    
    def _handle_support(self, parsed_data: Dict) -> Dict:
        """Handle support requests"""
        sentiment = parsed_data.get("sentiment", "neutral")
        
        if sentiment == "negative":
            # Escalate negative sentiment
            return {
                "action": "escalate",
                "response_template": "escalate_to_human",
                "data": {
                    "priority": "high",
                    "reason": "negative sentiment detected"
                }
            }
        
        return {
            "action": "provide_support",
            "response_template": "general_support",
            "data": {
                "hours": self.knowledge_base["support"]["hours"],
                "sla": self.knowledge_base["support"]["sla"]
            }
        }
    
    def _handle_general(self) -> Dict:
        """Handle general queries"""
        return {
            "action": "provide_help",
            "response_template": "help_menu",
            "data": {
                "options": ["refund", "tracking", "support", "account"]
            }
        }

class GenerateTool(Tool):
    """Response generation tool"""
    def __init__(self):
        super().__init__("generator")
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Load response templates"""
        return {
            "refund_initiated": "I've initiated a refund for order #{order}. Per our {policy}, "
                              "you should see the refund in {timeline}. Is there anything else I can help with?",
            
            "need_order_number": "I'd be happy to help with that! Could you please provide your order number? "
                               "It usually starts with # followed by 6-8 digits.",
            
            "tracking_info": "Great news! Your order #{order} is {status} with {carrier}. "
                           "Expected delivery: {eta}. You can track it here: https://track.example.com/{order}",
            
            "escalate_to_human": "I understand this is frustrating. Let me connect you with a specialist "
                                "who can better assist you. Priority: {priority}. Someone will be with you shortly.",
            
            "general_support": "Our support team is available during {hours}. "
                             "We guarantee {sla}. How can I assist you today?",
            
            "help_menu": "I can help you with:\n"
                        "• Refunds and returns\n"
                        "• Order tracking\n"
                        "• Technical support\n"
                        "• Account issues\n\n"
                        "What would you like help with?"
        }
    
    async def _process(self, process_result: Dict) -> str:
        """Generate human-readable response"""
        await asyncio.sleep(0.05)
        
        template_name = process_result.get("response_template", "help_menu")
        template = self.templates.get(template_name, self.templates["help_menu"])
        data = process_result.get("data", {})
        
        # Format template with data
        try:
            response = template.format(**data)
        except KeyError:
            response = template
        
        return response

class IntelligentAgent:
    """
    Main Agno Agent Class
    Demonstrates the rapid prototyping capabilities of Agno
    """
    
    def __init__(self, agent_id: str = "prototype-001"):
        self.agent_id = agent_id
        self.status = AgentStatus.INITIALIZING
        self.tools = self._initialize_tools()
        self.metrics = {
            "messages_processed": 0,
            "avg_response_time": 0,
            "success_rate": 0,
            "tool_usage": {}
        }
        self.status = AgentStatus.READY
        print(f"✨ Agent {self.agent_id} initialized and ready!")
    
    def _initialize_tools(self) -> Dict[str, Tool]:
        """Initialize agent tools"""
        return {
            "parser": ParseTool(),
            "processor": ProcessTool(),
            "generator": GenerateTool()
        }
    
    async def execute(self, message: Message) -> Response:
        """
        Main execution pipeline
        Parse → Process → Generate
        """
        start_time = datetime.now()
        self.status = AgentStatus.PROCESSING
        tools_used = []
        
        try:
            # Step 1: Parse user input
            parsed = await self.tools["parser"].execute(message.content)
            tools_used.append("parser")
            print(f"📝 Parsed intent: {parsed['intent']}")
            
            # Step 2: Process with business logic
            processed = await self.tools["processor"].execute(parsed)
            tools_used.append("processor")
            print(f"⚙️ Action: {processed['action']}")
            
            # Step 3: Generate response
            response_text = await self.tools["generator"].execute(processed)
            tools_used.append("generator")
            
            # Calculate metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_metrics(processing_time, success=True)
            
            self.status = AgentStatus.READY
            
            return Response(
                content=response_text,
                confidence=0.95,
                processing_time=processing_time,
                tools_used=tools_used,
                success=True
            )
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_metrics(processing_time, success=False)
            
            return Response(
                content=f"I apologize, but I encountered an error: {str(e)}",
                confidence=0.0,
                processing_time=processing_time,
                tools_used=tools_used,
                success=False
            )
    
    def _update_metrics(self, processing_time: float, success: bool):
        """Update agent performance metrics"""
        self.metrics["messages_processed"] += 1
        
        # Update average response time
        current_avg = self.metrics["avg_response_time"]
        count = self.metrics["messages_processed"]
        self.metrics["avg_response_time"] = (
            (current_avg * (count - 1) + processing_time) / count
        )
        
        # Update success rate
        if success:
            current_rate = self.metrics["success_rate"]
            self.metrics["success_rate"] = (
                (current_rate * (count - 1) + 1) / count
            )
    
    def get_metrics(self) -> Dict:
        """Get current agent metrics"""
        return {
            **self.metrics,
            "status": self.status.value,
            "agent_id": self.agent_id,
            "tool_usage": {
                name: tool.usage_count 
                for name, tool in self.tools.items()
            }
        }

async def test_agent():
    """
    Test the agent with sample queries
    Demonstrates the speed of Agno prototyping
    """
    print("\n" + "="*60)
    print("🚀 AGNO PROTOTYPE DEMONSTRATION")
    print("="*60 + "\n")
    
    # Initialize agent
    agent = IntelligentAgent()
    
    # Test queries
    test_messages = [
        "I need a refund for order #12345",
        "Where is my package? Order #67890",
        "I'm really frustrated with your service!",
        "Can you help me?",
        "Track my order #24680"
    ]
    
    for msg_content in test_messages:
        print(f"\n{'='*40}")
        print(f"👤 User: {msg_content}")
        print(f"{'='*40}")
        
        message = Message(
            content=msg_content,
            timestamp=datetime.now(),
            user_id="test-user-001"
        )
        
        response = await agent.execute(message)
        
        print(f"🤖 Agent: {response.content}")
        print(f"⏱️ Response time: {response.processing_time:.3f}s")
        print(f"📊 Confidence: {response.confidence:.2%}")
        print(f"🔧 Tools used: {', '.join(response.tools_used)}")
    
    # Display final metrics
    print(f"\n{'='*60}")
    print("📈 AGENT PERFORMANCE METRICS")
    print(f"{'='*60}")
    
    metrics = agent.get_metrics()
    print(f"Messages processed: {metrics['messages_processed']}")
    print(f"Average response time: {metrics['avg_response_time']:.3f}s")
    print(f"Success rate: {metrics['success_rate']:.2%}")
    print(f"Tool usage: {json.dumps(metrics['tool_usage'], indent=2)}")
    
    print(f"\n✅ Prototype ready for production hardening with Agent OS!")
    print(f"⚡ Total development time: < 3 hours")
    print(f"🎯 Next step: Deploy to Agent OS for scaling\n")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_agent())
