"""
TRUMAN AI Data Harvesting System
Collects training data from simulation runs for self-improvement

[SF] Clean data collection and storage
[AC] Atomic functions for data harvesting and processing
"""

import json
import time
import os
from .config import CHARACTER_NAME
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

@dataclass
class TrainingExample:
    """A single training example harvested from simulation"""
    input_prompt: str
    target_response: str
    context: Dict[str, Any]
    mood_state: Dict[str, float]
    personality_state: Dict[str, float]
    timestamp: float
    quality_score: float = 0.0
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass
class SimulationSession:
    """A complete simulation session for data harvesting"""
    session_id: str
    start_time: float
    end_time: float
    duration: float
    total_examples: int
    examples: List[TrainingExample]
    session_stats: Dict[str, Any]
    character_state_changes: Dict[str, Any]

class DataHarvester:
    """Harvests training data from simulation runs"""
    
    def __init__(self, data_dir: str = "data/harvested"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_session: Optional[SimulationSession] = None
        self.session_examples: List[TrainingExample] = []
        self.harvesting_enabled = True
        self.auto_save_interval = 300  # Save every 5 minutes
        self.last_auto_save = time.time()
        
        # Data quality thresholds
        self.min_response_length = 10
        self.max_response_length = 1000
        self.min_quality_score = 0.3
    
    def start_session(self, session_id: str = None) -> str:
        """Start a new harvesting session"""
        if session_id is None:
            session_id = f"session_{int(time.time())}"
        
        self.current_session = SimulationSession(
            session_id=session_id,
            start_time=time.time(),
            end_time=0.0,
            duration=0.0,
            total_examples=0,
            examples=[],
            session_stats={},
            character_state_changes={}
        )
        
        self.session_examples = []
        self.last_auto_save = time.time()
        
        print(f"Started harvesting session: {session_id}")
        return session_id
    
    def end_session(self) -> Optional[SimulationSession]:
        """End current harvesting session and return data"""
        if self.current_session is None:
            return None
        
        self.current_session.end_time = time.time()
        self.current_session.duration = self.current_session.end_time - self.current_session.start_time
        self.current_session.examples = self.session_examples.copy()
        self.current_session.total_examples = len(self.session_examples)
        
        # Calculate session statistics
        self.current_session.session_stats = self._calculate_session_stats()
        
        # Save session data
        self._save_session(self.current_session)
        
        session_data = self.current_session
        self.current_session = None
        self.session_examples = []
        
        print(f"Ended harvesting session: {session_data.session_id}")
        print(f"Collected {session_data.total_examples} training examples")
        
        return session_data
    
    def harvest_example(self, input_prompt: str, target_response: str,
                       context: Dict[str, Any], mood_state: Dict[str, float],
                       personality_state: Dict[str, float], tags: List[str] = None) -> bool:
        """Harvest a training example from simulation"""
        if not self.harvesting_enabled or self.current_session is None:
            return False
        
        # Quality checks
        if not self._is_quality_example(input_prompt, target_response):
            return False
        
        # Create training example
        example = TrainingExample(
            input_prompt=input_prompt,
            target_response=target_response,
            context=context,
            mood_state=mood_state,
            personality_state=personality_state,
            timestamp=time.time(),
            quality_score=self._calculate_quality_score(input_prompt, target_response),
            tags=tags or []
        )
        
        # Add to session
        self.session_examples.append(example)
        
        # Auto-save if needed
        if time.time() - self.last_auto_save > self.auto_save_interval:
            self._auto_save()
        
        return True
    
    def _is_quality_example(self, input_prompt: str, target_response: str) -> bool:
        """Check if example meets quality standards"""
        # Length checks
        if len(target_response) < self.min_response_length:
            return False
        if len(target_response) > self.max_response_length:
            return False
        
        # Content checks
        if not target_response.strip():
            return False
        
        # Avoid repetitive or generic responses
        generic_responses = ["I don't know", "I'm not sure", "Maybe", "Yes", "No"]
        if target_response.strip() in generic_responses:
            return False
        
        return True
    
    def _calculate_quality_score(self, input_prompt: str, target_response: str) -> float:
        """Calculate quality score for training example"""
        score = 0.5  # Base score
        
        # Length appropriateness
        response_length = len(target_response)
        if 50 <= response_length <= 300:
            score += 0.2
        elif 20 <= response_length <= 500:
            score += 0.1
        
        # Vocabulary diversity (simple check)
        words = target_response.split()
        unique_words = set(words)
        if len(words) > 0:
            diversity = len(unique_words) / len(words)
            score += diversity * 0.2
        
        # Sentence structure
        sentences = target_response.split('.')
        if len(sentences) > 1:
            score += 0.1
        
        # Emotional content
        emotional_words = ["happy", "sad", "angry", "excited", "worried", "calm", "frustrated"]
        if any(word in target_response.lower() for word in emotional_words):
            score += 0.1
        
        return min(1.0, max(0.0, score))
    
    def _calculate_session_stats(self) -> Dict[str, Any]:
        """Calculate statistics for the current session"""
        if not self.session_examples:
            return {}
        
        stats = {
            "total_examples": len(self.session_examples),
            "avg_quality_score": sum(ex.quality_score for ex in self.session_examples) / len(self.session_examples),
            "avg_response_length": sum(len(ex.target_response) for ex in self.session_examples) / len(self.session_examples),
            "examples_by_tag": {},
            "mood_distribution": {},
            "time_distribution": {}
        }
        
        # Tag distribution
        for example in self.session_examples:
            for tag in example.tags:
                stats["examples_by_tag"][tag] = stats["examples_by_tag"].get(tag, 0) + 1
        
        # Mood distribution
        mood_ranges = {"very_low": [], "low": [], "neutral": [], "high": [], "very_high": []}
        for example in self.session_examples:
            mood = example.mood_state.get("current_mood", 0.5)
            if mood < 0.2:
                mood_ranges["very_low"].append(example)
            elif mood < 0.4:
                mood_ranges["low"].append(example)
            elif mood < 0.6:
                mood_ranges["neutral"].append(example)
            elif mood < 0.8:
                mood_ranges["high"].append(example)
            else:
                mood_ranges["very_high"].append(example)
        
        for mood_range, examples in mood_ranges.items():
            stats["mood_distribution"][mood_range] = len(examples)
        
        return stats
    
    def _save_session(self, session: SimulationSession) -> None:
        """Save session data to file"""
        filename = self.data_dir / f"{session.session_id}.json"
        
        # Convert to serializable format
        session_data = {
            "session_id": session.session_id,
            "start_time": session.start_time,
            "end_time": session.end_time,
            "duration": session.duration,
            "total_examples": session.total_examples,
            "session_stats": session.session_stats,
            "character_state_changes": session.character_state_changes,
            "examples": [asdict(example) for example in session.examples]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
    
    def _auto_save(self) -> None:
        """Auto-save current session progress"""
        if self.current_session is None:
            return
        
        # Save temporary progress
        temp_filename = self.data_dir / f"{self.current_session.session_id}_temp.json"
        
        temp_data = {
            "session_id": self.current_session.session_id,
            "start_time": self.current_session.start_time,
            "examples_count": len(self.session_examples),
            "last_save": time.time(),
            "examples": [asdict(example) for example in self.session_examples[-100:]]  # Last 100 examples
        }
        
        with open(temp_filename, 'w', encoding='utf-8') as f:
            json.dump(temp_data, f, indent=2)
        
        self.last_auto_save = time.time()
    
    def get_harvested_data(self, limit: int = 1000, min_quality: float = 0.3) -> List[TrainingExample]:
        """Load harvested data for training"""
        examples = []
        
        # Load all session files
        for file_path in self.data_dir.glob("*.json"):
            if file_path.name.endswith("_temp.json"):
                continue  # Skip temp files
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                for example_data in session_data.get("examples", []):
                    if example_data.get("quality_score", 0) >= min_quality:
                        example = TrainingExample(**example_data)
                        examples.append(example)
                        
                        if len(examples) >= limit:
                            break
                
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
            
            if len(examples) >= limit:
                break
        
        return examples
    
    def clean_data(self, min_quality: float = 0.3, remove_duplicates: bool = True) -> int:
        """Clean harvested data by removing low-quality examples and duplicates"""
        removed_count = 0
        
        for file_path in self.data_dir.glob("*.json"):
            if file_path.name.endswith("_temp.json"):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                original_count = len(session_data.get("examples", []))
                
                # Filter by quality
                filtered_examples = [
                    ex for ex in session_data.get("examples", [])
                    if ex.get("quality_score", 0) >= min_quality
                ]
                
                # Remove duplicates if requested
                if remove_duplicates:
                    seen = set()
                    unique_examples = []
                    for example in filtered_examples:
                        # Create a unique key based on prompt and response
                        key = (example.get("input_prompt", ""), example.get("target_response", ""))
                        if key not in seen:
                            seen.add(key)
                            unique_examples.append(example)
                    filtered_examples = unique_examples
                
                session_data["examples"] = filtered_examples
                session_data["total_examples"] = len(filtered_examples)
                
                # Save cleaned data
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(session_data, f, indent=2, ensure_ascii=False)
                
                removed_count += original_count - len(filtered_examples)
                
            except Exception as e:
                print(f"Error cleaning {file_path}: {e}")
        
        return removed_count
    
    def get_harvesting_stats(self) -> Dict[str, Any]:
        """Get statistics about harvested data"""
        total_sessions = 0
        total_examples = 0
        total_size = 0
        
        session_files = list(self.data_dir.glob("*.json"))
        
        for file_path in session_files:
            if file_path.name.endswith("_temp.json"):
                continue
            
            try:
                total_sessions += 1
                file_size = file_path.stat().st_size
                total_size += file_size
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                    total_examples += session_data.get("total_examples", 0)
                
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        
        return {
            "total_sessions": total_sessions,
            "total_examples": total_examples,
            "total_size_mb": total_size / (1024 * 1024),
            "avg_examples_per_session": total_examples / total_sessions if total_sessions > 0 else 0,
            "data_directory": str(self.data_dir)
        }

class DataProcessor:
    """Processes harvested data for training"""
    
    def __init__(self, data_dir: str = "data/harvested"):
        self.data_dir = Path(data_dir)
        self.processed_dir = Path("data/processed")
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def create_training_dataset(self, output_file: str = "training_dataset.jsonl",
                              format_type: str = "jsonl", min_quality: float = 0.4) -> str:
        """Create a training dataset from harvested data"""
        output_path = self.processed_dir / output_file
        
        # Load all examples
        harvester = DataHarvester(self.data_dir)
        examples = harvester.get_harvested_data(limit=10000, min_quality=min_quality)
        
        # Process examples based on format
        if format_type == "jsonl":
            self._save_jsonl_format(examples, output_path)
        elif format_type == "json":
            self._save_json_format(examples, output_path)
        elif format_type == "csv":
            self._save_csv_format(examples, output_path)
        
        print(f"Created training dataset: {output_path}")
        print(f"Total examples: {len(examples)}")
        
        return str(output_path)
    
    def _save_jsonl_format(self, examples: List[TrainingExample], output_path: Path) -> None:
        """Save examples in JSONL format (one JSON per line)"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in examples:
                # Create training format
                training_example = {
                    "input": example.input_prompt,
                    "output": example.target_response,
                    "context": example.context,
                    "metadata": {
                        "mood": example.mood_state,
                        "personality": example.personality_state,
                        "quality_score": example.quality_score,
                        "tags": example.tags,
                        "timestamp": example.timestamp
                    }
                }
                
                f.write(json.dumps(training_example, ensure_ascii=False) + '\n')
    
    def _save_json_format(self, examples: List[TrainingExample], output_path: Path) -> None:
        """Save examples in JSON array format"""
        training_data = []
        
        for example in examples:
            training_example = {
                "input": example.input_prompt,
                "output": example.target_response,
                "context": example.context,
                "metadata": {
                    "mood": example.mood_state,
                    "personality": example.personality_state,
                    "quality_score": example.quality_score,
                    "tags": example.tags,
                    "timestamp": example.timestamp
                }
            }
            training_data.append(training_example)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)
    
    def _save_csv_format(self, examples: List[TrainingExample], output_path: Path) -> None:
        """Save examples in CSV format"""
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                "input_prompt", "target_response", "quality_score",
                "mood_level", "dominant_emotion", "tags", "timestamp"
            ])
            
            # Data rows
            for example in examples:
                writer.writerow([
                    example.input_prompt,
                    example.target_response,
                    example.quality_score,
                    example.mood_state.get("current_mood", 0.5),
                    example.mood_state.get("dominant_emotion", ("neutral", 0.0))[0],
                    ",".join(example.tags),
                    example.timestamp
                ])
    
    def analyze_data_quality(self) -> Dict[str, Any]:
        """Analyze quality of harvested data"""
        harvester = DataHarvester(self.data_dir)
        examples = harvester.get_harvested_data()
        
        if not examples:
            return {"error": "No data found"}
        
        analysis = {
            "total_examples": len(examples),
            "quality_distribution": {},
            "length_distribution": {"short": 0, "medium": 0, "long": 0},
            "tag_frequency": {},
            "mood_correlation": {},
            "time_distribution": {}
        }
        
        # Quality distribution
        quality_ranges = {"low": [], "medium": [], "high": []}
        for example in examples:
            quality = example.quality_score
            if quality < 0.4:
                quality_ranges["low"].append(example)
            elif quality < 0.7:
                quality_ranges["medium"].append(example)
            else:
                quality_ranges["high"].append(example)
        
        for quality_range, examples_list in quality_ranges.items():
            analysis["quality_distribution"][quality_range] = len(examples_list)
        
        # Length distribution
        for example in examples:
            length = len(example.target_response)
            if length < 100:
                analysis["length_distribution"]["short"] += 1
            elif length < 300:
                analysis["length_distribution"]["medium"] += 1
            else:
                analysis["length_distribution"]["long"] += 1
        
        # Tag frequency
        for example in examples:
            for tag in example.tags:
                analysis["tag_frequency"][tag] = analysis["tag_frequency"].get(tag, 0) + 1
        
        return analysis
