# -*- coding: utf-8 -*-

def checker(sh1, sh2, *args):

    for field_name in args:
        if getattr(sh1, field_name) == getattr(sh2, field_name):
            print ".",
        else:
            print getattr(sh1, field_name)
            print getattr(sh2, field_name)
            print field_name, "..false",


def checker2(sh, di, *args):
    for field_name in args:
        if getattr(sh, field_name) == di[field_name]:
            print ".",
        else:
            print field_name, "..false"


def check_gene(g_array1, g_array2):

    for g1, g2 in zip(g_array1, g_array2):
        for field_name, field_type in g1._fields_:
            if field_name == "bit_array":
                g1_value = (
                    field_name, [x for x in getattr(g1, field_name)])
                g2_value = (
                    field_name, [x for x in getattr(g2, field_name)])
            else:
                g1_value = (field_name, getattr(g1, field_name))
                g2_value = (field_name, getattr(g2, field_name))

            if g1_value == g2_value:
                print ".",
            else:
                print field_name, "false"


def check_gene2(sh, di):

    gene_list = di["gene"]
    gene_array = sh.gene

    for g, t in zip(gene_array, gene_list):
        i = 0
        for field_name, field_type in g._fields_:
            if field_name == "bit_array":
                t2 = (field_name, [x for x in getattr(g, field_name)])
            else:
                t2 = (field_name, getattr(g, field_name))
            if t2 == t[i]:
                print ".",
            else:
                print field_name, "..false",
            i += 1


def checker_utter_heard(str_array1, str_array2, field_name):

    sh_list1 = [getattr(x, field_name)
                for x in getattr(str_array1, field_name)]
    sh_list2 = [getattr(x, field_name)
                for x in getattr(str_array2, field_name)]

    sh_list1 = [x for x in sh_list1 if x is not None]
    sh_list2 = [x for x in sh_list2 if x is not None]

    if sh_list1 == sh_list2:
        print ".",
    else:
        print field_name, "..false",


def checker_utter_heard2(sh, di, field_name):
    # utter, heardの中身は同じか
    sh_list = [getattr(x, field_name)
               for x in getattr(sh, field_name)]
    sh_list = [x for x in sh_list if x is not None]
    di_list = di[field_name]
    if sh_list == di_list:
        print ".",
    else:
        print field_name, "..false",


def is_equal_shared2dict(shared_array, knowledge_tuple):
    """c_to_pが正しく動いているか
    """

    word_checklist = ["stem",
                      "past",
                      "understand",
                      "freq",
                      "active",
                      "past_life"]

    for k_s in shared_array:
        shared_word_array = k_s.words
        # print shared_word_array
        word_dict = knowledge_tuple[k_s.id][0]
        if k_s.communicate == knowledge_tuple[k_s.id][1][1]:
            print ".",
        else:
            print "communicate..false"
        for stem, member_dict in sorted(word_dict.items()):
            # print stem
            for sw in shared_word_array:
                # word structのstemが同じならメンバーはすべて同じか
                if stem == sw.stem:
                    checker2(sw, member_dict, *word_checklist)
                    checker_utter_heard2(sw, member_dict, "utter")
                    checker_utter_heard2(sw, member_dict, "heard")
                    # geneが同じかどうかチェックする
                    check_gene2(sw, member_dict)


def check_memory(shared_array1, shared_array2):
    """共有メモリの中身がマッパーを通してもすべて同じかチェックする

    一度pythonの辞書を通しているので構造体の順番は必ずしも同じではない

    Parameters
    ----------
    shared_array1 : ctypes sturucture array

    shared_array2 : ctypes sturucture array

    """

    knowledge_checklist = ["id", "communicate"]

    word_checklist = ["stem",
                      "past",
                      "understand",
                      "freq",
                      "active",
                      "past_life"]

    for s1 in shared_array1:
        for s2 in shared_array2:
            if s1.id == s2.id:

                checker(s1, s2, *knowledge_checklist)

                s1_stems = [x.stem for x in s1.words]
                s2_stems = [x.stem for x in s2.words]
                s1_stems = [x for x in sorted(s1_stems)]
                s2_stems = [x for x in sorted(s2_stems)]

                for w1, w2 in zip(s1_stems, s2_stems):
                    w1_struct = [x for x in s1.words if w1 == x.stem][0]
                    w2_struct = [x for x in s2.words if w2 == x.stem][0]
                    checker(w1_struct, w2_struct, *word_checklist)

                    check_gene(w1_struct.gene, w2_struct.gene)

                    checker_utter_heard(w1_struct, w2_struct, "utter")

                    checker_utter_heard(w1_struct, w2_struct, "heard")


def check_dict(knowledge, agent_id, word_stem, field_name):
    """Check after c_to_p_convert knowledge dictionary

    Parameters
    ----------
    knowledge : dict
    """

    for k, v in knowledge.items():
        if k == agent_id:
            print "Agent ID : ", k
            word_dict = v[0]

            for x, y in word_dict.items():
                if x == word_stem:
                    member_dict = y
                    print "Word stem : ", x

                    for fn, fv in member_dict.items():
                        if fn == field_name:
                            print "Field value : ", fn
                            print fv


def check_fields(struct):
    """check any structs fields values
    """
    for field_name, field_type in struct._fields_:
        a1 = getattr(struct, field_name)
        a2 = type(getattr(struct, field_name))
        print field_name, getattr(struct, field_name)


def get_fields_value(struct):
    """Return fileds values

    Parameters
    ----------
    struct : ctypes struct

    Returns
    -------
    valuesd ; dict
    """

    values = {}

    for field_name, field_type in struct._fields_:
        values[field_name] = getattr(struct, field_name)

    return values
