# -*- coding: utf-8 -*-

from ctypes import *
import DataStructure
from copy import deepcopy


class KnowledgeHolder(object):
    """
    共有メモリ上のAgentの知識、その中のwords,geneなど
    を探索する.
    特定のAgentIDを検索すると各メソッドの返り値が自動的に
    セットされる.同時に配列のどこまで値が書き込まれているのか
    もチェックする.その位置から書き込みが行われる

    また逆にC言語の構造体に書き込む処理も行う.

    注意事項
    1.基本的に共有メモリは単一のプロセスしかアクセスできない.
    2.共有メモリは線形探索しかできない(と思う)
    3.共有メモリ上の構造体にアクセスするときはctypesの仕様で構造体
      のメンバーがそのままコピーされるわけではなく,ラッパーオブジェクト
      が返される.
    4.forループゴリ押しで探索しているが、下手に他の関数をかませると
      メモリの別の位置を参照しているみたいだから変えないでね
    """

    def __init__(self, c_knowledge_array, agent_id):
        self.knowledge_array = c_knowledge_array
        self.agent_id = agent_id
        # print "c_knowledge_array", c_knowledge_array
        # print "self.knowledge_array", self.knowledge_array

        # 発話する単語を選ぶときに使う
        self.activewords = []
        self.inlexicon = []

        # word, geneの構造体リストに新しく追加する場合のindex
        self.wordinsert = 0
        self.geneinsert = 0

        # ***書き込みの際には利用できない***.インスタンスを作った時点での情報
        # になる.最新版というわけではない
        self.knowledgestruct = None
        self.wordstruct = None
        self.any_wordstruct = None
        self.genestruct = None

        for x in self.knowledge_array:
            if self.agent_id == x.id:
                self.knowledgestruct = x  # ラッパーオブジェクトを取り出す
                break
        """
        for field_name, field_type in self.knowledgestruct._fields_:
            print field_name, getattr(self.knowledgestruct, field_name)
        """
        self.wordstruct = self.knowledgestruct.words

    def find_agent_knowlede(self):
        """
        指定されたagentの構造体を取ってくる
        """
        return self.knowledgestruct

    def find_word(self, word):
        """
        word は必ず語幹
        agentの構造体から指定されたword構造体をとってくる.
        持っていない場合はNone
        """
        self.word = word
        for i, x in enumerate(self.wordstruct):
            if word == x.stem:
                self.any_wordstruct = x

        return self.any_wordstruct

    def find_genes(self):
        """
        find_wordで見つけたwordのgeneを返す
        持っていない場合はNone
        """
        return self.genestruct

    def active_words(self):
        """active flagが立っている単語とその頻度
        """

        self.activewords = [x for x in self.wordstruct
                            if x.active != 0]
        self.activewords = [(x.stem, x.freq) for x in self.activewords]
        self.activewords_dict = {}

        for s, v in self.activewords:
            self.activewords_dict[s] = v
        return self.activewords_dict

    def in_lexicon_words(self):
        """stem_in_lexフラグが立っている単語
        """

        self.inlexicon = [x for x in self.wordstruct
                          if x.stem_in_lex != 0]

        return self.inlexicon

    """
    以下書き込み用の処理
    >>> かならず任意の単語を検索した後でないとエラーになる
    >>> 書き込む可能性があるのはgene, word
    >>> 新しい過去形はどうやって保持しておく?

    """

    def insert_gene(self, c_knowledge_array, p_bit_array, score):
        """使用した遺伝子配列を構造体に挿入する

        Parameters
        ----------
        c_knowledge_array : Shared memory

        bit_array : python list(numpy array) like object

        score : Int

        Returns
        -------

        """
        for x in c_knowledge_array:
            if self.agent_id == x.id:
                self.wordstruct = x.words  # ラッパーオブジェクトを取り出す
                break

        for x in self.wordstruct:
            if x.stem == self.word:
                self.genestruct = x.gene
                break

        used = 1

        c_bit_array = (c_int * len(p_bit_array))(*p_bit_array)

        new_gene = DataStructure.GeneStruct(
            c_bit_array,
            score,
            used
        )

        for i, x in enumerate(self.genestruct):
            if x.used != 1:
                # 配列のi番目から値を挿入できる
                self.geneinsert = i
                break

        self.genestruct[self.geneinsert] = new_gene

    def register_utter(self, c_knowledge_array, past_form):
        """自分が発話した過去形を登録する

        Parameters
        ----------
        c_knowledge_array : Shared memory
                             *** Not any agent's id ***

        past_form : Str

        """

        for x in c_knowledge_array:
            if self.agent_id == x.id:
                self.wordstruct = x.words  # ラッパーオブジェクトを取り出す
                break

        for x in self.wordstruct:
            if x.stem == self.word:
                self.utter_array = x.utter
                break

        for x in self.utter_array:
            if x.utter == "0":
                setattr(x, "utter", past_form)
                break

    def register_heard(self, c_knowledge_array, past):
        """自分が聞いた過去形を登録する


        Parameters
        ----------
        c_knowledge_array : Shared memory
                             *** Not any agent's id ***

        past_form : Str

        だめ
        buf = (c_char * len(past))(*past)
        buf_ptr = cast(buf, c_char_p)
        print buf_ptr
        """
        past_form = past

        for x in c_knowledge_array:
            if self.agent_id == x.id:
                self.wordstruct = x.words  # ラッパーオブジェクトを取り出す
                break

        for x in self.wordstruct:
            if x.stem == self.word:
                self.heard_array = x.heard
                break

        for x in self.heard_array:
            # 0の場合は何も入っていない
            if x.heard == "0":
                setattr(x, "heard", past_form)
                break

    def insert_wordstruct(self, c_knowledge_array, *args):
        """聞いたことがない新しい単語が入ってきた場合に登録する

        Parameters
        ----------
        c_knowledge_array : Shared memory
                             *** Not any agent's id ***

        args : tiple(stem:String, past:String, meaning:Int, freq:Int)

        """

        for x in c_knowledge_array:
            if self.agent_id == x.id:
                self.wordstruct = x.words  # ラッパーオブジェクトを取り出す
                break

        notsetted_field_value = [
            #  Initialize filed value
            1,     # active
            0,     # stem_in_lex
            0,     # past_in_lex
            1000   # life
            ]

        field_value = [x for x in args]
        field_value.extend(notsetted_field_value)
        new_word = DataStructure.WordStruct(*field_value)
        # new_word_address = addressof(new_word)

        for i, x in enumerate(self.wordstruct):
            if x.stem is None:
                self.wordinsert = i
                # self.insertaddres = addressof(x)
                # print self.wordinsert
                break

        # メモリにバイナリを書き込む方法でもうまく行く
        # ただ共有メモリのシンクロが効いているかわからないから危険
        # memmove(self.insertaddres, new_word_address, sizeof(new_word))
        # この書き込みでもうまくいく
        self.wordstruct[self.wordinsert] = new_word

    def overwrite_past_form(self, c_knowledge_array, new_past_form):
        """過去形の形を変更刷る場合に呼ぶ
        word構造体のpastだけ書き換える

        Parameters
        ----------
        c_knowledge_array : Shared memory
                             *** Not any agent's knowledge ***

        new_past_form : string

        """

        for x in c_knowledge_array:
            if self.agent_id == x.id:
                self.wordstruct = x.words  # ラッパーオブジェクトを取り出す
                break

        for i, x in enumerate(self.wordstruct):
            if x.stem == self.word:
                self.wordinsert = i
                # overwrite_target_struct = x
                setattr(x, "past", new_past_form)
                break
        """
        values = DataStructure.get_fields_value(overwrite_target_struct)
        values['past'] = new_past_form
        new_word = DataStructure.WordStruct()

        for field_name, field_type in new_word._fields_:
            setattr(new_word, field_name, values.get(field_name, 0))


        print "new_word check", new_word
        DataStructure.check_fields(new_word)
        self.wordstruct[self.wordinsert] = new_word
        """
    def increment_comunicate_count(self, c_knowledge_array):
        """コミュニケーションした回数
        """
        for k in c_knowledge_array:
            if k.id == self.agent_id:
                c = k.communicate + 1
                setattr(k, "communicate", c)

    def increment_understand_count(self, c_knowledge_array):
        """任意の単語の過去形が理解された回数
        """
        for k in c_knowledge_array:
            if k.id == self.agent_id:
                w = k.words
                break

        for x in w:
            if x.stem == self.word:
                u = x.understand + 1
                setattr(x, "understand", u)
                break

    def decrement_wordlife(self, c_knowledge_array):
        """Holdしているagentのすべての単語のlifeをデクリメントする.
        最新の共有メモリを使わなければいけないので、必ず共有メモリ
        を受け取ること

        """

        for k in c_knowledge_array:
            if k.id == self.agent_id:
                w = k.words
                break

        for x in w[:self.wordinsert + 1]:
            x.life = x.life - 1
