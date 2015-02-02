# -*- coding: utf-8 -*-

import random
from ctypes import *
import DataStructure
import cbinarymethods as cbm
from multiprocessing import Lock
from multiprocessing.sharedctypes import Array
from settings import StructureSize
from check_util import check_fields


def test_settings(agent_size):
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

    b = cbm.value2binary(3)
    p = cbm.binary2value(b)
    print p
    exit()
    """

    p_bitarray1 = [1, 1, 1, 0, 1, 0, 0]
    p_bitarray2 = [1, 1, 0, 1, 1, 0, 1]
    p_bitarray3 = [1, 0, 1, 1, 1, 1, 1]

    # ルールテーブルの染色体を初期化
    table_size = StructureSize.table_array_size
    table_list = []
    for x in xrange(table_size):
        p_binary = cbm.value2binary(x)
        c_binary = (c_int * len(p_binary))(*p_binary)
        table_list.append(c_binary)

    # pythonのlistをcの配列に変更
    c_bitarray1 = (c_int * len(p_bitarray1))(*p_bitarray1)
    c_bitarray2 = (c_int * len(p_bitarray2))(*p_bitarray2)
    c_bitarray3 = (c_int * len(p_bitarray3))(*p_bitarray3)
    c_bit = [c_bitarray1, c_bitarray2, c_bitarray3]

    # 染色体配列の初期化
    gene_size = StructureSize.gene_array_size
    InitGeneArray = (DataStructure.GeneStruct * gene_size)
    InitTableArray = (DataStructure.GeneStruct * table_size)

    # インスタンスを作ってから値を代入する
    # 途中まで代入も可、開いている場所はすべて0

    c_gene_array = InitGeneArray()  # 必ずこれをすること
    c_table_array = InitTableArray()

    # ルールテーブルに(染色体)ビット列を配置する
    for t, bit in zip(c_table_array, table_list):
        t.bit_array = bit
        t.score = random.randint(1, 4)
        t.used = 1

    for gene in c_gene_array:
        gene.bit_array = random.choice(c_bit)
        gene.score = random.randint(1, 5)
        gene.used = 1

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

    genes = c_gene_array
    table = c_table_array

    word = DataStructure.WordStruct("spling",
                                    "splung",
                                    0, 1, 1, 1000,
                                    utter_array,
                                    heard_array,
                                    table, genes)

    word2 = DataStructure.WordStruct("foa",
                                     "foo",
                                     0, 1, 1, 500,
                                     utter_array,
                                     heard_array,
                                     table, genes)
    word3 = DataStructure.WordStruct("sing",
                                     "sang",
                                     0, 1, 1, 800,
                                     utter_array,
                                     heard_array,
                                     table, genes)

    word4 = DataStructure.WordStruct("pick",
                                     "puck",
                                     0, 1, 1, 890,
                                     utter_array,
                                     heard_array,
                                     table, genes)

    word5 = DataStructure.WordStruct("cloe",
                                     "cloo",
                                     0, 1, 1, 80,
                                     utter_array,
                                     heard_array,
                                     table, genes)

    word6 = DataStructure.WordStruct("cloe",
                                     "cloa",
                                     0, 1, 1, 80,
                                     utter_array,
                                     heard_array,
                                     table, genes)

    p_word_array = [word, word2, word3, word4, word5]
    p_word_array2 = [word, word2, word3, word4, word6]

    word_size = StructureSize.word_array_size
    # InitWordArray = (DataStructure.WordStruct * word_size)
    # c_word_array = InitWordArray()
    # c_word_array2 = InitWordArray()

    c_word_array = (DataStructure.WordStruct * word_size)(*p_word_array)
    c_word_array2 = (DataStructure.WordStruct * word_size)(*p_word_array2)

    """
    for x, w in zip(c_word_array, p_word_array):
        #  tm = random.choice(p_word_array)
        tm = w
        v = [getattr(tm, field_name) for field_name, field_type
             in tm._fields_]
        index = 0
        for field_name, field_type in x._fields_:
            setattr(x, field_name, v[index])
            index += 1

    for x, w in zip(c_word_array2, p_word_array2):
        #  tm = random.choice(p_word_array)
        tm = w
        v = [getattr(tm, field_name) for field_name, field_type
             in tm._fields_]
        index = 0
        for field_name, field_type in x._fields_:
            setattr(x, field_name, v[index])
            index += 1


    for x in c_word_array:
        if x.stem is None:
            break
        for field_name, field_type in x._fields_:
            if field_name == "table":
                print field_name, getattr(x, field_name)
                for t in getattr(x, field_name):
                    print [b for b in t.bit_array]
    """

    lock = Lock()

    utter_number = 0  # 発話する回数

    p_knowledge_array = []

    for i in xrange(agent_size):
        c_knowledge = DataStructure.KnowledgeStruct()
        setattr(c_knowledge, "id", i)
        setattr(c_knowledge, "words", c_word_array)
        setattr(c_knowledge, "communicate", utter_number)
        p_knowledge_array.append(c_knowledge)

    c_knowledge_array = (
        DataStructure.KnowledgeStruct * agent_size
        )(*p_knowledge_array)

    # 共有メモリに擬似データを格納する
    K = Array(DataStructure.KnowledgeStruct,
              c_knowledge_array, lock=lock)
    """
    for x in K:
        print "----------------------------------------"
        print x.id
        for y1 in x.words:
            print "******************************"
            check_fields(y1)
            print "******************************"
        print "----------------------------------------"
    """

    return K
