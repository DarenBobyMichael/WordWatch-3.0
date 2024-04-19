import requests
from ml2en import ml2en
from saraswati.gspeechtotext_video import transcribe_malayalam_audio


API_TOKEN="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"
API_URL = "https://api-inference.huggingface.co/models/Hate-speech-CNERG/deoffxlmr-mono-malyalam"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def predict_video(video_file):

    new_text=[]
    new_text.append(ml2en.transliterate(transcribe_malayalam_audio(video_file)))
    for i in new_text:
        print(i)
    output = query({
        "inputs": f"{new_text}",
    })
    print(output)
    off_rating=1 if output[0][2]['score']>0.5 or output[0][2]['score']>0.5  else 0
    ratings=[]
    labels=[]
    for i in output[0]:
        i['label']=''+' '.join(i['label'].split('_'))
        labels.append(i['label'])
        ratings.append(i['score'])
    return new_text,output[0],labels,ratings
    
    
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()




