# -*- coding: utf-8 -*-

import os
import sys
from vowel import verbparser as vp
from multiprocessing import Pipe, Process

dirpath = os.path.dirname(os.path.abspath(__file__))
utildir = 'util'

sys.path.append(dirpath+'/'+utildir)

from lookup import knowledge_lookup


def f(conn, _knowledge):

    verb = conn.recv()
    word_struct = knowledge_lookup(45, verb, _knowledge)

    if word_struct is None:
        print "I do not know."
    else:
        print "I know"

    vowel = vp(verb)
    conn.send(vowel)


def comunicate(knowledge):

    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn, knowledge))

    p.start()

    word_struct = knowledge_lookup(12, "sang", knowledge)
    verb = word_struct.past
    parent_conn.send(verb)
    print parent_conn.recv()
    p.join()
