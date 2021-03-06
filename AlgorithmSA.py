import nltk
import spacy
import deplacy
import re
from nrclex import NRCLex

nlp = spacy.load('en_core_web_sm')


# adding symbols to start and replacing an end
def replace_end_symbols(text):
    return ''.join(['<S> ', text.replace('.', '<S/>').replace('!', '<EM>').replace('?', '<QM>').replace('!?', '<QM>')])


def replace_all_tags(sentence):
    regex_alt = re.compile('\W?(not|no|never|none|neither|nobody|nothing|nowhere)\W')
    regex_th = re.compile('\W?(so|such)\W')
    regex_inc = re.compile('\W?(very|absolutely|completely|ever)\W')
    sentence = re.sub(regex_alt, " <ALT> ", sentence)
    sentence = re.sub(regex_th, " <TH> ", sentence)
    sentence = re.sub(regex_inc, " <INC> ", sentence)
    return sentence.replace('without', '<WT>').replace('"', '<Q>').replace(',', '<Z>').replace(':', '<Z>').replace(';', '<Z>').replace('-', '<Z>')


def mark_neg_pos(sentence):
    result = []
    for word in sentence.split():
        emotion = NRCLex(word)
        if 'positive' in emotion.affect_list:
            result.append('<POS>')
        elif 'negative' in emotion.affect_list:
            result.append('<NEG>')
        else:
            result.append(word)
    return result


# mark words written in caps
def mark_caps_CJ_pos_neg(sentence):
    marked_text = []
    for word in sentence.split():
        emotion = NRCLex(word.lower())
        if 'positive' in emotion.affect_list:
            if word.isupper() and word != 'I':
                marked_text.append('<POS><CAP>')
            else:
                marked_text.append('<POS>')
        elif 'negative' in emotion.affect_list:
            if word.isupper() and word != 'I':
                marked_text.append('<NEG><CAP>')
            else:
                marked_text.append('<NEG>')
        else:
            marked_text.append(replace_all_tags(word))
    return re.sub(r'[\ ]or|[\ ]and', ' CJ', ' '.join(marked_text))


def delete_words(sentence):
    result = []
    regex = re.compile('w+')
    for word in sentence.split():
        if not re.search('<[^/>][^>]*>', word):
            result.append('w')
        else:
            result.append(word)
    return re.sub(regex, "*", ''.join(result))


def lemmatization(sentence):
    lemm_sent = []
    for word in nlp(sentence):
        if word.text.isupper():
            lemm_sent.append(word.lemma_.upper())
        else:
            lemm_sent.append(word.lemma_)
    return ' '.join(lemm_sent)


def apply_rules(sentence):
    return sentence


def algorithm_sa_without_clauses(text):
    sentences = nltk.sent_tokenize(text)
    lemm_text = [lemmatization(sentence) for sentence in sentences]
    print(lemm_text)
    marked_text = [mark_caps_CJ_pos_neg(sentence) for sentence in lemm_text]
    tagged_end_text = [replace_end_symbols(sentence) for sentence in marked_text]
    print(tagged_end_text)
    polatity_do = [replace_all_tags(sentence) for sentence in tagged_end_text]
    print(polatity_do)
    res = [delete_words(sentence) for sentence in polatity_do]
    count_words = sum([len(sentence.split()) for sentence in marked_text])
    print(count_words)
    return res


example = 'AMAZING I LOVE it. The CIA has been not incompetent from its inception. ' \
          'The roster of incompetence includes subversion operations that cost the lives of hundreds of agents and accomplished nothing; ' \
          'CIA-managed coups that backfired, the Bay of Pigs and many others. ' \
          'Even operations that "succeeded" were pyrrhicThe CIA has been incompetent from its inception. ' \
          'I stopped believing in Santa Claus when my mother took me to see him in a department store, and he asked for my autograph. ' \
          'When you write a comic strip, the person on the left always speaks first. ' \
          'I used to jog, but the ice cubes kept falling out of my glass. '
example2 = '<POS> The CIA has been not no without incompetent from its inception. ' \
           'The roster of incompetence includes subversion operations that cost the lives of hundreds of agents and accomplished nothing; CIA-managed coups that backfired, the Bay of Pigs and many others. Even operations that "succeeded" were pyrrhic'
result = algorithm_sa_without_clauses(example)
print(result)
