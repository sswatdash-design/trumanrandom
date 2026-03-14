"""
TRUMAN AI Main Simulation
Master simulation loop and coordination of all systems

[SF] Clean simulation management and system coordination
[AC] Atomic functions for simulation steps and state updates
"""

import time
import random
import signal
import sys
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass

from .config import (
    CHARACTER_NAME, CHARACTER_BACKSTORY, SIMULATION_CONFIG,
    WEATHER_STATES, LOCATIONS, DAILY_SCHEDULES
)
from .world import TimeEngine, Location
from .events import EventEngine, LifeEvent
from .mood import MoodEngine
from .memory import MemorySystem, MemoryImportance
from .brain import Brain
from .display import Colors, DisplayManager

@dataclass
class SimulationState:
    """Overall simulation state"""
    running: bool = True
    paused: bool = False
    simulation_speed: float = 1.0
    current_location: str = "home"
    current_weather: str = "sunny"
    current_activities: List[str] = None
    recent_events: List[Dict] = None
    event_history: List[Dict] = None
    
    def __post_init__(self):
        if self.current_activities is None:
            self.current_activities = []
        if self.recent_events is None:
            self.recent_events = []
        if self.event_history is None:
            self.event_history = []

class TrumanAISimulation:
    """Main simulation class coordinating all systems"""
    
    def __init__(self):
        # Initialize all core systems
        self.state = SimulationState()
        self.time_engine = TimeEngine(SIMULATION_CONFIG["time_scale"])
        self.event_engine = EventEngine()
        self.mood_engine = MoodEngine()
        self.memory_system = MemorySystem()
        self.brain = Brain()
        self.display_manager = DisplayManager(CHARACTER_NAME)
        
        # Simulation timing
        self.last_update = time.time()
        self.update_interval = 1.0 / SIMULATION_CONFIG["target_fps"]
        self.simulation_start_time = time.time()
        self.last_event_check = time.time()
        self.event_check_interval = 30.0  # Check for events every 30 seconds
        
        # Character state
        self.character_state = {
            "has_job": True,
            "in_relationship": False,
            "is_student": False,
            "has_debt": False,
            "has_investments": False
        }
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Initialize simulation
        self._initialize_simulation()
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n{Colors.YELLOW}Shutting down Truman AI simulation...{Colors.RESET}")
        self.state.running = False
    
    def _initialize_simulation(self) -> None:
        """Initialize the simulation with starting conditions"""
        # Set initial location and weather
        self.state.current_location = "home"
        self.state.current_weather = random.choice(WEATHER_STATES)
        
        # Add initial memories
        self._add_initial_memories()
        
        # Set initial activities
        self.state.current_activities = ["waking_up", "preparing_for_day"]
        
        # Display startup message
        self.display_manager.display.render_info_message(
            f"Truman AI simulation started for {CHARACTER_NAME}"
        )
    
    def _add_initial_memories(self) -> None:
        """Add initial memories to establish character background"""
        initial_memories = [
            ("I am Marcus Thompson, a 28-year-old software developer", MemoryImportance.CRITICAL, "identity"),
            ("I value achievement and competence in my work", MemoryImportance.IMPORTANT, "values"),
            ("I live alone in a small apartment in the city", MemoryImportance.MODERATE, "living_situation"),
            ("I enjoy solving complex problems and learning new things", MemoryImportance.MODERATE, "interests"),
            ("Sometimes I feel lonely despite my independence", MemoryImportance.MODERATE, "emotions")
        ]
        
        for content, importance, tag in initial_memories:
            self.memory_system.add_experience(
                content, importance, 0.0, [tag], {"initial": True}
            )
    
    def update_simulation(self, delta_time: float) -> None:
        """Main simulation update loop"""
        if self.state.paused:
            return
        
        # Update time
        current_sim_time = self.time_engine.advance_time(delta_time * self.state.simulation_speed)
        
        # Update mood based on current activities and time
        self.mood_engine.update_mood(
            self.state.recent_events,
            self._get_current_context(),
            self.state.current_activities,
            delta_time * self.state.simulation_speed
        )
        
        # Consolidate memories periodically
        self.memory_system.consolidate_memories()
        
        # Check for and process events
        self._check_and_process_events()
        
        # Update character state based on current situation
        self._update_character_state()
        
        # Generate background thoughts
        self._generate_background_thoughts()
        
        # Update display
        self.display_manager.update_display(
            current_sim_time,
            self.state.current_location,
            self.state.current_weather,
            self.mood_engine,
            self.memory_system,
            self.brain,
            self.state.recent_events,
            self.state.current_activities,
            self.state.simulation_speed
        )
    
    def _get_current_context(self) -> Dict[str, Any]:
        """Get current context for mood and brain processing"""
        return {
            "social_situation": self._is_social_situation(),
            "work_situation": self._is_work_situation(),
            "stress_level": self._calculate_stress_level(),
            "location": self.state.current_location,
            "weather": self.state.current_weather,
            "time_of_day": self.time_engine.current_sim_time.hour
        }
    
    def _is_social_situation(self) -> bool:
        """Check if current situation is social"""
        social_activities = ["socializing", "meeting_friends", "family_gathering", "party"]
        return any(activity in self.state.current_activities for activity in social_activities)
    
    def _is_work_situation(self) -> bool:
        """Check if current situation is work-related"""
        work_activities = ["working", "meeting", "programming", "studying"]
        return any(activity in self.state.current_activities for activity in work_activities)
    
    def _calculate_stress_level(self) -> float:
        """Calculate current stress level"""
        stress = 0.0
        
        # Mood-based stress
        if self.mood_engine.current_mood < 0.3:
            stress += 0.5
        
        # Drive-based stress
        for drive_name, drive in self.mood_engine.drives.items():
            if drive.current_level < 0.3:
                stress += 0.1
        
        # Event-based stress
        for event in self.state.recent_events[-5:]:
            if event.get("mood_impact", 0) < -0.2:
                stress += 0.2
        
        return min(1.0, stress)
    
    def _check_and_process_events(self) -> None:
        """Check for and process life events"""
        current_time = time.time()
        
        if current_time - self.last_event_check < self.event_check_interval:
            return
        
        self.last_event_check = current_time
        
        # Select an event
        event = self.event_engine.select_event(self.character_state)
        
        if event:
            # Process the event
            reaction = self.brain.process_event(event, self.mood_engine, self.memory_system)
            
            # Add to event history
            event_data = {
                "title": event.title,
                "description": event.description,
                "pool": event.pool.value,
                "mood_impact": event.mood_impact,
                "timestamp": current_time,
                "reaction": reaction
            }
            
            self.state.recent_events.append(event_data)
            self.state.event_history.append(event_data)
            
            # Keep recent events manageable
            if len(self.state.recent_events) > 10:
                self.state.recent_events.pop(0)
            
            # Display event notification
            self.display_manager.display.render_event_notification(
                event.title, event.description, event.mood_impact
            )
            
            # Update character state based on event
            self._update_character_state_from_event(event)
    
    def _update_character_state_from_event(self, event: LifeEvent) -> None:
        """Update character state based on event effects"""
        # Update traits based on event impacts
        for trait, impact in event.trait_impacts.items():
            if trait in self.mood_engine.personality.traits:
                # Traits change slowly - small incremental changes
                current_value = self.mood_engine.personality.traits[trait]
                new_value = max(0.0, min(1.0, current_value + impact * 0.01))
                self.mood_engine.personality.traits[trait] = new_value
        
        # Update drives based on event impacts
        for drive, impact in event.drive_impacts.items():
            if drive in self.mood_engine.drives:
                current_level = self.mood_engine.drives[drive].current_level
                new_level = max(0.0, min(1.0, current_level + impact * 0.1))
                self.mood_engine.drives[drive].current_level = new_level
    
    def _update_character_state(self) -> None:
        """Update character state based on current situation"""
        current_hour = self.time_engine.current_sim_time.hour
        
        # Update activities based on time of day
        self._update_activities_by_time(current_hour)
        
        # Update location based on activities
        self._update_location_by_activities()
        
        # Update weather occasionally
        if random.random() < 0.01:  # 1% chance per update
            self.state.current_weather = random.choice(WEATHER_STATES)
    
    def _update_activities_by_time(self, hour: int) -> None:
        """Update activities based on time of day"""
        # Get appropriate schedule
        schedule = DAILY_SCHEDULES.get("weekday", DAILY_SCHEDULES["weekend"])
        
        # Find current activity based on time
        current_activity = "resting"
        for time_range, activity in schedule.items():
            start_hour, end_hour = map(int, time_range.split("-"))
            if start_hour <= hour < end_hour:
                current_activity = activity
                break
        
        # Update if activity changed
        if not self.state.current_activities or current_activity != self.state.current_activities[-1]:
            self.state.current_activities.append(current_activity)
            
            # Keep activity list manageable
            if len(self.state.current_activities) > 20:
                self.state.current_activities.pop(0)
            
            # Process the activity
            self._process_activity(current_activity)
    
    def _process_activity(self, activity: str) -> None:
        """Process a new activity"""
        # Add to memory
        self.memory_system.add_experience(
            f"Engaged in activity: {activity}",
            MemoryImportance.MINOR,
            self.mood_engine.current_mood - 0.5,
            ["activity"],
            {"activity_type": activity}
        )
        
        # Generate thought about activity
        if random.random() < 0.3:  # 30% chance of conscious thought
            situation = f"I'm currently {activity.replace('_', ' ')}"
            response = self.brain.process_situation(
                situation, self.mood_engine, self.memory_system,
                self.time_engine, self.state.current_location
            )
            
            # Store the thought
            self.memory_system.add_experience(
                f"Thought about {activity}: {response[:100]}",
                MemoryImportance.MINOR,
                self.mood_engine.current_mood - 0.5,
                ["thought", "activity"],
                {"activity": activity, "thought": response}
            )
    
    def _update_location_by_activities(self) -> None:
        """Update location based on current activities"""
        activity_location_map = {
            "working": "office",
            "sleeping": "home",
            "eating": "home",
            "socializing": "cafe",
            "exercising": "gym",
            "shopping": "store",
            "relaxing": "home"
        }
        
        for activity in self.state.current_activities[-3:]:  # Check recent activities
            if activity in activity_location_map:
                new_location = activity_location_map[activity]
                if new_location != self.state.current_location:
                    self.state.current_location = new_location
                    self.memory_system.add_experience(
                        f"Moved to {new_location}",
                        MemoryImportance.MINOR,
                        0.0,
                        ["location", "movement"],
                        {"from": self.state.current_location, "to": new_location}
                    )
                break
    
    def _generate_background_thoughts(self) -> None:
        """Generate background thinking processes"""
        if random.random() < 0.05:  # 5% chance per update
            thoughts = self.brain.simulate_thinking_pattern(1.0)
            
            for thought in thoughts:
                self.memory_system.add_experience(
                    f"Background thought: {thought}",
                    MemoryImportance.TRIVIAL,
                    self.mood_engine.current_mood - 0.5,
                    ["thought", "background"],
                    {"spontaneous": True}
                )
    
    def run_simulation(self) -> None:
        """Main simulation loop"""
        self._initialize_simulation()
        
        # Test Ollama connection immediately
        print("Testing Ollama connection...")
        test_response = self.brain.llm_interface.generate_response("Hello Marcus, how are you feeling today?")
        print(f"Ollama response: {test_response}")
        
        self.display_manager.display.render_info_message(
            f"Truman AI simulation started for {CHARACTER_NAME}"
        )
        self.display_manager.display.render_info_message(
            "Press Ctrl+C to stop simulation"
        )
        
        try:
            while self.state.running:
                # Calculate delta time
                current_time = time.time()
                delta_time = current_time - self.last_update
                self.last_update = current_time
                
                # Update simulation
                self.update_simulation(delta_time)
                
                # Control frame rate
                elapsed = time.time() - current_time
                if elapsed < self.update_interval:
                    time.sleep(self.update_interval - elapsed)
                
        except KeyboardInterrupt:
            pass
        finally:
            self._shutdown_simulation()
    
    def _shutdown_simulation(self) -> None:
        """Clean shutdown of simulation"""
        self.display_manager.display.render_info_message("Simulation ended")
        
        # Save final statistics
        self._save_simulation_stats()
        
        # Display summary
        self._display_simulation_summary()
    
    def _save_simulation_stats(self) -> None:
        """Save simulation statistics"""
        stats = {
            "simulation_duration": time.time() - self.simulation_start_time,
            "events_processed": len(self.state.event_history),
            "memories_created": len(self.memory_system.episodic_memory.memories),
            "final_mood": self.mood_engine.current_mood,
            "final_location": self.state.current_location
        }
        
        # In a real implementation, this would save to a file
        print(f"\nSimulation Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    def _display_simulation_summary(self) -> None:
        """Display a summary of the simulation"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}SIMULATION SUMMARY{Colors.RESET}")
        
        # Top events
        if self.state.event_history:
            print(f"\n{Colors.YELLOW}Top Events:{Colors.RESET}")
            for event in self.state.event_history[-5:]:
                print(f"  • {event['title']}: {event['description']}")
        
        # Mood trajectory
        mood_trend = self.mood_engine.get_mood_trend()
        print(f"\n{Colors.YELLOW}Final Mood:{Colors.RESET}")
        print(f"  {self.mood_engine.get_mood_description()} ({self.mood_engine.current_mood:.2f})")
        print(f"  Trend: {mood_trend}")
        
        # Memory summary
        memory_summary = self.memory_system.get_memory_summary()
        print(f"\n{Colors.YELLOW}Memory Summary:{Colors.RESET}")
        print(f"  Working Memory: {memory_summary['working_memory_count']} items")
        print(f"  Episodic Memory: {memory_summary['episodic_memory_count']} experiences")
        print(f"  Semantic Memory: {memory_summary['semantic_memory_count']} facts")
        print(f"  Semantic Memory: {memory_summary['semantic_memory_count']} facts")

def main():
    """Main entry point"""
    try:
        # Create and run simulation
        simulation = TrumanAISimulation()
        simulation.run_simulation()
        
    except Exception as e:
        print(f"Error running simulation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
