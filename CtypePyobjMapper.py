# -*- coding: utf-8 -*-

import os
import sys
import DataStructure
# import sharedmemory  # setting() が必要ないならいらない
from ctypes import c_int

dirpath = os.path.dirname(os.path.abspath(__file__))
utildir = 'util'

sys.path.append(dirpath+'/'+utildir)
from settings import StructureSize
from check_util import *


class CtypePyobjMapper(object):
    """Convert ctypes structure to python object and
       python object to ctypes.
    """

    def __init__(self):
        self.agent_id = 0
        self.word = None
        self.word_dict = {}
        self.knowledge_dict = {}

    def c_to_p_convert(self, knowledge_array):
        """Convert ctypes structure to python dict.

        **!!同じ単語はひとつしか登録できない!!**

        Parameters
        ----------
        Array : Shared memory array (Multiprocessing.sharedctypes.Array)

        Returns
        -------
        knowledge_dict : python dictionary

        *** Dict structure ***

        knoledge_dict = { agent_id : (word_dict, (commu_count, int)),
                          agent_id : (word_dict, (commu_count, int)),....}

        commu_count : エージェントが発話、受信した総数

        word_dict = { stem : member_dict, stem : member_dict, .....}

        member_dict = {stem       : string,
                       past       : string,
                       understand : int,
                       freq       : int,
                       active     : int,
                       past_life  : int,
                       is_ok      : int,
                       utter      : [any past utteranced form..],
                       heard      : [any past heard past form..],
                       table      : gene_list,
                       gene       : gene_list,
                       }

        gene_list : [((bit_array, [01001..]), (score, 2), (used, 1)),
                     ((bit_array, [01101..]), (score, 1), (used, 1)),... ]

        """

        def f(gene_struct):
            bit_array = [x for x in gene_struct.bit_array]
            score = gene_struct.score
            used = gene_struct.used

            _t1 = ("bit_array", bit_array)
            _t2 = ("score", score)
            _t3 = ("used", used)
            _t4 = (_t1, _t2, _t3)

            return _t4

        def _unfolding(struct_array):

            field_name = struct_array[0]._fields_[0][0]
            values = [getattr(x, field_name) for x in struct_array
                      if getattr(x, field_name) is not None]
            return values

        knowledge_dict = {}
        for k in knowledge_array:
            self.agent_id = k.id

            word_dict = {}
            self.communicate_count = k.communicate

            for w in k.words:

                if w.stem is None:
                    # Noneをkeyにすると挙動がおかしくなるので注意
                    break

                member_dict = {}

                for field_name, field_type in w._fields_:
                    member_dict[field_name] = getattr(w, field_name)

                member_dict["utter"] = _unfolding(
                    member_dict["utter"])
                member_dict["heard"] = _unfolding(
                    member_dict["heard"])

                self.gene_members = [f(g) for g in w.gene]
                self.table_members = [f(g) for g in w.table]

                member_dict["gene"] = self.gene_members
                member_dict["table"] = self.table_members

                word_dict[w.stem] = member_dict

            comu_tup = ("communication_count", self.communicate_count)
            knowledge_dict[self.agent_id] = (
                word_dict, comu_tup)

        return knowledge_dict

    def p_to_c_convert(self, knowledge_obj):
        """Convert python object to ctypes

        ***配列の代入で初期化するな***

        Parameters
        ----------
        knowledge_obj : dictionary


        Return
        ------
        Array : DataStructure.KnowledgeStruct * agent_num
                ** Not shared memory arrray**
        """
        word_size = StructureSize.word_array_size
        utterrance_size = StructureSize.utter_array_size
        heard_size = StructureSize.heard_array_size

        InitUtterArray = (DataStructure.Utterance * utterrance_size)
        InitHeardArray = (DataStructure.Heard * heard_size)

        self.agent_size = len(knowledge_obj)
        p_knowledge_array = []

        def _folding_gene(gene_tuples):
            genes_array = []
            for x in gene_tuples:

                p_bit_array = x[0][1]
                c_bit_array = (c_int * len(p_bit_array))(*p_bit_array)
                score = x[1][1]
                used = x[2][1]
                # print p_bit_array
                # print score
                # ok
                genes_array.append(
                    DataStructure.GeneStruct(c_bit_array, score, used)
                )
            return genes_array

        def _folding_list(string_list, any_array):
            for x, s in zip(any_array, string_list):
                for field_name, field_type in x._fields_:
                    # 文字列はpointに変換する
                    # s = c_char_p(s)
                    setattr(x, field_name, s)

            return any_array

        for agent, tuples in knowledge_obj.items():
            self.agent_id = agent

            word_dict = tuples[0]
            self.word_num = len(word_dict)
            communicate_count = tuples[1][1]
            p_word_array = []

            for word, v in word_dict.items():

                p_gene_array = _folding_gene(v["gene"])
                c_gene_array = (DataStructure.GeneStruct *
                                len(p_gene_array))(*p_gene_array)

                p_table_array = _folding_gene(v["table"])
                c_table_array = (DataStructure.GeneStruct *
                                 len(p_table_array))(*p_table_array)

                c_utter_array = _folding_list(v["utter"],
                                              InitUtterArray())
                c_heard_array = _folding_list(v["heard"],
                                              InitHeardArray())

                v["gene"] = c_gene_array
                v["table"] = c_table_array
                v["utter"] = c_utter_array
                v["heard"] = c_heard_array

                w = DataStructure.WordStruct()

                for field_name, field_type in w._fields_:
                    setattr(w, field_name, v[field_name])

                p_word_array.append(w)

            # 次にwordの各メンバーを代入していく
            c_word_array = (
                DataStructure.WordStruct * word_size
                )(*p_word_array)

            c_knowledge = DataStructure.KnowledgeStruct()
            setattr(c_knowledge, "id", self.agent_id)
            setattr(c_knowledge, "words", c_word_array)
            setattr(c_knowledge, "communicate", communicate_count)

            p_knowledge_array.append(c_knowledge)

        c_knowledge_array = (
            DataStructure.KnowledgeStruct *
            self.agent_size)(*p_knowledge_array)

        return c_knowledge_array

"""
if __name__ == '__main__':
    import pickle

    K = sharedmemory.setting()
    k_before = CtypePyobjMapper().c_to_p_convert(K)
    pickle.dump(k_before, open("k_dict.dump", "wb"))

    k_dict = pickle.load(open("k_dict.dump", "rb"))
    print k_before == k_dict
    K2 = CtypePyobjMapper().p_to_c_convert(k_dict)
    k_after = CtypePyobjMapper().c_to_p_convert(K)
    print k_before == k_after


    # for c_to_p check
    for k, v in k_dict.items():
        print k
        for x, y in v.items():
            print x
            for p in y:
                print p
            exit()


    lock = Lock()
    print "K in main", K2
    for k in K2:
        print k.id

    exit()
    """
