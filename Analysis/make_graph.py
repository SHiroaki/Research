# -*- coding: utf-8 -*-

import cPickle as pickle
import matplotlib.pyplot as plt
from settings import read_verbdict

verbs = read_verbdict()
stems = verbs.keys()


f = open('verb_freq.dump')
freq = pickle.load(f)
f.close()


def read_result(file_path):

    f = open(file_path, "r")
    ed_result = f.read()
    # stems = ['cleed', 'skring', 'preed', 'sprink', 'spling']
    f.close()
    # print stems

    results = ed_result.split("\n")
    results = [line.split(" ") for line in results
               if len(line.split(" ")) == 3]

    result_dic = {}
    for s in stems:
        r = []
        for x in results:
            if s == x[0]:
                r.append(x)
        result_dic[s] = r

    return result_dic


def get_values(word, result_dic):

    t = [(float(x[1]), float(x[2])) for x in result_dic[word]]
    # genetation = [x[0] for x in t]
    values = [x[1] for x in t]
    return values


def make_graphs(word):

    path_ed = "解析結果BA12agent_100gen_ed.txt"
    path_e = "解析結果BA12agent_100gen_e.txt"
    path_o = "解析結果BA12agent_100gen_o.txt"
    path_oa = "解析結果BA12agent_100gen_oa.txt"
    path_oo = "解析結果BA12agent_100gen_oo.txt"
    path_u = "解析結果BA12agent_100gen_u.txt"
    path_ue = "解析結果BA12agent_100gen_ue.txt"
    path_uo = "解析結果BA12agent_100gen_uo.txt"

    result_ed = read_result(path_ed)
    result_e = read_result(path_e)
    result_o = read_result(path_o)
    result_oa = read_result(path_oa)
    result_oo = read_result(path_oo)
    result_u = read_result(path_u)
    result_ue = read_result(path_ue)
    result_uo = read_result(path_uo)

    # [(世代, 規則化率)...]
    # word = "sprink"
    ed = get_values(word, result_ed)
    e = get_values(word, result_e)
    o = get_values(word, result_o)
    oa = get_values(word, result_oa)
    oo = get_values(word, result_oo)
    u = get_values(word, result_u)
    ue = get_values(word, result_ue)
    uo = get_values(word, result_uo)

    genetation = [x for x in xrange(len(ed))]
    frequ = freq[word]
    fig, ax1 = plt.subplots()
    title = word + "- freq:" + str(frequ)
    plt.title(title, fontsize=25, fontname='serif')  # タイトル
    plt.ylim([0, 1])
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Activity Ratio")

    for tl in ax1.get_yticklabels():
        tl.set_color("black")

    line1 = ax1.plot(genetation, ed, "b", label="ed")
    line2 = ax1.plot(genetation, e, "g", label="e")
    line3 = ax1.plot(genetation, o, "r", label="o")
    line4 = ax1.plot(genetation, oa, "c", label="oa")
    line5 = ax1.plot(genetation, oo, "m", label="oo")
    line6 = ax1.plot(genetation, u, "y", label="u")
    line7 = ax1.plot(genetation, ue, "k", label="ue")
    line8 = ax1.plot(genetation, uo, "#ff8c00", label="uo")

    lns = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc="upper left")

    save_file = str(word) + ".png"
    print "Save ->", save_file
    plt.savefig(save_file)
    plt.close()

if __name__ == '__main__':
    for word in stems:
        make_graphs(word)
