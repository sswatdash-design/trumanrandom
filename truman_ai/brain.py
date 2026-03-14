"""
TRUMAN AI Brain System
LLM interface, prompt assembly, and decision-making

[SF] Clean LLM interaction and prompt management
[AC] Atomic functions for reasoning and response generation
"""

import requests
import json
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from .config import CHARACTER_NAME, CHARACTER_BACKSTORY, PERSONALITY_TRAITS
from .memory import MemorySystem, MemoryType, MemoryImportance
from .mood import MoodEngine
from .world import TimeEngine
from .events import EventEngine, LifeEvent

@dataclass
class ThoughtProcess:
    """Represents a single thought process"""
    query: str
    context: Dict[str, Any]
    memories_recalled: Dict[MemoryType, List]
    reasoning_steps: List[str]
    conclusion: str
    confidence: float
    timestamp: float

class PromptBuilder:
    """Builds prompts for the LLM based on character state"""
    
    def __init__(self, character_name: str, character_backstory: str,
                 personality_traits: Dict[str, float]):
        self.character_name = character_name
        self.character_backstory = character_backstory
        self.personality_traits = personality_traits
        self.base_prompt = self._build_base_prompt()
    
    def _build_base_prompt(self) -> str:
        """Build the base character prompt"""
        traits_description = self._describe_traits()
        
        prompt = f"""You are {self.character_name}.

{self.character_backstory}

Personality Traits:
{traits_description}

You think, feel, and respond as this character would. Your responses should be:
- Authentic to your personality and background
- Emotionally consistent with your current mood
- Based on your memories and experiences
- Reflective of your current drives and needs

Always stay in character. Do not break the fourth wall or refer to being an AI."""
        
        return prompt
    
    def _describe_traits(self) -> str:
        """Describe personality traits in natural language"""
        descriptions = {
            "openness": "Open to new experiences and ideas" if self.personality_traits.get("openness", 0.5) > 0.6 else "Prefers familiarity and routine",
            "conscientiousness": "Organized and disciplined" if self.personality_traits.get("conscientiousness", 0.5) > 0.6 else "Spontaneous and flexible",
            "extraversion": "Outgoing and sociable" if self.personality_traits.get("extraversion", 0.5) > 0.6 else "Reserved and introspective",
            "agreeableness": "Cooperative and compassionate" if self.personality_traits.get("agreeableness", 0.5) > 0.6 else "Competitive and critical",
            "neuroticism": "Emotionally sensitive" if self.personality_traits.get("neuroticism", 0.5) > 0.6 else "Emotionally stable"
        }
        
        return "\n".join([f"- {trait}: {desc}" for trait, desc in descriptions.items()])
    
    def build_context_prompt(self, current_situation: str, mood_state: Dict,
                           drives: Dict, recent_memories: List,
                           current_time: str, location: str) -> str:
        """Build a prompt with current context"""
        mood_description = self._describe_mood(mood_state)
        drives_description = self._describe_drives(drives)
        memories_description = self._describe_memories(recent_memories)
        
        context_prompt = f"""
{self.base_prompt}

Current Situation:
{current_situation}

Time: {current_time}
Location: {location}

Current Mood: {mood_description}

Current Drives:
{drives_description}

Recent Memories:
{memories_description}

Based on this information, respond to the situation as {self.character_name}. Consider:
1. How your personality would interpret this situation
2. How your current mood affects your reaction
3. What your past experiences suggest about this
4. What your current needs and drives motivate you to do

Your response should be natural and in character."""
        
        return context_prompt
    
    def _describe_mood(self, mood_state: Dict) -> str:
        """Describe current mood state"""
        mood_level = mood_state.get("current_mood", 0.5)
        dominant_emotion = mood_state.get("dominant_emotion", ("neutral", 0.0))
        
        if mood_level > 0.7:
            mood_desc = "Very positive and upbeat"
        elif mood_level > 0.6:
            mood_desc = "Generally positive"
        elif mood_level > 0.4:
            mood_desc = "Neutral and balanced"
        elif mood_level > 0.3:
            mood_desc = "Somewhat down"
        else:
            mood_desc = "Feeling low"
        
        emotion_name, emotion_level = dominant_emotion
        if emotion_level > 0.3:
            mood_desc += f", with strong feelings of {emotion_name}"
        
        return mood_desc
    
    def _describe_drives(self, drives: Dict) -> str:
        """Describe current drive states"""
        descriptions = []
        
        for drive_name, drive_state in drives.items():
            level = drive_state.get("level", 0.5)
            if level > 0.7:
                descriptions.append(f"- {drive_name}: Very satisfied")
            elif level > 0.4:
                descriptions.append(f"- {drive_name}: Moderately satisfied")
            else:
                descriptions.append(f"- {drive_name}: Needs attention")
        
        return "\n".join(descriptions) if descriptions else "All drives are balanced"
    
    def _describe_memories(self, memories: List) -> str:
        """Describe relevant memories"""
        if not memories:
            return "No relevant memories come to mind"
        
        memory_descriptions = []
        for memory in memories[:5]:  # Top 5 most relevant
            memory_descriptions.append(f"- {memory.content}")
        
        return "\n".join(memory_descriptions)
    
    def build_decision_prompt(self, options: List[str], situation: str,
                            consequences: Dict[str, List[str]]) -> str:
        """Build a prompt for decision making"""
        options_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(options)])
        
        consequences_text = ""
        for option, consequence_list in consequences.items():
            consequences_text += f"\n{option}:\n"
            for consequence in consequence_list:
                consequences_text += f"  - {consequence}\n"
        
        decision_prompt = f"""
{self.base_prompt}

Decision Situation:
{situation}

Available Options:
{options_text}

Potential Consequences:
{consequences_text}

As {self.character_name}, consider:
1. Which option aligns best with your personality and values
2. How your current mood affects this decision
3. What past experiences suggest about these options
4. How each option affects your current needs and drives

Choose the option that feels most authentic to you and explain your reasoning."""
        
        return decision_prompt
    
    def build_reflection_prompt(self, experience: str, emotional_impact: float,
                              lessons: List[str]) -> str:
        """Build a prompt for self-reflection"""
        impact_desc = "very positive" if emotional_impact > 0.5 else "positive" if emotional_impact > 0 else "negative" if emotional_impact > -0.5 else "very negative"
        
        lessons_text = "\n".join([f"- {lesson}" for lesson in lessons]) if lessons else "No clear lessons yet"
        
        reflection_prompt = f"""
{self.base_prompt}

Reflection on Recent Experience:
{experience}

Emotional Impact: {impact_desc} ({emotional_impact:.2f})

Potential Lessons:
{lessons_text}

Take a moment to reflect on this experience as {self.character_name}:
1. How did this experience affect you emotionally?
2. What does this experience reveal about yourself?
3. How might this experience influence your future decisions?
4. What personal growth, if any, came from this?

Share your honest thoughts and feelings."""
        
        return reflection_prompt

class LLMInterface:
    """Interface for interacting with Ollama LLM"""
    
    def __init__(self):
        from .config import OLLAMA_URL, OLLAMA_MODEL
        self.api_url = OLLAMA_URL
        self.model = OLLAMA_MODEL
        self.conversation_history = []
        self.max_history_length = 50
        
    def generate_response(self, prompt: str, max_tokens: int = 500,
                      temperature: float = 0.7) -> str:
        """Generate a response from Ollama"""
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": prompt})
        
        # Prepare request payload
        payload = {
            "model": self.model,
            "messages": self.conversation_history,
            "stream": False
        }
        
        try:
            # Make request to Ollama
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if "message" in result and "content" in result["message"]:
                    llm_response = result["message"]["content"].strip()
                    
                    # Add response to history
                    self.conversation_history.append({"role": "assistant", "content": llm_response})
                    
                    # Maintain history length
                    if len(self.conversation_history) > self.max_history_length:
                        self.conversation_history = self.conversation_history[-self.max_history_length:]
                    
                    return llm_response
                else:
                    return "I'm not sure how to respond to that."
            else:
                return f"Error: Ollama returned status {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            print(f"DEBUG: RequestException: {str(e)}")
            return f"Error connecting to Ollama: {str(e)}"
        except Exception as e:
            print(f"DEBUG: General Exception: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history.clear()

class Brain:
    """Main brain system coordinating all cognitive functions"""
    
    def __init__(self):
        self.prompt_builder = PromptBuilder(
            CHARACTER_NAME, CHARACTER_BACKSTORY, PERSONALITY_TRAITS
        )
        self.llm_interface = LLMInterface()
        self.thought_history: List[ThoughtProcess] = []
        self.current_focus = None
        self.attention_span = 300  # 5 minutes in seconds
        
    def process_situation(self, situation: str, mood_engine: MoodEngine,
                         memory_system: MemorySystem, time_engine: TimeEngine,
                         location: str) -> str:
        """Process a situation and generate a response"""
        # Get current state
        current_time = time_engine.current_sim_time.strftime("%Y-%m-%d %H:%M")
        mood_state = {
            "current_mood": mood_engine.current_mood,
            "dominant_emotion": mood_engine.get_dominant_emotion()
        }
        drives = {name: {"level": drive.current_level} 
                 for name, drive in mood_engine.drives.items()}
        
        # Recall relevant memories
        recalled = memory_system.recall(situation, limit=5)
        recent_memories = []
        for memory_type, memory_list in recalled.items():
            recent_memories.extend([mem for mem, score in memory_list])
        
        # Build context prompt
        prompt = self.prompt_builder.build_context_prompt(
            situation, mood_state, drives, recent_memories, current_time, location
        )
        
        # Generate response
        response = self.llm_interface.generate_response(prompt)
        
        # Store thought process
        thought = ThoughtProcess(
            query=situation,
            context={
                "mood": mood_state,
                "drives": drives,
                "location": location,
                "time": current_time
            },
            memories_recalled=recalled,
            reasoning_steps=["Analyzed situation", "Recalled memories", "Considered mood"],
            conclusion=response,
            confidence=0.8,  # Would be calculated based on various factors
            timestamp=time.time()
        )
        
        self.thought_history.append(thought)
        
        # Store experience in memory
        memory_system.add_experience(
            f"Responded to: {situation}",
            MemoryImportance.MODERATE,
            mood_engine.current_mood - 0.5,  # Emotional valence relative to neutral
            tags=["response", "situation"],
            context={"response": response}
        )
        
        return response
    
    def make_decision(self, options: List[str], situation: str,
                     consequences: Dict[str, List[str]], mood_engine: MoodEngine,
                     memory_system: MemorySystem) -> Tuple[str, str]:
        """Make a decision between options"""
        # Build decision prompt
        prompt = self.prompt_builder.build_decision_prompt(
            options, situation, consequences
        )
        
        # Generate decision
        decision_response = self.llm_interface.generate_response(prompt)
        
        # Extract choice (simplified - would use more sophisticated parsing)
        chosen_option = options[0]  # Default to first option
        for i, option in enumerate(options):
            if str(i + 1) in decision_response:
                chosen_option = option
                break
        
        # Store decision process
        memory_system.add_experience(
            f"Decision: {chosen_option} in situation: {situation}",
            MemoryImportance.IMPORTANT,
            mood_engine.current_mood - 0.5,
            tags=["decision", "choice"],
            context={"options": options, "chosen": chosen_option}
        )
        
        return chosen_option, decision_response
    
    def reflect_on_experience(self, experience: str, emotional_impact: float,
                             lessons: List[str], mood_engine: MoodEngine,
                             memory_system: MemorySystem) -> str:
        """Reflect on a recent experience"""
        # Build reflection prompt
        prompt = self.prompt_builder.build_reflection_prompt(
            experience, emotional_impact, lessons
        )
        
        # Generate reflection
        reflection = self.llm_interface.generate_response(prompt)
        
        # Store reflection in memory
        memory_system.add_experience(
            f"Reflection on: {experience}",
            MemoryImportance.IMPORTANT,
            emotional_impact,
            tags=["reflection", "growth"],
            context={"reflection": reflection, "lessons": lessons}
        )
        
        return reflection
    
    def process_event(self, event: LifeEvent, mood_engine: MoodEngine,
                     memory_system: MemorySystem) -> str:
        """Process and respond to a life event"""
        # Apply mood impact
        mood_engine.apply_mood_impact(event.mood_impact)
        
        # Build event response prompt
        event_prompt = f"""
{self.prompt_builder.base_prompt}

Life Event: {event.title}
Description: {event.description}

This event has occurred in your life. How do you react to it emotionally and mentally?
Consider how this aligns with or conflicts with your personality, current mood, and past experiences.

Share your authentic reaction as {self.character_name}."""
        
        # Generate reaction
        reaction = self.llm_interface.generate_response(event_prompt)
        
        # Store event experience
        memory_system.add_experience(
            f"Experienced event: {event.title} - {event.description}",
            event.importance,
            event.mood_impact,
            tags=["life_event", event.pool.value],
            context={"reaction": reaction, "event_title": event.title}
        )
        
        return reaction
    
    def update_attention(self, new_focus: str) -> None:
        """Update current mental focus"""
        self.current_focus = new_focus
        # In a more complex implementation, this would affect memory recall and processing priorities
    
    def get_cognitive_state(self) -> Dict[str, Any]:
        """Get current cognitive state summary"""
        return {
            "current_focus": self.current_focus,
            "thought_count": len(self.thought_history),
            "conversation_length": len(self.llm_interface.conversation_history),
            "recent_thoughts": [thought.conclusion for thought in self.thought_history[-5:]]
        }
    
    def clear_cognitive_cache(self) -> None:
        """Clear cognitive caches and reset attention"""
        self.llm_interface.clear_history()
        self.current_focus = None
        # Keep thought_history for learning but could implement forgetting
    
    def simulate_thinking_pattern(self, duration: float) -> List[str]:
        """Simulate background thinking processes"""
        thoughts = []
        
        # Generate thoughts based on recent memories and current state
        if len(self.thought_history) > 0:
            recent_thought = self.thought_history[-1]
            
            # Associative thinking
            if random.random() < 0.3:  # 30% chance of associative thought
                thoughts.append(f"This reminds me of {random.choice(['a similar situation', 'something that happened before'])}")
            
            # Future planning
            if random.random() < 0.2:  # 20% chance of planning thought
                thoughts.append("I should consider the implications of this for the future")
            
            # Emotional processing
            if random.random() < 0.4:  # 40% chance of emotional processing
                thoughts.append("I need to process how I feel about this")
        
        return thoughts
