#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Draw degree rank plot and graph with matplotlib.
"""

import os
import powerlaw
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
from scipy import *


dirpath = (os.path.abspath(__file__)).split('/')
dirpath = dirpath[1:-2]
dirpath.append('fig/')
dirpath = "/".join(dirpath)
save_dir = "/" + dirpath


def plot_figure(G, name, extention):
    """Plot network figure.

    Coution :
              If you use "eps" extention, be careful to file size.
              It will be get huge size file and you need very long time
              to make it.

    Parameters
    ----------
    G : graph
        A network graph

    name : string
        A graph name.

    extentin : string
       A graph file extention.


    """
    print("----------------------------------------")
    print("making network figure.")
    degree_list = G.degree()
    pos = nx.spring_layout(G)

    nx.draw_networkx_edges(G, pos, width=0.3)
    nx.draw_networkx_nodes(G, pos, node_color='r',
                           nodelist=degree_list.keys(),
                           node_size=degree_list.values()*1000, alpha=0.8)
    plt.axis('off')
    save_file = save_dir + name + "." + extention
    print "Save ->", save_file
    plt.savefig(save_file)
    print("----------------------------------------\n")
    plt.show()
    plt.close()


def plot_figure_with_color(G, name, extention):
    """Plot network figure. Setting color.

    Coution :
              If you use "eps" extention, be careful to file size.
              It will be get huge size file and you need very long time
              to make it.

    Parameters
    ----------
    G : graph
        A network graph

    name : string
        A graph name.

    extentin : string
       A graph file extention.

    """

    print("----------------------------------------")
    print("making network figure.")
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G)
    color_list = []
    degree_list = []
    nodes = G.nodes()

    for n in G:
        for m in nodes:
            if G.node[n]['ID'] == m:
                color_list.append(G.node[n]['color'])
                degree_list.append(len(G.node[n]['Neighbors']))

    nx.draw_networkx_edges(G, pos, width=0.3)
    nx.draw_networkx_nodes(G, pos, node_color=color_list,
                           nodelist=nodes,
                           node_size=degree_list*100, alpha=0.8)

    plt.axis('off')
    save_file = save_dir + name + "." + extention
    print "Save ->", save_file
    # dpiで解像度を指定、pad_inchesで余白を削る
    plt.savefig(save_file, dpi=200, bbox_inches="tight", pad_inches=0.0)
    print("----------------------------------------\n")
    plt.show()
    plt.close()


def degree_ranking(G, name, extention):
    """Plot ranking graph

    Parameters
    ----------
    G : graph
        A network graph

    name : string
        A graph name.

    extentin : string
       A graph file extention.

    """

    degree_sequence = sorted([G.degree(n) for n in G])
    degree_set = set(degree_sequence)
    sorted_degree = sorted(list(degree_set), reverse=True)
    degree_rank = [x+1 for x in xrange(len(sorted_degree))]

    rank_degree = dict(zip(sorted_degree, degree_rank))
    
    mapped_rank_degree = [rank_degree[deg] for deg in degree_sequence]

    plt.loglog(degree_sequence, mapped_rank_degree, 'b-', marker='o')
    plt.title("Degree rank plot")
    plt.ylabel("rank")
    plt.xlabel("degree")

    """
    # draw graph in inset
    plt.axes([0.45, 0.45, 0.45, 0.45])
    Gcc = sorted(nx.connected_component_subgraphs(G), key=len,
                 reverse=True)[0]

    pos = nx.spring_layout(Gcc)
    plt.axis('off')
    nx.draw_networkx_nodes(Gcc, pos, node_size=20)
    nx.draw_networkx_edges(Gcc, pos, alpha=0.4)
    """
    save_file = save_dir + name + "." + extention

    plt.savefig(save_file)
    print("----------------------------------------")
    print("Finish ranking analysis.")
    print "Save ->", save_file
    print("----------------------------------------\n")
    plt.close()


def degree_distribution(G, name, extention):
    """Plot ranking graph

    Parameters
    ----------
    G : graph
        A network graph

    name : string
        A graph name.

    extentin : string
       A graph file extention.

    """

    degree_sequence = sorted([G.degree(n) for n in G])

    data = np.asarray(degree_sequence, dtype=np.float64)

    # xminを次数の最低値にしてあげないと近似がうまく行かないかも
    fit = powerlaw.Fit(data, xlim=2.0)  # xmin=2.0とか
    """
    べき分布と指数分布のどちらがもっともらしいか検定をかける。
    もしR>0ならべき分布の方がもっともらしい。
    pはp値のことで、説明変数の係数や定数項が”たまたま”その値である確率を示す.
    ある説明変数の係数の p 値が 5 %以下であった場合、
    「この説明変数は 5 %以下の確率で”たまたま”この係数である」ということ.
    """
    # print fit.distribution_compare('power_law', 'exponential')
    """
    param = fit.power_law.alpha
    xmin = fit.power_law.xmin
    print xmin, param

    theoretical_distribution = powerlaw.Power_Law(xmin=xmin,
                                                  parameters=[param])
    simulated_data = theoretical_distribution.generate_random(10000)
    print min(simulated_data), xmin
    """
    alpha = fit.power_law.alpha
    fig = powerlaw.plot_pdf(data, color='b', label='Empirical Data')
    # powerlaw.plot_pdf(simulated_data, linewidth=3, ax=fig)
    """
    fit.power_law.plot_pdf(data, linestyle='--', color='r',
                           label='Power law fit',
                           linewidth=2)
    """
    # 指定した座標の上にテキストを追加
    # fig.text(1, 1, slope, ha='center', va='bottom')
    slope = "slope = " + str(alpha)
    handles, labels = fig.get_legend_handles_labels()
    fig.legend(handles, labels, loc=3)

    fig.set_ylabel("p(k)")
    fig.set_xlabel("degree k")

    plt.title("Degree Distribution [ " + slope + " ]")
    save_file = save_dir + name + "." + extention

    plt.savefig(save_file)
    print("----------------------------------------")
    print("Finish deistribution analysis.")
    print "Save ->", save_file
    print("----------------------------------------\n")
    plt.close()


def old_degree_distribution(G, name, extention):
    """Plot degree distribution of G

    Parameters
    ----------
    G : graph
        A network graph

    name : string
        A graph name.

    extentin : string
       A graph file extention.

    """

    degs = {}
    for n in G.nodes():
        deg = G.degree(n)
        if deg not in degs:
            degs[deg] = 0
        degs[deg] += 1

    items = sorted(degs.items())

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # x軸をlogにy軸をそのままの値に変えた
    ax.loglog([k for (k, v) in items], [v for(k, v) in items], marker='o')
    plt.title("Degree Distribution")
    save_file = save_dir + name + "." + extention

    fig.savefig(save_file)
    print("----------------------------------------")
    print("Finish deistribution analysis.")
    print "Save ->", save_file
    print("----------------------------------------\n")

    plt.close()
