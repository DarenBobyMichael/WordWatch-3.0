import requests

API_TOKEN="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"
API_URL = "https://api-inference.huggingface.co/models/Hate-speech-CNERG/deoffxlmr-mono-malyalam"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

import requests

# API_URL_2 = "https://api-inference.huggingface.co/models/Hate-speech-CNERG/malayalam-codemixed-abusive-MuRIL"
API_URL_2 = "https://api-inference.huggingface.co/models/Hate-speech-CNERG/indic-abusive-allInOne-MuRIL"
headers_2 = {"Authorization": "Bearer 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"}

def query_2(payload):
	response = requests.post(API_URL_2, headers=headers_2, json=payload)
	return response.json()
	


def predict(text):
    output = query({
        "inputs": f"{text}",
    })
    output_2 = query_2({
	"inputs": f"{text}"
    })
    offensiveness=0
    normalness=0
    for item in output_2[0]:
    # Check if the label is 'LABEL_1'
        if item['label'] == 'LABEL_1':
            # Store the score if the label matches
            offensiveness = item['score']
        else:
            normalness = item['score']
    
    # off_rating=1 if output[0][2]['score']>0.5 or output[0][2]['score']>0.5  else 0
    ratings=[]
    labels=[]
    for i in output[0]:
        if i['label'] == 'Not_offensive':
            i['label'] =  "Abusive"
            i['score']= offensiveness
        
        i['label']=''+' '.join(i['label'].split('_'))
        labels.append(i['label'])
        ratings.append(i['score'])
    
    labels.append('Normal')
    ratings.append(normalness)
    print(output_2)
    
    return text,output[0],labels,ratings
    
    
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

predict('kutta sugalle')
