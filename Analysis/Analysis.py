# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import cPickle as pickle
import cbinarymethods as cbm
# from settings import read_verbdict


def read_result():

    result_file = "BA12Agent_100gen.dump"
    # result_file = "result_12ag_20gen_5utter_torna20.dump"
    f = open(result_file)
    result_dict = pickle.load(f)
    f.close()

    return result_dict


def read_rule():
    # rule_file = "rules_12ag_20gen_5utter_torna20.dump"
    rule_file = "rules.dump"
    f = open(rule_file)
    rule_dict = pickle.load(f)
    f.close()

    return rule_dict


def get_rule(rule_dict, rule):
    """
    全単語のルールの数値を求める
    """
    ed_rule_dict = {}
    stems = rule_dict.keys()

    for stem in stems:
        ed_rule = []
        for num, vowel in rule_dict[stem].items():
            if vowel == rule:
                ed_rule.append(num)
            ed_rule_dict[stem] = ed_rule

    return ed_rule_dict


def get_anaresult(result_dict, rule):
    """
    1,全世代の全agentのtableをbinaryから数値に変換する
    2,tableの中からedルールのものだけを残す
    """

    gen = result_dict.keys()
    rule_dict = read_rule()

    ed_rules = get_rule(rule_dict, rule)
    stems = rule_dict.keys()

    all_gen_table = {}
    """
    {世代: {agent_id : {stem:[table_value, ...],}}}
    """

    for g in gen:
        knowledges = result_dict[g]  # g世代目の全エージェントの知識
        all_agent_id = knowledges.keys()  # agent id
        all_agent_table_value = {}  # key:agent, value:table_list

        for agent in all_agent_id:
            knowledge_dict = knowledges[agent][0]
            stem_table = {}
            for stem, word_struct in knowledge_dict.items():

                tables = [x[0][1] for x in word_struct["table"]]
                # Agentの単語のtableをすべて数値に変換したもの
                table_value = map(cbm.binary2value, tables)
                max_table_length = float(len(table_value))
                # stemのedルールのものだけ残す
                table_value = [x for x in table_value if x in ed_rules[stem]]
                ed_rule_length = float(len(table_value))
                # 規則化率を計算
                reg_ratio = np.divide(ed_rule_length, max_table_length)
                stem_table[stem] = reg_ratio

            all_agent_table_value[agent] = stem_table
        all_gen_table[g] = all_agent_table_value
    """
    for g, k in all_gen_table.items():
        print "----------------------------------------"
        print "Gen", g
        for aid, wstruct in k.items():
            print "******************************"
            print "ID", aid, len(wstruct)
            for stem, r in wstruct.items():
                print stem, r
    """
    open_file = "解析結果BA12agent_100gen_" + str(rule) + ".txt"
    # fo = open('解析結果BA12agent_100gen_uo.txt', 'w')
    fo = open(open_file, 'w')
    sys.stdout = fo
    # 世代ごとに単語の平均規則化率を求める
    # target = ["spling", "skring", "sprink", "cleed", "preed"]

    for s in stems:
        print "----------------------------------------"
        word = s
        for g, k in all_gen_table.items():
            word_reg = 0.0
            for aid, wstruct in k.items():
                score = wstruct.get(word)
                if score is None:
                    # 高頻度単語
                    score = 0
                word_reg += score
            print word, g, np.divide(word_reg, float(len(k)))
    sys.stdout = sys.__stdout__

if __name__ == '__main__':

    analysis_rules = ["e", "ed", "o", "oa", "oo", "u", "ue", "uo"]
    result_dict = read_result()
    for rule in analysis_rules:
        get_anaresult(result_dict, rule)
