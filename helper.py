import sqlite3
import time
from datetime import datetime
import random
#To run program , write the following in the terminal 'pip install geopy networkx numpy'
import networkx as nx
from geopy import distance
import numpy as np
import sys

#If near by 5 miles or 30 mins
# print(sys.argv)
recieved_name = sys.argv[1]
recieved_Date = sys.argv[2]
recieved_Db_name = "LifeMap_"+recieved_name+".db"
# recieved_name = "GS12"
subject_names = ["GS1","GS2","GS3","GS4","GS5","GS6","GS7","GS8","GS9","GS10","GS11","GS12"]
dbNames = ["LifeMap_GS1.db","LifeMap_GS2.db","LifeMap_GS3.db","LifeMap_GS4.db","LifeMap_GS5.db","LifeMap_GS6.db","LifeMap_GS7.db","LifeMap_GS8.db","LifeMap_GS9.db","LifeMap_GS10.db","LifeMap_GS11.db","LifeMap_GS12.db"]
dbNames.remove(recieved_Db_name)
subject_names.remove(recieved_name)
userLocations = []
tempLocations = []
userTimes = []
tempTimes = []
conn = sqlite3.connect(recieved_Db_name)
conn.text_factory = str
cur = conn.cursor()

graph = nx.Graph()
graph.add_nodes_from(subject_names)

def read_from_db():
    cur.execute('SELECT * FROM locationTable')
    initData = cur.fetchall()
    for row in initData:
        userLocations.append((row[1]*10**-6,row[2]*10**-6))
    # print (userLocations)
    for id,x in enumerate(dbNames):
        conn = sqlite3.connect(x)
        cur.execute('SELECT * FROM locationTable')
        tempData = cur.fetchall()
        for row in initData:
            tempLocations.append((row[1]*10**-6,row[2]*10**-6))
        for mainrow in userLocations:
            for tempRow in tempLocations:
                if distance.distance(mainrow,tempRow).miles < 5:
                    graph.add_edge(recieved_name,subject_names[id])
        tempLocations.clear()

#Function to parse time data from the DB and check the
def read_time_from_db():
    cur.execute('SELECT * FROM stayTable')
    initData = cur.fetchall()
    for row in initData:
        userTimes.append((row[3],row[4]))
    # print(userTimes)
    for id, x in enumerate(dbNames):
        conn = sqlite3.connect(x)
        cur.execute('SELECT * FROM stayTable')
        tempTimeTable = cur.fetchall()
        for row in tempTimeTable:
            tempTimes.append((row[3],row[4]))
        for mainRowT1, mainRowT2 in userTimes:
            for tempRowT1, tempRowT2 in tempTimes:
                t1User = datetime.strptime(mainRowT1,'%Y%m%d%H%M%S%a')
                t2User = datetime.strptime(mainRowT2,'%Y%m%d%H%M%S%a')
                t1Temp = datetime.strptime(tempRowT1,'%Y%m%d%H%M%S%a')
                t2Temp = datetime.strptime(tempRowT2,'%Y%m%d%H%M%S%a')
                userDiff = t2User - t1User
                tempDiff = t2Temp - t1Temp
                secInDay = 24*60*60
                q, userSecDiff = divmod(userDiff.days*secInDay + userDiff.seconds,60)
                p, tempSecDiff = divmod(tempDiff.days*secInDay + tempDiff.seconds, 60)
                if (tempSecDiff - userSecDiff) < 30:
                    graph.add_edge(recieved_name,subject_names[id])

read_from_db()
read_time_from_db()
# conn.close()
# cur.close()
print("Nodes")
print(graph.nodes())
print("Edges")
print(graph.edges())
Adjacency_matrix = nx.adjacency_matrix(graph)
with open('Adjacency_matrix.txt','wb') as f:
    for line in Adjacency_matrix:
        np.savetxt(f, line, fmt='%.2f')
