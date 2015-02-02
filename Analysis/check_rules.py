# -*- coding: utf-8 -*-

import cPickle as pickle

f = open('rules.dump')
rules = pickle.load(f)
rd = pickle.dumps(rules)
f.close()

f = open('verb_freq.dump')
freq = pickle.load(f)
rd = pickle.dumps(rules)
f.close()


def check_rules():
    stem = raw_input()
    vowel = raw_input()
    print stem, vowel
    stem_rules = rules[stem]
    print stem_rules.values()
    ru = []
    for n, v in stem_rules.items():
        if v == vowel:
            ru.append(n)
    print ru


def check_freq():
    stem = raw_input()
    print freq[stem]


def read_most_freq():

    result_file = "most_freq.dump"
    # result_file = "result_12ag_20gen_5utter_torna20.dump"
    f = open(result_file)
    fe = pickle.load(f)
    f.close()
    print fe


if __name__ == '__main__':
    read_most_freq()
    check_rules()
    while True:
        pass
        # check_freq()
