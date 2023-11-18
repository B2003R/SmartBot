import json
import numpy as np
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
# loading constructer and opening pickled files and loading model
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
with open('words.pkl', 'rb') as f:
    words = pickle.load(f)
with open('classes.pkl', 'rb') as f:
    classes = pickle.load(f)

# words = pickle.load('words.pickle','rb')
# classes = pickle.load('words.pickle','rb')
model = load_model('chatbot_model.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_word = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_word:
        for i,word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r> ERROR_THRESHOLD]
    results.sort(key= lambda x:x[1] , reverse=True)
    return_list = []
    for r in results:
        print('intent :',classes[r[0]],"probability :",str(r[1]))

while True:
    sentence = input('Enter :')
    predict_class(sentence)