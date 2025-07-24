# main_orchestrator.py
import time
import subprocess
import os
import random
import json
from src.scenario_content_gen import generate_phishing_email, generate_malicious_website_html
from src.environment_manager import simulate_env_adjustment
from src.attack_agent import get_attack_decision, simulate_attack_step
from src.defense_agent import analyze_log_entry, execute_automated_response, SUSPICIOUS_KEYWORDS
from src.evaluation_agent import log_event, generate_evaluation_report, LOG_FILE_PATH

# Ensure logs directory exists for evaluation_agent
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

def run_cyber_range_exercise(duration_seconds=10):
    print("\n==============================================")
    print("=== Starting AI-Driven Cyber Range Exercise ===")
    print("==============================================\n")

    # --- 1. Dynamic Scenario Generation (Initial Setup) ---
    print("--- PHASE 1: Scenario Setup & Environment Provisioning ---")
    # Ensure Docker containers are up (re-apply Terraform if needed)
    print("Ensuring scenario containers are up-to-date via Terraform...")
    # This would ideally be an API call to a Terraform automation backend,
    # but for simulation, we'll re-run apply command.
    # subprocess.run(["terraform", "apply", "--auto-approve"], cwd="iac/", check=True) # Uncomment for actual run
    print("Scenario environment (Docker containers) provisioned/verified.")

    # Generate initial scenario content
    scenario_topic = "Phishing Campaign - Financial Fraud"
    phishing_email = generate_phishing_email("Jane Doe", "Acme Bank", scenario_topic)
    malicious_site = generate_malicious_website_html(scenario_topic, "bank_login")
    print(f"Generated scenario content: Email Subject='{phishing_email['subject']}', Malicious URL='{malicious_site['url']}'")
    log_event("SCENARIO_GENERATED", {"topic": scenario_topic, "email_link": phishing_email['link'], "website_url": malicious_site['url']})
    time.sleep(1)

    print("\n--- PHASE 2: Attack & Defense Cycle ---")
    start_time = time.time()
    current_time = start_time
    attack_counter = 0
    defense_counter = 0

    # Simulate a continuous attack-defense loop
    while (current_time - start_time) < duration_seconds:
        print(f"\n--- Current Time: {int(current_time - start_time)}s / {duration_seconds}s ---")

        # --- Intelligent Attack Simulation ---
        attack_counter += 1
        print(f"ATTACK AGENT (Cycle {attack_counter}): Deciding next step...")
        current_vulnerability_info = f"Scanned scenario_web_server, found port 80 open and Nginx."
        if attack_counter % 2 == 0: # Alternate attack targets
            current_vulnerability_info = f"Scanned scenario_db_server, found port 3306 open and MySQL."
            target_container = "scenario_db_server"
        else:
            target_container = "scenario_web_server"

        attack_decision = get_attack_decision(current_vulnerability_info, target_container)
        log_event("ATTACK_DECISION", {"decision": attack_decision, "target": target_container})
        time.sleep(0.5)

        attack_result = simulate_attack_step(target_container, attack_decision)
        log_event("ATTACK_SIMULATED", {"attack_type": attack_decision, "target": target_container, "success": attack_result['success'], "output": attack_result['output']})
        if not attack_result['success']:
            print(f"Attack failed for {target_container}. Adjusting strategy.")
            # Simulate dynamic environment adjustment (feedback loop: Attack -> Scenario Gen)
            simulate_env_adjustment("DEFENDER_WEAKNESS_IDENTIFIED", {"skill_gap": "Attack Resilience"}) # Conceptual
        else:
            print(f"Attack succeeded for {target_container}. Proceeding.")
        time.sleep(1)

        # --- Adaptive Defense Decision-Making ---
        defense_counter += 1
        print(f"DEFENSE AGENT (Cycle {defense_counter}): Analyzing logs...")
        # Simulate receiving a new log entry
        mock_log_entry = random.choice([
            f"[INFO] User bob logged in successfully from 192.168.1.100.",  # Normal
            f"[ALERT] Multiple failed login attempts from 10.0.0.{random.randint(1, 255)} for user 'root'!",  # Rule 2
            f"[CRITICAL] Unauthorized file access detected on scenario_web_server for sensitive.conf!",  # Rule 3
            f"[WARNING] Unusual process 'nc -lvp 4444' started on scenario_app_server.",  # Keyword match
            f"[ERROR] Service 'web_db_api' crashed due to segmentation fault."  # Potential anomaly
        ])
        log_event("RAW_LOG_ENTRY", {"log": mock_log_entry}) # Log raw input for defense

        is_anomaly = analyze_log_entry(mock_log_entry)
        if is_anomaly:
            print("Anomaly detected by Defense Agent. Triggering response.")
            log_event("ANOMALY_DETECTED", {"log_entry": mock_log_entry})

            response_details = {}
            if "failed login" in mock_log_entry.lower():
                response_details = {"response_type": "block_ip", "target": "10.0.0.5", "reason": "failed login attempts"}
            elif "unauthorized file access" in mock_log_entry.lower():
                response_details = {"response_type": "isolate_host", "target": "scenario_web_server", "reason": "unauthorized access"}
            else: # Default for other anomalies
                response_details = {"response_type": "review_alert", "target": "unknown", "reason": "unspecified anomaly"}

            defense_result = execute_automated_response(response_details)
            log_event("DEFENSE_EXECUTED", {"action_details": defense_result})

            if defense_result['success'] and "block_ip" in defense_result['action'].lower():
                # Simulate dynamic environment adjustment (feedback loop: Defense -> Scenario Gen)
                simulate_env_adjustment("ATTACK_BLOCKED", {"attacker_ip": defense_result['target']})
            else:
                simulate_env_adjustment("ATTACK_DETECTED", {"details": "Failed to fully mitigate."})
        else:
            print("No anomaly detected by Defense Agent.")
        time.sleep(1)

        current_time = time.time()
        if (current_time - start_time) < duration_seconds:
            time.sleep(0.5) # Short pause before next cycle

    print("\n--- Exercise Cycle Concluded ---")

    # --- 3. Automated Exercise Evaluation (Final Report) ---
    print("\n--- PHASE 3: Generating Final Evaluation Report ---")
    final_report = generate_evaluation_report(LOG_FILE_PATH)

    if final_report:
        print("\n========================================")
        print("=== FINAL CYBER RANGE EXERCISE REPORT ===")
        print("========================================\n")
        print("--- Summary ---")
        print(json.dumps(final_report["summary"], indent=4))
        print("\n--- Participant Skill Profiles ---")
        for skill, data in final_report["skill_profiles"].items():
            print(f"  {skill}: {data['percentage']:.2f}% demonstrated (total attempts: {data['total_attempts']})")
        print("\n--- Actionable Guidance ---")
        if final_report["summary"]["failed_attacks"] > 0:
            print("- Review logs for patterns in failed attacks to improve reconnaissance.")
        if final_report["skill_profiles"]["Network Defense"]["percentage"] < 100 and final_report["skill_profiles"]["Network Defense"]["total_attempts"] > 0:
            print("- Focus on network defense techniques, especially firewall rule management.")
        if final_report["skill_profiles"]["Vulnerability Exploitation"]["percentage"] < 100 and final_report["skill_profiles"]["Vulnerability Exploitation"]["total_attempts"] > 0:
            print("- Research advanced exploitation techniques for databases and web applications.")
    else:
        print("Error: Final report could not be generated.")

    print("\n==============================================")
    print("=== AI-Driven Cyber Range Exercise Finished ===")
    print("==============================================\n")

if __name__ == "__main__":
    # Ensure CALDERA and Docker containers are running before starting!
    # Example: docker ps
    #          Check CALDERA terminal
    # If you want to use the actual Terraform apply:
    # Uncomment the subprocess.run line in the function above:
    # subprocess.run(["terraform", "apply", "--auto-approve"], cwd="iac/", check=True)

    run_cyber_range_exercise(duration_seconds=10) # Run for 10 seconds of simulated time