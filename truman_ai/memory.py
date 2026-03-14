"""
TRUMAN AI Memory System
Three-layer memory system: working, episodic, and semantic memory

[SF] Clean memory management and retrieval
[AC] Atomic functions for memory storage and recall
"""

import time
import math
import random
from enum import Enum
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from .config import CHARACTER_NAME

class MemoryType(Enum):
    """Types of memories"""
    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"

class MemoryImportance(Enum):
    """Importance levels for memories"""
    TRIVIAL = 0.1
    MINOR = 0.3
    MODERATE = 0.5
    IMPORTANT = 0.7
    CRITICAL = 0.9

@dataclass
class Memory:
    """Represents a single memory"""
    id: str
    content: str
    memory_type: MemoryType
    importance: MemoryImportance
    timestamp: float
    emotional_valence: float  # -1.0 to 1.0
    tags: List[str] = field(default_factory=list)
    associations: List[str] = field(default_factory=list)  # Associated memory IDs
    retrieval_count: int = 0
    last_accessed: float = field(default_factory=time.time)
    decay_rate: float = 0.01  # How quickly memory fades
    context: Dict[str, Any] = field(default_factory=dict)

class WorkingMemory:
    """Short-term memory for immediate processing"""
    
    def __init__(self, capacity: int = 7):
        self.capacity = capacity  # Miller's magic number
        self.memories: List[Memory] = []
        self.decay_time = 30.0  # Seconds before decay starts
        
    def add_memory(self, content: str, importance: MemoryImportance = MemoryImportance.MODERATE,
                  emotional_valence: float = 0.0, tags: List[str] = None,
                  context: Dict[str, Any] = None) -> Memory:
        """Add a new memory to working memory"""
        memory = Memory(
            id=f"wm_{int(time.time() * 1000)}_{random.randint(1000, 9999)}",
            content=content,
            memory_type=MemoryType.WORKING,
            importance=importance,
            timestamp=time.time(),
            emotional_valence=emotional_valence,
            tags=tags or [],
            context=context or {}
        )
        
        # Add to working memory
        self.memories.append(memory)
        
        # Maintain capacity - remove least important/oldest
        if len(self.memories) > self.capacity:
            self._evict_weakest()
        
        return memory
    
    def _evict_weakest(self) -> None:
        """Remove the weakest memory from working memory"""
        if not self.memories:
            return
        
        # Calculate weakness score (lower = weaker)
        def weakness_score(memory):
            age = time.time() - memory.timestamp
            importance_factor = 1.0 - memory.importance.value
            return age * importance_factor
        
        weakest = min(self.memories, key=weakness_score)
        self.memories.remove(weakest)
    
    def get_active_memories(self) -> List[Memory]:
        """Get currently active memories (not decayed)"""
        current_time = time.time()
        active = []
        
        for memory in self.memories:
            age = current_time - memory.timestamp
            if age < self.decay_time:
                active.append(memory)
            else:
                # Decay effect - memory becomes less accessible
                decay_factor = math.exp(-(age - self.decay_time) * memory.decay_rate)
                if random.random() < decay_factor:
                    active.append(memory)
        
        return active
    
    def clear(self) -> None:
        """Clear working memory"""
        self.memories.clear()

class EpisodicMemory:
    """Long-term memory for personal experiences"""
    
    def __init__(self, max_memories: int = 10000):
        self.memories: Dict[str, Memory] = {}
        self.max_memories = max_memories
        self.consolidation_threshold = 0.5  # Importance needed for consolidation
        
    def add_memory(self, content: str, importance: MemoryImportance,
                  emotional_valence: float, tags: List[str] = None,
                  context: Dict[str, Any] = None) -> Optional[Memory]:
        """Add a new episodic memory"""
        if importance.value < self.consolidation_threshold:
            return None  # Not important enough to store
        
        memory = Memory(
            id=f"ep_{int(time.time() * 1000)}_{random.randint(1000, 9999)}",
            content=content,
            memory_type=MemoryType.EPISODIC,
            importance=importance,
            timestamp=time.time(),
            emotional_valence=emotional_valence,
            tags=tags or [],
            context=context or {}
        )
        
        self.memories[memory.id] = memory
        
        # Maintain memory limit
        if len(self.memories) > self.max_memories:
            self._evict_forgotten()
        
        return memory
    
    def _evict_forgotten(self) -> None:
        """Remove memories that have been forgotten"""
        if len(self.memories) <= self.max_memories:
            return
        
        # Calculate forgetting score
        def forgetting_score(memory):
            age = time.time() - memory.timestamp
            retrieval_factor = 1.0 / (1.0 + memory.retrieval_count)
            importance_factor = 1.0 - memory.importance.value
            return age * retrieval_factor * importance_factor
        
        # Sort by forgetting score and remove the most forgotten
        sorted_memories = sorted(self.memories.values(), key=forgetting_score, reverse=True)
        
        # Remove excess memories
        excess = len(self.memories) - self.max_memories
        for memory in sorted_memories[:excess]:
            del self.memories[memory.id]
    
    def recall_memories(self, query: str, limit: int = 10) -> List[Tuple[Memory, float]]:
        """Recall memories based on a query"""
        query_terms = query.lower().split()
        scored_memories = []
        
        for memory in self.memories.values():
            score = self._calculate_relevance(memory, query_terms)
            if score > 0.1:  # Minimum relevance threshold
                scored_memories.append((memory, score))
        
        # Sort by relevance and limit results
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        result = scored_memories[:limit]
        
        # Update retrieval statistics
        for memory, _ in result:
            memory.retrieval_count += 1
            memory.last_accessed = time.time()
        
        return result
    
    def _calculate_relevance(self, memory: Memory, query_terms: List[str]) -> float:
        """Calculate relevance score for a memory"""
        content_lower = memory.content.lower()
        tags_lower = [tag.lower() for tag in memory.tags]
        
        # Text matching
        text_score = 0.0
        for term in query_terms:
            if term in content_lower:
                text_score += 1.0
            for tag in tags_lower:
                if term in tag:
                    text_score += 0.5
        
        # Normalize text score
        text_score = text_score / len(query_terms) if query_terms else 0.0
        
        # Recency factor (more recent memories are more accessible)
        age = time.time() - memory.timestamp
        recency_factor = math.exp(-age / (7 * 24 * 3600))  # 7-day half-life
        
        # Importance factor
        importance_factor = memory.importance.value
        
        # Emotional valence factor (stronger emotions are more memorable)
        emotion_factor = abs(memory.emotional_valence)
        
        # Retrieval frequency factor
        retrieval_factor = min(1.0, memory.retrieval_count / 10.0)
        
        # Combine all factors
        relevance = (
            text_score * 0.4 +
            recency_factor * 0.2 +
            importance_factor * 0.2 +
            emotion_factor * 0.1 +
            retrieval_factor * 0.1
        )
        
        return relevance
    
    def get_memories_by_timeframe(self, start_time: float, end_time: float) -> List[Memory]:
        """Get memories within a specific timeframe"""
        result = []
        for memory in self.memories.values():
            if start_time <= memory.timestamp <= end_time:
                result.append(memory)
        return sorted(result, key=lambda m: m.timestamp, reverse=True)
    
    def get_memories_by_emotion(self, emotion_range: Tuple[float, float]) -> List[Memory]:
        """Get memories within an emotional valence range"""
        min_valence, max_valence = emotion_range
        result = []
        for memory in self.memories.values():
            if min_valence <= memory.emotional_valence <= max_valence:
                result.append(memory)
        return sorted(result, key=lambda m: m.importance.value, reverse=True)

class SemanticMemory:
    """Long-term memory for facts, concepts, and general knowledge"""
    
    def __init__(self):
        self.facts: Dict[str, Memory] = {}
        self.concepts: Dict[str, List[str]] = {}  # concept -> related facts
        self.relationships: Dict[str, List[str]] = {}  # fact_id -> related fact_ids
        
    def add_fact(self, content: str, concept: str, confidence: float = 1.0,
                 source: str = "experience") -> Memory:
        """Add a semantic fact"""
        fact_id = f"sm_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
        
        memory = Memory(
            id=fact_id,
            content=content,
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.MODERATE,
            timestamp=time.time(),
            emotional_valence=0.0,  # Facts are neutral
            tags=[concept, source],
            context={"confidence": confidence}
        )
        
        self.facts[fact_id] = memory
        
        # Update concept mapping
        if concept not in self.concepts:
            self.concepts[concept] = []
        self.concepts[concept].append(fact_id)
        
        return memory
    
    def add_relationship(self, fact1_id: str, fact2_id: str, relationship_type: str = "related") -> None:
        """Add a relationship between two facts"""
        if fact1_id in self.facts and fact2_id in self.facts:
            if fact1_id not in self.relationships:
                self.relationships[fact1_id] = []
            if fact2_id not in self.relationships:
                self.relationships[fact2_id] = []
            
            self.relationships[fact1_id].append(fact2_id)
            self.relationships[fact2_id].append(fact1_id)
    
    def query_facts(self, query: str, concept: str = None, limit: int = 10) -> List[Tuple[Memory, float]]:
        """Query semantic facts"""
        query_terms = query.lower().split()
        scored_facts = []
        
        facts_to_search = []
        if concept and concept in self.concepts:
            facts_to_search = [self.facts[fact_id] for fact_id in self.concepts[concept] 
                             if fact_id in self.facts]
        else:
            facts_to_search = list(self.facts.values())
        
        for fact in facts_to_search:
            score = self._calculate_fact_relevance(fact, query_terms)
            if score > 0.1:
                scored_facts.append((fact, score))
        
        scored_facts.sort(key=lambda x: x[1], reverse=True)
        return scored_facts[:limit]
    
    def _calculate_fact_relevance(self, fact: Memory, query_terms: List[str]) -> float:
        """Calculate relevance score for a semantic fact"""
        content_lower = fact.content.lower()
        
        # Text matching
        matches = sum(1 for term in query_terms if term in content_lower)
        text_score = matches / len(query_terms) if query_terms else 0.0
        
        # Confidence factor
        confidence = fact.context.get("confidence", 1.0)
        
        # Usage frequency (how often this fact is retrieved)
        usage_factor = min(1.0, fact.retrieval_count / 20.0)
        
        return text_score * confidence * (1.0 + usage_factor * 0.2)
    
    def get_concept_facts(self, concept: str) -> List[Memory]:
        """Get all facts related to a concept"""
        if concept not in self.concepts:
            return []
        
        return [self.facts[fact_id] for fact_id in self.concepts[concept] 
                if fact_id in self.facts]
    
    def update_confidence(self, fact_id: str, new_confidence: float) -> None:
        """Update confidence in a fact"""
        if fact_id in self.facts:
            self.facts[fact_id].context["confidence"] = new_confidence

class MemorySystem:
    """Main memory system coordinating all three layers"""
    
    def __init__(self):
        self.working_memory = WorkingMemory()
        self.episodic_memory = EpisodicMemory()
        self.semantic_memory = SemanticMemory()
        self.consolidation_interval = 60.0  # Seconds between consolidation checks
        self.last_consolidation = time.time()
        
    def add_experience(self, content: str, importance: MemoryImportance,
                      emotional_valence: float, tags: List[str] = None,
                      context: Dict[str, Any] = None) -> Memory:
        """Add a new experience to the memory system"""
        # Add to working memory immediately
        working_memory = self.working_memory.add_memory(
            content, importance, emotional_valence, tags, context
        )
        
        # Add to episodic memory if important enough
        episodic_memory = self.episodic_memory.add_memory(
            content, importance, emotional_valence, tags, context
        )
        
        return working_memory
    
    def add_fact(self, content: str, concept: str, confidence: float = 1.0,
                 source: str = "experience") -> Memory:
        """Add a semantic fact"""
        return self.semantic_memory.add_fact(content, concept, confidence, source)
    
    def recall(self, query: str, memory_types: List[MemoryType] = None,
                limit: int = 10) -> Dict[MemoryType, List[Tuple[Memory, float]]]:
        """Recall memories from specified layers"""
        if memory_types is None:
            memory_types = [MemoryType.WORKING, MemoryType.EPISODIC, MemoryType.SEMANTIC]
        
        results = {}
        
        if MemoryType.WORKING in memory_types:
            active_memories = self.working_memory.get_active_memories()
            working_results = [(mem, 1.0) for mem in active_memories 
                              if query.lower() in mem.content.lower()]
            results[MemoryType.WORKING] = working_results[:limit]
        
        if MemoryType.EPISODIC in memory_types:
            results[MemoryType.EPISODIC] = self.episodic_memory.recall_memories(query, limit)
        
        if MemoryType.SEMANTIC in memory_types:
            results[MemoryType.SEMANTIC] = self.semantic_memory.query_facts(query, limit=limit)
        
        return results
    
    def consolidate_memories(self) -> None:
        """Consolidate working memory to long-term memory"""
        current_time = time.time()
        
        if current_time - self.last_consolidation < self.consolidation_interval:
            return
        
        self.last_consolidation = current_time
        
        # Check working memories for consolidation
        for memory in self.working_memory.memories[:]:
            age = current_time - memory.timestamp
            
            # Consolidation criteria
            should_consolidate = (
                memory.importance.value >= 0.5 or  # Important enough
                abs(memory.emotional_valence) >= 0.7 or  # Strong emotion
                memory.retrieval_count >= 3 or  # Frequently accessed
                age >= 300  # 5 minutes old
            )
            
            if should_consolidate:
                # Add to episodic memory
                self.episodic_memory.add_memory(
                    memory.content,
                    memory.importance,
                    memory.emotional_valence,
                    memory.tags,
                    memory.context
                )
                
                # Remove from working memory
                self.working_memory.memories.remove(memory)
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get summary statistics of the memory system"""
        return {
            "working_memory_count": len(self.working_memory.memories),
            "episodic_memory_count": len(self.episodic_memory.memories),
            "semantic_memory_count": len(self.semantic_memory.facts),
            "concepts_count": len(self.semantic_memory.concepts),
            "relationships_count": len(self.semantic_memory.relationships)
        }
    
    def forget_old_memories(self, cutoff_days: int = 365) -> int:
        """Forget memories older than cutoff (returns count forgotten)"""
        cutoff_time = time.time() - (cutoff_days * 24 * 3600)
        forgotten = 0
        
        # Forget episodic memories
        to_forget = []
        for memory_id, memory in self.episodic_memory.memories.items():
            if memory.timestamp < cutoff_time and memory.importance.value < 0.7:
                to_forget.append(memory_id)
        
        for memory_id in to_forget:
            del self.episodic_memory.memories[memory_id]
            forgotten += 1
        
        return forgotten
    
    def create_associations(self) -> None:
        """Create associations between related memories"""
        # Get recent episodic memories
        recent_memories = list(self.episodic_memory.memories.values())[-50:]
        
        # Simple association based on shared tags and content similarity
        for i, mem1 in enumerate(recent_memories):
            for mem2 in recent_memories[i+1:]:
                # Check for shared tags
                shared_tags = set(mem1.tags) & set(mem2.tags)
                
                # Check content similarity (simple word overlap)
                words1 = set(mem1.content.lower().split())
                words2 = set(mem2.content.lower().split())
                similarity = len(words1 & words2) / len(words1 | words2) if words1 | words2 else 0
                
                # Create association if related
                if shared_tags or similarity > 0.3:
                    if mem2.id not in mem1.associations:
                        mem1.associations.append(mem2.id)
                    if mem1.id not in mem2.associations:
                        mem2.associations.append(mem1.id)
    
    def get_emotional_timeline(self, days: int = 30) -> List[Tuple[float, float]]:
        """Get emotional valence timeline for recent memories"""
        cutoff_time = time.time() - (days * 24 * 3600)
        timeline = []
        
        for memory in self.episodic_memory.memories.values():
            if memory.timestamp >= cutoff_time:
                timeline.append((memory.timestamp, memory.emotional_valence))
        
        timeline.sort(key=lambda x: x[0])
        return timeline
