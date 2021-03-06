import nltk
import spacy
import deplacy
import re
from nrclex import NRCLex

nlp = spacy.load('en_core_web_sm')


# dividing sentence into clause, but only for Compound Sentences
def divide_into_clauses(sentence):
    doc = nlp(sentence)
    # deplacy.render(doc)
    seen = set()
    clauses = []

    for sent in doc.sents:
        heads = [cc for cc in sent.root.children if cc.dep_ == 'conj']
        # heads = [cc for cc in sent.root.children]

        for head in heads:
            words = [ww for ww in head.subtree]
            for word in words:
                seen.add(word)
            clause = (' '.join([ww.text for ww in words]))
            clauses.append((head.i, clause))

        unseen = [ww for ww in sent if ww not in seen]
        clause = ' '.join([ww.text for ww in unseen])
        clauses.append((sent.root.i, clause))
    clauses = sorted(clauses, key=lambda x: x[0])
    return [cl for i, cl in clauses]
