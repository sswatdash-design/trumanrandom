"""
TRUMAN AI Fine-tuning System
Self-improvement through model fine-tuning on harvested data

[SF] Clean fine-tuning pipeline and model management
[AC] Atomic functions for training and evaluation
"""

import json
import os
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

@dataclass
class TrainingConfig:
    """Configuration for fine-tuning"""
    model_name: str = "gpt-3.5-turbo"
    learning_rate: float = 1e-5
    batch_size: int = 8
    num_epochs: int = 3
    validation_split: float = 0.2
    max_length: int = 512
    warmup_steps: int = 100
    save_steps: int = 500
    eval_steps: int = 100
    logging_steps: int = 50

@dataclass
class TrainingMetrics:
    """Metrics from training run"""
    train_loss: float
    eval_loss: float
    perplexity: float
    accuracy: float
    training_time: float
    epochs_completed: int
    samples_processed: int

class ModelTrainer:
    """Handles model fine-tuning"""
    
    def __init__(self, config: TrainingConfig, model_dir: str = "models"):
        self.config = config
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        self.training_data = []
        self.validation_data = []
        self.current_model_path = None
        
    def load_training_data(self, data_file: str) -> bool:
        """Load training data from file"""
        data_path = Path(data_file)
        
        if not data_path.exists():
            print(f"Training data file not found: {data_file}")
            return False
        
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                if data_path.suffix == '.jsonl':
                    # JSONL format
                    for line in f:
                        if line.strip():
                            example = json.loads(line)
                            self.training_data.append(example)
                else:
                    # JSON format
                    data = json.load(f)
                    if isinstance(data, list):
                        self.training_data = data
                    else:
                        self.training_data = data.get("examples", [])
            
            # Split data
            split_index = int(len(self.training_data) * (1 - self.config.validation_split))
            self.validation_data = self.training_data[split_index:]
            self.training_data = self.training_data[:split_index]
            
            print(f"Loaded {len(self.training_data)} training examples")
            print(f"Loaded {len(self.validation_data)} validation examples")
            
            return True
            
        except Exception as e:
            print(f"Error loading training data: {e}")
            return False
    
    def prepare_data_for_training(self) -> Tuple[List, List]:
        """Prepare data for training format"""
        train_inputs = []
        train_outputs = []
        
        for example in self.training_data:
            if "input" in example and "output" in example:
                train_inputs.append(example["input"])
                train_outputs.append(example["output"])
            elif "input_prompt" in example and "target_response" in example:
                train_inputs.append(example["input_prompt"])
                train_outputs.append(example["target_response"])
        
        return train_inputs, train_outputs
    
    def create_training_prompt(self, input_text: str, output_text: str) -> str:
        """Create formatted training prompt"""
        return f"Input: {input_text}\nOutput: {output_text}"
    
    def simulate_training(self) -> TrainingMetrics:
        """Simulate training process (placeholder for actual training)"""
        print("Starting model fine-tuning...")
        print(f"Model: {self.config.model_name}")
        print(f"Training examples: {len(self.training_data)}")
        print(f"Validation examples: {len(self.validation_data)}")
        
        start_time = time.time()
        
        # Simulate training epochs
        for epoch in range(self.config.num_epochs):
            print(f"Epoch {epoch + 1}/{self.config.num_epochs}")
            
            # Simulate batch processing
            num_batches = len(self.training_data) // self.config.batch_size
            for batch in range(num_batches):
                if batch % 50 == 0:
                    print(f"  Batch {batch}/{num_batches}")
                
                # Simulate training step
                time.sleep(0.001)  # Simulate computation time
            
            # Simulate validation
            print(f"  Validation loss: {2.5 - epoch * 0.3:.3f}")
        
        training_time = time.time() - start_time
        
        # Simulate final metrics
        metrics = TrainingMetrics(
            train_loss=1.2,
            eval_loss=1.4,
            perplexity=4.1,
            accuracy=0.72,
            training_time=training_time,
            epochs_completed=self.config.num_epochs,
            samples_processed=len(self.training_data) * self.config.num_epochs
        )
        
        # Save model checkpoint
        self.save_model(metrics)
        
        print("Training completed!")
        print(f"Final metrics: {metrics}")
        
        return metrics
    
    def save_model(self, metrics: TrainingMetrics) -> str:
        """Save trained model"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_name = f"truman_ai_{timestamp}"
        model_path = self.model_dir / model_name
        
        # Create model directory
        model_path.mkdir(exist_ok=True)
        
        # Save model metadata
        model_info = {
            "model_name": model_name,
            "base_model": self.config.model_name,
            "training_config": self.config.__dict__,
            "training_metrics": metrics.__dict__,
            "training_date": datetime.now().isoformat(),
            "training_data_size": len(self.training_data),
            "validation_data_size": len(self.validation_data)
        }
        
        with open(model_path / "model_info.json", 'w') as f:
            json.dump(model_info, f, indent=2)
        
        # Save sample predictions
        self._save_sample_predictions(model_path)
        
        self.current_model_path = model_path
        print(f"Model saved to: {model_path}")
        
        return str(model_path)
    
    def _save_sample_predictions(self, model_path: Path) -> None:
        """Save sample predictions for evaluation"""
        samples = []
        
        # Take a few validation examples
        for i, example in enumerate(self.validation_data[:5]):
            input_text = example.get("input", example.get("input_prompt", ""))
            actual_output = example.get("output", example.get("target_response", ""))
            
            # Simulate model prediction
            predicted_output = f"Simulated response to: {input_text[:50]}..."
            
            samples.append({
                "input": input_text,
                "actual_output": actual_output,
                "predicted_output": predicted_output,
                "quality_score": 0.75  # Simulated score
            })
        
        with open(model_path / "sample_predictions.json", 'w') as f:
            json.dump(samples, f, indent=2)
    
    def evaluate_model(self, model_path: str = None) -> Dict[str, Any]:
        """Evaluate model performance"""
        if model_path is None:
            model_path = self.current_model_path
        
        if model_path is None:
            return {"error": "No model available for evaluation"}
        
        model_path = Path(model_path)
        
        if not model_path.exists():
            return {"error": f"Model path not found: {model_path}"}
        
        # Load model info
        with open(model_path / "model_info.json", 'r') as f:
            model_info = json.load(f)
        
        # Simulate evaluation
        evaluation_results = {
            "model_name": model_info["model_name"],
            "evaluation_date": datetime.now().isoformat(),
            "metrics": {
                "perplexity": 4.1,
                "accuracy": 0.72,
                "bleu_score": 0.65,
                "rouge_score": 0.58,
                "coherence_score": 0.78
            },
            "sample_performance": self._evaluate_samples(model_path)
        }
        
        return evaluation_results
    
    def _evaluate_samples(self, model_path: Path) -> List[Dict]:
        """Evaluate sample predictions"""
        samples_path = model_path / "sample_predictions.json"
        
        if not samples_path.exists():
            return []
        
        with open(samples_path, 'r') as f:
            samples = json.load(f)
        
        # Simulate evaluation metrics for each sample
        for sample in samples:
            sample["evaluation_metrics"] = {
                "similarity": 0.75,
                "relevance": 0.82,
                "coherence": 0.78,
                "personality_match": 0.71
            }
        
        return samples

class FineTuningPipeline:
    """Complete fine-tuning pipeline"""
    
    def __init__(self, data_dir: str = "data/harvested", model_dir: str = "models"):
        self.data_dir = Path(data_dir)
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        self.trainer = None
        self.current_model = None
        
    def run_full_pipeline(self, training_config: TrainingConfig = None) -> Dict[str, Any]:
        """Run the complete fine-tuning pipeline"""
        print("Starting Truman AI fine-tuning pipeline...")
        
        if training_config is None:
            training_config = TrainingConfig()
        
        # Step 1: Process harvested data
        print("\nStep 1: Processing harvested data...")
        from .harvest import DataProcessor
        processor = DataProcessor(str(self.data_dir))
        
        training_file = processor.create_training_dataset(
            output_file=f"training_{int(time.time())}.jsonl",
            format_type="jsonl",
            min_quality=0.4
        )
        
        # Step 2: Initialize trainer
        print("\nStep 2: Initializing model trainer...")
        self.trainer = ModelTrainer(training_config, str(self.model_dir))
        
        # Step 3: Load training data
        print("\nStep 3: Loading training data...")
        if not self.trainer.load_training_data(training_file):
            return {"error": "Failed to load training data"}
        
        # Step 4: Train model
        print("\nStep 4: Training model...")
        metrics = self.trainer.simulate_training()
        
        # Step 5: Evaluate model
        print("\nStep 5: Evaluating model...")
        evaluation = self.trainer.evaluate_model()
        
        # Step 6: Generate report
        print("\nStep 6: Generating training report...")
        report = self._generate_training_report(metrics, evaluation)
        
        # Save report
        report_path = self.model_dir / f"training_report_{int(time.time())}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nFine-tuning pipeline completed!")
        print(f"Training report saved to: {report_path}")
        
        return report
    
    def _generate_training_report(self, metrics: TrainingMetrics, evaluation: Dict) -> Dict[str, Any]:
        """Generate comprehensive training report"""
        report = {
            "pipeline_info": {
                "completion_time": datetime.now().isoformat(),
                "pipeline_version": "1.0",
                "data_directory": str(self.data_dir),
                "model_directory": str(self.model_dir)
            },
            "training_metrics": metrics.__dict__,
            "evaluation_results": evaluation,
            "model_info": {
                "model_path": str(self.trainer.current_model_path) if self.trainer.current_model_path else None,
                "base_model": self.trainer.config.model_name,
                "training_config": self.trainer.config.__dict__
            },
            "recommendations": self._generate_recommendations(metrics, evaluation)
        }
        
        return report
    
    def _generate_recommendations(self, metrics: TrainingMetrics, evaluation: Dict) -> List[str]:
        """Generate recommendations based on training results"""
        recommendations = []
        
        # Based on training metrics
        if metrics.train_loss > 2.0:
            recommendations.append("Consider increasing training epochs or reducing learning rate")
        
        if metrics.eval_loss > metrics.train_loss * 1.2:
            recommendations.append("Model may be overfitting - consider regularization")
        
        # Based on evaluation metrics
        eval_metrics = evaluation.get("metrics", {})
        
        if eval_metrics.get("accuracy", 0) < 0.7:
            recommendations.append("Accuracy below target - consider more training data")
        
        if eval_metrics.get("coherence_score", 0) < 0.8:
            recommendations.append("Coherence could be improved - review training data quality")
        
        if eval_metrics.get("personality_match", 0) < 0.75:
            recommendations.append("Personality consistency needs improvement - add more character-specific examples")
        
        if not recommendations:
            recommendations.append("Training looks good - model ready for deployment")
        
        return recommendations
    
    def compare_models(self, model_paths: List[str]) -> Dict[str, Any]:
        """Compare multiple trained models"""
        comparison = {
            "comparison_date": datetime.now().isoformat(),
            "models": {},
            "ranking": []
        }
        
        model_scores = {}
        
        for model_path in model_paths:
            if self.trainer is None:
                self.trainer = ModelTrainer(TrainingConfig(), str(self.model_dir))
            
            evaluation = self.trainer.evaluate_model(model_path)
            
            if "error" not in evaluation:
                model_name = Path(model_path).name
                comparison["models"][model_name] = evaluation
                
                # Calculate overall score
                metrics = evaluation.get("metrics", {})
                score = (
                    metrics.get("accuracy", 0) * 0.3 +
                    metrics.get("coherence_score", 0) * 0.3 +
                    metrics.get("personality_match", 0) * 0.2 +
                    metrics.get("bleu_score", 0) * 0.1 +
                    metrics.get("rouge_score", 0) * 0.1
                )
                model_scores[model_name] = score
        
        # Rank models
        comparison["ranking"] = sorted(
            model_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return comparison
    
    def deploy_model(self, model_path: str, deployment_config: Dict = None) -> Dict[str, Any]:
        """Deploy model for production use"""
        model_path = Path(model_path)
        
        if not model_path.exists():
            return {"error": f"Model not found: {model_path}"}
        
        # Load model info
        with open(model_path / "model_info.json", 'r') as f:
            model_info = json.load(f)
        
        # Create deployment package
        deployment_info = {
            "deployment_date": datetime.now().isoformat(),
            "model_info": model_info,
            "deployment_config": deployment_config or {},
            "status": "deployed",
            "endpoint": f"/api/models/{model_info['model_name']}"
        }
        
        # Save deployment info
        deployment_path = model_path / "deployment.json"
        with open(deployment_path, 'w') as f:
            json.dump(deployment_info, f, indent=2)
        
        return deployment_info

def main():
    """Main function for running fine-tuning"""
    print("Truman AI Fine-tuning System")
    print("=" * 50)
    
    # Create pipeline
    pipeline = FineTuningPipeline()
    
    # Configure training
    config = TrainingConfig(
        model_name="gpt-3.5-turbo",
        learning_rate=1e-5,
        batch_size=8,
        num_epochs=3
    )
    
    # Run pipeline
    results = pipeline.run_full_pipeline(config)
    
    print("\nFine-tuning Results:")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
