import requests
import json
import sys

def get_service_ticket(base_uri, username, password):
    """Request service ticket from APIC-EM Controller."""
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"username": username, "password": password})
    
    try:
        resp = requests.post(base_uri + "/ticket", data=data, headers=headers)
        print(f"Authentication Status Code: {resp.status_code}")
        result = resp.json()
        
        if resp.status_code in [200, 201]:  # Accept both 200 and 201 as success
            if "serviceTicket" in result.get("response", {}):
                ticket = result["response"]["serviceTicket"]
                print('THE TICKET IS:', ticket)
                return ticket
            else:
                print(f"Authentication succeeded but no service ticket found in response: {result}")
                return None
        else:
            print(f"Authentication Error: {result}")
            return None
    except Exception as e:
        print(f"Error requesting service ticket: {e}")
        return None

def get_network_devices(base_uri, ticket):
    """Request list of network devices using the service ticket."""
    if not ticket:
        print("No valid service ticket. Cannot retrieve network devices.")
        return
    
    headers = {"X-Auth-Token": ticket}
    try:
        resp = requests.get(base_uri + "/network-device", headers=headers)
        print(f"Network Devices Status Code: {resp.status_code}")
        
        if resp.status_code == 200:
            result = resp.json()
            print(json.dumps(result, indent=4))
            
            for device in result["response"]:
                print(f"{device['hostname']} {device['serialNumber']} {device['softwareVersion']}")
        else:
            print("Failed to retrieve network devices")
    except Exception as e:
        print(f"Error getting network devices: {e}")

def main():
    base_uri = "http://localhost:58000/api/v1"
    
    # Update these credentials to match your APIC-EM setup
    username = "admin"  # Try different username
    password = "admin"  # Try different password
    
    ticket = get_service_ticket(base_uri, username, password)
    if ticket:
        get_network_devices(base_uri, ticket)
    else:
        print("Please verify your username, password, and that the APIC-EM controller is accessible.")
        sys.exit(1)

if __name__ == "__main__":
    main()







