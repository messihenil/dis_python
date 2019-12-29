import networkx as nx
import matplotlib.pyplot as plt
import nltk
from nltk import word_tokenize, sent_tokenize
import mysql.connector

myconn = mysql.connector.connect(host="localhost", user="root", passwd="", database="concept_map")
cur = myconn.cursor()
cur1 = myconn.cursor()
cur2 = myconn.cursor()
G = nx.DiGraph()
f = open("coref.txt", "rt")
string = f.read()
patt_arr = ['is', 'implemented', 'having', 'and', 'provides', 'but', 'found', 'in', 'allows', 'maintains', 'contains']
a = "a"
an = "an"
the = "the"
sent_tok = sent_tokenize(string)
root = ""
cnt = 1

def checkNode(node_text):
    sql = "select count(*) from nodes where nodename = %s"
    cur = myconn.cursor(prepared=True)
    cur.execute(sql, (node_text,))
    result = cur.fetchone()
    if result[0] > 0:  
        return 0
    else:
        return 1
    
for s in sent_tok:
    word_tok = word_tokenize(s)
    lst = []
    for w in word_tok:
        if not (w == a or w == an or w == the):
            lst.append(w)
    print(lst)
    d = dict(nltk.pos_tag(lst))
    #print(d)
    
    for w in lst:
        v = list()
        k = list()
        for key, value in d.items():                
            k.append(key)
            v.append(value)
        for index, key in enumerate(d):
            if key in patt_arr:
                if v[index - 1] == "NN" or v[index - 1] == "NNS" or v[index - 1] == "NNP":
                    if root == "":
                        root = k[index - 1]
                        cur.execute("DELETE from nodes")
                        myconn.commit()
                        sql = "INSERT INTO `nodes`(`fromNode`, `nodename`, `toNode`) VALUES (%s,%s,%s)"
                        cur.execute(sql,(0, root, 0))
                        myconn.commit()
                if v[index + 1] == "NN" and v[index + 2] == "IN" and (
                        v[index + 3] == "NNS" or v[index + 3] == "NN"):
                    second_root = k[index + 1] + '\n' + k[index + 2] + '\n' + k[index + 3]
                    i = checkNode(second_root)
                    if(i == 1):
                        sql = "INSERT INTO `nodes`(`fromNode`, `nodename`, `toNode`) VALUES (%s,%s,%s)"
                        cur.execute(sql, (0, second_root, cnt))
                        cnt+=1
                        myconn.commit()
                    second_root = ""
                elif v[index + 1] == "JJ" and (v[index + 2] == "JJ" or v[index + 2] == "NNS"):
                    third_root = k[index + 1] + '\n' + k[index + 2]
                    i = checkNode(third_root)
                    if(i == 1):
                        sql = "INSERT INTO `nodes`(`fromNode`, `nodename`, `toNode`) VALUES (%s,%s,%s)"
                        cur.execute(sql, (cnt-1, third_root, 0))
                        myconn.commit()
                    third_root = ""
                elif v[index + 1] == "JJ" and ((v[index + 2] == "IN" and v[index + 3] == "NN") or (v[index + 2] == "NN")):
                    if v[index + 2] == "NN":
                        second_root = k[index + 1] + '\n' + k[index + 2]
                    else:
                        second_root = k[index + 1] + '\n' + k[index + 2] + '\n' + k[index + 3]
                    i = checkNode(second_root)
                    if(i == 1):
                        sql = "INSERT INTO `nodes`(`fromNode`, `nodename`, `toNode`) VALUES (%s,%s,%s)"
                        cur.execute(sql, (0, second_root, cnt))
                        cnt+=1
                        myconn.commit()
                    second_root = ""
                elif v[index + 1] == "VBN" and v[index + 2] == "NN":
                    second_root = k[index + 1] + '\n' + k[index + 2]
                    i = checkNode(second_root)
                    if(i == 1):
                        sql = "INSERT INTO `nodes`(`fromNode`, `nodename`, `toNode`) VALUES (%s,%s,%s)"
                        cur.execute(sql, (0, second_root, cnt))
                        cnt+=1
                        myconn.commit()
                    second_root = ""

sql = "select nodename from nodes where fromNode = %s and toNode = %s"
cur.execute(sql, (0,0))
result = cur.fetchone()
if result[0] != "":  
    root = result[0]
    G.add_node(root)
    
cur.execute("select toNode, nodename from nodes where fromNode = 0 and toNode <> 0")
result1 = cur.fetchall()
for x in result1:
    c = x[0]
    node = x[1]
    G.add_node(node)
    G.add_edge(root, node)
    sql1 = "select nodename from nodes where fromNode = %s"
    cur.execute(sql1,(c,))
    result2 = cur.fetchone()
    if result2 != None:
        sub_node = result2[0]
    if sub_node != "":
        G.add_node(sub_node)
        G.add_edge(node, sub_node)
        sub_node = ""

nx.draw(G, node_size=1000, edge_color = 'green', edge_height = 500, edge_width = 500, node_color = 'white', node_width = 1000, with_labels = True, width = 2)
plt.savefig("db2.png")