#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx
import matplotlib.pyplot as plt
import nltk
from nltk import word_tokenize, sent_tokenize

def doGraph(string, G):
    root = ""
    second_root = ""
    third_root = ""
    img = 1
    wtok = word_tokenize(string)
    d = dict(nltk.pos_tag(wtok))
    isCD = True

    patt_arr = ['is', 'implemented', 'having', 'and', 'provides', 'but']

    nums = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
    r = dict(map(reversed, d.items()))
    for key, value in nums.items():
        isCD = "'", value, "'" in string

    if isCD == True:
        edge_cnt = nums[r['CD'].lower()]
        nodes = []
        for (key, value) in d.items():
            if value == "NNS" or value == "IN" or value == "JJ":
                root += key + " \n"  # adding root element
            elif value == "JJ" or value == "NN":
                nodes.append(key)  # adding leaf nodes

        G.add_node(root)
        for i in nodes:
            G.add_node(i)
            G.add_edge(root, i)
    else:
        v = list()
        k = list()
        for key, value in d.items():
            k.append(key)
            v.append(value)
        for index, key in enumerate(d):
            if key in patt_arr:
                print(index, " => ", key, " => ", d[key])
                if v[index - 1] == "NN" or v[index - 1] == "NNS" or v[index - 1] == "NNP":
                    #print("\nPrev Grammar : ", v[index - 1], "\nNext Grammar : ", v[index + 1], "\n")
                    if root == "":
                        root = k[index - 1]
                        G.add_node(root)

                    if v[index + 1] == "NN" and v[index + 2] == "IN" and (v[index + 3] == "NNS" or v[index + 3] == "NN"):
                        second_root = k[index + 1] + '\n' + k[index + 2] + '\n' + k[index + 3]
                        if second_root != "":
                            G.add_node(second_root)
                            G.add_edge(root, second_root)
                        second_root = ""
                    elif v[index + 1] == "JJ" and (v[index + 2] == "JJ" or v[index + 2] == "NNS"):
                        third_root = k[index + 1] + '\n' + k[index + 2]
                        if third_root != "":
                            G.add_node(third_root)
                            if second_root != "":
                                G.add_edge(second_root, third_root)
                            else:
                                G.add_edge(root, third_root)
                        third_root = ""
                    elif v[index + 1] == "JJ" and v[index + 2] == "IN" and v[index + 3] == "NN":
                        second_root = k[index + 1] + '\n' + k[index + 2] + '\n' + k[index + 3]
                        if second_root != "":
                            G.add_node(second_root)
                            G.add_edge(root, second_root)
                        second_root = ""
            #else:
                #print(index, " => ", key, " => ", d[key])
        print("\n", d)
        print(second_root if second_root != "" else "")
        print(third_root if third_root != "" else "")
        nx.draw(G, node_size=1000, edge_color = 'red', edge_width = 500, node_width = 700, node_color = 'white', with_labels = True, width = 2)
        i1 = "img"
        i2 = ".png"
        c = i1 + str(img_cnt) + i2
        plt.savefig(c)
        
    
f = open("coref.txt", "rt")
string = f.read()
img_cnt = 0
sent_tok = sent_tokenize(string)
#G = [10]
l = [None] * 10
for s in sent_tok:
    l[img_cnt] = nx.DiGraph()
    doGraph(s, l[img_cnt])
    img_cnt += 1

