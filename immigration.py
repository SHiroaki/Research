# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import networkx as nx

# カレントと違うディレクトリからimportする
dirpath = os.path.dirname(os.path.abspath(__file__))
utildir = 'util'

sys.path.append(dirpath+'/'+utildir)

from plot_methods import *
from graph_util import *

edge_num_with_new_node = 2


def small_immigration(G, num_of_node):
    """Add new node(s) by Numpy matrix resizing.

    Add any node to the existing network.
    ( Keep scale-free )

    Parameters
    ----------
    G : graph
        A networkx graph


    add_num : interger
       The number of added node(s).

    Returns
    ------
    G : Networkx graph

    """

    number_of_init_graph_nodes = len(G)

    degree_sequenceG = [G.degree(n) for n in G]
    id_sequenceG = [n for n in G]

    degree_sequenceG = np.asarray(degree_sequenceG, dtype=np.float64)
    degrees_sum = degree_sequenceG.sum()
    probabilities_G = np.divide(degree_sequenceG, degrees_sum)

    # enumerateは0スタート
    add_nodes = [len(G)+i for i, x in enumerate(xrange(num_of_node))]
    adding_node_attributes(G)
    # 連結するノードのペアをつくる
    for i in add_nodes:

        n = choice_tied_nodes(
            probabilities_G, id_sequenceG, edge_num_with_new_node
        )

        node_pairs = [(i, j) for j in n]
        G.add_edges_from(node_pairs)

        degree_sequenceG = [G.degree(x) for x in G]
        id_sequenceG = [x for x in G]
        degree_sequenceG = np.asarray(degree_sequenceG,
                                      dtype=np.float64)
        degrees_sum = degree_sequenceG.sum()
        probabilities_G = np.divide(degree_sequenceG, degrees_sum)

    adding_node_attributes(G)

    # 色情報追加
    for n in G:
        if n < number_of_init_graph_nodes:
            G.node[n]['color'] = 'b'
        else:
            G.node[n]['color'] = 'r'

    return G


def large_immigration(G, H):
    """Connect sub network to existed graph.

       It means that large number of immigrant come form sub network.

    Parameters
    ----------
    G : graph
        A networkx graph. It is base netowork.

    H : graph
        A networkx graph. It is immigrant network.

    Returns
    -------
    R : graph
      A networkx graph. Connected G and H.

    """
    connect_edge_ratio = 0.6

    R = nx.disjoint_union(G, H)
    # Hのラベルはlen(G)より大きい数値ラベルになる

    # それぞのグラフの各ノードの次数を出す
    degree_sequenceH = [R.degree(n) for n in R if n >= len(G)]  # Hのnode
    id_sequenceH = [n for n in R if n >= len(G)]

    degree_sequenceG = [R.degree(n) for n in R if n < len(G)]  # Gのnode
    id_sequenceG = [n for n in R if n < len(G)]

    degree_sequenceH = np.asarray(degree_sequenceH, dtype=np.float64)
    degree_sequenceG = np.asarray(degree_sequenceG, dtype=np.float64)

    bound = int(len(H) * connect_edge_ratio)

    probabilities_H = np.divide(degree_sequenceH, degree_sequenceH.sum())
    probabilities_G = np.divide(degree_sequenceG, degree_sequenceG.sum())

    node_in_H_connect_to_G = choice_tied_nodes(probabilities_H,
                                               id_sequenceH, bound)

    node_in_G_connect_to_H = [random_pick(id_sequenceG, probabilities_G)
                              for x in xrange(bound)]

    # 連結するノードのペアをつくる
    node_pairs = tuple(zip(node_in_G_connect_to_H, node_in_H_connect_to_G))

    R.add_edges_from(node_pairs)
    adding_node_attributes(R)

    """
    for n in R:
        print R.node[n]
    print "----------------------------------------"
    raw_input()
    adding_node_attributes(R)
    print "----------------------------------------"
    for n in R:
        print R.node[n]
    """

    # 色情報を追加
    for n in R:
        if n < len(G):
            R.node[n]['color'] = "b"
        else:
            R.node[n]['color'] = "r"

    return R
