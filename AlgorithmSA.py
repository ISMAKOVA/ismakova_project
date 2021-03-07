import nltk
import spacy
import deplacy
import re
import csv
from nrclex import NRCLex

nlp = spacy.load('en_core_web_sm')


# adding symbols to start and replacing an end
def replace_end_symbols(text):
    return ''.join(['<S> ', text.replace('.', '<S/>').replace('?!', '<QM>').replace('!', '<EM>').replace('?', '<QM>')])


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
    return re.sub(r'[\ ]or|[\ ]and', ' <CJ>', ' '.join(marked_text))


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
    count = 0
    regex_rule_1_1 = re.compile('<ALT>((?!<Z>|<CJ>|<TH>|<NEG>).)*<POS>|<POS>((?!<Z>|<CJ>|<TH>|<NEG>).)*<ALT>')
    regex_rule_1_2 = re.compile('<ALT>((?!<Z>|<CJ>|<TH>|<POS>).)*<NEG>|<NEG>((?!<Z>|<CJ>|<TH>|<POS>).)*<ALT>')
    regex_rule_2_1 = re.compile('<INC>((?!<Z>|<CJ>|<TH>|<POS>).)*<NEG>|<NEG>((?!<Z>|<CJ>|<TH>|<POS>).)*<INC>')
    regex_rule_2_2 = re.compile('<INC>((?!<Z>|<CJ>|<TH>|<NEG>).)*<POS>|<POS>((?!<Z>|<CJ>|<TH>|<NEG>).)*<INC>')
    regex_rule_3_1 = re.compile('<TH><ALT>((?!<Z>|<CJ>|<NEG>).)*<POS>')
    regex_rule_3_2 = re.compile('<TH><ALT>((?!<Z>|<CJ>|<POS>).)*<NEG>')
    regex_rule_4 = re.compile('<S><POS><QM>')
    regex_rule_5 = re.compile('<S>((?!<NEG>|<POS>).)*<QM>')
    regex_rule_6 = re.compile('<Q><POS><Q>')
    regex_rule_7_1 = re.compile('(?:<WT>|<ALT>)<POS>')
    regex_rule_7_2 = re.compile('(?:<WT>|<ALT>)<NEG>')
    regex_rule_8 = re.compile('.*<EM>')
    regex_rule_9_1 = re.compile('<POS><CAP>|<CAP><POS>')
    regex_rule_9_2 = re.compile('<NEG><CAP>|<CAP><NEG>')

    #print(1, sentence)
    sentence = re.sub(regex_rule_3_1, "<POS>", sentence)
    # print(2, sentence)
    sentence = re.sub(regex_rule_3_2, "<NEG>", sentence)
    # print(3, sentence)
    sentence = re.sub(regex_rule_1_1, "<NEG>", sentence)
    # print(4, sentence)
    sentence = re.sub(regex_rule_1_2, "<POS>", sentence)
    # print(5, sentence)
    sentence = re.sub(regex_rule_2_1, "<NEG><NEG>", sentence)
    # print(6, sentence)
    sentence = re.sub(regex_rule_2_2, "<POS><POS>", sentence)
    # print(7, sentence)
    sentence = sentence.replace('<QM><EM>', '<QM>')
    # print(8, sentence)
    sentence = re.sub(regex_rule_4, "<NEG>", sentence)
    # print(9, sentence)
    sentence = re.sub(regex_rule_5, "<NEG>", sentence)
    # print(10, sentence)
    sentence = re.sub(regex_rule_6, "<NEG>", sentence)
    # print(11, sentence)
    sentence = re.sub(regex_rule_7_1, "<NEG>", sentence)
    # print(12, sentence)
    sentence = re.sub(regex_rule_7_2, "<POS>", sentence)
    # print(13, sentence)
    sentence = re.sub(regex_rule_9_1, "<POS><POS>", sentence)
    # print(14, sentence)
    sentence = re.sub(regex_rule_9_2, "<NEG><NEG>", sentence)
    # print(15, sentence)

    count += -1 * len(re.findall(re.compile('<NEG>'), sentence))
    count += 1 * len(re.findall(re.compile('<POS>'), sentence))
    if re.fullmatch(regex_rule_8, sentence):
        if count > 0:
            count += 1
        else:
            count -= 1
    print(count)
    return sentence, count


def algorithm_sa_without_clauses(text):
    sentences = nltk.sent_tokenize(text)
    lemm_text = [lemmatization(sentence) for sentence in sentences]
    #print(lemm_text)
    marked_text = [mark_caps_CJ_pos_neg(sentence) for sentence in lemm_text]
    tagged_end_text = [replace_end_symbols(sentence) for sentence in marked_text]
    #print(tagged_end_text)
    polatity_do = [replace_all_tags(sentence) for sentence in tagged_end_text]
    #print(polatity_do)
    res = [delete_words(sentence) for sentence in polatity_do]
    with_rules = [apply_rules(sentence) for sentence in res]
    #print(with_rules)
    count_words = sum([len(sentence.split()) for sentence in marked_text])

    return sentences, with_rules


def form_data(text):
    formed_data = []
    total_res = 0
    sentences, with_rules = algorithm_sa_without_clauses(text)
    for i in range(len(sentences)):
        formed_data.append([sentences[i], with_rules[i][0], with_rules[i][1]])
        total_res += with_rules[i][1]
    return formed_data, total_res


def write_doc(text):
    res = ""
    formed_data, total_res = form_data(text)
    for i in formed_data:
        res += i[0]
    with open("doc.csv", 'a', encoding='utf-8') as file:
        a_pen = csv.writer(file)
        # columns = ['doc', 'class']
        # a_pen.writerow(columns)
        a_pen.writerow([res, total_res])


def write_confusion_matrix(number):
    conf_m = []
    with open("confusion_matrix.csv") as f:
        reader = csv.DictReader(f, delimiter=',')
        for line in reader:
            conf_m.append([line["TP"], line["FP"], line["TN"], line["FN"]])
    if number == 0:
        conf_m[0][0] = int(conf_m[0][0])+1
    elif number == 1:
        conf_m[0][1] = int(conf_m[0][1]) + 1
    elif number == 2:
        conf_m[0][2] = int(conf_m[0][2]) + 1
    elif number == 3:
        conf_m[0][3] = int(conf_m[0][3]) + 1
    with open("confusion_matrix.csv", 'w', encoding='utf-8') as file:
        a_pen = csv.writer(file)
        columns = ['TP', 'FP', 'TN', 'FN']
        a_pen.writerow(columns)
        a_pen.writerow([conf_m[0][0], conf_m[0][1], conf_m[0][2], conf_m[0][3]])


def read_confusion_matrix():
    conf_m = []
    with open("confusion_matrix.csv") as f:
        reader = csv.DictReader(f, delimiter=',')
        for line in reader:
            conf_m.append([line["TP"], line["FP"], line["TN"], line["FN"]])
    return conf_m


def count_words(text):
    sentences = nltk.sent_tokenize(text)
    count_words = sum([len(sentence.split()) for sentence in sentences])
    print("Words: ", count_words)
    write_doc(text)
    return count_words



example = 'Happy? LOVE! The CIA has been not incompetent from its inception. ' \
          'The roster of incompetence includes subversion operations that cost the lives of hundreds of agents and accomplished nothing; ' \
          'CIA-managed coups that backfired, the Bay of Pigs and many others. ' \
          'Even operations that "succeeded" were pyrrhicThe CIA has been incompetent from its inception. ' \
          'I stopped believing in Santa Claus when my mother took me to see him in a department store, and he asked for my autograph. ' \
          'When you write a comic strip, the person on the left always speaks first. ' \
          'I used to jog, but the ice cubes kept falling out of my glass. '
example2 = '<POS> The CIA has been not no without incompetent from its inception. ' \
           'The roster of incompetence includes subversion operations that cost the lives of hundreds of agents and accomplished nothing; CIA-managed coups that backfired, the Bay of Pigs and many others. Even operations that "succeeded" were pyrrhic'
# result = algorithm_sa_without_clauses(example)
# print()
# for i in form_data(example):
#     print(i[0], i[1], i[2])

write_confusion_matrix(2)