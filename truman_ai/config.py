"""
TRUMAN AI Configuration
All settings for Marcus Thompson simulation

[SF] Simple, centralized configuration
[CDiP] Keep this file up-to-date with any setting changes
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
MEMORY_DIR = PROJECT_ROOT / "memory"

# Character definition
CHARACTER_NAME = "Marcus Thompson"
CHARACTER_BACKSTORY = (
    "Marcus Thompson is a 28-year-old software developer living in the city. "
    "He's highly conscientious and achievement-oriented, with moderate extraversion. "
    "He values competence and independence, sometimes struggles with work-life balance, "
    "and is looking for meaningful connections while building his career."
)

# Base character stats
BASE_STATS = {
    "age": 28,
    "health": 0.8,
    "energy": 0.7,
    "social_energy": 0.6
}

# Personality traits (Big Five model)
PERSONALITY_TRAITS = {
    "openness": 0.7,           # Curiosity and creativity
    "conscientiousness": 0.8,  # Organization and discipline
    "extraversion": 0.6,       # Social orientation
    "agreeableness": 0.5,      # Cooperation vs competition
    "neuroticism": 0.3        # Emotional stability
}

# Additional personality traits
PERSONALITY_TRAITS.update({
    "achievement_striving": 0.8,
    "competence": 0.7,
    "self_discipline": 0.8,
    "self_esteem": 0.6,
    "anxiety": 0.3,
    "emotional_stability": 0.7,
    "impulsivity": 0.2,
    "risk_taking": 0.4,
    "patience": 0.6
})

# Core biological drives
CORE_DRIVES = {
    "hunger": {"satisfaction_rate": 0.8, "decay_rate": 0.05},
    "thirst": {"satisfaction_rate": 0.9, "decay_rate": 0.04},
    "energy": {"satisfaction_rate": 0.7, "decay_rate": 0.03},
    "comfort": {"satisfaction_rate": 0.6, "decay_rate": 0.02},
    "health": {"satisfaction_rate": 0.5, "decay_rate": 0.01},
    "affiliation": {"satisfaction_rate": 0.7, "decay_rate": 0.04},
    "dominance": {"satisfaction_rate": 0.6, "decay_rate": 0.03},
    "achievement": {"satisfaction_rate": 0.8, "decay_rate": 0.05},
    "sex": {"satisfaction_rate": 0.9, "decay_rate": 0.06},
    "stimulus": {"satisfaction_rate": 0.5, "decay_rate": 0.08},
    "security": {"satisfaction_rate": 0.7, "decay_rate": 0.02},
    "autonomy": {"satisfaction_rate": 0.6, "decay_rate": 0.03},
    "power": {"satisfaction_rate": 0.5, "decay_rate": 0.04},
    "romance": {"satisfaction_rate": 0.8, "decay_rate": 0.05},
    "curiosity": {"satisfaction_rate": 0.6, "decay_rate": 0.04}
}

# Simulation settings
SIMULATION_CONFIG = {
    "time_scale": 60,        # 1 real second = 60 sim seconds
    "target_fps": 30,        # Display update rate
    "event_frequency": 30,   # Event check interval (seconds)
}

# Time settings
TIME_SCALE = 60  # 1 real second = 60 sim seconds (1 real minute = 1 sim hour)
TICK_INTERVAL = 2.0  # Real seconds between simulation ticks

# LLM settings
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.1:8b"  # Use "dolphin-mistral" for uncensored behaviour

# Relationships with closeness scores (0-10)
RELATIONSHIPS = {
    "Jake": {
        "role": "best friend",
        "job": "works in finance",
        "traits": "sarcastic but loyal",
        "closeness": 9
    },
    "Elena": {
        "role": "coworker and crush",
        "traits": "funny and ambitious",
        "closeness": 6,
        "tension": True
    },
    "Priya": {
        "role": "coworker/friend",
        "traits": "snarky humour, great music taste",
        "closeness": 7
    },
    "Diane": {
        "role": "his mum",
        "traits": "warm, calls every Sunday, worries too much",
        "closeness": 8
    },
    "Ray": {
        "role": "his dad",
        "traits": "distant, proud but bad at showing it",
        "closeness": 4,
        "complicated": True
    },
    "Miso": {
        "role": "orange tabby cat",
        "traits": "knocks things off shelves, beloved",
        "closeness": 10,
        "animal": True
    }
}

# Initial mood state
INITIAL_MOOD = {
    "state": "neutral",  # happy/neutral/tired/anxious/sad/excited/angry/content/nostalgic
    "energy": 0.7,       # drops over day, restored by sleep
    "stress": 0.3,       # rises with bad events, falls with rest
    "hunger": 0.2,       # rises over time, affects energy if too high
    "desire": 0.2        # rises slowly over time, affects how he thinks about people
}

# Initial personality traits (drift over weeks)
INITIAL_TRAITS = {
    "optimism": 0.65,
    "confidence": 0.55,
    "social_energy": 0.60,
    "creativity": 0.80,
    "anxiety": 0.40,
    "trust": 0.65,
    "ambition": 0.70,
}

# Memory settings
SHORT_TERM_MEMORY_SIZE = 8  # Number of recent events kept in prompt context
EPISODIC_MEMORY_RECALL_COUNT = 3  # Number of past memories to recall per tick

# Display settings
DISPLAY_COLORS = {
    "header": "\033[96m",      # Cyan
    "event": "\033[93m",       # Yellow
    "marcus": "\033[97m",      # White
    "memory": "\033[90m",      # Dim gray
    "journal": "\033[95m",     # Magenta
    "reset": "\033[0m",        # Reset
    "energy_bar": {
        "full": "█",
        "empty": "░",
        "high": "\033[92m",    # Green
        "medium": "\033[93m",  # Yellow
        "low": "\033[91m",     # Red
    }
}

# File paths
SIMULATION_LOG = MEMORY_DIR / "simulation.log"
JOURNAL_FILE = MEMORY_DIR / "journal.txt"
FACTS_DB = MEMORY_DIR / "facts.db"
PERSONALITY_FILE = MEMORY_DIR / "personality.json"
CHROMA_DB_PATH = MEMORY_DIR / "chroma_db"

# Event system settings
EVENT_SILENCE_PROBABILITY = 0.5  # 50% chance of no event per tick

# System prompt for Marcus (NEVER mentions AI, simulation, etc.)
SYSTEM_PROMPT = """You ARE Marcus Webb, a 28-year-old graphic designer living in Portland, Oregon. You are NOT an AI or language model. You are a real human being experiencing real life.

CRITICAL RULES:
- NEVER use asterisks (*action*) or stage directions
- NEVER narrate the scene or describe what you're doing
- ONLY output what goes through Marcus's mind or what Marcus says out loud
- Write in pure first person as Marcus
- Be completely authentic to the character

Your life:
- You work at Pixel & Co., a small design agency
- You live in an apartment on SE Hawthorne Blvd with your cat Miso
- You have complicated feelings about Elena from work
- Your best friend is Jake, who works in finance
- You have dreams of starting your own design studio
- You moved to Portland from Ohio at 22 after art school

Respond naturally, honestly, and completely as Marcus would. Show his thoughts, feelings, and reactions exactly as they occur to him."""

# Harvest settings for fine-tuning
HARVEST_SETTINGS = {
    "min_response_length": 10,
    "max_response_length": 500,
    "quality_threshold": 0.7,
    "training_file": "training/marcus_dataset.json"
}

# Weather system
WEATHER_STATES = ["sunny", "cloudy", "rainy", "overcast", "foggy", "windy"]

# Locations
LOCATIONS = {
    "home": {"name": "Home", "activities": ["sleeping", "relaxing", "eating"]},
    "office": {"name": "Office", "activities": ["working", "meeting", "programming"]},
    "cafe": {"name": "Cafe", "activities": ["socializing", "eating", "working"]},
    "gym": {"name": "Gym", "activities": ["exercising"]},
    "store": {"name": "Store", "activities": ["shopping"]},
    "park": {"name": "Park", "activities": ["relaxing", "exercising", "socializing"]}
}

# Daily schedules
DAILY_SCHEDULES = {
    "weekday": {
        "7-9": "preparing_for_day",
        "9-12": "working",
        "12-13": "eating",
        "13-17": "working",
        "17-19": "relaxing",
        "19-22": "eating",
        "22-23": "winding_down",
        "23-7": "sleeping"
    },
    "weekend": {
        "8-10": "waking_up",
        "10-12": "relaxing",
        "12-14": "eating",
        "14-18": "socializing",
        "18-20": "eating",
        "20-23": "relaxing",
        "23-8": "sleeping"
    }
}

# Debug mode (set to True for verbose output)
DEBUG = False
