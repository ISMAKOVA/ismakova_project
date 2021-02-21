import nltk
import spacy
import deplacy
import re

nlp = spacy.load('en_core_web_sm')


# adding symbols to start and replacing an end
def replace_end_symbols(text):
    return ''.join(['<S>', text.replace('.', '</S>').replace('!', '<EM>').replace('?', '<QM>').replace('!?', '<QM>')])


# replacing symbols in inner parts
def replace_inner_symbols(text):
    text_replaced = text.replace('"', '<Q>').replace(',', '<Z>').replace(':', '<Z>').replace(';', '<Z>').replace('-', '<Z>')
    return re.sub(r'[\ ]or|[\ ]and', ' CJ', text_replaced)


def mark_caps(splitted_sentence):
    marked_text = []
    for word in splitted_sentence:
        if word.isupper() and word != 'CJ' and word != 'I':
            word = ''.join([word, '<CAP>'])
            marked_text.append(word)
        else:
            marked_text.append(word)
    return marked_text



#dividing sentence into clause, but only for Compound Sentences
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
    # result = []
    # for i, cl in clauses:
    #     if i == 1:
    #         cl = ''.join(cl.split())
    #         result.append(cl)
    #     else:
    #         result.append(cl)
    return [cl for i, cl in clauses]


exampleq = 'The CIA has been incompetent from its inception. ' \
          'The roster of incompetence includes subversion operations that cost the lives of hundreds of agents and accomplished nothing; ' \
          'CIA-managed coups that backfired, the Bay of Pigs and many others. ' \
          'Even operations that "succeeded" were pyrrhicThe CIA has been incompetent from its inception. ' \
          'I stopped believing in Santa Claus when my mother took me to see him in a department store, and he asked for my autograph. ' \
          'When you write a comic strip, the person on the left always speaks first. ' \
          'I used to jog, but the ice cubes kept falling out of my glass. '
example ='The CIA has been incompetent from its inception. The roster of incompetence includes subversion operations that cost the lives of hundreds of agents and accomplished nothing; CIA-managed coups that backfired, the Bay of Pigs and many others. Even operations that "succeeded" were pyrrhic'
sentences = nltk.sent_tokenize(example)
print('-----------tagged_end_text------------')
tagged_end_text = [replace_end_symbols(sentence) for sentence in sentences]
print(tagged_end_text)
print('-----------tagged_inner_text------------')
tagged_inner_text = [replace_inner_symbols(sentence) for sentence in tagged_end_text]
print(tagged_inner_text)

################ for clauses #########################
# print('-----------divide_into_clauses------------')
# clauses = [divide_into_clauses(sentence) for sentence in tagged_end_text]
# print(clauses)
#
# print('-----------tagged_inner_text------------')
# tagged_inner_text = [[replace_inner_symbols(chunk) for chunk in clause] for clause in clauses]
# print(tagged_inner_text)
#####################################################


print('-----------marked_CAPS_text ans splitted ------------')
marked_text = [mark_caps(sentence.split()) for sentence in tagged_inner_text]
print(marked_text)


print('-----------count_words------------')
count_words = sum([len(sentence) for sentence in marked_text])
print(count_words)
