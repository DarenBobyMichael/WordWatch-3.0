
import pandas as pd
import numpy as np
import joblib

mal_data = pd.read_csv("Malayalam_offensive_data_Training-YT (1).csv")
mal_data_test = pd.read_csv("final_test_mal-offensive-with-labels (1).csv")
mal_data.drop("ID", axis = 1, inplace = True)
mal_data_test.drop("ID", axis = 1, inplace = True)

import re
def remove_symbols(string):
    a = re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)","",string)
    return a
mal_data["Tweets"] = mal_data["Tweets"].map(remove_symbols)

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

mal_data["Tweets"] = mal_data["Tweets"].map(remove_emojis)
mal_data['Labels'] = mal_data['Labels'].replace({'OFF' : 1, 'NOT' : 0})
mal_data_test['Labels'] = mal_data_test['Labels'].replace({'HOF' : 1, 'NOT' : 0})


import openpyxl

mal_data.head(5)

mal_data_test.head(100)

X_train = mal_data["Tweets"]
y_train = mal_data["Labels"]
X_test = mal_data_test["Tweets"]
y_test = mal_data_test["Labels"]

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(X_train)

X_test = vectorizer.transform(X_test)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators =60,criterion ='gini',max_depth=400,max_features ='log2',min_samples_split =5,max_leaf_nodes =450)

model.fit(X_train,y_train)

joblib.dump(model, 'random_forest_model.joblib')
joblib.dump(vectorizer, 'count_vectorizer.joblib')
import pickle

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer()
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

with open('vectorizer.pkl', 'wb') as file:
    pickle.dump(cv, file)

filename = 'malayalam_model.sav'
pickle.dump(model, open(filename, 'wb'))

from sklearn.metrics import classification_report

y_predicted = model.predict(X_test)

# from sklearn import metrics
# print(f"Accuracy = {metrics.accuracy_score(y_test, y_predicted)}\n\n")
# print(classification_report(y_predicted,y_test))

