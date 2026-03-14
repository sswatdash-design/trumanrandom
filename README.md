# Truman AI

An advanced AI simulation system that creates a believable, evolving digital character with personality, memory, emotions, and life experiences.

## Overview

Truman AI is a sophisticated character simulation system that models a digital person named Marcus Thompson through multiple interconnected systems:

- **World System**: Time progression, locations, and daily schedules
- **Event System**: 200+ life events across 9 categories
- **Mood System**: Biological drives and personality traits
- **Memory System**: Three-layer memory (working, episodic, semantic)
- **Brain System**: LLM interface and decision-making
- **Display System**: Real-time terminal visualization
- **Self-Training**: Data harvesting and fine-tuning capabilities

## Features

### 🧠 Personality & Psychology
- **Big Five personality traits** with dynamic expression
- **Biological drives** (hunger, thirst, energy, etc.)
- **Emotional state** tracking and processing
- **Mood calculation** based on internal and external factors

### 🌍 World & Environment
- **Time engine** with configurable time scales
- **Multiple locations** with contextual activities
- **Weather system** affecting mood and behavior
- **Daily schedules** and routines

### 📅 Life Events
- **200+ unique events** across 9 categories:
  - Career (25 events)
  - Relationships (30 events)
  - Health (25 events)
  - Finance (25 events)
  - Education (20 events)
  - Social (25 events)
  - Family (25 events)
  - Personal Growth (25 events)
  - Unexpected (25 events)

### 🧠 Memory System
- **Working memory**: Short-term immediate processing
- **Episodic memory**: Personal experiences and events
- **Semantic memory**: Facts and general knowledge
- **Memory consolidation** and forgetting mechanisms

### 💭 Cognitive Processing
- **Contextual reasoning** based on current state
- **Decision making** with personality-aligned choices
- **Self-reflection** and learning from experiences
- **Background thinking** processes

### 🎨 Visual Interface
- **Real-time terminal display** with color coding
- **Progress bars** for drives and mood
- **Activity logs** and event notifications
- **Character state visualization**

### 🔄 Self-Improvement
- **Data harvesting** from simulation runs
- **Training dataset** creation
- **Model fine-tuning** pipeline
- **Performance evaluation** and comparison

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd truman
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the simulation:
```bash
python -m truman_ai.main
```

## Usage

### Basic Simulation
```bash
# Run the main simulation
python -m truman_ai.main

# The simulation will start with Marcus Thompson at 7 AM
# Watch as he experiences life events, makes decisions, and evolves
```

### Data Harvesting
```python
from truman_ai.harvest import DataHarvester

# Start harvesting training data
harvester = DataHarvester()
harvester.start_session("session_001")

# Harvest examples during simulation
harvester.harvest_example(
    input_prompt="How are you feeling today?",
    target_response="I'm feeling quite optimistic about the day ahead...",
    context={"time": "morning", "location": "home"},
    mood_state={"current_mood": 0.7, "dominant_emotion": "happy"},
    personality_state={"extraversion": 0.6, "neuroticism": 0.3}
)
```

### Model Fine-tuning
```python
from truman_ai.finetune import FineTuningPipeline, TrainingConfig

# Configure training
config = TrainingConfig(
    model_name="gpt-3.5-turbo",
    learning_rate=1e-5,
    num_epochs=3
)

# Run fine-tuning pipeline
pipeline = FineTuningPipeline()
results = pipeline.run_full_pipeline(config)
```

## Architecture

### Core Components

1. **config.py**: Configuration settings and character data
2. **world.py**: Time engine and location management
3. **events.py**: Life event generation and processing
4. **mood.py**: Emotional state and drive management
5. **memory.py**: Three-layer memory system
6. **brain.py**: LLM interface and cognitive processing
7. **display.py**: Terminal UI and visualization
8. **main.py**: Master simulation loop
9. **harvest.py**: Data collection for training
10. **finetune.py**: Model fine-tuning pipeline

### Data Flow

```
World Events → Mood Engine → Memory System → Brain → Display
     ↓              ↓              ↓        ↓       ↓
Time Progression → Drive Updates → Storage → Decisions → UI
```

### Character Profile

**Name**: Marcus Thompson  
**Age**: 28  
**Occupation**: Software Developer  
**Personality**: High in achievement striving, moderate extraversion, low neuroticism  
**Backstory**: Independent software developer focused on competence and achievement

## Configuration

### Simulation Settings
```python
SIMULATION_CONFIG = {
    "time_scale": 60,        # 1 real second = 60 sim seconds
    "target_fps": 30,        # Display update rate
    "event_frequency": 30,   # Event check interval (seconds)
}
```

### Personality Traits
```python
PERSONALITY_TRAITS = {
    "openness": 0.7,           # Curiosity and creativity
    "conscientiousness": 0.8,  # Organization and discipline
    "extraversion": 0.6,       # Social orientation
    "agreeableness": 0.5,      # Cooperation vs competition
    "neuroticism": 0.3        # Emotional stability
}
```

### Biological Drives
```python
CORE_DRIVES = {
    "hunger": {"satisfaction_rate": 0.8, "decay_rate": 0.05},
    "thirst": {"satisfaction_rate": 0.9, "decay_rate": 0.04},
    "energy": {"satisfaction_rate": 0.7, "decay_rate": 0.03},
    # ... more drives
}
```

## Customization

### Creating New Characters
1. Modify `CHARACTER_NAME` and `CHARACTER_BACKSTORY` in `config.py`
2. Adjust `PERSONALITY_TRAITS` values
3. Update `BASE_STATS` for physical characteristics
4. Customize `DAILY_SCHEDULES` for routines

### Adding New Events
```python
# In events.py, add to the appropriate pool
LifeEvent(
    "Custom Event",
    "Description of what happens",
    EventPool.CAREER,
    mood_impact=0.3,
    trait_impacts={"achievement_striving": 0.2},
    drive_impacts={"achievement": 0.3},
    requirements=["has_job"]
)
```

### Extending Memory System
```python
# Add new memory types or consolidation strategies
class CustomMemory(Memory):
    def __init__(self, ...):
        # Custom memory implementation
        pass
```

## Output Examples

### Terminal Display
```
═══════════════════════════════════════════════════════════════════════════
                           Marcus Thompson AI Simulation                           
═══════════════════════════════════════════════════════════════════════════
Time: 2024-03-15 08:30 | Location: office | Weather: sunny
───────────────────────────────────────────────────────────────────────────────

🧠 MOOD & EMOTIONS
┌───────────────────────────────────────────────────────────────────────────────┐
│ Overall Mood: Happy           [████████████████████████████] 72.0%          │
│ Emotions:     happiness:0.45 anger:0.02 fear:0.01                             │
│ Trend:         Stable                                                          │
└───────────────────────────────────────────────────────────────────────────────┘

🎯 BIOLOGICAL DRIVES
┌───────────────────────────────────────────────────────────────────────────────┐
│ Hunger         Very Satisfied [████████████████████] 85.0%                    │
│ Thirst         Moderately S [███████████████░░░░] 60.0%                       │
│ Energy         Needs attention [█████░░░░░░░░░░░░░░] 25.0%                    │
└───────────────────────────────────────────────────────────────────────────────┘
```

### Event Notifications
```
🎉 EVENT: Promotion at Work
Your hard work pays off with a well-deserved promotion.
Mood Impact: +0.30
──────────────────────────────────────────
```

### Memory Examples
```
🧠 MEMORY SYSTEM
┌───────────────────────────────────────────────────────────────────────────────┐
│ Working Memory:   3 items                                                      │
│ Episodic Memory:  1,247 items                                                  │
│ Semantic Memory:  89 facts                                                     │
│ Concepts:         12 concepts                                                  │
└───────────────────────────────────────────────────────────────────────────────┘
```

## Development

### Code Structure
- **[SF]** Clean, modular design with single responsibilities
- **[AC]** Atomic functions for predictable behavior
- **Type hints** for better code documentation
- **Comprehensive comments** explaining complex systems

### Testing
```bash
# Run tests (when implemented)
python -m pytest tests/

# Code quality checks
python -m flake8 truman_ai/
python -m black truman_ai/
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Future Roadmap

### Phase 1: Core Enhancement
- [ ] LLM integration for authentic responses
- [ ] Enhanced memory association algorithms
- [ ] More sophisticated emotional modeling
- [ ] GUI interface option

### Phase 2: Multi-Character
- [ ] Multiple character interactions
- [ ] Relationship dynamics
- [ ] Social network simulation
- [ ] Group behavior modeling

### Phase 3: Advanced AI
- [ ] Reinforcement learning for behavior
- [ ] Neural memory networks
- [ ] Advanced natural language processing
- [ ] Real-time learning adaptation

### Phase 4: Platform Features
- [ ] Web interface
- [ ] Mobile app
- [ ] API for external integrations
- [ ] Cloud-based simulation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by cognitive science and personality psychology research
- Built with modern Python and AI/ML best practices
- Designed for educational and research purposes
- Open source contribution to AI simulation field

---

**Truman AI** - Bringing digital characters to life through sophisticated simulation and authentic psychology.
