import requests

url = "http://127.0.0.1:7860/api/v1/flows/upload/"

payload = {}
files = {
    'file': ('EdApp.json', open('EdApp.json', 'rb'), 'application/json')
}
headers = {
    'Accept': 'application/json'
}

response = requests.post(url, headers=headers, files=files)
print(response.text)
