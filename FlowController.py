# -*- coding: utf-8 -*-

import os
import sys
from InitSimulation import *
from multiprocessing import Process, Queue, cpu_count
import memorymap
import numpy as np
import networkx as nx
from comunication import comunicate
import cPickle as pickle
from CtypePyobjMapper import CtypePyobjMapper as cpmap
from copy import deepcopy
from GeneticAlgorithm import ApplyGA
from multiprocessing import Lock
from multiprocessing.sharedctypes import Array

dirpath = os.path.dirname(os.path.abspath(__file__))
utildir = 'util'

sys.path.append(dirpath+'/'+utildir)

from test_util import test_settings
from settings import *
from check_util import *
from plot_methods import *
from graph_util import *

agent_size = 12
mapper = cpmap()


class FlowController(object):
    """
    """
    def __init__(self, Gen):
        self.comunicate = comunicate
        self.agents = []
        self.GEN = Gen

    def utterance_scheduler(self, q):
        """Make utterance.

        Make uttarance of agents.
        Choice any agent A and one of it's neighbors B, and choice any verb V
        in Agent A's knowledge(Lexicon and Active memory).
        So, it means that Agent A comunicate B use verb V.

        本番は使う動詞もserverで呼び出された時に選ぶようにする
        ここでDBの更新処理を行う

        *** Refresh counter of verb V in Agent A, B(if in knowledge) **
        あとで作る

        Parameters
        ----------
        Graph : Netwokx graph
            Use node ID as Agent name.

        q : Queue
            Multiprocess Queue


        Put
        ---
        list : utterance parameters
            [Agent name, Agent name, verb]

        """
        # 発話スケジュール設定
        shcedule_dict = {}
        finished_utter_count = {}

        """
        for n in self.G:
            print self.G.node[n]["ID"], self.G.node[n]["Neighbors"]
        """

        uc = utter_setting()

        G = self.G  # グラフ構造を受け取る
        for x in G:
            # だれに何回発話するか
            utter_count_dict = {str(x): uc for x in
                                G.node[x]["Neighbors"]}
            shcedule_dict[x] = utter_count_dict
            finished_utter_count[x] = G.node[x]["utter_count"]

        # 発話エージェントを選ぶ 100agent : 1(s), 1000agent:20(s)
        while True:

            utterancable = [x for x in finished_utter_count.keys()
                            if finished_utter_count[x] > 0]
            if len(utterancable) == 0:
                break
            # ランダム抽出(重複なし)
            agent = np.random.choice(utterancable, 1, replace=False)
            finished_utter_count[agent[0]] -= 1

            # 聞き手エージェントを選ぶ
            listeners = [x for x in shcedule_dict[agent[0]].keys()
                         if shcedule_dict[agent[0]][x] > 0]

            if len(listeners) == 0:
                # この状況は起きないけど念の為
                continue

            listener = np.random.choice(listeners, 1, replace=False)
            shcedule_dict[agent[0]][listener[0]] -= 1

            query = [int(agent[0]), int(listener[0])]

            q.put(query)

            # os.kill(os.getpid(), signal.SIGTERM)

    def server(self, SharedKnowledgeStructArray, rules, most_freq,
               verb_freq, g):
        """Start server

        Server get uttarance parameters from Queue, and boot comunication
        process.

        """

        q = Queue()
        p = Process(target=self.utterance_scheduler, args=(q,))

        # スケジューラプロセス起動
        p.start()

        while True:
            # どうやって効率よくQueueがemptyなことを判断するか
            # もしくは発話の回数を予め調べておいてfor文で実行するか
            processes = []

            # プロセスを作成
            for x in xrange(cpu_count() / 2):
                param = q.get()
                # self.agents.append(param[0])
                # print param

                processes.append(
                    Process(target=self.comunicate,
                            args=(param,
                                  SharedKnowledgeStructArray,
                                  rules,
                                  most_freq,
                                  verb_freq)
                            )
                    )
            # コミュニケーションプロセスを起動
            [x.start() for x in processes]

            # コミュニケーションプロセスの終了を待つ
            [x.join() for x in processes]

            if q.empty():
                break

        p.join()

        # 評価語の共有メモリを辞書に変換しGAにかける
        k = SharedKnowledgeStructArray
        # SharedKnowledgeStructArrayとkは同じものを指している
        scored_verb = []
        """
        for x in SharedKnowledgeStructArray:
            print g, "----------------------------------------"
            print "ID", x.id
            for y in x.words:
                ta = y.table
                for g in ta:
                    if g.score > 0:
                        scored_verb.append(y.stem)
                        print(y.stem, y.freq, g.score,
                              cbm.binary2value([b for b in g.bit_array]),
                              [b for b in g.bit_array])
        """
        k_dic = mapper.c_to_p_convert(k)

        """
        fname = str(g) + "k_dic.dump"
        f = open(fname, "w")
        pickle.dump(k_dic, f)
        f.close()
        """
        ga = ApplyGA(k_dic)
        ga.start_ga()
        new_knowledge = ga.new_generation_knowledge
        scored_verb = list(set(scored_verb))
        # print scored_verb

        """
        for agent, v in new_knowledge.items():
            print "----------------------------------------"
            print "ID", agent
            if agent != 0:
                break
            for stem, y in v[0].items():
                if stem in scored_verb:
                    print "******************************"
                    print stem
                    for filed_name, table_array in y.items():
                        if filed_name == "table":
                            for g in table_array:
                                print cbm.binary2value(g[0][1])
        """

        return new_knowledge

    def simulation(self):
        """start simulation.
        """
        # グラフ構造を作成
        self.G = nx.barabasi_albert_graph(agent_size, 2)
        # self.G = nx.complete_graph(agent_size)
        adding_node_attributes(self.G)
        plot_figure(self.G, "penatest", "png")

        # 共有メモリの準備(1世代目だけ)
        SharedKnowledgeStructArray = init_knowledge_array(agent_size)

        # 全世代を通してルールテーブルが表す母音と高頻度単語は共通
        # なのでdumpして保存しておく.使用する場合は読み込んで
        f = open('rules.dump')
        rules = pickle.load(f)
        rd = pickle.dumps(rules)
        f.close()

        f = open('most_freq.dump')
        freq_verbs = pickle.load(f)
        f.close()

        f = open('verb_freq.dump')
        freq_of_verbs = pickle.load(f)
        fv = pickle.dumps(freq_of_verbs)
        f.close()

        result = {}
        # １世代目だけ別で行う
        print("-- Generation %i --" % 0)
        knowledge_dict = self.server(
            SharedKnowledgeStructArray, rd, freq_verbs, fv, 0)

        # c_knowledge_array = mapper.p_to_c_convert(knowledge_dict)
        result[0] = deepcopy(knowledge_dict)

        lock = Lock()

        for g in xrange(self.GEN-1):
            g = g + 1
            print("-- Generation %i --" % g)
            c_knowledge_array = mapper.p_to_c_convert(knowledge_dict)
            # 共有メモリにデータを格納
            K = Array(DataStructure.KnowledgeStruct,
                      c_knowledge_array, lock=lock)
            knowledge_dict = self.server(K, rd, freq_verbs, fv, g)
            # print type(knowledge_dict)
            result[g] = deepcopy(knowledge_dict)

        f = open("BA12Agent_100gen_100utter.dump", "w")
        pickle.dump(result, f)
        f.close()

if __name__ == '__main__':
    # 世代
    GEN = 50
    f = FlowController(GEN)
    f.simulation()
