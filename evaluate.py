# -*- coding: utf-8 -*-

import fuzzy
from Levenshtein import distance

dmeta = fuzzy.DMetaphone()


def eval_syllable(stem, utter):
    """音節が増えないかどうか
    単語がdかtで終わっているときに規則化するとペナ
    """
    stem_end = stem[-1:]
    utter_end = utter[-2:]

    unnatural_stem_end = ["d", "t"]

    if stem_end in unnatural_stem_end and utter_end == "ed":
        # 音節が増える
        return -5.0
    else:
        # 音節が増えない
        return 0


def eval_unnatural(stem, most_freq):
    """
    高頻度の単語に発音が似ていないか
    """
    stem_meta = dmeta(stem)[0]
    most_freq_meta = [dmeta(x)[0] for x in most_freq]
    distances = [distance(stem_meta, x) for x in most_freq_meta]

    if 1 in distances:
        # 高頻度の単語に似ている.規則化すると不自然
        return -5.0
    else:
        # 高頻度の単語に似ていない
        return 0
