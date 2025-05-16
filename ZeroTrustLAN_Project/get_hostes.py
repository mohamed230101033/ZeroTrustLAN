import json
import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Authentication function to get a service ticket
def get_service_ticket(username="admin", password="admin"):
    auth_url = "http://localhost:58000/api/v1/ticket"
    body = {
        "username": username,
        "password": password
    }
    response = requests.post(auth_url, json=body, verify=False)
    if response.status_code in [200, 201]:  # Accept both 200 OK and 201 Created
        return response.json()["response"]["serviceTicket"]
    else:
        print(f"Authentication failed. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

# Get a service ticket
service_ticket = get_service_ticket()
if not service_ticket:
    print("Failed to obtain service ticket. Exiting.")
    exit(1)

api_url = "http://localhost:58000/api/v1/host"
headers = {
    "X-Auth-Token": service_ticket
}

# Make the API request
resp = requests.get(api_url, headers=headers, verify=False)
print("Request status: ", resp.status_code)

# Check if request was successful
if resp.status_code != 200:
    print(f"API request failed. Status code: {resp.status_code}")
    print(f"Response: {resp.text}")
    exit(1)

# Parse the JSON response
try:
    response_json = resp.json()
    print(f"Response structure: {json.dumps(response_json, indent=2)[:200]}...")
    
    hosts = response_json.get("response", [])
    
    # Check if hosts is a list before iterating
    if isinstance(hosts, list):
        for host in hosts:
            if isinstance(host, dict):
                print(
                    host.get("hostName", "N/A"), "\t",
                    host.get("hostIp", "N/A"), "\t",
                    host.get("hostMac", "N/A"), "\t",
                    host.get("connectedInterfaceName", "N/A")
                )
            else:
                print(f"Unexpected host data format: {host}")
    else:
        print(f"Unexpected response format. 'response' is not a list: {hosts}")
except Exception as e:
    print(f"Error processing response: {e}")
    print(f"Raw response: {resp.text[:200]}...")
