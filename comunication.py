# -*- coding: utf-8 -*-

import os
import sys
from ParseWord import verbparser as vp
from multiprocessing import Pipe, Process
import KnowledgeLookup as klup
from evaluate import eval_syllable, eval_unnatural
import time
import random
from copy import deepcopy
import cbinarymethods as cbm
import cPickle as pickle

dirpath = os.path.dirname(os.path.abspath(__file__))
utildir = 'util'

sys.path.append(dirpath+'/'+utildir)

from random_pick import random_weight_pick

COMPB = 0.4  # 音節チェック、類似度チェックを行う確率
# LONGPB = 0.6  # 高頻度の単語の場合、ペナルティを与える

"""
このプログラム(プロセス)の外から共有メモリを書き換えるための
値を取ってくると書き込んでもNoneになる可能性あり
"""


def f(conn, i, knowledge, rd):
    # print "Im c", i
    # ルールテーブルをpickleを使って復元する
    rules = pickle.loads(rd)

    # 聞き手エージェントの情報を得る
    knowledge_holder = klup.KnowledgeHolder(
        knowledge, i)

    # 発話エージェントからの情報を受け取る
    heard_info = conn.recv()
    stem = heard_info[0]
    # regular_past = heard_info[1]
    ablaut_vowel = heard_info[2]
    # print "c", ablaut_vowel
    # 聞いた単語の知識をとってくる
    heardword = knowledge_holder.find_word(stem)

    # 自分もランダムに母音交替パターンを選ぶ
    heard_verbs_pattern = rules[stem]

    gene_list = [x for x in heardword.table]
    use_gene = random.choice(gene_list)  # 比較に使われる遺伝子
    copy_use_gene = deepcopy(use_gene)
    use_gene_bit_array = [x for x in copy_use_gene.bit_array]
    pattern_num = cbm.binary2value(use_gene_bit_array)

    # ルールに当てはまらない遺伝子が出てきた場合は伝わらないと同じ扱い
    my_chage_vowel = heard_verbs_pattern.get(pattern_num)

    if ablaut_vowel is None:
        # そもそも発話できてない
        return_value = 99

    elif ablaut_vowel == my_chage_vowel:
        # 同じ母音交替をした
        return_value = 1

    elif ablaut_vowel != my_chage_vowel:
        # 異なる母音交替をした, または致死遺伝子を引いた
        return_value = 0

    # 返答
    # print my_chage_vowel, return_value
    conn.send(return_value)


def comunicate(l, knowledge, rd, most_freq, fv):

    child_k = knowledge
    parent = l[0]  # agent id
    child = l[1]  # agent id

    # ルールテーブルをpickleを使って復元する
    rules = pickle.loads(rd)

    # 単語の頻度辞書をpickleを使って復元する
    freq_of_verbs = pickle.loads(fv)

    # print "Im p", parent
    # 発話エージェントの知識を得る
    knowledge_holder = klup.KnowledgeHolder(
        knowledge, parent)

    # 発話する単語を重み付き選択で選ぶ
    active_words_dict = knowledge_holder.active_words()
    utter_verb = random_weight_pick(active_words_dict)  # 発話対象の語幹
    wordstruct = knowledge_holder.find_word(utter_verb)

    # 発話する単語の母音交替パターンをルールテーブルから決定する
    # 発話できない遺伝子だったら特殊な文字列を送信する
    utter_verbs_pattern = rules[utter_verb]
    gene_list = [x for x in wordstruct.table]
    use_gene = random.choice(gene_list)  # 発話に使われる遺伝子
    copy_use_gene = deepcopy(use_gene)
    use_gene_bit_array = [x for x in copy_use_gene.bit_array]
    # use_gene_bit_array = [1, 1, 1, 1, 1, 1, 1, 1]
    pattern_num = cbm.binary2value(use_gene_bit_array)
    # 発話できない染色体を引いたらchange_vowelはNoneになる
    change_vowel = utter_verbs_pattern.get(pattern_num)
    # parsed = vp(utter_verb)

    # 母音交替させた過去形
    # ablaut = (parsed[0], change_vowel, parsed[2])
    # 規則化した過去形
    regularize = utter_verb + "ed"
    # print stem, ablaut, "p", use_gene_bit_array

    # 発話 (語幹、規則化、母音交替)
    v = (utter_verb, regularize, change_vowel)

    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn, child, child_k, rd))
    p.start()
    # 聞き手エージェントに送る
    # 発話できない遺伝子の場合は99が帰ってくる
    parent_conn.send(v)

    # 伝わったかどうか帰ってくる
    is_ok = parent_conn.recv()
    is_increse_sylable = 0
    is_similar = 0
    # print "is_ok", is_ok

    # pattern_numを評価する

    if is_ok == 1:
        # print "Yes"
        # 意味が伝わった場合
        # 使った遺伝子と同じルールの遺伝子全てに加点するok
        add_score = 10

        winner = [n for n, vo in utter_verbs_pattern.items()
                  if vo == change_vowel]
        for g in gene_list:
            g_bit = [x for x in g.bit_array]
            if cbm.binary2value(g_bit) in winner:
                setattr(g, "score", getattr(g, "score")+add_score)

    elif is_ok == 99:
        # print "Cant"
        # 発話できてない場合、致死遺伝子は0になる
        setattr(use_gene, "score", 0)
    else:
        # 伝わらなかった場合
        # ある程度の確率で音節が増えていないか、高頻度の単語と似ていないか
        # のチェックが入る
        # 基本的に1点を加えるがたまにペナルティが入る
        # print "No"
        add_score = 10

        if freq_of_verbs[utter_verb] == 1000:
            # 高頻度でedをつけると長くなるからペナルティ
            add_score -= 5

        if random.random() < COMPB:
            is_increse_sylable = eval_syllable(utter_verb, regularize)
            is_similar = eval_unnatural(utter_verb, most_freq)

        winner = [n for n, vo in utter_verbs_pattern.items()
                  if vo == "ed"]
        add_score = add_score + is_increse_sylable + is_similar

        if add_score < 0:
            add_score = 0
        # print add_score
        for g in gene_list:
            g_bit = [x for x in g.bit_array]
            if cbm.binary2value(g_bit) in winner:
                setattr(g, "score", getattr(g, "score")+add_score)

    """
    点数は入っている
    ed_winner = [n for n, vo in utter_verbs_pattern.items()
                 if vo == "ed"]
    for g in gene_list:
        g_bit = [x for x in g.bit_array]
        if cbm.binary2value(g_bit) in ed_winner:
            print "ed score", getattr(g, "score")
    """
    p.join()
