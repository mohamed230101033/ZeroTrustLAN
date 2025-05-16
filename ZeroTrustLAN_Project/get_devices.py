import json
import requests
import sys
# Disable SSL warnings (only for development environments)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to get service ticket
def get_service_ticket():
    auth_url = "http://localhost:58000/api/v1/ticket"
    headers = {
        "Content-Type": "application/json"
    }
    # Replace with your actual credentials
    body = {
        "username": "admin",
        "password": "admin"  # Change this to your actual password
    }
    
    try:
        response = requests.post(auth_url, headers=headers, json=body, verify=False)
        if response.status_code in [200, 201]:  # Accept both 200 OK and 201 Created
            return response.json()["response"]["serviceTicket"]
        else:
            print(f"Authentication failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

# Get service ticket
service_ticket = get_service_ticket()
if not service_ticket:
    print("Failed to get service ticket. Exiting.")
    sys.exit(1)

# Use the service ticket for the API request
api_url = "http://localhost:58000/api/v1/network-device"
headers = {
    "X-Auth-Token": service_ticket
}

try:
    resp = requests.get(api_url, headers=headers, verify=False)
    print("Request status: ", resp.status_code)
    
    if resp.status_code == 200:
        response_json = resp.json()
        if "response" in response_json:
            networkDevices = response_json["response"]
            if networkDevices:
                print("\nHostname\tPlatform ID\tManagement IP")
                print("-" * 60)
                for networkDevice in networkDevices:
                    # Use get method to safely retrieve values that might be missing
                    hostname = networkDevice.get("hostname", "N/A")
                    platform = networkDevice.get("platformId", "N/A")
                    mgmt_ip = networkDevice.get("managementIpAddress", "N/A")
                    print(f"{hostname}\t{platform}\t{mgmt_ip}")
            else:
                print("No network devices found.")
        else:
            print("Unexpected response format:", json.dumps(response_json, indent=2))
    else:
        print(f"Request failed with status code: {resp.status_code}")
        print(f"Response: {resp.text}")
except Exception as e:
    print(f"Error occurred: {e}")
