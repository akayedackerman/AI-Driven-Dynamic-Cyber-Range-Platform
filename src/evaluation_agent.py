# src/evaluation_agent.py
import json
import os
from datetime import datetime
import time

LOG_FILE_PATH = "logs/cyber_range_events.log" # Path to your simulated log file

# --- Simulated Event Logging Function ---
def log_event(event_type: str, details: dict):
    """Logs a structured event to a file."""
    timestamp = datetime.now() # Store as datetime object temporarily
    log_entry = {
        "timestamp": timestamp.isoformat(), # Convert to string for JSON
        "event_type": event_type,
        "details": details
    }
    # Add specific timestamps to details for calculation later
    if event_type == "ANOMALY_DETECTED" or event_type == "DEFENSE_EXECUTED":
        log_entry["details"]["event_timestamp"] = timestamp.isoformat()
    with open(LOG_FILE_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    print(f"Logged event: {event_type}")

# src/evaluation_agent.py (Updated generate_evaluation_report)

# NEW: Skill mapping (based on NIST/NICE, simplified)
SKILL_MAPPING = {
    "Log Analysis": ["ANOMALY_DETECTED"],
    "Intrusion Detection": ["ANOMALY_DETECTED"],
    "Network Defense": ["block_ip", "isolate_host"],
    "Vulnerability Exploitation": ["ATTACK_SIMULATED"],
    "Incident Response": ["DEFENSE_EXECUTED"] # General response
}

def generate_evaluation_report(log_path: str) -> dict:
    """Generates a comprehensive evaluation report from event logs."""
    print(f"\n--- Generating Evaluation Report from: {log_path} ---")
    successful_attacks = 0
    failed_attacks = 0
    anomalies_detected = 0
    defenses_triggered = 0

    # For time-based metrics
    attack_timestamps = {} # {attack_id: timestamp}
    anomaly_timestamps = {} # {anomaly_id: timestamp}
    defense_timestamps = {} # {anomaly_id: timestamp of defense}
    time_to_detect_sum_seconds = 0
    time_to_remediate_sum_seconds = 0
    detected_attacks_count = 0
    remediated_attacks_count = 0

    # For skill profiling
    skill_activity = {skill: {"demonstrated": 0, "total_attempts": 0} for skill in SKILL_MAPPING.keys()}

    if not os.path.exists(log_path):
        print(f"Error: Log file not found at {log_path}. Cannot generate report.")
        return {}

    with open(log_path, "r") as f:
        for line in f:
            try:
                event = json.loads(line)
                event_type = event.get("event_type")
                details = event.get("details", {})
                event_timestamp_str = details.get("event_timestamp") or event.get("timestamp") # Use details timestamp if present
                event_dt = datetime.fromisoformat(event_timestamp_str) if event_timestamp_str else None

                if event_type == "ATTACK_SIMULATED":
                    successful_attacks += 1 if details.get("success") else 0
                    failed_attacks += 1 if not details.get("success") else 0
                    # Assign unique ID to track attack for detection time calculation
                    attack_id = f"attack_{successful_attacks + failed_attacks}"
                    attack_timestamps[attack_id] = event_dt
                    # Update skill
                    skill_activity["Vulnerability Exploitation"]["total_attempts"] += 1
                    if details.get("success"):
                        skill_activity["Vulnerability Exploitation"]["demonstrated"] += 1

                elif event_type == "ANOMALY_DETECTED":
                    anomalies_detected += 1
                    # Assign unique ID to link anomaly to potential attack for detection time
                    # For simplicity, let's link to the *last* attack simulated
                    last_attack_id = f"attack_{successful_attacks + failed_attacks}" # This is simplistic, would need real correlation
                    anomaly_timestamps[last_attack_id] = event_dt # Store time of anomaly detection
                    detected_attacks_count += 1
                    # Update skills
                    skill_activity["Log Analysis"]["demonstrated"] += 1
                    skill_activity["Log Analysis"]["total_attempts"] += 1
                    skill_activity["Intrusion Detection"]["demonstrated"] += 1
                    skill_activity["Intrusion Detection"]["total_attempts"] += 1


                elif event_type == "DEFENSE_EXECUTED":
                    defenses_triggered += 1
                    # Link defense to the anomaly it's responding to
                    last_attack_id = f"attack_{successful_attacks + failed_attacks}" # Simplistic correlation
                    defense_timestamps[last_attack_id] = event_dt # Store time of defense execution
                    remediated_attacks_count += 1
                    # Update skill for Incident Response
                    skill_activity["Incident Response"]["demonstrated"] += 1
                    skill_activity["Incident Response"]["total_attempts"] += 1
                    # Update Network Defense if relevant action was successful
                    if details.get("action_details", {}).get("success"):
                        if "block_ip" in details.get("action_details", {}).get("action", "").lower() or \
                           "isolate_host" in details.get("action_details", {}).get("action", "").lower():
                            skill_activity["Network Defense"]["demonstrated"] += 1
                    skill_activity["Network Defense"]["total_attempts"] += 1


            except json.JSONDecodeError as e:
                print(f"Warning: Could not parse log line: {line.strip()} - {e}")
            except Exception as e:
                print(f"Warning: Error processing event: {event.get('event_type')} - {e}")

    # Calculate time-based metrics
    for attack_id, attack_dt in attack_timestamps.items():
        if attack_id in anomaly_timestamps:
            time_to_detect_sum_seconds += (anomaly_timestamps[attack_id] - attack_dt).total_seconds()
        if attack_id in defense_timestamps:
            # If defense happened after anomaly, calc remediation time from anomaly detection
            if attack_id in anomaly_timestamps and defense_timestamps[attack_id] > anomaly_timestamps[attack_id]:
                time_to_remediate_sum_seconds += (defense_timestamps[attack_id] - anomaly_timestamps[attack_id]).total_seconds()
            # If defense happened without an explicit anomaly_detected (direct response)
            else:
                 time_to_remediate_sum_seconds += (defense_timestamps[attack_id] - attack_dt).total_seconds() # Remediate from attack start

    avg_time_to_detect = (time_to_detect_sum_seconds / detected_attacks_count) if detected_attacks_count > 0 else 0
    avg_time_to_remediate = (time_to_remediate_sum_seconds / remediated_attacks_count) if remediated_attacks_count > 0 else 0


    # Final skill percentages
    skill_profiles = {}
    for skill, data in skill_activity.items():
        skill_profiles[skill] = {
            "demonstrated_count": data["demonstrated"],
            "total_attempts": data["total_attempts"],
            "percentage": (data["demonstrated"] / data["total_attempts"]) * 100 if data["total_attempts"] > 0 else 0
        }

    report = {
        "summary": {
            "total_attacks_attempted": successful_attacks + failed_attacks,
            "successful_attacks": successful_attacks,
            "failed_attacks": failed_attacks,
            "anomalies_detected": anomalies_detected,
            "defenses_triggered": defenses_triggered,
            "avg_time_to_detect_seconds": f"{avg_time_to_detect:.2f}",
            "avg_time_to_remediate_seconds": f"{avg_time_to_remediate:.2f}"
        },
        "skill_profiles": skill_profiles
    }
    return report

if __name__ == "__main__":
    # --- Simulate an Exercise Session for logging ---
    # Ensure the logs directory exists
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    # Clear previous logs for a fresh simulation
    if os.path.exists(LOG_FILE_PATH):
        os.remove(LOG_FILE_PATH)

    print("--- Simulating Cyber Range Session for Logging ---")

    # Simulate Attack Agent actions
    log_event("ATTACK_SIMULATED", {"attack_type": "directory_traversal", "target": "web_server", "success": True, "output": "found /etc/passwd"})
    time.sleep(0.5)
    log_event("ATTACK_SIMULATED", {"attack_type": "sql_injection", "target": "db_server", "success": False, "output": "connection refused"})
    time.sleep(0.5)

    # Simulate Defense Agent actions
    log_event("ANOMALY_DETECTED", {"type": "failed_login", "source_ip": "10.0.0.5"})
    time.sleep(0.5)
    log_event("DEFENSE_EXECUTED", {"action": "block_ip", "target": "10.0.0.5", "success": True, "reason": "repeated failed login"})
    time.sleep(0.5)
    log_event("ANOMALY_DETECTED", {"type": "data_exfil_attempt", "source_host": "compromised_server"})
    time.sleep(0.5)
    log_event("DEFENSE_EXECUTED", {"action": "isolate_host", "target": "compromised_server", "success": True, "reason": "data exfiltration attempt"})

    print("\n--- Exercise Simulation Logs Generated ---")

    # --- Generate Evaluation Report ---
    report = generate_evaluation_report(LOG_FILE_PATH)
    if report:
        print("\n--- Comprehensive Evaluation Report ---")
        print(json.dumps(report["summary"], indent=4))
        print("\n--- Participant Skill Profiles ---")
        for skill, data in report["skill_profiles"].items():
            print(f"  {skill}: {data['percentage']:.2f}% demonstrated (total attempts: {data['total']})")
        print("\n--- Actionable Guidance (Conceptual) ---")
        if report["summary"]["failed_attacks"] > 0:
            print("- Review logs for patterns in failed attacks to improve reconnaissance.")
        if report["skill_profiles"]["Network Defense"]["percentage"] < 100 and report["skill_profiles"]["Network Defense"]["total"] > 0:
            print("- Focus on network defense techniques, especially firewall rule management.")
        if report["skill_profiles"]["Vulnerability Exploitation"]["percentage"] < 100 and report["skill_profiles"]["Vulnerability Exploitation"]["total"] > 0:
            print("- Research advanced exploitation techniques for databases and web applications.")
    else:
        print("Report could not be generated.")

    print("\nAutomated Exercise Evaluation capabilities demonstrated.")