import time
import requests

AGGREGATE_URL = "http://127.0.0.1:5000/aggregate"

# Dictionary to store downtime counters for each instance
downtime_counters = {}

CRITICAL_THRESHOLD = 3  # Threshold for critical condition

def is_node_healthy(instance):
    """
    Simulated function to check if a node is in a healthy state.
    Replace this with the actual health-check logic.
    """
    if instance != "node_3":
        return True

    # For now, simulate that nodes are healthy after recovering.
    # Replace this condition with actual health-check criteria.
      # Always assume the node is healthy for this example.

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
                if downtime_counters[instance] >= CRITICAL_THRESHOLD:
                    print(f"CRITICAL: {instance} is in a critical condition!")
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