# -*- coding: utf-8 -*-

import os
import sys
from copy import deepcopy
import DataStructure
from CtypePyobjMapper import CtypePyobjMapper as cpmap
from multiprocessing import Lock
from multiprocessing.sharedctypes import Array
from GeneticAlgorithm import ApplyGA
from InitSimulation import *

# カレントと違うディレクトリからimportする
dirpath = os.path.dirname(os.path.abspath(__file__))
utildir = 'util'

sys.path.append(dirpath+'/'+utildir)

from test_util import test_settings
from graph_util import *
from check_util import *
from settings import utter_setting, get_rule_parameters


def insert_knowlwdge(G, SharedKnowledgeStructArray):
    """
    グラフ構造に共有メモリの内容を挿入する

    グラフも参照が渡されていることに注意

    *一応リバースしてから代入とか試してみる ok
    *incert前後でknowlede以外の値はすべて同じかどうかチェックする ok

    Parametars
    ----------
    G : networkx graph

    SharedKnowledgeStructArray : 共有メモリ

    Returns
    -------
    knowledge : Dict
    """

    mapper = cpmap()
    knowledge = mapper.c_to_p_convert(SharedKnowledgeStructArray)

    for k, v in sorted(knowledge.items()):
        G.node[k]['knowledge'] = v
    # print knowledge
    return knowledge


def graph2memory(G):
    """グラフ構造を受け取りknowledeだけ取り出し共有メモリに入れる
    >p_to_cを使えるようにするクッション関数

    Parameters
    ----------
    G : networkx graph

    Returns
    -------
    Shared Memory Array

    """

    knowledge_dict = {}
    mapper = cpmap()
    G_new = deepcopy(G)
    for n in G_new:
        knowledge_dict[n] = G_new.node[n]["knowledge"]

    lock = Lock()
    ctypes_knowledge_array = mapper.p_to_c_convert(knowledge_dict)

    # 共有メモリにデータを格納
    K = Array(DataStructure.KnowledgeStruct,
              ctypes_knowledge_array, lock=lock)
    return K
"""
if __name__ == "__main__":

    agent_size = 10
    SharedKnowledgeStructArray_Base = init_knowledge_array(agent_size)

    G = nx.barabasi_albert_graph(agent_size, 2)

    adding_node_attributes(G)
    # im.small_immigration(G, 0)  # color keyを登録するため一回通す

    nx.write_gpickle(G, "before.gpickle")

    # ctypesの構造体リストをアトリビュートに持たせる
    # k2 = insert_knowlwdge(G, SharedKnowledgeStructArray_Base)
    # print k2.keys()
    mapper = cpmap()
    k = mapper.c_to_p_convert(SharedKnowledgeStructArray_Base)
    a = ApplyGA(deepcopy(k))  # コピーしてわたさないと元も変わる
    a.start_ga()

    # GAの更新処理
    for x in k2:
        ApplyGA(k2[x])

    exit()

    a.start_ga()
    new_knowledge = a.new_generation_knowledge
    test = "spling"
    print k[1][0][test]["table"]
    print new_knowledge[1][0][test]["table"]
    exit()
    nx.write_gpickle(G, "after.gpickle")
    G_new = nx.read_gpickle("after.gpickle")
    adding_node_attributes(G_new)
    new_memory = graph2memory(G_new)
    print new_memory
    # check_memory(new_memory, SharedKnowledgeStructArray_Base)


    for x, s in zip(new_memory, SharedKnowledgeStructArray_Base):
        print "----------------------------------------"
        print x.id, s.id
        for y1, y2 in zip(x.words, s.words):
            print "******************************"
            check_fields(y1)
            check_fields(y2)
            print "******************************"
        print "----------------------------------------"
        exit()

    for x, y in zip(G, G_new):
        pass

        print "ID", G.node[x]["ID"] == G_new.node[x]["ID"]
        print "Nei", G.node[x]["Neighbors"] == G.node[x]["Neighbors"]
        Neibhorsはソートしてから比較すること
        print "key", G.node[x]["key"] == G_new.node[x]["key"]
        # print G.node[x]["utter_count"], G_new.node[x]["utter_count"]
"""
