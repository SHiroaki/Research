# -*- coding: utf-8 -*-

import random
import numpy as np
from random_pick import random_prob_pick
import networkx as nx
from networkx.utils import is_string_like
from settings import utter_setting


def m3():
    """無限に整数を返すジェネレーター
    """
    i = 0
    while True:
        i += 1
        yield i


g = m3()


def make_keystring():

    source_str = 'abcdefghijklmnopqrstuvwxyz'
    keystring = "".join([random.choice(source_str) for x in xrange(10)])
    keystring = keystring + str(g.next())
    return keystring


def adding_node_attributes(G, pre=None):
    """Adding attributes to nodes.

    アトリビュートを持っていないノードに登録を行う

    Parameters
    ----------
    G : graph
        A networkx graph

    prefix : string
        Rename node like a prefix + n.

    Returns
    ------
    G : Networkx graph

    """

    def add_prefix(graph, prefix):

        if prefix is None:
            return graph

        def label(x):
            if is_string_like(x):
                name = prefix+x
            else:
                name = prefix+repr(x)
            return name
        return nx.relabel_nodes(graph, label)

    G_relabel = add_prefix(G, pre)

    for n in G_relabel:

        # このループですべてのnodeを走査できる
        new_neighbors = G_relabel.neighbors(n)
        G_relabel.node[n]['ID'] = n
        G_relabel.node[n]['Time'] = 0
        G_relabel.node[n]['Neighbors'] = new_neighbors
        G_relabel.node[n]["utter_count"] = len(new_neighbors) * utter_setting()

        # keyは二度と更新されることはない
        if G_relabel.node[n].get("key"):
            # print "I have key string."
            continue
        else:
            G_relabel.node[n]['key'] = make_keystring()
            # print "Generate new key string"

    return G_relabel


def connect_new_node(numpy_adjacency_matrix, target_nodes, changed_row):
    """Connect new node.

    Replace ndmatrix[new_node, target_node] to 1.
    It means that new_node connect with target node.

    Parameters
    ----------
    numpy_adjacency_matrix : Numpy matrix
        Already added new node col and row(Not initial matrix).

    target_nodes : Python List
        It made by choice_tied_nodes.

    changed_row : integer
        Manipulate this row.

    Returns
    -------
    numpy_adjacency_matrix : Numpy matrix
    """

    for x in target_nodes:
        numpy_adjacency_matrix[changed_row, x] = 1

    return numpy_adjacency_matrix


def choice_tied_nodes(p, node_list, number_of_add_nodes):
    """Judge a link new edge with exist node or not.

    Parameters
    ----------
    p : Numpy ndarray
        Tied probabilities of all node.

    node_list : List of node.
        We select linked node in this list.

    number_of_add_edge : integer
        New edge number want to link.

    Returns
    -------
    link_target_nodes : List
       [linked_node, ....] Length of list is equal to number_of_add_edge.

    """

    link_target_nodes = []

    while True:
        #  必要な数が揃うまで繰り返す
        picked_node = random_prob_pick(node_list, p)

        if len(link_target_nodes) == number_of_add_nodes:
            break

        elif picked_node not in link_target_nodes:
            link_target_nodes.append(picked_node)

    return link_target_nodes


def get_degree_of_node(G_numpy_adjacency_matrix):
    """Calc dgree of node.

    Parameters
    ----------
    G_numpy_adjacency_matrix : Numpy matrix
         Adjacency List of networkx graph.

    Returns
    ------
    degrees : numpy ndarrary
        Degree of all node
    """

    degrees = np.sum(G_numpy_adjacency_matrix, axis=1)  # 行方向の和を取る
    return np.asarray(degrees)
