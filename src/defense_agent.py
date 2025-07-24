# src/defense_agent.py
import time
import random
import docker
import re # For simple pattern matching in logs

# --- Mock Baseline for Normal Activity (simplified for this example) ---
# In a real system, this would be learned from historical data.
NORMAL_LOG_PATTERNS = [
    r"\[INFO\] User \w+ logged in successfully",
    r"\[DEBUG\] Process \d+ started",
    r"\[HTTP\] GET /index.html 200",
]
SUSPICIOUS_KEYWORDS = [
    "failed login", "error 401", "connection refused", "unauthorized",
    "malware", "exploit", "shell", "privilege escalation", "suspicious"
]

# --- Defense Agent Logic ---
# src/defense_agent.py (Updated analyze_log_entry)
# --- Mock Baseline for Normal Activity (simplified for this example) ---
# In a real system, this would be learned from historical data.
NORMAL_LOG_PATTERNS = [
    r"\[INFO\] User \w+ logged in successfully",
    r"\[DEBUG\] Process \d+ started",
    r"\[HTTP\] GET /index.html 200",
    r"\[CRITICAL\] Unauthorized file access detected on scenario_web_server for sensitive.conf!" # Added for testing specific scenario
]
SUSPICIOUS_KEYWORDS = [
    "failed login", "error 401", "connection refused", "unauthorized",
    "malware", "exploit", "shell", "privilege escalation", "suspicious"
]

# Simple Rule-Based Anomaly Detection Function
def analyze_log_entry(log_entry: str) -> bool:
    """Simulates behavioral analytics to detect anomalies using rules."""
    log_entry_lower = log_entry.lower()
    print(f"\n--- Analyzing Log Entry ---")
    print(f"Log: '{log_entry.strip()}'")

    # Rule 1: Direct Suspicious Keyword Match
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in log_entry_lower:
            print(f"--> Rule: Suspicious keyword '{keyword}' found. ANOMALY DETECTED.")
            return True

    # Rule 2: Multiple Failed Logins from Same IP (requires state, mock for now)
    # This would require maintaining state of IPs/failures. For a simple demo,
    # we'll look for pattern implying multiple failures.
    if "multiple failed login attempts" in log_entry_lower and "root" in log_entry_lower:
        print("--> Rule: Pattern 'multiple failed login attempts for root' found. ANOMALY DETECTED.")
        return True

    # Rule 3: Unexpected File Access (based on a known sensitive file)
    if "unauthorized file access detected" in log_entry_lower and "sensitive.conf" in log_entry_lower:
        print("--> Rule: Pattern 'unauthorized file access for sensitive.conf' found. ANOMALY DETECTED.")
        return True

    # Rule 4: Check if it matches any "normal" patterns
    for pattern in NORMAL_LOG_PATTERNS:
        if re.search(pattern, log_entry):
            print("--> Rule: Log matches a normal pattern. No anomaly.")
            return False

    # If no specific suspicious rule triggered and no normal pattern matched, it's still an anomaly for review
    print("--> Rule: No specific rule triggered, and no normal pattern matched. POTENTIAL ANOMALY DETECTED for human review.")
    return True # Consider as anomaly if not explicitly normal and no specific rule hit

def execute_automated_response(anomaly_details: dict) -> dict:
    """Simulates an automated defensive action within the Docker environment."""
    response_type = anomaly_details.get("response_type", "block_ip")
    target = anomaly_details.get("target", "unknown")
    reason = anomaly_details.get("reason", "unspecified anomaly")

    print(f"\n--- Executing Automated Defense Response ---")
    print(f"Response Type: {response_type}")
    print(f"Target: {target}")
    print(f"Reason: {reason}")

    try:
        client = docker.from_env()
        # Find the web server container to simulate actions on it
        container = client.containers.get("scenario_web_server") # Assuming web server is the target for simple defense

        if response_type == "block_ip" and target != "unknown":
            print(f"Simulating firewall rule addition: Blocking attacker IP {target} on scenario_web_server...")
            # In a real scenario, this would execute `iptables` or similar command
            exit_code, output = container.exec_run(f"iptables -A INPUT -s {target} -j DROP")
            output = output.decode('utf-8').strip()
            if exit_code == 0:
                print(f"Simulated IP block successful. Output: {output}")
                return {"success": True, "action": "IP_BLOCKED", "target": target}
            else:
                print(f"Simulated IP block failed. Exit code: {exit_code}, Output: {output}")
                return {"success": False, "action": "IP_BLOCK_FAILED", "details": output}
        elif response_type == "isolate_host":
            print(f"Simulating isolation of host {target} from network...")
            # This would involve detaching from Docker network or modifying container's network config
            mock_output = f"Host {target} isolated from scenario_network."
            print(mock_output)
            return {"success": True, "action": "HOST_ISOLATED", "target": target}
        else:
            print("Unsupported response type for simulation.")
            return {"success": False, "action": "UNSUPPORTED_RESPONSE"}

    except docker.errors.NotFound:
        print(f"Error: Docker container 'scenario_web_server' not found. Is it running?")
        return {"success": False, "output": "Defense target container not found"}
    except Exception as e:
        print(f"An unexpected error occurred during defense simulation: {e}")
        return {"success": False, "output": str(e)}

if __name__ == "__main__":
    print("--- Adaptive Defense Decision-Making Agent ---")

    # Simulate various log entries and trigger responses
    # Scenario 1: Normal activity
    print("\nScenario 1: Normal Log Entry")
    log1 = "[INFO] User alice logged in successfully from 192.168.1.10"
    if analyze_log_entry(log1):
        print("Anomaly detected, triggering response.")
        execute_automated_response({"response_type": "none", "target": "none", "reason": "false positive"})
    else:
        print("No anomaly, no response needed.")

    # Scenario 2: Suspicious keyword
    print("\nScenario 2: Suspicious Log Entry - Failed Login Attempt")
    log2 = "[WARNING] Failed login attempt for user 'admin' from IP 10.0.0.5."
    if analyze_log_entry(log2):
        print("Anomaly detected, triggering response.")
        response_result = execute_automated_response({"response_type": "block_ip", "target": "10.0.0.5", "reason": "repeated failed login"})
        print(f"Defense response result: {response_result['action']}")
    else:
        print("No anomaly, no response needed.")

    # Scenario 3: Unknown but potentially anomalous pattern
    print("\nScenario 3: Unknown Log Pattern")
    log3 = "Unauthorized access detected to sensitive_data.zip"
    if analyze_log_entry(log3):
        print("Anomaly detected, triggering response.")
        response_result = execute_automated_response({"response_type": "isolate_host", "target": "compromised_server", "reason": "data exfiltration attempt"})
        print(f"Defense response result: {response_result['action']}")
    else:
        print("No anomaly, no response needed.")

    print("\nDefense Agent's basic anomaly detection and automated response capabilities demonstrated.")