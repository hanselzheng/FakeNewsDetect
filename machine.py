# This program detects real (0) and fake (1) news using machine learning
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
import joblib

# Dataset
df = pd.read_csv('dataset\Fake_news.csv')
dt = pd.read_csv('dataset\True_news.csv')

def combine_textitle():
    # Combine rows in both dataset,
    # Shuffle rows,
    # Merge title and text
    data_merge = pd.concat([df, dt], axis=0)
    data_shuffle = data_merge.sample(frac=1)
    data_shuffle['combined'] = data_shuffle['title'] + '' + data_shuffle['text']

    # Save combined data using joblib
    data_shuffle.to_csv('combined_data.csv', index=False)

    return data_shuffle


def preprocess_text(text):
    # 1. Remove non-alphabetic characters
    # 2. Convert to lowercase and split into words
    # 3. Remove stop words and perform stemming
    # 4. Join the words back into a single string
    letters_only = re.sub('[^A-Za-z]', ' ', text)
    words = letters_only.lower().split()

    porter = PorterStemmer()
    meaningful_words = [porter.stem(word) for word in words if word not in stopwords.words('english')]
    joined_words = ' '.join(meaningful_words)

    return joined_words



def train_eval_model():
    dataset = pd.read_csv('combined_data.csv')
    X = dataset['combined']
    Y = dataset['label']      # 0 for Real, 1 for Fake

    # Preprocessing and Logistic Regression pipeline
    pipeline = Pipeline([
        ('preprocess', TfidfVectorizer(preprocessor=preprocess_text)),
        ('model', LogisticRegression())
    ])

    # Split data to train and test
    # train size = 0.70
    # test size = 0.30
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30, stratify=Y, random_state=0)

    # Fit pipeline to training data
    pipeline.fit(X_train, Y_train)

    # Predictions
    X_train_predict = pipeline.predict(X_train)
    X_test_predict = pipeline.predict(X_test)

    # Accuracy scores
    train_accuracy = accuracy_score(X_train_predict, Y_train)
    test_accuracy = accuracy_score(X_test_predict, Y_test)

    # Save trained pipeline components as joblib file
    with open('model.pkl', 'wb') as model_file:
        joblib.dump(pipeline, model_file)

    return train_accuracy, test_accuracy


def predict_news(input):

    # Call trained machine
    with open('model.pkl', 'rb') as model_file:
        pipeline = joblib.load(model_file)

    transformed_text = pipeline.named_steps['preprocess'].transform([input])
    prediction = pipeline.named_steps['model'].predict(transformed_text)

    reliable = "This news article is reliable (real news)"
    unreliable = "This news article is NOT reliable (fake news)"

    if prediction[0] == 0:
        return reliable
    else:
        return unreliable



# For Testing Accuracy Score, uncomment these 3 lines below

# train_accuracy, test_accuracy = train_eval_model()
# print(f"Accuracy Score: {train_accuracy}")
# print(f"Accuracy Score: {test_accuracy}")




# Run the Program!
print("\nWelcome to Scammer Scanner — Where we scan for scams in news articles!")

user_input = input("Enter a news article: \n")
prediction_result = predict_news(user_input)
print("\nPrediction:", prediction_result)
