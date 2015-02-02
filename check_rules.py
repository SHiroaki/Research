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
    ru = []
    for n, v in stem_rules.items():
        if v == vowel:
            ru.append(n)
    print ru

def check_freq():
    stem = raw_input()
    print freq[stem]

if __name__ == '__main__':
    while True:
        # check_rules()
        check_freq()
