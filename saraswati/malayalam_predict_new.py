import requests

API_TOKEN="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"
API_URL = "https://api-inference.huggingface.co/models/Hate-speech-CNERG/deoffxlmr-mono-malyalam"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def predict(text):
    query(text)

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

ask=input("Enter the query: ")
	
output = query({
	"inputs": f"{ask}",
})