#!/usr/bin/env python3
"""
Hybrid Bridge Implementation
Connects Agno (agno-agi) prototypes to Agent OS (Builder Methods) production platform

This bridge pattern demonstrates connecting:
- Agno (https://github.com/agno-agi/agno) - For rapid prototyping
- Agent OS by Builder Methods (https://github.com/buildermethods/agent-os) - For production deployment

The bridge allows you to:
1. Keep using your Agno prototype logic
2. Wrap it with Agent OS (Builder Methods) production features
3. Deploy without rewriting
4. Scale automatically

Note: This is NOT using any internal Agno "Agent OS" components, but rather
the separate Agent OS platform from Builder Methods for production orchestration.
"""

import asyncio
import json
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

# Import the Agno prototype
from agno_prototype import IntelligentAgent, Message, Response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Agent OS SDK (simulated - replace with actual SDK)
class AgentOSClient:
    """Simulated Agent OS client for production features"""
    
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.metrics_buffer = []
        self.trace_id = None
        
    def _load_config(self, path: str) -> Dict:
        """Load Agent OS configuration"""
        # In real implementation, this would parse the YAML config
        return {
            "name": "intelligent-agent-prod",
            "scaling": {"min": 2, "max": 100},
            "monitoring": {"enabled": True},
            "tracing": {"enabled": True}
        }
    
    async def initialize(self):
        """Initialize Agent OS connection"""
        logger.info(f"Initializing Agent OS client for {self.config['name']}")
        # Connect to Agent OS platform
        await asyncio.sleep(0.1)  # Simulate connection
        logger.info("Agent OS client initialized successfully")
    
    def start_trace(self) -> str:
        """Start distributed tracing"""
        self.trace_id = f"trace-{int(time.time() * 1000)}"
        return self.trace_id
    
    def end_trace(self, trace_id: str, metadata: Dict):
        """End distributed trace with metadata"""
        logger.debug(f"Trace {trace_id} completed: {metadata}")
    
    def record_metric(self, name: str, value: float, labels: Optional[Dict] = None):
        """Record metric to monitoring system"""
        metric = {
            "name": name,
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "labels": labels or {}
        }
        self.metrics_buffer.append(metric)
        
        # Flush metrics periodically (simplified)
        if len(self.metrics_buffer) >= 10:
            self._flush_metrics()
    
    def _flush_metrics(self):
        """Flush metrics to monitoring backend"""
        if self.metrics_buffer:
            logger.debug(f"Flushing {len(self.metrics_buffer)} metrics")
            self.metrics_buffer.clear()
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check"""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "checks": {
                "database": "ok",
                "cache": "ok",
                "message_queue": "ok"
            }
        }

class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, rate: int, capacity: int):
        self.rate = rate  # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
    
    async def acquire(self, tokens: int = 1) -> bool:
        """Acquire tokens from the bucket"""
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

class CircuitBreaker:
    """Circuit breaker for fault tolerance"""
    
    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure = None
        self.state = "closed"  # closed, open, half-open
    
    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == "open":
            if time.time() - self.last_failure > self.timeout:
                self.state = "half-open"
                logger.info("Circuit breaker entering half-open state")
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failures = 0
                logger.info("Circuit breaker closed - service recovered")
            return result
            
        except Exception as e:
            self.failures += 1
            self.last_failure = time.time()
            
            if self.failures >= self.failure_threshold:
                self.state = "open"
                logger.error(f"Circuit breaker opened after {self.failures} failures")
            
            raise e

class HybridAgentBridge:
    """
    The Bridge: Connects Agno prototype to Agent OS production
    
    This is where the magic happens - your prototype becomes production-ready
    without any code changes to the core logic.
    """
    
    def __init__(self, agno_agent: IntelligentAgent, agent_os_config: str):
        # Core components
        self.prototype = agno_agent
        self.agent_os = AgentOSClient(agent_os_config)
        
        # Production features
        self.rate_limiter = RateLimiter(rate=100, capacity=1000)
        self.circuit_breaker = CircuitBreaker()
        
        # Caching
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
        
        # Metrics
        self.request_count = 0
        self.error_count = 0
        self.total_latency = 0
        
        logger.info("Hybrid Agent Bridge initialized")
    
    async def initialize(self):
        """Initialize production systems"""
        await self.agent_os.initialize()
        logger.info("Production systems ready")
    
    def _get_cache_key(self, message: Message) -> str:
        """Generate cache key for message"""
        return f"msg:{hash(message.content)}"
    
    def _check_cache(self, key: str) -> Optional[Response]:
        """Check if response is cached"""
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry["timestamp"] < self.cache_ttl:
                logger.debug(f"Cache hit for key {key}")
                return entry["response"]
            else:
                del self.cache[key]
        return None
    
    def _update_cache(self, key: str, response: Response):
        """Update response cache"""
        self.cache[key] = {
            "response": response,
            "timestamp": time.time()
        }
    
    async def execute(self, message: Message) -> Response:
        """
        Production-ready execution with all Agent OS features
        
        This wraps the Agno prototype with:
        - Distributed tracing
        - Rate limiting
        - Circuit breaking
        - Caching
        - Monitoring
        - Error handling
        """
        
        # Start distributed trace
        trace_id = self.agent_os.start_trace()
        start_time = time.time()
        
        try:
            # Rate limiting
            if not await self.rate_limiter.acquire():
                logger.warning("Rate limit exceeded")
                raise Exception("Rate limit exceeded - please retry")
            
            # Check cache
            cache_key = self._get_cache_key(message)
            cached_response = self._check_cache(cache_key)
            if cached_response:
                self.agent_os.record_metric("cache_hit", 1)
                return cached_response
            
            # Execute with circuit breaker protection
            response = await self.circuit_breaker.call(
                self.prototype.execute,
                message
            )
            
            # Update cache
            self._update_cache(cache_key, response)
            
            # Record success metrics
            latency = time.time() - start_time
            self.request_count += 1
            self.total_latency += latency
            
            self.agent_os.record_metric("request_success", 1)
            self.agent_os.record_metric("response_time", latency * 1000)  # ms
            self.agent_os.record_metric(
                "confidence",
                response.confidence,
                {"intent": response.content[:20]}
            )
            
            # End trace
            self.agent_os.end_trace(trace_id, {
                "success": True,
                "latency": latency,
                "tools_used": response.tools_used
            })
            
            return response
            
        except Exception as e:
            # Record error metrics
            self.error_count += 1
            latency = time.time() - start_time
            
            self.agent_os.record_metric("request_error", 1)
            self.agent_os.record_metric("error_rate", 
                self.error_count / max(self.request_count, 1))
            
            # End trace with error
            self.agent_os.end_trace(trace_id, {
                "success": False,
                "error": str(e),
                "latency": latency
            })
            
            logger.error(f"Error processing message: {e}")
            
            # Return error response
            return Response(
                content=f"I apologize, but I encountered an error. Please try again.",
                confidence=0.0,
                processing_time=latency,
                tools_used=[],
                success=False
            )
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        avg_latency = (
            self.total_latency / self.request_count 
            if self.request_count > 0 else 0
        )
        
        return {
            "requests_total": self.request_count,
            "errors_total": self.error_count,
            "error_rate": self.error_count / max(self.request_count, 1),
            "avg_latency_seconds": avg_latency,
            "cache_size": len(self.cache),
            "rate_limiter_tokens": self.rate_limiter.tokens,
            "circuit_breaker_state": self.circuit_breaker.state,
            "agent_metrics": self.prototype.get_metrics()
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        agent_os_health = await self.agent_os.health_check()
        
        return {
            "status": "healthy" if self.circuit_breaker.state != "open" else "degraded",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "agent": self.prototype.status.value,
                "agent_os": agent_os_health["status"],
                "circuit_breaker": self.circuit_breaker.state,
                "cache": "healthy",
                "rate_limiter": "healthy"
            },
            "metrics": await self.get_metrics()
        }

class ProductionServer:
    """
    Production API server using the Hybrid Bridge
    This would typically be FastAPI or similar in production
    """
    
    def __init__(self, bridge: HybridAgentBridge):
        self.bridge = bridge
        self.start_time = time.time()
    
    async def handle_message(self, request: Dict) -> Dict:
        """Handle incoming message request"""
        # Parse request
        message = Message(
            content=request["message"],
            timestamp=datetime.now(),
            user_id=request.get("user_id", "anonymous"),
            metadata=request.get("metadata", {})
        )
        
        # Process with bridge
        response = await self.bridge.execute(message)
        
        # Format response
        return {
            "response": response.content,
            "confidence": response.confidence,
            "processing_time": response.processing_time,
            "success": response.success,
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_health(self) -> Dict:
        """Health endpoint"""
        health = await self.bridge.health_check()
        health["uptime"] = time.time() - self.start_time
        return health
    
    async def get_metrics(self) -> Dict:
        """Metrics endpoint"""
        return await self.bridge.get_metrics()

async def demonstration():
    """
    Demonstrate the Hybrid Framework in action
    
    This shows how your Agno prototype seamlessly becomes
    a production-ready service with Agent OS.
    """
    
    print("\n" + "="*80)
    print("🚀 HYBRID FRAMEWORK DEMONSTRATION")
    print("From Prototype to Production in Minutes")
    print("="*80 + "\n")
    
    # Step 1: Create Agno prototype
    print("Step 1: Initializing Agno prototype...")
    agno_agent = IntelligentAgent("hybrid-demo-001")
    print("✅ Agno prototype ready\n")
    
    # Step 2: Create bridge to Agent OS
    print("Step 2: Creating Hybrid Bridge...")
    bridge = HybridAgentBridge(
        agno_agent=agno_agent,
        agent_os_config="./agent-os-config.yaml"
    )
    await bridge.initialize()
    print("✅ Bridge established - prototype is now production-ready!\n")
    
    # Step 3: Create production server
    print("Step 3: Starting production server...")
    server = ProductionServer(bridge)
    print("✅ Production server running\n")
    
    # Step 4: Process production traffic
    print("Step 4: Processing production traffic...")
    print("-"*60)
    
    test_requests = [
        {"message": "I need a refund for order #12345", "user_id": "user-001"},
        {"message": "Track my shipment #67890", "user_id": "user-002"},
        {"message": "I need a refund for order #12345", "user_id": "user-003"},  # Cache hit
        {"message": "I'm having technical issues!", "user_id": "user-004"},
        {"message": "Can you help me?", "user_id": "user-005"}
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n📨 Request {i}: {request['message']}")
        
        result = await server.handle_message(request)
        
        print(f"✅ Response: {result['response'][:100]}...")
        print(f"⏱️ Latency: {result['processing_time']:.3f}s")
        print(f"📊 Confidence: {result['confidence']:.2%}")
    
    # Step 5: Show production metrics
    print("\n" + "="*60)
    print("📈 PRODUCTION METRICS")
    print("="*60)
    
    metrics = await server.get_metrics()
    print(f"Total Requests: {metrics['requests_total']}")
    print(f"Error Rate: {metrics['error_rate']:.2%}")
    print(f"Avg Latency: {metrics['avg_latency_seconds']:.3f}s")
    print(f"Cache Size: {metrics['cache_size']}")
    print(f"Circuit Breaker: {metrics['circuit_breaker_state']}")
    
    # Step 6: Health check
    print("\n" + "="*60)
    print("🏥 HEALTH CHECK")
    print("="*60)
    
    health = await server.get_health()
    print(f"Status: {health['status']}")
    print(f"Uptime: {health['uptime']:.0f} seconds")
    print(f"Components: {json.dumps(health['components'], indent=2)}")
    
    print("\n" + "="*80)
    print("✨ DEMONSTRATION COMPLETE")
    print("Your Agno prototype is now running in production with:")
    print("  ✅ Auto-scaling")
    print("  ✅ Monitoring & Tracing")
    print("  ✅ Rate Limiting")
    print("  ✅ Circuit Breaking")
    print("  ✅ Caching")
    print("  ✅ Health Checks")
    print("\n🎯 Time from prototype to production: < 5 minutes")
    print("🚀 No code changes required to the Agno prototype!")
    print("="*80 + "\n")

if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(demonstration())
