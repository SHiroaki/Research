# -*- coding: utf-8 -*-

import os
import networkx as nx

dirpath = os.path.dirname(os.path.abspath(__file__))
resultdir = 'result'

save_dir = dirpath + resultdir


def save_graph(G, file_name):
    name = save_dir + file_name + ".gpickle"
    nx.write_gpickle(G, name)
