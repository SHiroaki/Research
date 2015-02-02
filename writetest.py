# -*- coding: utf-8 -*-

import os
import sys
from ctypes import *
import DataStructure
import KnowledgeLookup as klup
from CtypePyobjMapper import CtypePyobjMapper as cpmap
from multiprocessing import Lock
from multiprocessing.sharedctypes import Array
import random
import numpy as np
import DataStructure
import cbinarymethods as cbm


# カレントと違うディレクトリからimportする
dirpath = os.path.dirname(os.path.abspath(__file__))
utildir = 'util'

sys.path.append(dirpath+'/'+utildir)

from settings import StructureSize
from check_util import *


def test():

    p_bitarray1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    p_bitarray2 = [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
    p_bitarray3 = [1, 1, 1, 1, 1, 1, 1, 0, 1, 1]

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
        t.score = 3
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

    genes = c_gene_array
    table = c_table_array

    d = {"stem": "spling", "past": "splung"}
    word = DataStructure.WordStruct(d["stem"],
                                    d["past"],
                                    0, 1, 1, 1000,
                                    utter_array,
                                    heard_array,
                                    table, genes)
    print word.stem
    setattr(word, "stem", "spp")
    print getattr(word, "stem")
    print word.stem

if __name__ == "__main__":
    test()
