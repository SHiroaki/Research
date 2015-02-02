# -*- coding: utf-8 -*-

from ctypes import *
import DataStructure
from multiprocessing import Lock
from multiprocessing.sharedctypes import Array


def verbgene():
    verbs = ["spling", "skring", "sprink", "cleed", "preed", "queed", "cloe",
             "froe", "plare", "quare"]
    verb = random.choice(verbs)
    return verb


def setting(gene_size, word_size, agent_size):
    """Make shared memory array.
    *** It used for test only. ***

    Parameters
    ----------
    gene_size : Int
                wordが持つgeneの数

    word_size : Int
                knowledge struct が持つwordの数

    agent_size : Int
               共有メモリarrayの持つknowledge struct の数

    固定した数のテストが終わったら,
    aget_size 以外はこの関数の中でランダムで決めてもいい

    Return
    ------

    K : shared memory array

    """

    p_bitarray1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    p_bitarray2 = [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
    p_bitarray3 = [1, 1, 1, 1, 1, 1, 1, 0, 1, 1]

    # pythonのlistをcの配列に変更
    c_bitarray1 = (c_int * len(p_bitarray1))(*p_bitarray1)
    c_bitarray2 = (c_int * len(p_bitarray2))(*p_bitarray2)
    c_bitarray3 = (c_int * len(p_bitarray3))(*p_bitarray3)
    c_bit = [c_bitarray1, c_bitarray2, c_bitarray3]

    # 配列の初期化
    InitGeneArray = (DataStructure.GeneStruct * gene_size)

    # インスタンスを作ってから値を代入する
    # 途中まで代入も可、開いている場所はすべて0
    import random
    c_gene_array = InitGeneArray()  # 必ずこれをすること

    for gene in c_gene_array[:23]:
        gene.bit_array = random.choice(c_bit)
        gene.score = random.randint(1, 5)
        gene.used = 1

    utterrance_size = 100
    heard_size = 100

    InitUtterArray = (DataStructure.Utterance * utterrance_size)
    utter_array = InitUtterArray()

    InitHeardArray = (DataStructure.Heard * heard_size)
    heard_array = InitHeardArray()

    genes = c_gene_array

    word = DataStructure.WordStruct("spling", "splung",
                                    0, 1, 1, 1000, 1000, 500,
                                    utter_array,
                                    heard_array,
                                    genes)

    word2 = DataStructure.WordStruct("foa", "foo",
                                     0, 1, 1, 500, 600, 400,
                                     utter_array,
                                     heard_array,
                                     genes)
    word3 = DataStructure.WordStruct("sing", "sang",
                                     0, 1, 1, 800, 700, 200,
                                     utter_array,
                                     heard_array,
                                     genes)

    p_word_array = [word, word2, word3]

    InitWordArray = (DataStructure.WordStruct * word_size)
    c_word_array = InitWordArray()

    for x, w in zip(c_word_array, p_word_array):
        #  tm = random.choice(p_word_array)
        tm = w
        v = [getattr(tm, field_name) for field_name, field_type
             in tm._fields_]
        index = 0
        for field_name, field_type in x._fields_:
            setattr(x, field_name, v[index])
            index += 1
    """
    for x in c_word_array:
        for field_name, field_type in x._fields_:
            print field_name, getattr(x, field_name)
    """

    lock = Lock()

    # Kを共有メモリとする,この方法で良さそう
    K = Array(DataStructure.KnowledgeStruct, agent_size, lock=lock)

    utter_number = 100  # 発話する回数

    # 共有メモリに擬似データを格納する
    for i, agent in enumerate(K):
        agent.id = i
        agent.communicate = utter_number
        agent.words = c_word_array

    return K

"""
if __name__ == '__main__':
    f = setting(50, 100, 2)
"""
