"""
Tiny Essay Writer Demo - CrewAI + MLflow + Kubeflow Pipeline
"""

from crewai import Agent, Task, Crew
import mlflow
import time
from kfp import dsl, compiler
from typing import Dict

# Kubeflow Components
@dsl.component
def create_essay_with_crewai(topic: str) -> Dict:
    """Kubeflow component that uses CrewAI to write essays"""
    
    from crewai import Agent, Task, Crew
    import time
    
    # Create agents
    writer_agent = Agent(
        role="Essay Writer",
        goal="Write high-quality essays on any topic",
        backstory="Expert writer with years of experience",
        verbose=True
    )
    
    checker_agent = Agent(
        role="Quality Checker", 
        goal="Evaluate and score essays",
        backstory="Experienced editor who scores writing quality",
        verbose=True
    )
    
    # Create tasks
    writing_task = Task(
        description=f"Write a 300-word essay about '{topic}' with intro, body, conclusion.",
        agent=writer_agent,
        expected_output="Complete structured essay"
    )
    
    evaluation_task = Task(
        description="Score the essay 1-10 and give brief feedback.",
        agent=checker_agent, 
        expected_output="Score and feedback"
    )
    
    # Run crew
    start_time = time.time()
    crew = Crew(agents=[writer_agent, checker_agent], tasks=[writing_task, evaluation_task])
    results = crew.kickoff()
    writing_time = time.time() - start_time
    
    # Parse results
    essay = results[0] if len(results) > 0 else "No essay"
    evaluation = results[1] if len(results) > 1 else "No evaluation"
    
    # Extract score
    score = 7.0
    try:
        import re
        match = re.search(r'(\d+(?:\.\d+)?)', evaluation)
        if match:
            score = float(match.group(1))
            if score > 10:
                score = score / 10  # Handle cases like "75" meaning 7.5
    except:
        pass
    
    return {
        "topic": topic,
        "essay": essay,
        "evaluation": evaluation, 
        "score": min(score, 10.0),
        "writing_time": writing_time,
        "word_count": len(essay.split())
    }

@dsl.component
def log_to_mlflow(essay_data: Dict, experiment_name: str) -> str:
    """Kubeflow component to log results to MLflow"""
    
    import mlflow
    
    mlflow.set_experiment(experiment_name)
    
    with mlflow.start_run() as run:
        # Log parameters
        mlflow.log_params({
            "topic": essay_data["topic"],
            "agent_pipeline": "crewai_kubeflow"
        })
        
        # Log metrics
        mlflow.log_metrics({
            "essay_score": essay_data["score"],
            "writing_time_sec": essay_data["writing_time"],
            "word_count": essay_data["word_count"]
        })
        
        # Save essay
        with open("essay.txt", "w") as f:
            f.write(f"Topic: {essay_data['topic']}\n\n{essay_data['essay']}")
        mlflow.log_artifact("essay.txt")
        
        return run.info.run_id

# Kubeflow Pipeline
@dsl.pipeline
def essay_writer_pipeline(
    topic: str = "Benefits of reading",
    experiment_name: str = "Kubeflow_Essay_Demo"
) -> str:
    """Simple Kubeflow pipeline for essay writing with CrewAI"""
    
    # Step 1: Write essay with CrewAI
    essay_task = create_essay_with_crewai(topic=topic)
    
    # Step 2: Log to MLflow
    mlflow_task = log_to_mlflow(
        essay_data=essay_task.output,
        experiment_name=experiment_name
    )
    
    return mlflow_task.output

# Demo runner (non-Kubeflow for quick testing)
class QuickDemo:
    def __init__(self):
        mlflow.set_experiment("Quick_Essay_Demo")
        
    def run_single_essay(self, topic: str):
        """Quick test without Kubeflow"""
        print(f"🚀 Quick test: {topic}")
        
        # Use the same logic as Kubeflow component
        from crewai import Agent, Task, Crew
        
        writer = Agent(
            role="Essay Writer",
            goal="Write essays",
            backstory="Experienced writer"
        )
        
        task = Task(
            description=f"Write a short essay about '{topic}'",
            agent=writer,
            expected_output="Complete essay"
        )
        
        crew = Crew(agents=[writer], tasks=[task])
        result = crew.kickoff()
        
        # Log to MLflow
        with mlflow.start_run() as run:
            mlflow.log_params({"topic": topic, "mode": "quick_test"})
            mlflow.log_metrics({"word_count": len(str(result).split())})
            
            print(f"✅ Essay created: {len(str(result).split())} words")
            print(f"📊 MLflow run: {run.info.run_id}")
            
        return result

def compile_pipeline():
    """Compile the Kubeflow pipeline"""
    compiler.Compiler().compile(essay_writer_pipeline, 'essay_pipeline.yaml')
    print("✅ Pipeline compiled to essay_pipeline.yaml")

def run_quick_demo():
    """Run quick demo without Kubeflow"""
    print("🎓 Quick Essay Demo (No Kubeflow)")
    print("=" * 40)
    
    demo = QuickDemo()
    topics = ["Benefits of exercise", "Impact of technology"]
    
    for topic in topics:
        try:
            demo.run_single_essay(topic)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("🎉 Quick demo done!")

if __name__ == "__main__":
    print("Choose option:")
    print("1. Compile Kubeflow pipeline")
    print("2. Run quick demo")
    
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "1":
        compile_pipeline()
    else:
        run_quick_demo()