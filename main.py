import json
import random
import numpy as np
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import mysql.connector
# loading constructer and opening pickled files and loading model
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
with open('words.pkl', 'rb') as f:
    words = pickle.load(f)
with open('classes.pkl', 'rb') as f:
    classes = pickle.load(f)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "Bollam23$",
    database = "smartbot"
)
mycursor = db.cursor()
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
        return_list.append({'intents' : classes[r[0]],"probability " : str(r[1])})
    return return_list
def get_responses(intent_list , intent_json):
    tag = intent_list[0]['intents']
    if tag == 'get_event':
        mycursor.execute("select * from events")
        for x in mycursor:
            print(x[0])
            print(x[1])
            print("")
    list_of_intents = intent_json['intents']
    for i in list_of_intents:
        if i['class'] == tag:
            result = random.choice(i['responses'])
            break
    return result
while True:
    sentence = input('Enter :')
    ints = predict_class(sentence)
    # print(ints)
    res = get_responses(ints,intents)
    print(res)