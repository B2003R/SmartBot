# from sklearn.feature_extraction.text import CountVectorizer
# import json
# import numpy as np
# # intents = json.loads(open('intents.json').read())
# # corupus = {'greeting ' : ['hello','hi','whats up?' ,'brooo']}
# # vectorizer = CountVectorizer()
# # x = vectorizer.fit_transform(corupus['greeting '])
# # print(x)
# data = [[1,2],[10,20]]
# data = np.array(data)
# print(data[: , 1])
import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "Bollam23$",
    database = "main"
)
mycursor = db.cursor()
mycursor.execute('select * from users')
