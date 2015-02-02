# -*- coding: utf-8 -*-

import os
import sys
from ctypes import *

dirpath = os.path.dirname(os.path.abspath(__file__))
utildir = 'util'

sys.path.append(dirpath+'/'+utildir)

from settings import StructureSize


"""
このクラスをfrom importすると共有メモリが作成されない.
必ず import DataStructure すること
"""


class GeneStruct(Structure):
    """Gene of GA and it's score
    """
    bit_array_size = StructureSize.bit_array_size

    _fields_ = [("bit_array", c_int * bit_array_size),
                ("score", c_double),
                # ("rule", c_char_p),  # 最終手段はプロセスごとに読み込む
                ("used", c_int)  # 構造体の値が使われている場合は1
                ]


class Utterance(Structure):
    """Agent utteranced past tence
    # それぞれc_char_pからc_charの配列に変更
    """
    buf_size = StructureSize.char_buffer_size

    _fields_ = [("utter", c_char * buf_size)]


class Heard(Structure):
    """Agent heard past tence
    # それぞれc_char_pからc_charの配列に変更
    """
    buf_size = StructureSize.char_buffer_size

    _fields_ = [("heard", c_char * buf_size)]


class WordStruct(Structure):

    gene_size = StructureSize.gene_array_size
    utter_size = StructureSize.utter_array_size
    hear_size = StructureSize.heard_array_size
    table_size = StructureSize.table_array_size
    buf_size = StructureSize.char_buffer_size
    # _pack_ = 1
    _fields_ = [("stem", c_char * buf_size),
                ("past", c_char * buf_size),
                ("understand", c_int),
                ("freq", c_int),
                ("active", c_int),
                ("past_life", c_int),
                ("utter", Utterance * utter_size),
                ("heard", Heard * hear_size),
                ("table", GeneStruct * table_size),
                ("gene", GeneStruct * gene_size)]


class KnowledgeStruct(Structure):
    """wordsとgeneのサイズは可変だとmulitiprocessing.Array
    に載せられないので固定

    データが格納されていない構造体メンバの値
    >>> c_char_pの場合はNone
    stem, pastには None が入っている

    >>> その他数値型の場合は0で埋められる
    """

    word_size = StructureSize.word_array_size

    _fields_ = [("id", c_int),  # Agent name
                ("communicate", c_int),  # コミュニケーションした回数
                ("words", WordStruct * word_size)]

"""
def dynamic_words_struct(size):
    class WordStruct(Structure):

        _fields_ = [("stem", c_char_p),
                    ("past", c_char_p),
                    ("meaning", c_int),
                    ("freq", c_int),
                    ("active", c_int),
                    ("stem_in_lex", c_int),
                    ("past_in_lex", c_int),
                    ("gene", GeneStruct * size)]

    return WordStruct


def dynamic_knowledge_struct(size, _WordStruct):
    class KnowledgeStruct(Structure):

        _fields_ = [("id", c_int),  # Agent name
                    ("words", _WordStruct * size)]
    return KnowledgeStruct

"""
