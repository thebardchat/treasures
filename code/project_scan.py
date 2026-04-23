#!/usr/bin/env python3
"""
PROJECT SCANNER
Look at local project folders. Understand what Shane is building.
Build unified memory. Generate assembly plan.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

LOG_FILE = "project_scan.log"
PROJECT_MEMORY = "project_memory.json"

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
    print("✓ API ready")
except ImportError:
    print("ERROR: pip install anthropic python-dotenv")
    raise SystemExit

# PROJECT FOLDERS - Shane's actual work locations
PROJECT_FOLDERS = [
    # Desktop - Active projects
    r"C:\Users\Shane\Desktop\angelcloud-actual",
    r"C:\Users\Shane\Desktop\angel-cloud-main",
    r"C:\Users\Shane\Desktop\shanebrain-core",
    r"C:\Users\Shane\Desktop\myprojectfolder",
    r"C:\Users\Shane\Desktop\cmd-fast-balance-for-coding",
    r"C:\Users\Shane\Desktop\coach-corner",
    r"C:\Users\Shane\Desktop\PortableDadAnswers",
    r"C:\Users\Shane\Desktop\ScreenRec_app",
    
    # Documents - Development stuff
    r"C:\Users\Shane\Documents\shanebrainlangxtra",
    r"C:\Users\Shane\Documents\GitHub",
    
    # Downloads - Active deployable versions (ignoring .zip backups)
    r"C:\Users\Shane\Downloads\angel-cloud-main",
    r"C:\Users\Shane\Downloads\deployable_angel_cloud_app",
    r"C:\Users\Shane\Downloads\daily-memory-updated",
]

print("\n" + "="*70)
print("PROJECT SCANNER")
print("="*70)
print("\nConfigured project folders:")
for folder in PROJECT_FOLDERS:
    exists = "✓" if Path(folder).exists() else "✗"
    print(f"  {exists} {folder}")

print("\n" + "-"*70)
response = input("\nAre these correct? (y/n): ").strip().lower()

if response != 'y':
    print("\nEdit PROJECT_FOLDERS in project_scan.py to match your actual paths")
    print("Example: r'C:\\Users\\Shane\\Documents\\ShaneBrain'")
    raise SystemExit

# SCAN PROJECT STRUCTURE
def scan_project_folder(folder_path):
    """Get structure and key files from a project folder"""
    
    project = {
        "path": str(folder_path),
        "name": folder_path.name,
        "files": [],
        "structure": {},
        "code_files": [],
        "doc_files": [],
        "config_files": []
    }
    
    try:
        # Get all files
        for filepath in folder_path.rglob("*"):
            if filepath.is_file() and not filepath.name.startswith('.'):
                # Skip binaries
                if filepath.suffix in ['.exe', '.dll', '.bin', '.pyc', '.zip']:
                    continue
                
                rel_path = filepath.relative_to(folder_path)
                file_info = {
                    "path": str(rel_path),
                    "name": filepath.name,
                    "suffix": filepath.suffix,
                    "size": filepath.stat().st_size
                }
                
                project["files"].append(file_info)
                
                # Categorize
                if filepath.suffix in ['.py', '.js', '.html', '.css', '.bat', '.sh']:
                    project["code_files"].append(str(rel_path))
                elif filepath.suffix in ['.md', '.txt', '.doc', '.docx', '.pdf']:
                    project["doc_files"].append(str(rel_path))
                elif filepath.suffix in ['.json', '.yaml', '.yml', '.env', '.config']:
                    project["config_files"].append(str(rel_path))
        
        # Build structure tree
        for file_info in project["files"]:
            parts = Path(file_info["path"]).parts
            current = project["structure"]
            for part in parts[:-1]:  # Folders
                if part not in current:
                    current[part] = {}
                current = current[part]
    
    except Exception as e:
        logger.error(f"Scan error for {folder_path}: {e}")
    
    return project

# UNDERSTAND PROJECT PURPOSE
def analyze_project(project):
    """Claude analyzes what this project is for"""
    
    # Build file summary
    file_summary = f"""
Project: {project['name']}
Total files: {len(project['files'])}
Code files: {len(project['code_files'])}
Docs: {len(project['doc_files'])}
Config: {len(project['config_files'])}

Key files:
"""
    
    # List important files
    for f in project['code_files'][:10]:
        file_summary += f"  - {f}\n"
    
    for f in project['doc_files'][:5]:
        file_summary += f"  - {f}\n"
    
    # Read a few key files for context
    sample_content = ""
    folder_path = Path(project['path'])
    
    for filename in ['README.md', 'readme.md', 'README.txt', project['name'] + '.py']:
        file_path = folder_path / filename
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()[:1000]
                    sample_content += f"\n{filename}:\n{content}\n"
                    break
            except:
                pass
    
    prompt = f"""Analyze this project:

{file_summary}

Sample content:
{sample_content if sample_content else '(No README found)'}

Answer:
1. What is this project? (one sentence)
2. Current status? (working/in-progress/abandoned/unclear)
3. What does it DO? (specific function)
4. How does it fit Shane's goals? (Angel Cloud, ShaneBrain, LogiBot, family income)

Be specific. Direct. No fluff."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        
        analysis = response.content[0].text.strip()
        return analysis
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return "Analysis failed"

# FIND CONNECTIONS
def find_project_connections(projects):
    """How do these projects connect to each other?"""
    
    # Build summary
    summary = "PROJECTS FOUND:\n\n"
    for proj in projects:
        summary += f"{proj['name']}: {proj['analysis']}\n\n"
    
    prompt = f"""{summary}

These are Shane's active projects. Analyze:

1. How do they connect? (which projects depend on others)
2. What's the integration path? (how they should work together)
3. What's missing? (gaps in the system)
4. What should be built NEXT? (priority order)

Shane's goals:
- Angel Cloud: Mental wellness platform for 800M Windows users
- ShaneBrain: Digital legacy system (his consciousness preserved)
- LogiBot: Autonomous business automation
- Family income: Monetizable solutions

Be SPECIFIC about integration points and next steps."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )
        
        connections = response.content[0].text.strip()
        return connections
        
    except Exception as e:
        logger.error(f"Connection analysis error: {e}")
        return "Analysis failed"

# GENERATE ASSEMBLY PLAN
def generate_assembly_plan(projects, connections):
    """Create step-by-step plan to assemble everything"""
    
    prompt = f"""Based on Shane's projects and how they connect:

{connections}

Create a 30-day assembly plan:

WEEK 1: [Immediate integration tasks]
WEEK 2: [Build missing pieces]
WEEK 3: [Test and refine]
WEEK 4: [Launch and monetize]

Each week should have 3-5 SPECIFIC tasks.
Each task must be:
- Completable in 2-4 hours
- Builds on previous tasks
- Moves toward working product

End with: FIRST REVENUE TARGET (what, when, how much)"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        plan = response.content[0].text.strip()
        return plan
        
    except Exception as e:
        logger.error(f"Plan generation error: {e}")
        return "Plan generation failed"

# MAIN SCAN
print("\n" + "="*70)
print("SCANNING PROJECTS")
print("="*70)

projects = []
for folder_path_str in PROJECT_FOLDERS:
    folder_path = Path(folder_path_str)
    if not folder_path.exists():
        print(f"\n⚠ Skipping: {folder_path} (not found)")
        continue
    
    print(f"\nScanning: {folder_path.name}")
    project = scan_project_folder(folder_path)
    print(f"  ✓ Found {len(project['files'])} files")
    
    print(f"  Analyzing purpose...")
    project['analysis'] = analyze_project(project)
    print(f"  ✓ Analysis complete")
    
    projects.append(project)
    logger.info(f"Scanned {folder_path.name}: {len(project['files'])} files")

if not projects:
    print("\n⚠ No projects found")
    print("Edit PROJECT_FOLDERS in project_scan.py")
    raise SystemExit

print("\n" + "="*70)
print("PROJECT ANALYSIS")
print("="*70)

for proj in projects:
    print(f"\n{proj['name']}:")
    print("-" * 50)
    print(proj['analysis'])

print("\n" + "="*70)
print("FINDING CONNECTIONS")
print("="*70)

connections = find_project_connections(projects)
print(f"\n{connections}")

print("\n" + "="*70)
print("GENERATING ASSEMBLY PLAN")
print("="*70)

assembly_plan = generate_assembly_plan(projects, connections)
print(f"\n{assembly_plan}")

# SAVE EVERYTHING
project_memory = {
    "scan_time": datetime.now().isoformat(),
    "projects": projects,
    "connections": connections,
    "assembly_plan": assembly_plan
}

with open(PROJECT_MEMORY, 'w') as f:
    json.dump(project_memory, f, indent=2)

# CREATE READABLE REPORT
report = f"""
{'='*70}
PROJECT INTELLIGENCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}

PROJECTS SCANNED
{'-'*70}
"""

for proj in projects:
    report += f"""
{proj['name']}
  Location: {proj['path']}
  Files: {len(proj['files'])}
  Code: {len(proj['code_files'])} | Docs: {len(proj['doc_files'])} | Config: {len(proj['config_files'])}
  
  {proj['analysis']}
"""

report += f"""
{'='*70}
PROJECT CONNECTIONS
{'='*70}

{connections}

{'='*70}
30-DAY ASSEMBLY PLAN
{'='*70}

{assembly_plan}

{'='*70}
NEXT STEPS
{'='*70}

1. Review this plan
2. Run run_project_assemble.bat (will be generated next)
3. System will guide you through each integration step
4. Memory builds across all sessions

All data saved to: {PROJECT_MEMORY}
{'='*70}
"""

with open("PROJECT_REPORT.txt", 'w') as f:
    f.write(report)

print("\n" + "="*70)
print("SCAN COMPLETE")
print("="*70)
print(f"\nFiles created:")
print(f"  ✓ {PROJECT_MEMORY}")
print(f"  ✓ PROJECT_REPORT.txt")
print(f"\nReview PROJECT_REPORT.txt for full analysis")
print(f"\nReady to generate assembly system...")
print("="*70)

logger.info(f"Scan complete: {len(projects)} projects analyzed")
