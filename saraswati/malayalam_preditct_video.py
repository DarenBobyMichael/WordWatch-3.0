import re
import joblib
from ml2en import ml2en
import gspeechtotext_video

# Function to remove symbols
def remove_symbols(string):
    a = re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", "", string)
    return a

# Function to remove emojis
def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def is_english_string(input_string):
    return all(ord(char) < 128 for char in input_string)

# Load the model and vectorizer
loaded_model = joblib.load('random_forest_model.joblib')
loaded_vectorizer = joblib.load('count_vectorizer.joblib')

# Example text for prediction and detecting whether it is malayalam or english characters

# final_text=input("Enter the string to be predicted: ")
# if is_english_string(final_text):
#     pass
# else:
#     final_text=ml2en.transliterate(final_text)

new_text=[]
new_text.append(ml2en.transliterate(gspeechtotext_video.transcribe_malayalam_audio()))

# Preprocess the new text
new_text = [remove_emojis(remove_symbols(text)) for text in new_text]

# Transform the new text using the loaded vectorizer
new_text_transformed = loaded_vectorizer.transform(new_text)

# Make predictions using the loaded model
predictions = loaded_model.predict(new_text_transformed)

# Display the predictions
for text, prediction in zip(new_text, predictions):
    print(f"Text: {text}\nPrediction: {'Offensive' if prediction == 1 else 'Not Offensive'}\n")
