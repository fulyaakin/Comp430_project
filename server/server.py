from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

import mysql.connector
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import csv
import numpy as np
import math
import random

db_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="onlinemarket",
  auth_plugin="mysql_native_password"
)
print(db_connection)


# creating database_cursor to perform SQL operation
db_cursor = db_connection.cursor(buffered=True)


db_cursor.execute("USE onlinemarket")

addresses = {'Akyurt':0, 'Altindag':0, 'Ayas':0, 'Bala':0, 'Beypazari':0, 'Camlidere':0, 'Cankaya':0, 'Cubuk':0, 'Elmadag':0, 
               'Etimesgut':0, 'Evren':0, 'Golbasi':0, 'Gudul':0, 'Haymana':0, 'Kahramankazan':0, 'Kalecik':0, 'Kecioren':0, 
               'Kizilcahamam':0, 'Mamak':0, 'Nallihan':0, 'Polatli':0, 'Pursaklar':0, 'Sincan':0, 'Sereflikochisar':0, 
               'Yenimahalle':0, 'Adalar':0, 'Arnavutkoy':0, 'Atasehir':0, 'Avcilar':0, 'Bagcilar':0, 'Bahcelievler':0, 
               'Bakirkoy':0, 'Basaksehir':0, 'Bayrampasa':0, 'Besiktas':0, 'Beykoz':0, 'Beylikduzu':0, 'Beyoglu':0, 
               'Buyukcekmece':0, 'Catalca':0, 'Cekmekoy':0, 'Esenler':0, 'Esenyurt':0, 'Eyupsultan':0, 'Fatih':0, 
               'Gaziosmanpasa':0, 'Gungoren':0, 'Kadikoy':0, 'Kagithane':0, 'Kartal':0, 'Kucukcekmece':0, 'Maltepe':0, 
               'Pendik':0, 'Sancaktepe':0, 'Sariyer':0, 'Silivri':0, 'Sultanbeyli':0, 'Sultangazi':0, 'Sile':0, 'Sisli':0, 
               'Tuzla':0, 'Umraniye':0, 'Uskudar':0, 'Zeytinburnu':0, 'Aliaga':0, 'Balcova':0, 'Bayindir':0, 'Bayrakli':0, 
               'Bergama':0, 'Beydag':0, 'Bornova':0, 'Buca':0, 'Cesme':0, 'Cigli':0, 'Dikili':0, 'Foca':0, 'Gaziemir':0, 'Guzelbahce':0, 
               'Karabaglar':0, 'Karaburun':0, 'Karsiyaka':0, 'Kemalpasa':0, 'Kinik':0, 'Kiraz':0, 'Konak':0, 'Menderes':0, 
               'Menemen':0, 'Narlidere':0, 'Odemis':0, 'Seferihisar':0, 'Selcuk':0, 'Tire':0, 'Torbali':0, 'Urla':0}

ages = {'18':0,'19':0,'20':0,'21':0,'22':0,'23':0,'24':0,'25':0,'26':0,'27':0,'28':0,'29':0,'30':0,'31':0,'32':0,'33':0,'34':0,'35':0,'36':0,'37':0,'38':0,'39':0,'40':0,'41':0,'42':0,'43':0,'44':0,'45':0,'46':0,'47':0,'48':0,'49':0}

genders = {'Female':0, 'Male':0}

def add_laplace_noise(real_answer: dict, sensitivity: float, epsilon: float):
    output = {}
    for key in real_answer:
        r = np.random.laplace(0, sensitivity/epsilon)
        output[key] = real_answer[key] + r

    return output


def private_histogram(my_dict, df: list, n: int, epsilon: float):
    sensitivity = 1.0
    
    current_dict = {}
    
    if my_dict == 'address':
        current_dict = addresses.copy()
    
    elif my_dict == 'age':
        current_dict = ages.copy()
        
    elif my_dict == 'gender':
        current_dict = genders.copy()
        
    
    for ix in df.index:
        current_dict[df.loc[ix][0]] += 1        
    
    noisy_counts = add_laplace_noise(current_dict, sensitivity, epsilon)

    return noisy_counts


def apply_exponential_mechanism(my_dict, dataset, epsilon):
    current_dict = {}
    
    if my_dict == 'address':
        current_dict = addresses.copy()
    
    elif my_dict == 'age':
        current_dict = ages.copy()
        
    elif my_dict == 'gender':
        current_dict = genders.copy()
    
    range_number = len(current_dict)
    
    sensitivity = 1.0
    counts = private_histogram(my_dict, dataset, 1, epsilon).values()
    counts = list(counts)
    
    total_prob = 0
    indv_prob = []
    for i in range(range_number):
        x = math.exp((epsilon * counts[i]) / (2 * sensitivity))
        indv_prob.append(x)
        total_prob += x

    for indv in indv_prob:
        indv = indv/total_prob
        
    keys_list = list(current_dict)
    if my_dict != 'gender':
        key = keys_list[indv_prob.index(max(indv_prob))]
    else:
        return keys_list[indv_prob.index(max(indv_prob))] 
    return key


app = Flask(__name__)
CORS(app)


@app.route("/value_1")
@cross_origin()
def get_value1():
    #Address value with most orders with Exponential Mechanism
    sql = """ SELECT gender FROM Orders """
    db_cursor.execute(sql)
    result = db_cursor.fetchall()
    fieldnames1 = [i[0] for i in db_cursor.description]
    df1 = pd.DataFrame(list(result), columns=fieldnames1)
    #Laplace noise added DP Histogram of Age values
    sql2 = """ SELECT age FROM Orders """
    db_cursor.execute(sql2)
    result2 = db_cursor.fetchall()
    fieldnames2 = [i[0] for i in db_cursor.description]
    df2 = pd.DataFrame(list(result2), columns=fieldnames2)
    return {'content': apply_exponential_mechanism('gender',df1,0.5),'content2':private_histogram('age',df2,10,0.5)}


@app.route("/value_2")
@cross_origin()
def get_value2():
    #Address value with most orders with Exponential Mechanism
    sql = """ SELECT address FROM Orders """
    db_cursor.execute(sql)
    result = db_cursor.fetchall()
    fieldnames = [i[0] for i in db_cursor.description]
    df = pd.DataFrame(list(result), columns=fieldnames)
    #Laplace noise added DP Histogram of Address values
    sql2 = """ SELECT address FROM Orders """
    db_cursor.execute(sql2)
    result2 = db_cursor.fetchall()
    fieldnames2 = [i[0] for i in db_cursor.description]
    df2 = pd.DataFrame(list(result2), columns=fieldnames2)
    return {'content': apply_exponential_mechanism('address',df,2),'content2' : private_histogram('address',df2,1,2)}

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000, debug=True)