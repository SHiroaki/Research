# -*- coding: utf-8 -*-

import os
import sys
import fuzzy
import itertools
import numpy as np
from sklearn.cluster import KMeans

from Levenshtein import distance

# カレントと違うディレクトリからimportする
dirpath = os.path.dirname(os.path.abspath(__file__))
utildir = 'util'

sys.path.append(dirpath+'/'+utildir)

from read_verb import read_verb


def dmeta(w):

    dmeta = fuzzy.DMetaphone()
    dmeta_str = dmeta(w)

    return dmeta_str[0]  # 一つだけ返す


def distance_vec():
    verblist = read_verb()
    verb_combi = [element for element in itertools.combinations(verblist, 2)]
    dmeta_comb = [(dmeta(x), dmeta(y)) for x, y in verb_combi]
    dmeta_distance = [distance(*x) for x in dmeta_comb]

    for x, y in zip(verb_combi, dmeta_distance):
        if x[0] == "spling":
            print x, y

    f = open("distance.txt", 'w')
    f.close()


def main():
    distance_vec()

if __name__ == '__main__':
    main()
