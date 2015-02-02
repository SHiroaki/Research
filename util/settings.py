# -*- coding: utf-8 -*-

import random
import ParseWord
import fuzzy
from itertools import chain
import numpy as np
from Levenshtein import distance
from itertools import chain

path = "/home/hiroaki/Research/Text/irregular_verb_list.txt"

# 規則化の割合
re_parameter = 0.02


class StructureSize(object):

    bit_array_size = 7
    gene_array_size = 1  # つかわない
    utter_array_size = 1  # つかわない
    heard_array_size = 1  # つかわない
    table_array_size = int(100 * re_parameter) + 100  # ed分も余計に
    word_array_size = 55  # 上位５単語は抜く
    # word_array_size = 5  # 上位５単語は抜く
    char_buffer_size = 15


class TableParam(object):
    regularization_rate = re_parameter


def utter_setting():
    utterance_time = 100
    return utterance_time


def read_verb():
    f = open(path, "r")
    verblist = []

    for line in f:
        itemlist = line[:-1].split(" ")
        if len(itemlist) != 2 and len(itemlist) != 1:
            verblist.append(itemlist)
    f.close()

    tmp = verblist[4:]
    verblist = []

    for x in tmp:
        verblist.append(x[0])
        verblist.append(x[-1])

    verblist = [x.rstrip("\t")for x in verblist]
    return verblist


def set_verb_frequency():
    """
    各動詞の頻度を決める
    Return
    ------
    dict : key = stem, value = freq
    """

    verbdict = read_verbdict()
    stems = [k for k, v in verbdict.items()]
    random.shuffle(stems)

    freq_distribution = get_freq_distribution()

    freq_list = []

    for k, v in freq_distribution.items():
        for i in xrange(v):
            freq_list.append(k)

    random.shuffle(freq_list)
    """
    d = {}
    for c in freq_list:
        d[c] = d.get(c, 0) + 1
    print d
    """
    d = {}

    for stem, freq in zip(stems, freq_list):
        d[stem] = freq

    return d


def get_freq_distribution():
    distribution = {
        # 各頻度に何個の動詞が属しているか
        100000: 1,
        10000: 4,
        1000: 12,
        100: 22,
        10: 17,
        1: 4
        }
    return distribution


def read_verbdict():
    verbs = {
        # Prototypical pseudo-irregular
        "spling": "splung",
        "skring": "skrung",
        "sprink": "sprunk",
        "cleed": "cled",
        "preed": "pred",
        "queed": "qued",
        "cloe": "cloo",
        "froe": "froo",
        "plare": "plore",
        "quare": "quore",
        # Intermmediate pseudo-irregular
        "fring": "frung",
        "ning": "nung",
        "frink": "frunk",
        "cleef": "clef",
        "preek": "prek",
        "queef": "quef",
        "foa": "foo",
        "voa": "voo",
        "jare": "jore",
        "grare": "grore",
        # Distant pseudo-irregular
        "trisp": "trusp",
        "nist": "nust",
        "blip": "blup",
        "gleef": "glef",
        "keeb": "keb",
        "meep": "mep",
        "goav": "goov",
        "joam":	"joom",
        "flape": "flope",
        "blafe": "blofe",
        # Prototypical pseudo-regular
        "plip": "plup",
        "glip": "glup",
        "brip": "brup",
        "gloke": "glook",
        "proke": "prook",
        "greem": "grem",
        "pleem": "plem",
        "treem": "trem",
        "slace": "sloce",
        "nace": "noce",
        # Intermediate pseudo-regular
        "brilth": "brulth",
        "glinth": "glunth",
        "plimph": "plumph",
        "ploab": "ploob",
        "ploag": "ploog",
        "smeeb": "smeb",
        "smeeg": "smeg",
        "smeej": "smej",
        "smaib": "smobe",
        "smaig": "smoag",
        # Distant presudo-regular
        "frilg": "frulg",
        "krilg": "krulg",
        "trilb": "trulb",
        "ploamph": "ploomph",
        "ploanth": "ploonth",
        "smeelth": "smelth",
        "smeenth": "smenth",
        "smeerg": "smerg",
        "smairg": "smoarg",
        "smairph": "smoarph"
    }
    return verbs


def get_rule_parameters(vdict, target):
    """単語のルールテーブルの割合を求める
    誤差はしょうがないか...

    Parameters
    ----------
    vdict : verb dict

    target : target verb

    Return
    ------

    rule_paramters : dict 母音とその平均距離
    """
    verbparser = ParseWord.verbparser

    vowel = 1
    stemlist = vdict.keys()
    dmeta = fuzzy.DMetaphone()
    verb_combi = [(target, v) for v in stemlist if v != target]
    dmeta_combi = [(dmeta(x)[0], dmeta(y)[0]) for x, y in verb_combi]
    dmeta_distance = [distance(*x) for x in dmeta_combi]

    distance_rank = {}  # (target, verb) : 距離
    for x, y in zip(verb_combi, dmeta_distance):
        distance_rank[x] = y

    distance_distribute = {}
    # 距離がvの単語がいくつあるか
    for k, v in distance_rank.items():
        distance_distribute[v] = distance_distribute.get(v, 0) + 1

    # 距離dの単語の過去形の母音交代パターンを求める
    past_vowels = {}  # {距離: [母音,母音,....]}
    vowels_distance = {}
    for k, v in distance_distribute.items():
        vowels = []
        for pair, d in distance_rank.items():
            if k == d:
                vowel_string = (verbparser(vdict[pair[1]])[vowel])
                vowels.append(vowel_string)
                vowels_distance[vowel_string] = vowels_distance.get(
                    vowel_string, 0) + d

        past_vowels[k] = vowels

    patterms = past_vowels.values()
    patterms = list(chain.from_iterable(patterms))
    vowels_appear = {}
    for c in patterms:
        vowels_appear[c] = vowels_appear.get(c, 0) + 1

    # あるルールの平均距離を求める 距離のアルゴリズム上
    # あまり差がでない
    rule_parameters = {}
    for vo, dis in vowels_distance.items():
        avg = np.divide(np.double(dis), np.double(vowels_appear[vo]))
        # 小数点以下２桁で四捨五入
        rule_parameters[vo] = np.around(avg, decimals=2)

    return rule_parameters

    """
    # ある距離の中で一番使われているパターンを探す
    # 重複しないように
    best_vowel = {}
    for dis, v in past_vowels.items():
        d = {}
        for c in v:
            d[c] = d.get(c, 0) + 1
        bests = [vo for vo, dist in d.items() if dist == max(d.values())]

        best_vowel[dis] = bests
        print best_vowel
        print best_vowel.
    """


def wrap_init_table():
    """単語と数字を指定するとルールがでてくるような辞書を返す
    """
    verbdict = read_verbdict()
    stems = verbdict.keys()
    word_and_rule = {}

    for s in stems:
        word_and_rule[s] = init_table(verbdict, s)
        # print word_and_rule[s]

    return word_and_rule


def init_table(verbdict, target):
    """各単語のルールテーブルの割合を決める
    edは別枠でつくるように変更


    Parameters
    ----------

    target : word string


    Return
    ------

    list : ルールに応じた整数をサイズ分発生させたもの
    """

    params = get_rule_parameters(verbdict, target)

    # ルールテーブルの初期化
    table_size = StructureSize.table_array_size
    re_rate = TableParam.regularization_rate  # edルールの割合
    ed_rule_size = table_size * re_rate

    # paramの逆数を求める
    reciprocal = {}
    for vowel, param in params.items():
        if param == 0.:
            param = 0.1  # 0の場合は0.1にする
        reciprocal[vowel] = np.divide(1.0, param)

    param_y = (table_size / (np.sum(reciprocal.values())))
    # print param_y
    table_ratio = {str(vowel): np.around(reciprocal[vowel] * param_y)
                   for vowel, param in reciprocal.items()}
    # print table_ratio, np.sum(table_ratio.values())

    rules_ratio = np.sum(table_ratio.values())

    # どうしても誤差がでるのでランダムに選んで調整する
    if rules_ratio < table_size:
        adjustment = table_size - rules_ratio
        ks = np.random.choice(table_ratio.keys(),
                              adjustment, replace=False)
        for k in ks:
            table_ratio[k] += 1
    elif rules_ratio > table_size:
        adjustment = rules_ratio - table_size
        ks = np.random.choice(table_ratio.keys(),
                              adjustment, replace=False)
        for k in ks:
            table_ratio[k] -= 1

    # 割合に応じて整数を割り振る *単語によって異なるので保存しておく

    rule_numbers = {}
    table_ratio["ed"] = ed_rule_size
    start = 0

    for k, v in sorted(table_ratio.items()):
        stop = start + int(v)
        rule_numbers[k] = [x for x in xrange(start, stop)]
        start = stop

    number_rule = {}
    numbers = rule_numbers.values()
    flat = list(chain.from_iterable(numbers))

    # 数字を指定するとどのルールかでてくるように変更
    for k, v in sorted(rule_numbers.items()):
        for x in flat:
            if x in v:
                number_rule[x] = k

    return number_rule
