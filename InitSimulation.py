# -*- coding: utf-8 -*-

import os
import sys
from ctypes import c_int
import DataStructure
import cbinarymethods as cbm
from multiprocessing import Lock
from multiprocessing.sharedctypes import Array
import cPickle as pickle
import random as rand

dirpath = os.path.dirname(os.path.abspath(__file__))
utildir = 'util'

sys.path.append(dirpath+'/'+utildir)

from settings import read_verbdict, set_verb_frequency
from settings import wrap_init_table, StructureSize
# from check_util import *


class InitSimulation(object):
    """
    シミュレーションの初期化スクリプト
    共有メモリに配置するまでの処理を行う
    !!!一回しか呼ぶな!!!

    Parameters
    ----------
    N : agent size

    Returns
    -------
    K : 共有メモリ

    """

    def __init__(self):
        print "Im init"
        # 使用する単語の原形と過去形を読み込む
        self.use_verbs = read_verbdict()

        # 使用する単語の頻度
        self.use_verbs_freq = set_verb_frequency()
        print self.use_verbs_freq
        f = open('verb_freq.dump', 'w')
        pickle.dump(self.use_verbs_freq, f)
        f.close()

        # 単語のルールテーブルを読み込む
        self.word_and_rule = wrap_init_table()
        # 保存して各プロセスから使えるようにする
        f = open('rules.dump', 'w')
        pickle.dump(self.word_and_rule, f)
        f.close()

        # 最も頻度が高い単語５つを選ぶ
        self.most_freq_verbs = self.get_most_freqent()
        # 保存して各プロセスから使えるようにする
        f = open('most_freq.dump', 'w')
        pickle.dump(self.most_freq_verbs, f)
        f.close()

    def get_most_freqent(self):
        # 頻度の上位5単語を探す
        most_freq = [100000, 10000]
        most_freq_verbs = []
        for v, f in self.use_verbs_freq.items():
            if f in most_freq:
                most_freq_verbs.append(v)
        return most_freq_verbs

    def init_rule_array(self):
        """
        単語のルールテーブルを初期化する
        ルールテーブルサイズの文だけbit列を生成するし,
        そのbit列をscore, usedとともに構造体に配置する

        Returns
        -------
        c_gene_array : Cの配列

        """

        bit_array_size = StructureSize.bit_array_size
        table_size = StructureSize.table_array_size
        int_list = [x for x in xrange(table_size)]
        table_bit_list = map(cbm.value2binary, int_list)
        # print len(int_list)
        # Cの配列のリストに変換する
        p_cbinary_list = [
            (c_int * bit_array_size)(*bit_array)
            for bit_array in table_bit_list]

        # Geneのデータ構造をtableサイズ分だけつくる
        init_score = 0
        init_used = 0
        p_gene_list = []

        for cbi in p_cbinary_list:
            c_gene = DataStructure.GeneStruct()
            setattr(c_gene, "bit_array", cbi)
            setattr(c_gene, "score", init_score)
            setattr(c_gene, "used", init_used)
            p_gene_list.append(c_gene)

        # Gene構造体のリストをCの配列に変換する
        c_gene_array = (DataStructure.GeneStruct * table_size)(
            *p_gene_list)
        """
        for x in c_gene_array:
            for field_name, field_type in x._fields_:
                print field_name, getattr(x, field_name)
            print [y for y in x.bit_array]
        """
        return c_gene_array

    def init_word_array(self):
        """
        単語のデータ構造を初期化する
        gene, utter, heardは使わないが念の為初期化だけはしておく

        Returns
        -------
        c_word_array : 55単語すべての構造体配列

        """
        gene_size = StructureSize.gene_array_size
        InitGeneArray = (DataStructure.GeneStruct * gene_size)
        gene_array = InitGeneArray()

        utterrance_size = StructureSize.utter_array_size
        heard_size = StructureSize.heard_array_size

        InitUtterArray = (DataStructure.Utterance * utterrance_size)
        utter_array = InitUtterArray()

        InitHeardArray = (DataStructure.Heard * heard_size)
        heard_array = InitHeardArray()

        # heard, utterは0で初期化
        for x, y in zip(heard_array, utter_array):
            x.heard = "0"
            y.utter = "0"

        init_understand = 0
        init_active = 1
        init_past_life = 0

        p_word_array = []
        # 各フィールドに値を挿入していく

        for stem, past in self.use_verbs.items():
            if stem not in self.most_freq_verbs:
                word_struct = DataStructure.WordStruct()
                setattr(word_struct, "stem", stem)
                setattr(word_struct, "past", past)
                setattr(word_struct, "understand", init_understand)
                setattr(word_struct, "freq",
                        self.use_verbs_freq[stem])
                setattr(word_struct, "active", init_active)
                setattr(word_struct, "past_life", init_past_life)
                setattr(word_struct, "utter", utter_array)
                setattr(word_struct, "heard", heard_array)
                setattr(word_struct, "table", self.init_rule_array())
                setattr(word_struct, "gene", gene_array)
                p_word_array.append(word_struct)

        # Cの配列に変換する
        word_size = StructureSize.word_array_size
        c_word_array = (DataStructure.WordStruct * word_size)(*p_word_array)

        return c_word_array


def init_knowledge_array(agent_size):

    """agent_sizeにしたがって共有メモリ配列を作成する
    """
    init_methods = InitSimulation()
    p_knowledge_array = []
    init_communicate = 0

    for i in xrange(agent_size):
        c_knowledge = DataStructure.KnowledgeStruct()
        setattr(c_knowledge, "id", i)
        setattr(c_knowledge, "words", init_methods.init_word_array())
        setattr(c_knowledge, "communicate", init_communicate)
        p_knowledge_array.append(c_knowledge)

    c_knowledge_array = (
        DataStructure.KnowledgeStruct * agent_size
    )(*p_knowledge_array)

    lock = Lock()
    # 共有メモリにデータを格納する
    K = Array(DataStructure.KnowledgeStruct,
              c_knowledge_array, lock=lock)
    return K
