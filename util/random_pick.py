# -*- coding: utf-8 -*-

import random


def random_prob_pick(some_list, probabilities):
    """Random choice by cunulative probability.

    確率で重み付けされたリストから確率にしたがってランダムでアイテムを取り出す

    Parameters
    ----------
    some_list : list
        target list.

    probabilities : list
        probability list.

    Returns
    -------

    item : item

    """

    x = random.uniform(0, 1)
    cunulative_probability = 0.0

    for item, item_probability in zip(some_list, probabilities):
        cunulative_probability += item_probability
        if x < cunulative_probability:
            break

    return item


def random_weight_pick(d):
    """確率でない値で重み付けされたリストからランダムでアイテムを取り出す
    重みは0~1のあいだでなくても良い

    Parameters
    ----------
    d : dict. key = item, value = weight
    """
    s = 0
    for k, v in d.items():
        s += v
        if random.randrange(s) < v:
            n = k
    return n
