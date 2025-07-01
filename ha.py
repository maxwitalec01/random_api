import time
import requests
import random

AGGREGATE_URL = "http://127.0.0.1:5000/aggregate"

# Dictionary to store downtime counters for each instance
downtime_counters = {}

CRITICAL_THRESHOLD = 3  # Threshold for critical condition

# Dummy list of hostnames for pinging
HOST_LIST = ["host1.example.com", "host2.example.com", "host3.example.com", "host4.example.com", "host5.example.com"]

def is_node_healthy(instance):
    """
    Simulated function to check if a node is in a healthy state.
    Replace this with the actual health-check logic.
    """
    return True # Always assume the node is unhealthy for this example.

def simulate_ping(hostname):
    """
    Simulates a ping to a hostname.
    Returns True if the ping is successful, False otherwise.
    """
    # Simulate a random success/failure for ping
    return random.choice([True, False])

def handle_critical_node(instance):
    """
    Handles a critical node by pinging a list of hostnames and printing results.
    """
    print("Retrieving host list...")
    successful_pings = 0

    for hostname in HOST_LIST:
        if simulate_ping(hostname):
            successful_pings += 1

    # Determine action based on ping results
    if successful_pings > len(HOST_LIST) / 2:
        print(f"{instance}: Probably nothing (successful pings: {successful_pings}/{len(HOST_LIST)})")
    else:
        print(f"{instance}: Evacuating node! (successful pings: {successful_pings}/{len(HOST_LIST)})")

def fetch_aggregate():
    """
    Fetches data from the /aggregate endpoint and keeps track of node downtimes.
    Checks if any node is in a critical condition and handles maintenance mode.
    """
    global downtime_counters
    try:
        response = requests.get(AGGREGATE_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Data fetched: {data}")
            
            # Initialize or update downtime counters
            for instance, status in data.items():
                if instance not in downtime_counters:
                    downtime_counters[instance] = 0
                
                if status == "Error":
                    downtime_counters[instance] += 1
                else:
                    # Check if the node is healthy before resetting the counter
                    if is_node_healthy(instance):
                        downtime_counters[instance] = 0
                    else:
                        print(f"{instance} is recovering but remains in maintenance mode.")

                # Check for critical condition
                if downtime_counters[instance] == CRITICAL_THRESHOLD:
                    print(f"CRITICAL: {instance} is in a critical condition!")
                    handle_critical_node(instance)
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    print("Starting to poll the /aggregate endpoint every 5 seconds...")
    while True:
        fetch_aggregate()
        print(f"Downtime counters: {downtime_counters}")
        time.sleep(5)