"""
Test suite for Truman AI simulation
Tests core functionality after bug fixes
"""

import unittest
import time
from datetime import datetime

# Test imports
from truman_ai.config import (
    CHARACTER_NAME, PERSONALITY_TRAITS, CORE_DRIVES,
    SIMULATION_CONFIG, WEATHER_STATES
)
from truman_ai.world import TimeEngine, ScheduleManager, WeatherSystem, World
from truman_ai.events import EventEngine, EventPool, LifeEvent
from truman_ai.mood import MoodEngine, DriveState, PersonalityProfile
from truman_ai.memory import MemorySystem, MemoryType, MemoryImportance
from truman_ai.brain import Brain, PromptBuilder, LLMInterface
from truman_ai.display import Colors, Display, ProgressBar, DisplayManager
from truman_ai.harvest import DataHarvester, TrainingExample
from truman_ai.finetune import TrainingConfig, ModelTrainer, FineTuningPipeline


class TestConfig(unittest.TestCase):
    """Test configuration module"""
    
    def test_character_name_exists(self):
        """Test that character name is defined"""
        self.assertIsInstance(CHARACTER_NAME, str)
        self.assertTrue(len(CHARACTER_NAME) > 0)
    
    def test_personality_traits_valid(self):
        """Test personality traits are valid"""
        self.assertIsInstance(PERSONALITY_TRAITS, dict)
        for trait, value in PERSONALITY_TRAITS.items():
            self.assertIsInstance(trait, str)
            self.assertIsInstance(value, float)
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)
    
    def test_core_drives_valid(self):
        """Test core drives are valid"""
        self.assertIsInstance(CORE_DRIVES, dict)
        for drive, config in CORE_DRIVES.items():
            self.assertIn("satisfaction_rate", config)
            self.assertIn("decay_rate", config)


class TestTimeEngine(unittest.TestCase):
    """Test time engine functionality"""
    
    def test_time_initialization(self):
        """Test time engine initializes correctly"""
        engine = TimeEngine(time_scale=60)
        self.assertIsNotNone(engine.current_sim_time)
    
    def test_advance_time(self):
        """Test time advancement"""
        engine = TimeEngine(time_scale=60)
        initial_time = engine.current_sim_time
        new_time = engine.advance_time(1.0)
        self.assertGreater(new_time, initial_time)
    
    def test_get_time_string(self):
        """Test time string formatting"""
        engine = TimeEngine(time_scale=60)
        time_str = engine.get_time_string()
        self.assertIsInstance(time_str, str)
    
    def test_is_weekend(self):
        """Test weekend detection"""
        engine = TimeEngine(time_scale=60)
        # Just test it returns a boolean
        result = engine.is_weekend()
        self.assertIsInstance(result, bool)


class TestEventEngine(unittest.TestCase):
    """Test event engine functionality"""
    
    def test_event_engine_initialization(self):
        """Test event engine initializes"""
        engine = EventEngine()
        self.assertIsNotNone(engine.events)
    
    def test_event_pools_exist(self):
        """Test all event pools are defined"""
        engine = EventEngine()
        for pool in EventPool:
            self.assertIn(pool, engine.events)
            self.assertGreater(len(engine.events[pool]), 0)
    
    def test_select_event(self):
        """Test event selection"""
        engine = EventEngine()
        character_state = {"has_job": True, "in_relationship": False}
        event = engine.select_event(character_state)
        # Event may be None due to randomness, but shouldn't crash
        if event is not None:
            self.assertIsInstance(event, LifeEvent)


class TestMoodEngine(unittest.TestCase):
    """Test mood engine functionality"""
    
    def test_mood_initialization(self):
        """Test mood engine initializes"""
        engine = MoodEngine()
        self.assertIsNotNone(engine.drives)
        self.assertIsNotNone(engine.personality)
    
    def test_drive_states_initialized(self):
        """Test drives are initialized"""
        engine = MoodEngine()
        self.assertGreater(len(engine.drives), 0)
        for drive in engine.drives.values():
            self.assertIsInstance(drive, DriveState)
    
    def test_update_drives(self):
        """Test drive updates"""
        engine = MoodEngine()
        initial_energy = engine.drives["energy"].current_level
        engine.update_drives(time_delta=1.0, activities=[])
        # Energy should decay slightly
        self.assertLessEqual(engine.drives["energy"].current_level, initial_energy)
    
    def test_get_mood_description(self):
        """Test mood description"""
        engine = MoodEngine()
        desc = engine.get_mood_description()
        self.assertIsInstance(desc, str)


class TestMemorySystem(unittest.TestCase):
    """Test memory system functionality"""
    
    def test_memory_system_initialization(self):
        """Test memory system initializes"""
        system = MemorySystem()
        self.assertIsNotNone(system.working_memory)
        self.assertIsNotNone(system.episodic_memory)
        self.assertIsNotNone(system.semantic_memory)
    
    def test_add_experience(self):
        """Test adding experience to memory"""
        system = MemorySystem()
        memory = system.add_experience(
            "Test experience",
            MemoryImportance.MODERATE,
            0.5,
            ["test"],
            {"test_key": "test_value"}
        )
        self.assertIsNotNone(memory)
        self.assertEqual(memory.content, "Test experience")
    
    def test_recall_memories(self):
        """Test memory recall"""
        system = MemorySystem()
        system.add_experience("Important event", MemoryImportance.IMPORTANT, 0.8, ["important"])
        results = system.recall("event", limit=5)
        self.assertIsInstance(results, dict)


class TestBrain(unittest.TestCase):
    """Test brain functionality"""
    
    def test_brain_initialization(self):
        """Test brain initializes"""
        brain = Brain()
        self.assertIsNotNone(brain.prompt_builder)
        self.assertIsNotNone(brain.llm_interface)
    
    def test_prompt_builder(self):
        """Test prompt builder"""
        builder = PromptBuilder(
            "Test Character",
            "Test backstory",
            {"openness": 0.5}
        )
        self.assertIsNotNone(builder.base_prompt)
    
    def test_llm_interface(self):
        """Test LLM interface"""
        llm = LLMInterface()
        # Test with mock response
        response = llm.generate_response("Test prompt")
        self.assertIsInstance(response, str)


class TestDisplay(unittest.TestCase):
    """Test display functionality"""
    
    def test_colors_defined(self):
        """Test colors are defined"""
        self.assertTrue(hasattr(Colors, "RESET"))
        self.assertTrue(hasattr(Colors, "RED"))
        self.assertTrue(hasattr(Colors, "GREEN"))
    
    def test_progress_bar(self):
        """Test progress bar rendering"""
        bar = ProgressBar.render(0.5, 1.0, width=20)
        self.assertIsInstance(bar, str)
        self.assertIn("[", bar)
        self.assertIn("]", bar)
    
    def test_display_initialization(self):
        """Test display initializes"""
        display = Display("Test Character")
        self.assertEqual(display.character_name, "Test Character")


class TestHarvest(unittest.TestCase):
    """Test data harvesting functionality"""
    
    def test_harvester_initialization(self):
        """Test harvester initializes"""
        harvester = DataHarvester(data_dir="data/test_harvest")
        self.assertIsNotNone(harvester.data_dir)
    
    def test_training_example_creation(self):
        """Test training example creation"""
        example = TrainingExample(
            input_prompt="Test input",
            target_response="Test response",
            context={"test": True},
            mood_state={"current_mood": 0.5},
            personality_state={"optimism": 0.6},
            timestamp=time.time()
        )
        self.assertEqual(example.input_prompt, "Test input")
        self.assertEqual(example.target_response, "Test response")


class TestFinetune(unittest.TestCase):
    """Test fine-tuning functionality"""
    
    def test_training_config(self):
        """Test training config creation"""
        config = TrainingConfig(
            model_name="test-model",
            learning_rate=1e-5,
            num_epochs=3
        )
        self.assertEqual(config.model_name, "test-model")
        self.assertEqual(config.num_epochs, 3)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_world_system(self):
        """Test complete world system"""
        world = World(time_scale=60)
        world.update(1.0)
        state = world.get_current_state()
        self.assertIn("time", state)
        self.assertIn("location", state)
        self.assertIn("weather", state)
    
    def test_mood_update_cycle(self):
        """Test complete mood update cycle"""
        engine = MoodEngine()
        context = {"social_situation": False, "work_situation": True}
        activities = ["working"]
        events = []
        
        new_mood = engine.update_mood(events, context, activities, time_delta=1.0)
        self.assertIsInstance(new_mood, float)
        self.assertGreaterEqual(new_mood, 0.0)
        self.assertLessEqual(new_mood, 1.0)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestTimeEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestEventEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestMoodEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestMemorySystem))
    suite.addTests(loader.loadTestsFromTestCase(TestBrain))
    suite.addTests(loader.loadTestsFromTestCase(TestDisplay))
    suite.addTests(loader.loadTestsFromTestCase(TestHarvest))
    suite.addTests(loader.loadTestsFromTestCase(TestFinetune))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
