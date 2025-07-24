# src/environment_manager.py
import time
import random

def simulate_env_adjustment(event_type: str, details: dict = None):
    print(f"\n--- Dynamic Environment Adjustment Triggered ---")
    print(f"Event: {event_type}")
    if details:
        print(f"Details: {details}")

    if event_type == "VULNERABILITY_PATCHED":
        print("Response: Detected a vulnerability was patched. Automatically introducing a new, simulated 'zero-day' threat or escalating attack intensity.")
        # In a real system, this would trigger specific Terraform/Docker/Kubernetes API calls
        # to deploy a new vulnerable service, modify firewall rules, or launch a new attack vector.
    elif event_type == "ATTACK_DETECTED":
        print("Response: Detected an ongoing attack. Increasing defensive posture by tightening firewall rules on scenario_web_server.")
        # Example: This would execute a command inside the web_server container or on a firewall host.
        # E.g., docker exec scenario_web_server iptables -A INPUT -p tcp --dport 80 -s attacker_ip -j DROP
    elif event_type == "DEFENDER_WEAKNESS_IDENTIFIED":
        skill_gap = details.get("skill_gap", "unknown skill")
        print(f"Response: Identified defender weakness in '{skill_gap}'. Adapting scenario to provide more challenges in this area (e.g., adding more complex log files for analysis).")
    else:
        print(f"Unrecognized event type: {event_type}. No specific adjustment performed.")
    print("---------------------------------------------")

if __name__ == "__main__":
    print("Environment Manager: Ready to receive dynamic events.")
    # Simulate a few events
    simulate_env_adjustment("VULNERABILITY_PATCHED")
    time.sleep(2)
    simulate_env_adjustment("ATTACK_DETECTED", {"source_ip": "172.17.0.5", "target_service": "web_server"})
    time.sleep(2)
    simulate_env_adjustment("DEFENDER_WEAKNESS_IDENTIFIED", {"skill_gap": "Log Analysis"})