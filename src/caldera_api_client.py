# src/caldera_api_client.py
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

class CalderaApiClient:
    def __init__(self, base_url="http://127.0.0.1:8888", api_key=None):
        self.base_url = base_url
        if api_key is None:
            self.api_key = os.getenv("CALDERA_RED_API_TOKEN") # Get from .env
            if self.api_key is None:
                raise ValueError("CALDERA_RED_API_TOKEN not found. Please set it in your .env file or pass as argument.")
        else:
            self.api_key = api_key

        self.headers = {
            "Accept": "application/json",
            "KEY": self.api_key
        }
        print(f"CalderaApiClient initialized for {self.base_url}")

    def _make_request(self, method, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, verify=False) # verify=False for self-signed certs
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data, verify=False)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data, verify=False)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers, verify=False)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
            raise

    def get_agents(self):
        print("Fetching agents from Caldera...")
        return self._make_request("GET", "/api/rest") # This is a placeholder, real endpoint will vary by CALDERA version

    def get_abilities(self):
        print("Fetching abilities from Caldera...")
        return self._make_request("POST", "/api/rest", data={"index": "abilities"}) # Example: fetch abilities

    def deploy_agent(self, payload_name, group, contact_type="http"):
        print(f"Deploying agent with payload '{payload_name}' to group '{group}' via {contact_type}...")
        # This is a highly simplified mock for demonstration.
        # Real CALDERA agent deployment requires more specific setup
        # like agent payloads, C2 configurations etc.
        # You would create a manual payload in CALDERA and then call its API to deploy/download it.
        # For POC, we just simulate telling CALDERA to "track" a deployment.
        # Actual agent binary would be downloaded by the target manually or via side channel.
        return {"agent_id": f"simulated_agent_{os.urandom(4).hex()}", "status": "deployed", "host": "127.0.0.1"}

    def start_operation(self, name, group, adversary_id, jitter=2, cleanup=True, fact_source=None):
        print(f"Starting Caldera operation '{name}' for group '{group}' with adversary '{adversary_id}'...")
        data = {
            "name": name,
            "group": group,
            "adversary_id": adversary_id,
            "jitter": jitter,
            "cleanup": cleanup
        }
        if fact_source:
            data["fact_source"] = fact_source
        # This is a placeholder, actual endpoint and data may vary for your CALDERA version
        return self._make_request("POST", "/api/rest", data={"operation": "start", "data": data})

    def get_operation_results(self, op_id):
        print(f"Fetching results for operation {op_id}...")
        # Placeholder, actual endpoint for results will vary
        return self._make_request("POST", "/api/rest", data={"operation": "status", "id": op_id})


# Example of how to use this client (for testing)
if __name__ == "__main__":
    # --- MANUAL STEP: REPLACE WITH YOUR ACTUAL CALDERA RED TEAM API TOKEN ---
    # You can find this in your CALDERA terminal output on startup or in conf/local.yml
    # Example: API_TOKEN: qeSfxvYFkUT_rL4rbmO0ZLDWjRERFN-vE2ZUpUTaTsQ
    # Or, create a .env file in your project root with:
    # CALDERA_RED_API_TOKEN="your_red_team_api_token_here"
    # ----------------------------------------------------------------------

    print("Testing Caldera API Client...")
    try:
        client = CalderaApiClient()
        print("\nTesting get_agents:")
        # In Caldera 3.x, fetching agents might be via /api/rest/agents
        # or a POST to /api/rest with data={"index": "agents"}
        # The exact endpoint varies by version.
        # For this simplified client, `get_agents` is just calling /api/rest (which will error)
        # We'll use a specific endpoint once we know your exact CALDERA API version.

        # For CALDERA 3.x, a more typical API call might be:
        # resp = client._make_request("POST", "/api/rest", data={"index": "agents"})
        # print(json.dumps(resp, indent=4))

        # Test a mock deploy and start operation
        print("\nSimulating agent deploy and operation start (using mock calls for now):")
        mock_agent_id = client.deploy_agent("sandcat_linux", "my_group")
        print(f"Mock Agent Deployed: {mock_agent_id}")

        # You would need a valid adversary ID from your Caldera UI
        # For 3.x, you can find default adversaries under "Adversaries" menu
        # E.g., 'a8a25227-2c13-43f6-8c43-f4277b0798e9' for "Atomic Red Team" if it's there
        # mock_adversary_id = "a8a25227-2c13-43f6-8c43-f4277b0798e9"
        # mock_operation_name = "test_operation"
        # mock_operation = client.start_operation(mock_operation_name, "my_group", mock_adversary_id)
        # print(f"Mock Operation Started: {mock_operation}")

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred during client test: {e}")