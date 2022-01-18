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
import os
from anytree import Node, RenderTree
from pandas import DataFrame, read_csv

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

dgh_dict = {}
node_dict = {}

def read_dataset(dataset, qi_list, sa):
    result = dataset.dropna()
    result = result[result.columns.intersection(qi_list + sa)]
    return result

def read_DGHs(DGH_folder: str) -> dict:
    with os.scandir(DGH_folder) as directory:
        node_list = []
        for file in directory:
            lines = open(file).read().splitlines()
            for line in lines:
                line = line.rstrip(' ')
                line = line.rstrip()
                if len(line) - len(line.lstrip()) == 0:
                    dgh_dict[os.path.splitext(file)[0][5:]] = Node(line)
                    node_list.insert(0, dgh_dict[os.path.splitext(file)[0][5:]])
                else:
                    node_name = line.lstrip()
                    node_dict[node_name] = Node(node_name, parent=node_list[len(line) - len(line.lstrip()) - 1])
                    node_list.insert(len(line) - len(line.lstrip()), node_dict[node_name])

    return dgh_dict

def cost_LM(raw_dataset_file: str, anonymized_dataset_file: str, columns, depths, current):
    anonymized_cost = 0
    raw_cost = 0

    if depths[current] == 0:
        anonymized_cost = len(anonymized_dataset_file) / (columns - 1)
    else:
        for anonymized_entry in anonymized_dataset_file:
            anonymized_entry = node_dict[anonymized_entry]
            anonymized_cost += ( 1 / (columns - 1) * ((len(anonymized_entry.path[depths[current]].leaves) - 1) / (len(anonymized_entry.root.leaves) - 1)))

    for raw_entry in raw_dataset_file:
        raw_entry = node_dict[raw_entry]
        if depths[current] < raw_entry.depth:
            raw_cost += ( 1 / (columns - 1) * ((len(raw_entry.path[depths[current] + 1].leaves) - 1) / (len(raw_entry.root.leaves) - 1)))

    return (anonymized_cost, raw_cost)

def anonymizer(raw_dataset):
    k = 2
    copy_dataset = raw_dataset.copy()
    depths = [0] * (len(copy_dataset.columns) - 1)
    current = len(copy_dataset)

    while(current > k):
        score_list = [0] * (len(copy_dataset.columns) - 1)
        lm_cost_anonymized = copy_dataset.copy()
        lm_cost_raw = copy_dataset.copy()
        current_column = 0
        for column in copy_dataset.iloc[:,:-1]:

            current_depth = depths[current_column]
            for i in copy_dataset[column].index:
                current_node = node_dict[copy_dataset.at[i, column]]
                current_node_depth = current_node.depth
                if current_depth <= current_node_depth:
                    lm_cost_anonymized.at[i, column] = current_node.path[current_depth].name
                else:
                    lm_cost_anonymized.at[i, column] = current_node.path[current_node_depth].name
                if current_depth < current_node_depth:
                    lm_cost_raw.at[i, column] = current_node.path[current_depth + 1].name
                else:
                    lm_cost_raw.at[i, column] = current_node.path[current_node_depth].name

            score_list[copy_dataset.columns.get_loc(column)] = cost_LM(lm_cost_raw[column], lm_cost_anonymized[column], len(copy_dataset.columns), depths, current_column)
            current_column += 1
        scores = []
        for score in score_list:
            scores.append(score[0] - score[1])
        max_improve_column = scores.index(max(scores))
        column = copy_dataset.columns[max_improve_column]
        result = lm_cost_anonymized.copy()
        result = result.assign(**{column: lm_cost_raw[column].values})
        depths[max_improve_column] += 1
        eq_class_size = result.groupby(['gender','address','restaurant'], axis=0, as_index=False).size()['size']
        minSize = min(eq_class_size)
        current = minSize

    return result

'''
db_cursor.execute(SELECT * FROM Orders)
result2 = db_cursor.fetchall()
fieldnames2 = [i[0] for i in db_cursor.description]
df2 = pd.DataFrame(list(result2), columns=fieldnames2)
raw_dataset = read_dataset(df2, ['gender','address','restaurant'], ['cost'])
read_DGHs("DGHs")
anonymized_dataset = anonymizer(raw_dataset)
print(raw_dataset)
'''

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
    sql = '''SELECT * FROM Orders WHERE age = %(age)s'''
    db_cursor.execute(sql,{'age':'21'})
    result3 = db_cursor.fetchall()
    fieldnames2 = [i[0] for i in db_cursor.description]
    df3 = pd.DataFrame(list(result3), columns=fieldnames2)
    raw_dataset = read_dataset(df3, ['gender','address','restaurant'], ['cost'])
    read_DGHs("DGHs")
    anonymized_dataset = anonymizer(raw_dataset)
    print(anonymized_dataset)
    return {'content': apply_exponential_mechanism('gender',df1,0.5),'content2':private_histogram('age',df2,10,0.5), 'content3':anonymized_dataset.to_dict()}

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
    sql = '''SELECT * FROM Orders WHERE address = %(address)s'''
    db_cursor.execute(sql,{'address':'Narlidere'})
    result3 = db_cursor.fetchall()
    fieldnames3 = [i[0] for i in db_cursor.description]
    df3 = pd.DataFrame(list(result3), columns=fieldnames3)
    raw_dataset = read_dataset(df3, ['gender','address','restaurant'], ['cost'])
    read_DGHs("DGHs")
    anonymized_dataset = anonymizer(raw_dataset)
    print(anonymized_dataset)
    return {'content': apply_exponential_mechanism('address',df,2),'content2' : private_histogram('address',df2,1,2),'content3':anonymized_dataset.to_dict()}


@app.route("/users", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_users():
    sql = """ SELECT username,password,salt FROM Users """
    db_cursor.execute(sql)
    result = db_cursor.fetchall()
    print(result)
    return {'content': result}


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000, debug=True)