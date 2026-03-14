"""
TRUMAN AI World System
Time engine, locations, and daily schedules

[SF] Clean time and location management
[AC] Atomic functions for time progression
"""

import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from .config import WEATHER_STATES

class TimeEngine:
    """Manages simulated time progression"""
    
    def __init__(self, time_scale: int = 60):
        self.time_scale = time_scale  # 1 real second = X sim seconds
        self.start_real_time = time.time()
        self.sim_start_time = datetime(2024, 3, 15, 7, 0, 0)  # Marcus starts at 7 AM
        self.current_sim_time = self.sim_start_time
        
    def advance_time(self, real_seconds_passed: float) -> datetime:
        """Advance simulated time based on real time passed [AC]"""
        sim_seconds_passed = real_seconds_passed * self.time_scale
        self.current_sim_time += timedelta(seconds=sim_seconds_passed)
        return self.current_sim_time
    
    def get_current_time(self) -> datetime:
        """Get current simulated time"""
        return self.current_sim_time
    
    def get_time_string(self) -> str:
        """Get formatted time string"""
        return self.current_sim_time.strftime("%I:%M %p").lower()
    
    def get_day_of_week(self) -> str:
        """Get day of week"""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return days[self.current_sim_time.weekday()]
    
    def is_weekend(self) -> bool:
        """Check if it's weekend"""
        return self.current_sim_time.weekday() >= 5
    
    def is_nighttime(self) -> bool:
        """Check if it's nighttime (10 PM - 6 AM)"""
        hour = self.current_sim_time.hour
        return hour >= 22 or hour < 6
    
    def is_work_hours(self) -> bool:
        """Check if it's work hours (9 AM - 5 PM on weekdays)"""
        hour = self.current_sim_time.hour
        return 9 <= hour < 17 and not self.is_weekend()
    
    def get_hour_decimal(self) -> float:
        """Get hour as decimal (e.g., 2:30 PM = 14.5)"""
        return self.current_sim_time.hour + self.current_sim_time.minute / 60

class Location:
    """Represents a location where Marcus can be"""
    
    def __init__(self, name: str, activity: str, event_weights: Dict[str, float]):
        self.name = name
        self.activity = activity
        self.event_weights = event_weights  # Weights for different event pools
    
    def get_description(self) -> str:
        """Get location description"""
        return f"{self.name} ({self.activity})"

class ScheduleManager:
    """Manages Marcus's daily schedule and location transitions"""
    
    def __init__(self):
        self.locations = self._initialize_locations()
        self.weekday_schedule = self._create_weekday_schedule()
        self.weekend_schedule = self._create_weekend_schedule()
        self.current_location = None
        
    def _initialize_locations(self) -> Dict[str, Location]:
        """Initialize all possible locations [SF]"""
        return {
            "home": Location(
                "Home (SE Hawthorne apartment)",
                "at home",
                {
                    "MISO_EVENTS": 0.3,
                    "PHONE_EVENTS": 0.2,
                    "HOME_AMBIENT": 0.2,
                    "INNER_THOUGHTS": 0.2,
                    "SENSORY_EVENTS": 0.1
                }
            ),
            "work": Location(
                "Pixel & Co. office",
                "at work",
                {
                    "WORK_EVENTS": 0.5,
                    "SOCIAL_EVENTS": 0.2,
                    "PHONE_EVENTS": 0.15,
                    "INNER_THOUGHTS": 0.1,
                    "SENSORY_EVENTS": 0.05
                }
            ),
            "coffee_shop": Location(
                "Stumptown Coffee",
                "getting coffee",
                {
                    "SOCIAL_EVENTS": 0.3,
                    "SENSORY_EVENTS": 0.3,
                    "INNER_THOUGHTS": 0.2,
                    "PHONE_EVENTS": 0.15,
                    "STREET_EVENTS": 0.05
                }
            ),
            "bar": Location(
                "The Goodfoot Lounge",
                "at a bar",
                {
                    "SOCIAL_EVENTS": 0.6,
                    "SENSORY_EVENTS": 0.2,
                    "PHONE_EVENTS": 0.1,
                    "INNER_THOUGHTS": 0.1
                }
            ),
            "gym": Location(
                "24 Hour Fitness",
                "at the gym",
                {
                    "INNER_THOUGHTS": 0.4,
                    "SENSORY_EVENTS": 0.3,
                    "SOCIAL_EVENTS": 0.2,
                    "PHONE_EVENTS": 0.1
                }
            ),
            "grocery": Location(
                "Trader Joe's",
                "grocery shopping",
                {
                    "SOCIAL_EVENTS": 0.3,
                    "SENSORY_EVENTS": 0.3,
                    "STREET_EVENTS": 0.2,
                    "INNER_THOUGHTS": 0.2
                }
            ),
            "park": Location(
                "Laurelhurst Park",
                "at the park",
                {
                    "SENSORY_EVENTS": 0.4,
                    "INNER_THOUGHTS": 0.3,
                    "SOCIAL_EVENTS": 0.2,
                    "STREET_EVENTS": 0.1
                }
            ),
            "studio": Location(
                "Home design studio",
                "working on personal projects",
                {
                    "INNER_THOUGHTS": 0.4,
                    "SENSORY_EVENTS": 0.3,
                    "MISO_EVENTS": 0.2,
                    "PHONE_EVENTS": 0.1
                }
            )
        }
    
    def _create_weekday_schedule(self) -> List[Tuple[float, str]]:
        """Create weekday schedule (hour, location) [SF]"""
        return [
            (6.0, "home"),      # 6:00 AM - Wake up
            (7.0, "home"),      # 7:00 AM - Morning routine
            (8.0, "coffee_shop"), # 8:00 AM - Coffee on way to work
            (9.0, "work"),      # 9:00 AM - Work starts
            (12.0, "work"),     # 12:00 PM - Lunch at work
            (13.0, "work"),     # 1:00 PM - Back to work
            (17.0, "coffee_shop"), # 5:00 PM - After work coffee
            (18.0, "home"),     # 6:00 PM - Home
            (19.0, "home"),     # 7:00 PM - Dinner
            (20.0, "studio"),   # 8:00 PM - Personal projects
            (22.0, "home"),     # 10:00 PM - Wind down
            (23.0, "home"),     # 11:00 PM - Getting ready for bed
        ]
    
    def _create_weekend_schedule(self) -> List[Tuple[float, str]]:
        """Create weekend schedule (hour, location) [SF]"""
        return [
            (8.0, "home"),      # 8:00 AM - Sleep in
            (9.0, "coffee_shop"), # 9:00 AM - Brunch/coffee
            (10.0, "park"),     # 10:00 AM - Park time
            (12.0, "grocery"),  # 12:00 PM - Grocery shopping
            (13.0, "home"),     # 1:00 PM - Lunch at home
            (14.0, "studio"),   # 2:00 PM - Personal projects
            (17.0, "bar"),      # 5:00 PM - Meet friends
            (19.0, "home"),     # 7:00 PM - Home
            (20.0, "home"),     # 8:00 PM - Dinner
            (22.0, "home"),     # 10:00 PM - Wind down
            (23.0, "home"),     # 11:00 PM - Bed routine
        ]
    
    def get_current_location(self, time_engine: TimeEngine) -> Location:
        """Get current location based on time and schedule [AC]"""
        current_hour = time_engine.get_hour_decimal()
        
        # Choose schedule based on weekday/weekend
        schedule = self.weekend_schedule if time_engine.is_weekend() else self.weekday_schedule
        
        # Find appropriate time slot
        for i, (hour, location_name) in enumerate(schedule):
            if current_hour < hour:
                if i == 0:
                    # Before first entry
                    prev_location_name = schedule[-1][1]
                else:
                    prev_location_name = schedule[i-1][1]
                return self.locations[prev_location_name]
        
        # After last entry
        return self.locations[schedule[-1][1]]
    
    def get_location_description(self, time_engine: TimeEngine) -> str:
        """Get human-readable location description"""
        location = self.get_current_location(time_engine)
        return location.get_description()

class WeatherSystem:
    """Manages weather conditions"""
    
    def __init__(self):
        self.current_weather = random.choice(WEATHER_STATES)
        self.weather_duration = random.randint(4, 8)  # Hours
        self.hours_since_change = 0
        
    def update_weather(self, time_engine: TimeEngine):
        """Update weather if duration has passed [AC]"""
        self.hours_since_change += 1/60  # Assuming called every minute
        
        if self.hours_since_change >= self.weather_duration:
            self.current_weather = random.choice(WEATHER_STATES)
            self.weather_duration = random.randint(4, 8)
            self.hours_since_change = 0
    
    def get_weather_description(self) -> str:
        """Get weather description"""
        weather_descriptions = {
            "sunny": "bright and sunny",
            "cloudy": "overcast with clouds",
            "rainy": "rainy and damp",
            "overcast": "grey and overcast",
            "foggy": "foggy and misty",
            "windy": "windy with gusts"
        }
        return weather_descriptions.get(self.current_weather, "neutral")

class World:
    """Main world system combining time, location, and weather"""
    
    def __init__(self, time_scale: int = 60):
        self.time_engine = TimeEngine(time_scale)
        self.schedule_manager = ScheduleManager()
        self.weather_system = WeatherSystem()
        
    def update(self, real_seconds_passed: float):
        """Update all world systems [AC]"""
        self.time_engine.advance_time(real_seconds_passed)
        self.weather_system.update_weather(self.time_engine)
    
    def get_current_state(self) -> Dict[str, str]:
        """Get current world state snapshot"""
        location = self.schedule_manager.get_current_location(self.time_engine)
        return {
            "time": self.time_engine.get_time_string(),
            "day": self.time_engine.get_day_of_week(),
            "location": location.get_description(),
            "weather": self.weather_system.get_weather_description(),
            "is_work_hours": str(self.time_engine.is_work_hours()),
            "is_nighttime": str(self.time_engine.is_nighttime())
        }
