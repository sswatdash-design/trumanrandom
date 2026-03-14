"""
TRUMAN AI Mood System
Biological drives, personality traits, and emotional state management

[SF] Clean mood calculation and personality modeling
[AC] Atomic functions for drive satisfaction and trait expression
"""

import math
import random
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from .config import PERSONALITY_TRAITS, CORE_DRIVES, BASE_STATS

@dataclass
class DriveState:
    """Represents the current state of a biological drive"""
    current_level: float  # 0.0 to 1.0
    satisfaction_rate: float  # How quickly this drive is satisfied
    decay_rate: float  # How quickly this drive decays over time
    last_satisfied: float  # Timestamp of last satisfaction
    
class PersonalityProfile:
    """Manages personality traits and their expressions"""
    
    def __init__(self, traits: Dict[str, float] = None):
        self.traits = traits or PERSONALITY_TRAITS.copy()
        self.trait_expressions = {}  # Current expression levels
        self.trait_history = []  # Historical trait expressions
        
    def update_trait_expression(self, mood: float, context: Dict) -> None:
        """Update how traits are currently expressed based on mood and context"""
        for trait, base_value in self.traits.items():
            # Base expression modified by mood
            mood_modifier = 1.0 + (mood - 0.5) * 0.3  # Mood affects expression intensity
            
            # Context modifiers
            context_modifier = 1.0
            if trait == "extraversion" and context.get("social_situation", False):
                context_modifier *= 1.2
            elif trait == "neuroticism" and context.get("stress_level", 0) > 0.5:
                context_modifier *= 1.3
            elif trait == "conscientiousness" and context.get("work_situation", False):
                context_modifier *= 1.2
            elif trait == "openness" and context.get("novelty", False):
                context_modifier *= 1.2
            elif trait == "agreeableness" and context.get("conflict", False):
                context_modifier *= 1.3
            
            # Calculate current expression
            expression = base_value * mood_modifier * context_modifier
            self.trait_expressions[trait] = max(0.0, min(1.0, expression))
        
        # Store in history
        self.trait_history.append(self.trait_expressions.copy())
        if len(self.trait_history) > 100:  # Keep last 100 entries
            self.trait_history.pop(0)
    
    def get_dominant_traits(self, top_n: int = 3) -> List[Tuple[str, float]]:
        """Get the most strongly expressed traits"""
        sorted_traits = sorted(self.trait_expressions.items(), key=lambda x: x[1], reverse=True)
        return sorted_traits[:top_n]

class MoodEngine:
    """Manages mood calculation and emotional state"""
    
    def __init__(self):
        self.personality = PersonalityProfile()
        self.drives = self._initialize_drives()
        self.current_mood = 0.5  # Neutral starting mood
        self.mood_history = []
        self.emotional_state = {
            "happiness": 0.5,
            "sadness": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "surprise": 0.0,
            "disgust": 0.0
        }
        
    def _initialize_drives(self) -> Dict[str, DriveState]:
        """Initialize all biological drives"""
        drives = {}
        for drive_name, drive_config in CORE_DRIVES.items():
            drives[drive_name] = DriveState(
                current_level=0.5,  # Start at neutral
                satisfaction_rate=drive_config.get("satisfaction_rate", 0.1),
                decay_rate=drive_config.get("decay_rate", 0.05),
                last_satisfied=0.0
            )
        return drives
    
    def update_drives(self, time_delta: float, activities: List[str]) -> None:
        """Update drive levels based on time and activities"""
        # Natural decay over time
        for drive_name, drive in self.drives.items():
            drive.current_level -= drive.decay_rate * time_delta
            drive.current_level = max(0.0, min(1.0, drive.current_level))
        
        # Activity-based satisfaction
        activity_effects = {
            "eating": {"hunger": 0.8, "thirst": 0.3},
            "drinking": {"thirst": 0.9, "hunger": 0.1},
            "sleeping": {"energy": 0.7, "comfort": 0.4},
            "socializing": {"affiliation": 0.6, "dominance": 0.2},
            "working": {"achievement": 0.5, "dominance": 0.3},
            "exercising": {"energy": -0.3, "health": 0.4},  # Energy cost, health gain
            "relaxing": {"comfort": 0.5, "energy": 0.2},
            "learning": {"achievement": 0.4, "curiosity": 0.6},
            "intimacy": {"sex": 0.8, "affiliation": 0.4},
            "competing": {"dominance": 0.6, "achievement": 0.3},
            "creating": {"achievement": 0.5, "curiosity": 0.4}
        }
        
        for activity in activities:
            if activity in activity_effects:
                for drive_name, effect in activity_effects[activity].items():
                    if drive_name in self.drives:
                        drive = self.drives[drive_name]
                        # Apply satisfaction
                        if effect > 0:
                            drive.current_level += effect * drive.satisfaction_rate
                            drive.last_satisfied = time.time()
                        else:
                            drive.current_level += effect  # Negative effects apply directly
                        drive.current_level = max(0.0, min(1.0, drive.current_level))
    
    def calculate_drive_satisfaction(self) -> float:
        """Calculate overall drive satisfaction as a mood component"""
        if not self.drives:
            return 0.5
        
        total_satisfaction = 0.0
        total_weight = 0.0
        
        for drive_name, drive in self.drives.items():
            # Higher current level = more satisfied
            satisfaction = drive.current_level
            
            # Weight by drive importance (can be customized)
            weight = 1.0
            if drive_name in ["hunger", "thirst", "energy"]:
                weight = 2.0  # Basic needs are more important
            elif drive_name in ["affiliation", "achievement"]:
                weight = 1.5  # Psychological needs are moderately important
            
            total_satisfaction += satisfaction * weight
            total_weight += weight
        
        return total_satisfaction / total_weight if total_weight > 0 else 0.5
    
    def calculate_trait_contribution(self) -> float:
        """Calculate personality trait contribution to mood"""
        trait_mood_contributions = {
            "extraversion": 0.1,      # Extraverts tend to have higher baseline mood
            "neuroticism": -0.2,      # Neuroticism reduces mood stability
            "conscientiousness": 0.05, # Conscientiousness provides stability
            "agreeableness": 0.1,      # Agreeableness promotes positive interactions
            "openness": 0.05          # Openness provides novelty and growth
        }
        
        contribution = 0.0
        for trait, weight in trait_mood_contributions.items():
            trait_value = self.personality.traits.get(trait, 0.5)
            contribution += trait_value * weight
        
        return contribution
    
    def calculate_emotional_state(self, events: List[Dict]) -> None:
        """Update emotional state based on recent events"""
        # Decay existing emotions
        for emotion in self.emotional_state:
            self.emotional_state[emotion] *= 0.9  # Emotional decay
        
        # Process events
        for event in events[-10:]:  # Consider last 10 events
            event_mood = event.get("mood_impact", 0.0)
            event_type = event.get("type", "neutral")
            
            if event_mood > 0.2:
                self.emotional_state["happiness"] += abs(event_mood) * 0.3
            elif event_mood < -0.2:
                if event_type == "loss":
                    self.emotional_state["sadness"] += abs(event_mood) * 0.4
                elif event_type == "conflict":
                    self.emotional_state["anger"] += abs(event_mood) * 0.3
                elif event_type == "threat":
                    self.emotional_state["fear"] += abs(event_mood) * 0.4
                elif event_type == "disgusting":
                    self.emotional_state["disgust"] += abs(event_mood) * 0.3
            
            if event.get("surprising", False):
                self.emotional_state["surprise"] += 0.3
        
        # Normalize emotions
        for emotion in self.emotional_state:
            self.emotional_state[emotion] = min(1.0, self.emotional_state[emotion])
    
    def calculate_overall_mood(self, events: List[Dict], context: Dict) -> float:
        """Calculate overall mood from all components"""
        # Drive satisfaction component
        drive_mood = self.calculate_drive_satisfaction()
        
        # Personality trait component
        trait_mood = self.calculate_trait_contribution()
        
        # Recent events component
        event_mood = 0.0
        for event in events[-20:]:  # Consider last 20 events
            event_mood += event.get("mood_impact", 0.0) * (1.0 / (1.0 + len(events) - events.index(event)))
        
        # Emotional state component
        emotion_mood = (
            self.emotional_state["happiness"] * 0.4 +
            self.emotional_state["sadness"] * -0.3 +
            self.emotional_state["anger"] * -0.2 +
            self.emotional_state["fear"] * -0.3 +
            self.emotional_state["surprise"] * 0.1 +
            self.emotional_state["disgust"] * -0.1
        )
        
        # Context modifiers
        context_modifier = 1.0
        if context.get("social_situation", False):
            context_modifier += self.personality.traits.get("extraversion", 0.5) * 0.2
        if context.get("work_situation", False):
            context_modifier += self.personality.traits.get("conscientiousness", 0.5) * 0.2
        if context.get("stress_level", 0) > 0.5:
            context_modifier -= self.personality.traits.get("neuroticism", 0.5) * 0.3
        
        # Combine all components
        combined_mood = (
            drive_mood * 0.4 +      # Drive satisfaction is most important
            trait_mood * 0.2 +      # Personality provides baseline
            event_mood * 0.3 +      # Recent events have strong impact
            emotion_mood * 0.1      # Current emotional state
        )
        
        # Apply context modifier
        final_mood = combined_mood * context_modifier
        
        # Add some randomness for natural variation
        final_mood += random.uniform(-0.05, 0.05)
        
        # Ensure valid range
        final_mood = max(0.0, min(1.0, final_mood))
        
        return final_mood
    
    def update_mood(self, events: List[Dict], context: Dict, activities: List[str], time_delta: float) -> float:
        """Main mood update function"""
        # Update drives
        self.update_drives(time_delta, activities)
        
        # Calculate emotional state
        self.calculate_emotional_state(events)
        
        # Update personality expressions
        self.current_mood = self.calculate_overall_mood(events, context)
        self.personality.update_trait_expression(self.current_mood, context)
        
        # Store in history
        self.mood_history.append({
            "mood": self.current_mood,
            "drives": {name: drive.current_level for name, drive in self.drives.items()},
            "emotions": self.emotional_state.copy(),
            "traits": self.personality.trait_expressions.copy()
        })
        
        # Keep history manageable
        if len(self.mood_history) > 1000:
            self.mood_history.pop(0)
        
        return self.current_mood
    
    def get_mood_description(self) -> str:
        """Get a textual description of current mood"""
        if self.current_mood > 0.8:
            return "Ecstatic"
        elif self.current_mood > 0.7:
            return "Very Happy"
        elif self.current_mood > 0.6:
            return "Happy"
        elif self.current_mood > 0.5:
            return "Content"
        elif self.current_mood > 0.4:
            return "Neutral"
        elif self.current_mood > 0.3:
            return "Slightly Down"
        elif self.current_mood > 0.2:
            return "Sad"
        elif self.current_mood > 0.1:
            return "Very Sad"
        else:
            return "Depressed"
    
    def get_dominant_emotion(self) -> Tuple[str, float]:
        """Get the most prominent current emotion"""
        return max(self.emotional_state.items(), key=lambda x: x[1])
    
    def get_drive_status(self) -> Dict[str, str]:
        """Get human-readable drive status"""
        status = {}
        for drive_name, drive in self.drives.items():
            level = drive.current_level
            if level > 0.8:
                status[drive_name] = "Very Satisfied"
            elif level > 0.6:
                status[drive_name] = "Satisfied"
            elif level > 0.4:
                status[drive_name] = "Neutral"
            elif level > 0.2:
                status[drive_name] = "Unsatisfied"
            else:
                status[drive_name] = "Very Unsatisfied"
        return status
    
    def apply_mood_impact(self, impact: float) -> None:
        """Apply an external mood impact (from events, etc.)"""
        self.current_mood += impact
        self.current_mood = max(0.0, min(1.0, self.current_mood))
    
    def get_mood_trend(self, window_size: int = 10) -> str:
        """Calculate mood trend over recent history"""
        if len(self.mood_history) < window_size:
            return "Insufficient data"
        
        recent_moods = [entry["mood"] for entry in self.mood_history[-window_size:]]
        if len(recent_moods) < 2:
            return "Stable"
        
        # Simple trend calculation
        first_half = sum(recent_moods[:window_size//2]) / (window_size//2)
        second_half = sum(recent_moods[window_size//2:]) / (window_size//2)
        
        difference = second_half - first_half
        
        if difference > 0.1:
            return "Improving"
        elif difference < -0.1:
            return "Declining"
        else:
            return "Stable"
