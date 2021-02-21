import nltk
import spacy
import deplacy

nlp = spacy.load('en_core_web_sm')


# adding symbols to start and replacing an end
def replace_end_symbols(text):
    return ' '.join(['<S>', text.replace('.', '</S>').replace('!', '<EM>').replace('?', '<QM>').replace('!?', '<QM>')])


# replacing symbols in inner parts
def replace_inner_symbols(text):
    return text.replace('"', '<Q>').replace(',', '<Z>').replace(':', '<Z>').replace(';', '<Z>').replace('-', '<Z>') \
        .replace('and', 'CJ').replace('or', 'CJ')


def divide_into_clauses(sentence):
    doc = nlp(sentence)
    #deplacy.render(doc)
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
    return clauses


example = 'The CIA has been incompetent from its inception. ' \
          'The roster of incompetence includes subversion operations that cost the lives of hundreds of agents and accomplished nothing; ' \
          'CIA-managed coups that backfired, the Bay of Pigs and many others. ' \
          'Even operations that "succeeded" were pyrrhicThe CIA has been incompetent from its inception. ' \
          'The roster of incompetence includes subversion operations, that cost the lives of hundreds of agents and accomplished nothing; ' \
          'When you write a comic strip, the person on the left always speaks first. ' \
          'I used to jog, but the ice cubes kept falling out of my glass. '
sentences = nltk.sent_tokenize(example)
tagged_end_text = [replace_end_symbols(sentence) for sentence in sentences]
# print(tagged_end_text)
# clauses = [divide_into_clauses(sentence) for sentence in tagged_end_text]
# print(clauses)
tagged_inner_text = [replace_inner_symbols(sentence) for sentence in tagged_end_text]
# print(tagged_inner_text)



###### ЭТА ЧАСТЬ ПОД ВОПРОСОМ, ВЫДЕЛЕНИЕ КЛАУЗЕМ #########

#text = "The roster of incompetence includes subversion operations that cost the lives of hundreds of agents and accomplished nothing."
#text = "I used to jog, but the ice cubes kept falling out of my glass."
text = "I stopped believing in Santa Claus when my mother took me to see him in a department store, and he asked for my autograph."

clauses = divide_into_clauses(text)
for i, clause in clauses:
    print(i, clause)

########################################################