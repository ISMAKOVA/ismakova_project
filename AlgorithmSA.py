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
    return text.replace('"', '<Q>').replace(',', '<Z>').replace(':', '<Z>').replace(';', '<Z>').replace('-', '<Z>')


# mark words written in caps
def mark_caps_CJ(sentence):
    marked_text = []
    for word in sentence.split():
        if word.isupper() and word != 'CJ' and word != 'I':
            word = ''.join([word, '<CAP>'])
            marked_text.append(word)
        else:
            marked_text.append(word)
    return re.sub(r'[\ ]or|[\ ]and', ' CJ', ' '.join(marked_text))


def lemmatization(sentence):
    lemm_sent = []
    for word in nlp(sentence):
        if word.text.isupper():
            lemm_sent.append(word.lemma_.upper())
        else:
            lemm_sent.append(word.lemma_)
    return ' '.join(lemm_sent)


def polarity_modifiers(sentence):
    return sentence.replace('not', '<ALT>').replace('no', '<ALT>').replace('neither', '<ALT>').replace('never', '<ALT>') \
        .replace('none', '<ALT>').replace('nobody', '<ALT>').replace('nothing', '<ALT>').replace('nowhere', '<ALT>')\
        .replace('without', '<WT>')


def polarity_amplifiers(sentence):
    return sentence.replace('very', '<INC>').replace('absolutely', '<INC>').replace('completely', '<INC>')\
        .replace('ever', '<INC>')


def polarity_anti_modifiers(sentence):
    return sentence.replace('so', '<TH>').replace('such', '<TH>')

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
    # result = []
    # for i, cl in clauses:
    #     if i == 1:
    #         cl = ''.join(cl.split())
    #         result.append(cl)
    #     else:
    #         result.append(cl)
    return [cl for i, cl in clauses]


def algorithm_sa_without_clauses(text):
    sentences = nltk.sent_tokenize(text)
    lemm_text = [lemmatization(sentence) for sentence in sentences]
    # print(lemm_text)
    marked_text = [mark_caps_CJ(sentence) for sentence in lemm_text]
    # print(marked_text)
    tagged_end_text = [replace_end_symbols(sentence) for sentence in marked_text]
    # print(tagged_end_text)
    tagged_inner_text = [replace_inner_symbols(sentence) for sentence in tagged_end_text]
    count_words = sum([len(sentence.split()) for sentence in marked_text])
    print(count_words)
    return tagged_inner_text


example = 'The CIA has been not incompetent from its inception. ' \
          'The roster of incompetence includes subversion operations that cost the lives of hundreds of agents and accomplished nothing; ' \
          'CIA-managed coups that backfired, the Bay of Pigs and many others. ' \
          'Even operations that "succeeded" were pyrrhicThe CIA has been incompetent from its inception. ' \
          'I stopped believing in Santa Claus when my mother took me to see him in a department store, and he asked for my autograph. ' \
          'When you write a comic strip, the person on the left always speaks first. ' \
          'I used to jog, but the ice cubes kept falling out of my glass. '
example2 = 'The CIA has been not no without incompetent from its inception. ' \
           'The roster of incompetence includes subversion operations that cost the lives of hundreds of agents and accomplished nothing; CIA-managed coups that backfired, the Bay of Pigs and many others. Even operations that "succeeded" were pyrrhic'
result = algorithm_sa_without_clauses(example)
# print(result)

alt = polarity_modifiers(example2)
print(alt)
# print('-----------tagged_end_text------------')
# tagged_end_text = [replace_end_symbols(sentence) for sentence in sentences]
# print(tagged_end_text)
# print('-----------tagged_inner_text------------')
# tagged_inner_text = [replace_inner_symbols(sentence) for sentence in tagged_end_text]
# print(tagged_inner_text)

################ for clauses #########################
# print('-----------divide_into_clauses------------')
# clauses = [divide_into_clauses(sentence) for sentence in tagged_end_text]
# print(clauses)
#
# print('-----------tagged_inner_text------------')
# tagged_inner_text = [[replace_inner_symbols(chunk) for chunk in clause] for clause in clauses]
# print(tagged_inner_text)
#####################################################


# print('-----------marked_CAPS_text ans splitted ------------')
# marked_text = [mark_caps_CJ(sentence.split()) for sentence in tagged_inner_text]
# print(marked_text)
#
#
# print('-----------count_words------------')
# count_words = sum([len(sentence) for sentence in marked_text])
# print(count_words)
