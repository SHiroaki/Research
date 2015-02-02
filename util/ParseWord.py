# -*- coding: utf-8 -*-

import os
import sys
import fuzzy
import itertools
import numpy as np
from Levenshtein import distance
from itertools import chain

START_CONSONANT = ["y", "s", "p", "t", "k", "q", "c", "b",
                   "d", "g", "f", "v", "j", "z", "l", "m",
                   "n", "r", "w", "h", "ch", "gh", "gn", "ph",
                   "ps", "rh", "sh", "th", "ts", "wh"]

# 元の音素クラスタには"j"は含まれていないが、ピンカーのデータに
# 対応するため拡張する(不自然な語に対応するためとかでも書いとく)
END_CONSONANT = ["h", "r", "l", "m", "n", "b", "d", "g", "c",
                 "x", "f", "v", "i", "s", "z", "p", "t", "k",
                 "q", "bb", "ch", "ck", "dd", "dg", "ff", "gg",
                 "gh", "gn", "ks", "ll", "ng", "nn", "ph", "pp",
                 "ps", "rr", "sh", "sl", "ss", "tch", "th", "ts",
                 "tt", "zz", "u", "e", "es", "ed", "j"]

# uaとuoだけ入ってないけど１文字が連続で並んでる場合でもおｋにした
VOWELS = ["e", "i", "o", "u", "a", "y", "ai", "au", "aw", "ay", "ea",
          "ee", "ei", "eu", "ew", "ey", "ie", "oa", "oe", "oi", "oo",
          "ou", "ow", "oy", "ue", "ui", "uy"]


class ParseVerb(object):
    """Parse input verb.
    """
    def __init__(self):
        self.position = 0
        self.start_consonant = ""
        self.vowel = ""
        self.end_consonant = ""

    def process_start_consonant(self):

        if self.position != self.buffer_end:
            self.next = self.buffer[self.position+1]
            next = self.next

        if self.next in START_CONSONANT:
            self.tmp_buffer.extend(self.character)
            tmp_buffer = self.tmp_buffer
            self.position += 1

        elif self.next in VOWELS:
            self.tmp_buffer.extend(self.character)
            tmp_buffer = self.tmp_buffer
            self.start_consonant = "".join(self.tmp_buffer)
            self.position += 1
            self.tmp_buffer[:] = []
            start_cons = self.start_consonant
        else:
            print "Error can not parsing this vreb."
            exit()

    def process_vowel(self):
        if self.position != self.buffer_end:
            self.next = self.buffer[self.position+1]
            next = self.next
        elif self.position == self.buffer_end:
            self.next = self.character
            next = self.next

        if self.next in VOWELS and self.position != self.buffer_end:
            # 2文字の母音のケースの一文字目を読んでいる状態
            self.tmp_buffer.extend(self.character)
            tmp_buffer = self.tmp_buffer
            self.position += 1
            """
            dvowel = "".join(self.tmp_buffer)
            if dvowel in VOWELS:
                self.vowel = dvowel
                self.position += 1
                self.tmp_buffer[:] = []
                vowel = self.vowel
            else:
                pass
            """

        elif self.next in VOWELS and self.position == self.buffer_end:
            # ２文字の母音のケースの2文字目を読んでいる状態
            self.tmp_buffer.extend(self.character)
            tmp_buffer = self.tmp_buffer
            dvowel = "".join(self.tmp_buffer)
            if dvowel in VOWELS:
                self.vowel = dvowel
                self.position += 1
                self.tmp_buffer[:] = []
                vowel = self.vowel
            else:
                pass

        elif self.next in END_CONSONANT:
            self.tmp_buffer.extend(self.character)
            tmp_buffer = self.tmp_buffer
            self.vowel = "".join(self.tmp_buffer)
            self.position += 1
            self.tmp_buffer[:] = []
            vowel = self.vowel
        else:
            print "Error can not parsing this vreb."
            exit()

    def process_end_consonant(self):
        if self.position != self.buffer_end:
            self.tmp_buffer.extend(self.character)
            tmp_buffer = self.tmp_buffer
            self.position += 1
        else:
            self.tmp_buffer.extend(self.character)
            tmp_buffer = self.tmp_buffer
            self.end_consonant = "".join(self.tmp_buffer)
            # print self.end_consonant
            self.position += 1

    def parse(self, input):
        self.buffer = input
        self.buffer_end = len(input) - 1
        self.tmp_buffer = []
        # 一度終端子音解析にはいったらe,uが出てきても母音とは見なさない
        after_vowel = 0

        while self.position <= self.buffer_end:

            self.character = self.buffer[self.position]
            character = self.character
            if (self.character in START_CONSONANT and
                    len(self.vowel) == 0 and after_vowel == 0):
                self.process_start_consonant()

            elif (self.character in VOWELS and after_vowel == 0):
                self.process_vowel()

            else:
                after_vowel = 1
                self.process_end_consonant()

        if len(self.vowel) > 2:
            # queeの場合の例外処理
            self.start_consonant = self.start_consonant + self.vowel[0]
            self.vowel = self.vowel[1:]

        return (self.start_consonant, self.vowel, self.end_consonant)

    def printtest(self):
        print self.buffer
        print self.buffer_end
        print self.tmp_buffer


def verbparser(input):
    """Parse input verb.
    # 人工動詞の語幹はすべて解析できるがたまにエラーをはくときがある
    # blowとか

    Parse verb to three part
    such as: (start_consonant, vowel, end_consonant)

    Parameters
    ----------
    input : string
        Verb to parser.

    Return

    ------
    tuple : (start_consonant, vowel, end_consonant)
    """
    return ParseVerb().parse(input)


if __name__ == "__main__":

    """
    stems = v.keys()
    pasts = v.values()
    past_vowel_paterns = [verbparser(s)[1] for s in pasts]
    stem_vowel_paterns = [verbparser(s)[1] for s in stems]

    d = {}
    d2 = {}

    for c in past_vowel_paterns:
        d[c] = d.get(c, 0) + 1
    for c in stem_vowel_paterns:
        d2[c] = d.get(c, 0) + 1

    # 距離が似ている単語を探して母音が何に変わっているか調べる
    for s in stems:
        print s
        print get_rule_parameters(v, s)
    """
