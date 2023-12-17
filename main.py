import json
import random
import numpy as np
import pickle
import nltk
# nltk.download()
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
    database = "main"
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
            print(x[2])
            print("")
        pass
    list_of_intents = intent_json['intents']
    for i in list_of_intents:
        if i['class'] == tag:
            result = random.choice(i['responses'])
            break
    return result
def add_event(admin_id):
    name = input('Please enter the event name:')
    detail = input('please enter details of events :')
    mycursor.execute('insert into events values(%s,null,%s,%s)',(name,detail,admin_id))
    db.commit()


def track_event(admin_id):
    mycursor.execute('select event_id from events where admin_id = %s',(admin_id,))
    parameter = mycursor.fetchone()
    # for x in mycursor:
    #     parameter = x[0]
    mycursor.execute('select username,roll_no from users where event_id = %s',(parameter[0],))
    # for x in mycursor:
    #     print(x)
    print(mycursor.fetchall())
    print("Here you go")

def admin_flow(id):
    while True:
        sentence = input('Hello '+id+' how can i help you : \n 1.Creat a Event \n 2.Track a Existing event')
        ints = predict_class(sentence)
        # print(ints)
        if ints[0]['intents'] == 'add_event':
            add_event(id)
            print('Congraulations')
        elif ints[0]['intents'] == 'track_event':
            track_event(id)
        else :
            print(ints)

def user_flow(id):
    sentence = input('Hello '+id+' How can i help you \n 1.get event')
    ints = predict_class(sentence)
    print(ints)
    if ints[0]['intents'] == 'get_event':
        mycursor.execute("select * from events")
        for x in mycursor:
            print(x[0])
            print(x[1])
            print(x[2])
            print("")
        val = input('If you wanna book any event ,Please enter its name')
        # mycursor.execute("select username from users")
        mycursor.execute("select * from events")
        for x in mycursor:
            print(x[0])
            if x[0] == val:
                mycursor.execute('select event_id from events where eventname = %s',(x[0],))
                parameter = mycursor.fetchone()
                # print(parameter)
                mycursor.execute('update users set event_id = %s',(parameter[0],))
                print('Congratulation you seat has been booked ! ')
                db.commit()
                break
# while True:
#     sentence = input('Enter :')
#     ints = predict_class(sentence)
#     # print(ints)
#     res = get_responses(ints,intents)
#     print(res)
while True:
    id = input('please enter id :')
    password = input('please enter the password')
    mycursor.execute('select * from admin')
    for x in mycursor:
        if x[0] == id and x[1] == password:
            admin_flow(id)
    mycursor.execute('select username,password from users')
    for x in mycursor:
        if x[0] == id and x[1] == password:
            user_flow(id)
            # print('hello user')
            continue
    print("wrong username or password")
