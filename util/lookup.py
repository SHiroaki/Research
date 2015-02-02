# -*- coding: utf-8 -*-


def knowledge_lookup(agent_id, use_word, knowledges):
    """Lookup agent_id's knowledge in shared memory

    Parameter
    ---------
    agent_id : int

    use_word : string must be past tence form.
               It used by compare to WordStructure.words.past

    knowledges : List of KnowledgeStructure


    Return
    ------
    word_struct : WordStructure

    or

    None

    """

    agent_knowledge = [x for x in knowledges if x.id == agent_id][0]

    try:
        word_struct = [x for x in agent_knowledge.words
                       if x.past == use_word][0]
    except (IndexError):
        return None

    return word_struct
