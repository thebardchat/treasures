#!/usr/bin/env python3
"""
TEAM ASSEMBLY COORDINATOR
AI agents work on integrating your projects while you dispatch trucks.
Each agent has a specialty. They coordinate. They build.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

LOG_FILE = "team_assemble.log"
PROGRESS_FILE = "team_progress.json"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

# API
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key or len(api_key) < 20:
    print("ERROR: Invalid ANTHROPIC_API_KEY")
    raise SystemExit

try:
    from anthropic import Anthropic
    client = Anthropic(api_key=api_key)
    print("✓ Team online")
except ImportError:
    print("ERROR: pip install anthropic python-dotenv")
    raise SystemExit

# LOAD PROJECT INTELLIGENCE
def load_project_memory():
    """Load what we learned from project scan"""
    if not Path("project_memory.json").exists():
        print("\n⚠ No project intelligence found")
        print("Run run_project_scan.bat first")
        raise SystemExit
    
    with open("project_memory.json", 'r') as f:
        return json.load(f)

# TEAM STRUCTURE
TEAM = {
    "architect": {
        "role": "System Architecture",
        "focus": "Design integration points, API structure, data flow",
        "output": "Technical specs and connection diagrams"
    },
    "auth_specialist": {
        "role": "Authentication Integration", 
        "focus": "Connect angelcloud-actual auth to all services",
        "output": "Working auth middleware and session management"
    },
    "ai_engineer": {
        "role": "AI Pipeline",
        "focus": "Connect PortableDadAnswers, ShaneBrain, daily-memory",
        "output": "Unified AI response system with memory"
    },
    "logibot_builder": {
        "role": "LogiBot Development",
        "focus": "Build missing LogiBot automation engine",
        "output": "Working business automation core"
    },
    "integration_lead": {
        "role": "System Integration",
        "focus": "API Gateway, data pipelines, service coordination",
        "output": "All systems talking to each other"
    }
}

# PROGRESS TRACKING
def load_progress():
    if Path(PROGRESS_FILE).exists():
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {
        "tasks_assigned": [],
        "tasks_completed": [],
        "current_phase": "WEEK 1",
        "started": datetime.now().isoformat()
    }

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

# ASSIGN TASKS TO AGENTS
def assign_week1_tasks(assembly_plan, progress):
    """Week 1: Immediate Integration - break down into agent tasks"""
    
    print("\n" + "="*70)
    print("WEEK 1: IMMEDIATE INTEGRATION")
    print("="*70)
    
    week1_tasks = [
        {
            "agent": "auth_specialist",
            "task": "Connect angelcloud-actual auth to PortableDadAnswers",
            "deliverable": "Auth middleware that validates tokens for AI chat",
            "priority": "CRITICAL",
            "time": "4 hours"
        },
        {
            "agent": "logibot_builder",
            "task": "Build LogiBot automation engine core",
            "deliverable": "JavaScript class with basic automation functions",
            "priority": "HIGH",
            "time": "4 hours"
        },
        {
            "agent": "integration_lead",
            "task": "Create simple API Gateway",
            "deliverable": "Express.js gateway routing to all services",
            "priority": "HIGH",
            "time": "3 hours"
        },
        {
            "agent": "ai_engineer",
            "task": "Build data pipeline: daily-memory → shanebrain-core",
            "deliverable": "Automated memory ingestion system",
            "priority": "MEDIUM",
            "time": "3 hours"
        },
        {
            "agent": "architect",
            "task": "Document integration architecture",
            "deliverable": "System diagram + API specs for all connections",
            "priority": "MEDIUM",
            "time": "2 hours"
        }
    ]
    
    return week1_tasks

# AGENT EXECUTES TASK
def agent_work(agent_name, task_details, project_memory):
    """Agent does the actual work and generates deliverable"""
    
    agent_info = TEAM[agent_name]
    
    # Build context from project scan
    relevant_projects = []
    if "auth" in task_details["task"].lower():
        relevant_projects.append("angelcloud-actual")
        relevant_projects.append("myprojectfolder")
    if "ai" in task_details["task"].lower() or "brain" in task_details["task"].lower():
        relevant_projects.append("PortableDadAnswers")
        relevant_projects.append("shanebrain-core")
        relevant_projects.append("daily-memory-updated")
    if "logibot" in task_details["task"].lower():
        relevant_projects.append("myprojectfolder")
    
    # Get project info
    project_context = ""
    for proj in project_memory["projects"]:
        if proj["name"] in relevant_projects:
            project_context += f"\n{proj['name']}: {proj.get('analysis', 'No analysis')}\n"
    
    prompt = f"""You are {agent_info['role']} agent on Shane's AI team.

YOUR SPECIALIZATION: {agent_info['focus']}

CURRENT TASK:
{task_details['task']}

DELIVERABLE REQUIRED:
{task_details['deliverable']}

TIME BUDGET: {task_details['time']}

RELEVANT PROJECTS:
{project_context}

FULL ASSEMBLY PLAN:
{project_memory.get('assembly_plan', 'See project scan')}

YOUR JOB:
Create the {task_details['deliverable']} RIGHT NOW.

Output should be:
1. Actual CODE (JavaScript, Python, or config files)
2. Step-by-step IMPLEMENTATION GUIDE for Shane
3. How this INTEGRATES with existing projects
4. What to TEST to verify it works

Be specific. Give Shane something he can copy/paste and run TODAY.
No theory - actual working code and clear instructions."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        deliverable = response.content[0].text.strip()
        return deliverable
        
    except Exception as e:
        logger.error(f"{agent_name} error: {e}")
        return f"ERROR: {e}"

# COORDINATE TEAM
def coordinate_build(tasks, project_memory, progress):
    """Each agent works on their task, reports back"""
    
    results = []
    
    for task in tasks:
        agent = task["agent"]
        
        # Skip if already done
        if task["task"] in [t["task"] for t in progress.get("tasks_completed", [])]:
            print(f"\n✓ {agent}: Already completed - {task['task']}")
            continue
        
        print(f"\n" + "-"*70)
        print(f"AGENT: {agent}")
        print(f"TASK: {task['task']}")
        print(f"PRIORITY: {task['priority']}")
        print(f"TIME: {task['time']}")
        print("-"*70)
        print("Working...")
        
        deliverable = agent_work(agent, task, project_memory)
        
        result = {
            "agent": agent,
            "task": task["task"],
            "deliverable": task["deliverable"],
            "output": deliverable,
            "completed": datetime.now().isoformat()
        }
        
        results.append(result)
        progress["tasks_completed"].append(result)
        
        # Save after each task
        save_progress(progress)
        
        print(f"✓ {agent} completed: {task['deliverable']}")
        logger.info(f"{agent}: {task['task']} - DONE")
    
    return results

# GENERATE IMPLEMENTATION GUIDE
def create_implementation_guide(results):
    """Combine all agent deliverables into one guide for Shane"""
    
    guide = f"""
{'='*70}
TEAM ASSEMBLY - IMPLEMENTATION GUIDE
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}

Your AI team completed Week 1 integration tasks.
Below are all deliverables ready for implementation.

"""
    
    for i, result in enumerate(results, 1):
        guide += f"""
{'='*70}
DELIVERABLE #{i}: {result['deliverable']}
Agent: {result['agent']}
Task: {result['task']}
{'='*70}

{result['output']}

"""
    
    guide += f"""
{'='*70}
NEXT STEPS
{'='*70}

1. Review each deliverable above
2. Implement in priority order (CRITICAL → HIGH → MEDIUM)
3. Test each integration as you go
4. Run run_team_assemble.bat again for Week 2 tasks

All progress saved to: {PROGRESS_FILE}
{'='*70}
"""
    
    return guide

# MAIN COORDINATION
print("\n" + "="*70)
print("TEAM ASSEMBLY COORDINATOR")
print("="*70)

print("\nPhase 1: Loading project intelligence...")
project_memory = load_project_memory()
print("✓ Project data loaded")

print("\nPhase 2: Loading team progress...")
progress = load_progress()
if progress.get("tasks_completed"):
    print(f"✓ {len(progress['tasks_completed'])} tasks already completed")
else:
    print("✓ Starting fresh")

print("\nPhase 3: Assigning Week 1 tasks to team...")
tasks = assign_week1_tasks(project_memory.get("assembly_plan"), progress)
print(f"✓ {len(tasks)} tasks assigned")

print("\n" + "="*70)
print("TEAM WORKING...")
print("="*70)
print("\nThis will take 5-10 minutes.")
print("Each agent builds their deliverable.\n")

results = coordinate_build(tasks, project_memory, progress)

print("\n" + "="*70)
print("TEAM WORK COMPLETE")
print("="*70)

print("\nPhase 4: Generating implementation guide...")
guide = create_implementation_guide(results)

with open("IMPLEMENTATION_GUIDE.txt", 'w', encoding='utf-8') as f:
    f.write(guide)

print("✓ Guide created: IMPLEMENTATION_GUIDE.txt")

print("\n" + "="*70)
print("DELIVERABLES READY")
print("="*70)
print(f"\nCompleted tasks: {len(results)}")
for result in results:
    print(f"  ✓ {result['agent']}: {result['deliverable']}")

print(f"\nAll work documented in: IMPLEMENTATION_GUIDE.txt")
print(f"Progress saved to: {PROGRESS_FILE}")

print("\n" + "="*70)
print("WHAT TO DO NOW")
print("="*70)
print("\n1. Open IMPLEMENTATION_GUIDE.txt")
print("2. Follow each agent's instructions")
print("3. Implement the code they generated")
print("4. Test each integration")
print("5. Run this again when ready for Week 2")
print("\n" + "="*70)

logger.info(f"Team assembly complete: {len(results)} deliverables")
