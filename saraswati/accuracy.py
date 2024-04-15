import joblib
import pandas as pd
import re
# Load the offloaded model and vectorizer
model = joblib.load('random_forest_model.joblib')
vectorizer = joblib.load('count_vectorizer.joblib')

import re
def remove_symbols(string):
    a = re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)","",string)
    return a

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
# Load the test data
mal_data_test = pd.read_csv("final_test_mal-offensive-with-labels (1).csv")
mal_data_test.drop("ID", axis=1, inplace=True)

# Preprocess the test data
mal_data_test["Tweets"] = mal_data_test["Tweets"].map(remove_symbols)
mal_data_test["Tweets"] = mal_data_test["Tweets"].map(remove_emojis)
mal_data_test['Labels'] = mal_data_test['Labels'].replace({'HOF': 1, 'NOT': 0})

# Extract features from the test data
X_test = mal_data_test["Tweets"]
y_test = mal_data_test["Labels"]
X_test_transformed = vectorizer.transform(X_test)

# Make predictions using the loaded model
y_predicted = model.predict(X_test_transformed)

# Evaluate accuracy
from sklearn.metrics import accuracy_score, classification_report

accuracy = accuracy_score(y_test, y_predicted)
print("Accuracy:", accuracy)
print("\nClassification Report:\n", classification_report(y_test, y_predicted))
