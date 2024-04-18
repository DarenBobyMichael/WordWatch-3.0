import requests

API_TOKEN="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"
API_URL = "https://api-inference.huggingface.co/models/Hate-speech-CNERG/deoffxlmr-mono-malyalam"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def predict(text):
    output = query({
        "inputs": f"{text}",
    })
    print(output)
    off_rating=1 if output[0][2]['score']>0.5 or output[0][2]['score']>0.5  else 0
    ratings=[]
    labels=[]
    for i in output[0]:
        labels.append(i['label'])
        ratings.append(i['score'])
    return text,output[0],labels,ratings
    
    
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

print(predict('enthada'))