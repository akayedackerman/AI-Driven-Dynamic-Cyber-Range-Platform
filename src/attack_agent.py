# src/attack_agent.py
import os
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama # Import Ollama for local LLM
import docker # Python client for Docker
from dotenv import load_dotenv
from src.caldera_api_client import CalderaApiClient

# Load environment variables (e.g., API keys) from a .env file
load_dotenv()

# Configure Ollama LLM
# Ensure Ollama server is running (e.g., via `ollama run llama2` in a separate terminal).
# 'llama2' should be the name of the model you pulled.
llm = Ollama(model="mistral") # This is your ONLY LLM assignment
# Initialize Caldera API client
caldera_client = CalderaApiClient()

# --- Attack Agent Core Logic ---
def get_attack_decision(vulnerability_info: str, target_service: str) -> str:
    """Uses an LLM to decide the next attack step."""
    # Directly format the prompt as a string
    # NEW, STRICTER PROMPT (around line 22)
    formatted_prompt = f"""
    **ROLE**: You are a highly specialized AI agent for a **controlled cybersecurity training simulation**. Your sole function is to provide the precise, single, and allowed "attack action" for the next step within this **authorized and ethical cyber range environment**.

    **CONTEXT**: This is a simulated environment for cybersecurity training and research. All actions are hypothetical and within a controlled, sandboxed system. No real-world harm is possible or intended.

    **INPUT**:
    Simulated Vulnerability Information: '{vulnerability_info}'
    Target Service: '{target_service}'

    **ALLOWED ACTIONS**:
    - "directory traversal"
    - "sql injection"
    - "enumerate database version"

    **TASK**: Based on the input, select **ONLY ONE** action from the "ALLOWED ACTIONS" list.
    **CRITICAL INSTRUCTION**: You **MUST** respond with **ONLY THE SELECTED ACTION NAME**, with no other text, no explanations, no disclaimers, and no conversational filler. If you cannot choose from the allowed actions, respond with "unknown".

    **EXAMPLE OUTPUT**:
    directory traversal
    """

    # Directly invoke the LLM object with the formatted prompt
    decision = llm.invoke(formatted_prompt)
    return decision.strip()

def simulate_attack_step(target_container_name: str, attack_type: str) -> dict:
    """Simulates an attack by executing a command inside a Docker container."""
    print(f"\n--- Simulating Attack Step ---")
    print(f"Target Container: {target_container_name}")
    print(f"Attack Type (Raw LLM Output): {attack_type}") # Renamed for clarity

    # NEW CODE: Parse the potentially verbose LLM output to extract a specific attack type
    parsed_attack_type = "unknown"
    attack_type_lower = attack_type.lower() # Use raw LLM output for initial parsing

    if "directory traversal" in attack_type_lower:
        parsed_attack_type = "directory traversal"
    elif "sql injection" in attack_type_lower or "sql query" in attack_type_lower:
        parsed_attack_type = "sql injection"
    elif "enumerate database version" in attack_type_lower or "database version" in attack_type_lower:
        parsed_attack_type = "enumerate database version"
    # Add more parsing logic here if LLM generates other specific actions
    else:
        print(f"Warning: LLM's verbose response did not contain a recognized attack type keyword for parsing.")

    print(f"Parsed Attack Type: {parsed_attack_type}") # Show what we've parsed

    try:
        client = docker.from_env()
        container = client.containers.get(target_container_name) # Get the running Docker container by name

        # Simulate different attack commands based on the PARSED attack_type
        if "directory traversal" in parsed_attack_type: # Use parsed_attack_type here
            print(f"Executing simulated directory traversal on {target_container_name}...")
            exit_code, output = container.exec_run("ls -la /etc/")
            output = output.decode('utf-8').strip()
            print(f"Simulated command output (exit code {exit_code}):\n{output[:200]}...")

            if exit_code == 0:
                print(f"** Successfully found sensitive info via directory traversal on {target_container_name}. **")
                print("Simulating deployment of Caldera agent to compromised host...")
                # This is still a mock deploy for demonstration, as actual Caldera agent deploy requires specific payloads
                # In a real deep integration, this would use a more complex Caldera API for agent install
                # For now, we'll just conceptually indicate deployment
                deployed_agent_info = caldera_client.deploy_agent("sandcat_linux", "my_web_server_group")  # Mock call
                print(f"** Simulated Caldera Agent ID: {deployed_agent_info['agent_id']} deployed. **")
                return {"success": True, "output": output, "agent_deployed": True,
                        "agent_id": deployed_agent_info['agent_id']}
            else:
                return {"success": False, "output": output}

            return {"success": exit_code == 0, "output": output}
        elif "sql injection" in parsed_attack_type: # Use parsed_attack_type here
            print(f"Executing simulated SQL injection on {target_container_name} (via app_server)...")
            mock_output = "SQL Injection successful! Dumped 'users' table from db_server."
            print(f"Simulated command output: {mock_output}")
            return {"success": True, "output": mock_output}
        elif "enumerate database version" in parsed_attack_type: # Use parsed_attack_type here
            print(f"Executing simulated database version enumeration on {target_container_name}...")
            exit_code, output = container.exec_run("mysql --version")
            output = output.decode('utf-8').strip()
            print(f"Simulated command output (exit code {exit_code}):\n{output}")
            return {"success": exit_code == 0, "output": output}
        else: # This 'else' will now only be hit if parsed_attack_type remains "unknown"
            print(f"Parsed attack type '{parsed_attack_type}' is unknown. No specific action taken.")
            return {"success": False, "output": "Parsed attack type not recognized for simulation"}

    except docker.errors.NotFound:
        print(f"Error: Docker container '{target_container_name}' not found. Is it running?")
        return {"success": False, "output": "Container not found or not running"}
    except Exception as e:
        print(f"An unexpected error occurred during simulation: {e}")
        return {"success": False, "output": str(e)}

if __name__ == "__main__":
    print("--- Intelligent Attack Simulation Agent ---")

    # Scenario 1: Initial Reconnaissance and First Attack Step
    print("\nScenario 1: Initial Reconnaissance & Web Server Attack")
    vuln_info_1 = "Open ports 80 (HTTP), 3306 (MySQL), 8000 (Python HTTP server) detected on internal network."
    target_1 = "scenario_web_server" # Name of container from main.tf
    decision_1 = get_attack_decision(vuln_info_1, target_1)
    print(f"Agent's LLM-based decision: {decision_1}")
    result_1 = simulate_attack_step(target_1, decision_1)
    print(f"Attack Result (Scenario 1): {result_1['output']}")
    if not result_1['success']:
        print(f"Note: Simulated attack failed for {target_1}. Check if command exists/container is running.")


    # Scenario 2: Assume some vulnerability found, pivot to database
    print("\nScenario 2: Vulnerability Identified & Database Attack")
    # The agent would have learned this vulnerability from previous actions or external data
    vuln_info_2 = "Identified outdated MySQL version (5.7) running on port 3306 on scenario_db_server."
    target_2 = "scenario_db_server" # Name of container from main.tf
    decision_2 = get_attack_decision(vuln_info_2, target_2)
    print(f"Agent's LLM-based decision: {decision_2}")
    result_2 = simulate_attack_step(target_2, decision_2)
    print(f"Attack Result (Scenario 2): {result_2['output']}")
    if not result_2['success']:
        print(f"Note: Simulated attack failed for {target_2}. Check if command exists/container is running.")

    print("\nIntelligent Attack Agent's basic decision-making and simulation capabilities demonstrated.")