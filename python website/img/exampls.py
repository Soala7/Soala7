import requests
# API URL (keyless and free)
url = "https://official-joke-api.appspot.com/random_joke"
# Make a GET request
response = requests.get(url)
# Check if the request was successful
if response.status_code == 200:
    joke = response.json()  # Convert JSON to dictionary
    print("Here's a joke for you:")
    print(joke['setup'])
    print(joke['punchline'])
else:
    print("Failed to get a joke. Try again later.")
