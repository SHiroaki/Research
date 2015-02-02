# -*- coding: utf-8 -*-

import os
import sys
from multiprocessing import Pool
from deap import base, creator, tools
import DataStructure
from copy import deepcopy
import time
import cbinarymethods as cbm
from random import randint
import numpy as np

# カレントと違うディレクトリからimportする
dirpath = os.path.dirname(os.path.abspath(__file__))
utildir = 'util'

sys.path.append(dirpath+'/'+utildir)

from settings import *
from random_pick import random_weight_pick as randpick


def get_array_info(data):
    # とりあえずgeneのbitとスコアを返しておく
    # gene_array = data["gene"]
    table_array = data["table"]

    # gene_bit_score_array = [(x[0][1], x[1][1]) for x in gene_array]
    table_bit_score_array = [(x[0][1], x[1][1]) for x in table_array]

    return table_bit_score_array


def create_population(container, array):
    pop = [container(x) for x in array]
    return pop


def ga(stem, data):
    """GAを行う

    Parameters
    ----------
    stem : 動詞の語幹

    data : stemのtableとgeneのタプル

    Return : (stem, 新しい染色体)
    """

    # Init GA
    CXPB, MUTPB = 0.6, 0.02  # 0.5->0.1 CXPBが0.1, 0.6でうまく行った
    # 評価関数が最大の組み合わせを求めるからweights=1
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # 個体群の初期化
    toolbox = base.Toolbox()
    toolbox.register("array", get_array_info, data)
    base_array = toolbox.array()
    bit_array = [x[0] for x in base_array]
    pop = create_population(creator.Individual, bit_array)
    # print "init", stem, pop ok
    # Operationの初期化
    toolbox.register("mate", tools.cxUniform)  # 一様交叉
    # ルーレット選択だと全く選ばれないので
    toolbox.register("select", tools.selTournament, tournsize=2)  # 2-> 4
    toolbox.register("select_random", tools.selRandom)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    # print len(pop)
    # リストから個体の評価値をとってくる
    fitnesses = [(x[1], ) for x in base_array]
    # fitnesses = [(2, ) for x in base_array]

    """
    リスト内の値がすべて0の時は一度も発話されていない単語.
    ルールテーブルを徐々に均等割りにするようなスケーリングを行う.
    世代を減るごとにスケーリングの効き具合を強くしていく.
    つまり各単語は発話のされなかった世代数のカウンタを持っていて
    大きくなればスケーリングは強く働く.発話されればクリアされる.
    この仕組みはutterとかのフィールドに書き込んでおく
    一定でいいとおもう
    ここは最後に作る
    """

    # 非同期でやるとpopのサイズが変わっていることがある
    # それに点数が全然ついていない
    # 個体群の評価(染色体についている点数をそのまま評価値とする)
    # print stem
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        # print stem, ind, ind.fitness.values
    # print pop, fitnesses

    # 次世代の個体群を選択
    # ルーレット選択の場合点数が0だと一つも選択されない
    if np.sum(fitnesses) == 0:
        # 一回も発話されていない単語はそのままテーブルを返す
        offspring = toolbox.select_random(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))
        # 次世代群をoffspringにする
        pop[:] = offspring
        pop = [list(x) for x in pop]

        return stem, pop

    else:
        offspring = toolbox.select(pop, len(pop))
        """
        for off in offspring:
            print stem, "after select :", off
        """

    # 個体群のクローンを生成
    offspring = list(map(toolbox.clone, offspring))

    # 選択した個体群に交差と突然変異を適応する
    # 偶数番目と奇数番目の個体を取り出して交差
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CXPB:
            toolbox.mate(child1, child2, CXPB)
            del child1.fitness.values
            del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

    # 次世代群をoffspringにする
    pop[:] = offspring
    pop = [list(x) for x in pop]
    """
    for p in pop:
        print "next", stem, p
    """
    return stem, pop


def wrapper_ga(args):
    # 並列処理時に複数の引数を渡す
    return ga(*args)


class ApplyGA(object):
    """
    GAを行うときに呼ばれる

    Parameters
    ----------

    knowledge_dict : All Agent knowledge dict

    Returns
    -------

    new_knowledge : After applying GA knowledge dict

    """

    def __init__(self, knowledge_dict):

        self.knowledge_dict = knowledge_dict
        self.genetic_operation = wrapper_ga
        # self.genetic_operation = ga
        self.make_gene_tuple = make_gene_tuple
        self.new_generation_knowledge = {}
        self.results = []

    def start_ga(self):
        # エージェントごとに単語を取り出してGAにかける
        for agent, knowledge_tuple in self.knowledge_dict.items():
            self.knowledge = knowledge_tuple[0]  # 単語辞書
            self.communication = knowledge_tuple[1]  # コミュニケーション数
            self.agent_id = agent
            # 単語辞書を取り出す
            wd = self.make_word_list(self.knowledge)
            agents_next_table = self.applyGA(wd)
            self.set_next_table(agents_next_table)

    def make_word_list(self, knowledge):
        # すべての単語の辞書を作る.asyncに投げるデータ
        # d = { str(x):x*3 for x in range(10) }
        need = ("table",)

        word_dict = {}

        for k, v in knowledge.items():
            values = {}
            for fn, fv in v.items():
                if fn in need:
                    values[fn] = [x[:2] for x in fv]  # used, geneは要らない
            word_dict[k] = values

        return word_dict

    def collect_results(result):
        self.results.extend(result)

    def applyGA(self, agents_word_dict):

        pool = Pool()
        next_table = []
        # クラスタならmapの方が早い
        TASKS = [(stem, data) for stem, data in agents_word_dict.items()]
        # これでデバッグしろ.ちゃんと値がついているか確認
        """
        for t in TASKS:
            next_table.append(self.genetic_operation(t))
        """

        self.results = pool.map_async(self.genetic_operation, TASKS)
        """
        for t in TASKS:
            pool.apply_async(
                self.genetic_operation, args=(t,),
                callback=self.collect_results)

        results = [pool.apply_async(self.genetic_operation, t)
                   for t in TASKS]

        next_table = [result.get() for result in results]
        """
        pool.close()
        pool.join()
        # d = {str(x): y for x, y in next_table}
        d = {str(x): y for x, y in self.results.get()}

        return d

    def set_next_table(self, table):
        # エージェントの単語辞書に新しいテーブルを挿入する
        field_names = [x[0] for x in DataStructure.GeneStruct._fields_]
        stems = table.keys()

        template = [[x, 0] for x in field_names]  # usedも0になるから注意

        for s in stems:
            wd = deepcopy(self.knowledge[s])
            stem_bit_arrays = table[s]
            gene_tuples = self.make_gene_tuple(
                stem_bit_arrays, template)
            # 前世代の染色体を次世代の染色体と入れ替える
            wd["table"] = gene_tuples
            # print self.knowledge[s]["table"]
            self.knowledge[s] = wd
            # print self.knowledge[s]["table"]

        self.new_generation_knowledge[self.agent_id] = deepcopy(
            (self.knowledge, self.communication))


def make_gene_tuple(bit_arrays, template):
    tup = []
    for x in bit_arrays:
        t = deepcopy(template)
        t[0][1] = x
        t = [tuple(y) for y in t]
        tup.append(tuple(t))
    return tup

"""
def main():

    a = Agent()
    exit()
    d = set_verb_frequency()

    utters = [randpick(d) for x in xrange(200)]

    d2 = {}
    for c in utters:
        d2[c] = d.get(c, 0) + 1
    print d2, len(d2)

if __name__ == '__main__':
    main()
"""
