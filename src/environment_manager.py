# src/environment_manager.py
import time
import random
import docker

def simulate_env_adjustment(event_type: str, details: dict = None):
    print(f"\n--- Dynamic Environment Adjustment Triggered ---")
    print(f"Event: {event_type}")
    if details:
        print(f"Details: {details}")

    try:
        client = docker.from_env() # Initialize Docker client
        # (Assuming target_container might be passed in details for consistency)
        target_container = details.get("target_container", "unknown_target")

        if event_type == "VULNERABILITY_PATCHED":
            print("Response: Detected a vulnerability was patched. Automatically introducing a new, simulated 'zero-day' threat or escalating attack intensity.")
        elif event_type == "ATTACK_DETECTED":
            print("Response: Detected an ongoing attack. Taking real action to reduce impact.")
            if target_container == "scenario_web_server": # Only stop web server for now
                print(f"Action: Attempting to stop {target_container} to contain threat.")
                container = client.containers.get(target_container)
                container.stop()
                print(f"Successfully stopped {target_container}.")
            else:
                print(f"No specific stop action defined for {target_container}. Simulating increased defensive posture.")
        elif event_type == "DEFENDER_WEAKNESS_IDENTIFIED":
            skill_gap = details.get("skill_gap", "unknown skill")
            print(f"Response: Identified defender weakness in '{skill_gap}'. Adapting scenario to provide more challenges in this area (e.g., adding more complex log files for analysis).")
        elif event_type == "ATTACK_BLOCKED": # ADD THIS NEW ELIF BLOCK
            attacker_ip = details.get("attacker_ip", "unknown IP")
            print(f"Response: Attack from {attacker_ip} was successfully blocked/mitigated. Environment posture maintained or slightly relaxed.")
            # You could add a conceptual action here, like "redeploy honeypot" or "log success to SIEM"
        else:
            print(f"Unrecognized event type: {event_type}. No specific adjustment performed.")

    except docker.errors.NotFound:
        print(f"Error: Docker container '{target_container}' not found for dynamic adjustment.")
    except Exception as e:
        print(f"An unexpected error occurred during dynamic adjustment: {e}")

    print("---------------------------------------------")

if __name__ == "__main__":
    print("Environment Manager: Ready to receive dynamic events.")
    # Simulate a few events
    simulate_env_adjustment("VULNERABILITY_PATCHED")
    time.sleep(2)
    simulate_env_adjustment("ATTACK_DETECTED", {"source_ip": "172.17.0.5", "target_service": "web_server"})
    time.sleep(2)
    simulate_env_adjustment("DEFENDER_WEAKNESS_IDENTIFIED", {"skill_gap": "Log Analysis"})