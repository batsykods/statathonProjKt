# in services.py
import requests

# We'll use a public test API for this example.
# Replace this with your actual government API endpoint when you're ready.
PUBLIC_API_ENDPOINT = " "

def fetch_government_data():
    """
    Fetches data from a public API that does not require an API key.
    """
    try:
        # The headers dictionary is no longer needed
        response = requests.get(PUBLIC_API_ENDPOINT)
        
        # This will raise an error for bad responses (like 404 Not Found)
        response.raise_for_status()
        
        # Return the data as a Python list of dictionaries
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return None