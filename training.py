import random
import json
import pickle
import numpy as np
import nltk
# nltk.download()
from nltk.stem import WordNetLemmatizer
from keras.models import  Sequential
from keras.layers import Dense , Activation , Dropout
from keras.optimizers import SGD
lemmatizer = WordNetLemmatizer()
# taking intents json file
intents = json.loads(open('intents.json').read())
#declaring variable
words = []
classes = []
documents = []
ignore_letters = ['?',".",",","!"]
# preprocessing the patterns in intents
for intent in intents['intents']:
    for pattern in intent['pattern']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list,intent['class']))
        if intent['class'] not in classes:
            classes.append(intent['class'])
# Lemmatizing the words
# words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
word_lemma = []
for word in words:
    if word not in ignore_letters:
        word_lemma.append(lemmatizer.lemmatize(word))
words = word_lemma
words = sorted(set(words))
# print(words)
# saving it as a pickle file
pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))

# extracting feature so that we can send numeric values to the ML model , so here we are using bag-of-words feture extracting technique
training = []
output_empty = [0]*len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag,output_row])

# training = np.array(training)
# random.shuffle(training)
# print(training)
train_x = []
train_y = []
for train in training:
    # print(train)
    train_x.append(train[0])
    train_y.append(train[1])
train_x = list(train_x)
train_y = list(train_y)
# print(train_x)
# print(len(train_y))
# buildind model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),) , activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation = 'softmax'))
sgd = SGD(lr = 0.01, momentum = 0.9, nesterov=True)
model.compile(loss = 'categorical_crossentropy',optimizer = sgd , metrics=['accuracy'])
sm = model.fit(np.array(train_x),np.array(train_y),epochs = 200 , batch_size = 5 , verbose = 1)
model.save('chatbot_model.h5',sm)
print("done")

