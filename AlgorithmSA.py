import os
import nltk
import spacy
import re
import csv
from nrclex import NRCLex

nlp = spacy.load('en_core_web_sm')


# добавление тегов в начало и конец предложения
def replace_end_symbols(text):
    return ''.join(['<S> ', text.replace('.', '<S/>')
                   .replace('?!', '<QM>').replace('!', '<EM>').replace('?', '<QM>')])


# замена специальнох слов и символов пунктуации тегами
def replace_all_tags(sentence):
    regex_alt = re.compile('\W?(not|no|never|none|neither|nobody|nothing|nowhere)\W')
    regex_th = re.compile('\W?(so|such)\W')
    regex_inc = re.compile('\W?(very|absolutely|completely|ever)\W')
    sentence = re.sub(regex_alt, " <ALT> ", sentence)
    sentence = re.sub(regex_th, " <TH> ", sentence)
    sentence = re.sub(regex_inc, " <INC> ", sentence)
    return sentence.replace('without', '<WT>').replace('"', '<Q>').replace(',', '<Z>') \
        .replace(':', '<Z>').replace(';', '<Z>').replace('-', '<Z>')


# замена слов с позитивным и негативным окрасом на соответсвтующие теги
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

    sentence = re.sub(regex_rule_3_1, "<POS>", sentence)
    sentence = re.sub(regex_rule_3_2, "<NEG>", sentence)
    sentence = re.sub(regex_rule_1_1, "<NEG>", sentence)
    sentence = re.sub(regex_rule_1_2, "<POS>", sentence)
    sentence = re.sub(regex_rule_2_1, "<NEG><NEG>", sentence)
    sentence = re.sub(regex_rule_2_2, "<POS><POS>", sentence)
    sentence = sentence.replace('<QM><EM>', '<QM>')
    sentence = re.sub(regex_rule_4, "<NEG>", sentence)
    sentence = re.sub(regex_rule_5, "<NEG>", sentence)
    sentence = re.sub(regex_rule_6, "<NEG>", sentence)
    sentence = re.sub(regex_rule_7_1, "<NEG>", sentence)
    sentence = re.sub(regex_rule_7_2, "<POS>", sentence)
    sentence = re.sub(regex_rule_9_1, "<POS><POS>", sentence)
    sentence = re.sub(regex_rule_9_2, "<NEG><NEG>", sentence)

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
    # print(lemm_text)
    marked_text = [mark_caps_CJ_pos_neg(sentence) for sentence in lemm_text]
    tagged_end_text = [replace_end_symbols(sentence) for sentence in marked_text]
    # print(tagged_end_text)
    polatity_do = [replace_all_tags(sentence) for sentence in tagged_end_text]
    # print(polatity_do)
    res = [delete_words(sentence) for sentence in polatity_do]
    with_rules = [sent for sent, count in [apply_rules(sentence) for sentence in res]]
    count_values = [count for sent, count in [apply_rules(sentence) for sentence in res]]
    total_value_of_doc = sum(count_values)
    sentiment = 1 if total_value_of_doc > 0 else 0
    print(with_rules)
    print(count_values)
    count_words = sum([len(sentence.split()) for sentence in marked_text])

    return sentences, with_rules, count_values, total_value_of_doc, sentiment


def from_data(text):
    result = []
    sentences, with_rules, count_values, total_value_of_doc, sentiment = algorithm_sa_without_clauses(text)
    for i in range(len(sentences)):
        result.append([sentences[i], with_rules[i], count_values[i]])

    return result, total_value_of_doc, sentiment


def make_sentiment_analysis(path):
    splitted_path = os.path.splitext(path)
    print(splitted_path[-1])
    if splitted_path[-1] == '.txt':
        text = read_txt(path)
        return from_data(text)
    elif splitted_path[-1] == '.csv':
        work_with_x_sv(path, "csv")
        return None
    elif splitted_path[-1] == '.tsv':
        work_with_x_sv(path, "tsv")
        return None


def read_txt(path):
    result = open(path)
    return result.read()


def read_csv(path):
    doc = []
    with open(path) as f:
        reader = csv.DictReader(f, delimiter=',')
        for line in reader:
            doc.append([line["id"], line["sentiment"], line["review"]])
    return doc


def read_tsv(path):
    doc = []
    with open(path) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for line in reader:
            doc.append([line["id"], line["sentiment"], line["review"]])
    return doc


def write_full_dataset(dataset, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        a_pen = csv.writer(file)
        columns = ['id', 'doc', 'markup', 'count', 'sentiment']
        a_pen.writerow(columns)
        for line in dataset:
            a_pen.writerow(line[0], line[1], line[2], line[3], line[4])


def additional_recording(file_name, line):
    with open(file_name, 'a', encoding='utf-8') as file:
        a_pen = csv.writer(file)
        a_pen.writerow([line[0], line[1], line[2], line[3], line[4]])
        # line consist of 'id', 'doc', 'markup', 'count', 'sentiment'


def write_confusion_matrix(number):
    conf_m = []
    with open("confusion_matrix.csv") as f:
        reader = csv.DictReader(f, delimiter=',')
        for line in reader:
            conf_m.append([line["TP"], line["FP"], line["TN"], line["FN"]])
    if number == 0:
        conf_m[0][0] = int(conf_m[0][0]) + 1
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


def work_with_x_sv(path, x):
    splitted_path = os.path.splitext(path)
    dataset = []
    for line in read_csv(path) if x == "csv" else read_tsv(path):
        sentences, with_rules, count_values, total_value_of_doc, sentiment = algorithm_sa_without_clauses(line[2])
        dataset.append([line[0], ' '.join(sentences), ' '.join(with_rules), total_value_of_doc, sentiment])
        if sentiment == 1 and int(line[1]) == 1:
            write_confusion_matrix(0)
        elif sentiment == 1 and int(line[1]) == 0:
            write_confusion_matrix(1)
        elif sentiment == 0 and int(line[1]) == 0:
            write_confusion_matrix(2)
        elif sentiment == 0 and int(line[1]) == 1:
            write_confusion_matrix(3)

    write_full_dataset(dataset, splitted_path[-2])


# def form_data(text):
#     formed_data = []
#     total_res = 0
#     sentences, with_rules = algorithm_sa_without_clauses(text)
#     for i in range(len(sentences)):
#         formed_data.append([sentences[i], with_rules[i][0], with_rules[i][1]])
#         total_res += with_rules[i][1]
#     return formed_data, total_res
#
#
# def write_doc(text):
#     res = ""
#     markup = ""
#     formed_data, total_res = form_data(text)
#     for i in formed_data:
#         res += i[0]
#         markup += i[1]
#     with open("doc.csv", 'a', encoding='utf-8') as file:
#         a_pen = csv.writer(file)
#         # columns = ['doc', 'class']
#         # a_pen.writerow(columns)
#         if total_res > 0:
#             a_pen.writerow([res, markup, total_res, 1])
#         else:
#             a_pen.writerow([res, markup, total_res, 0])
#
#
# def write_confusion_matrix(number):
#     conf_m = []
#     with open("confusion_matrix.csv") as f:
#         reader = csv.DictReader(f, delimiter=',')
#         for line in reader:
#             conf_m.append([line["TP"], line["FP"], line["TN"], line["FN"]])
#     if number == 0:
#         conf_m[0][0] = int(conf_m[0][0])+1
#     elif number == 1:
#         conf_m[0][1] = int(conf_m[0][1]) + 1
#     elif number == 2:
#         conf_m[0][2] = int(conf_m[0][2]) + 1
#     elif number == 3:
#         conf_m[0][3] = int(conf_m[0][3]) + 1
#     with open("confusion_matrix.csv", 'w', encoding='utf-8') as file:
#         a_pen = csv.writer(file)
#         columns = ['TP', 'FP', 'TN', 'FN']
#         a_pen.writerow(columns)
#         a_pen.writerow([conf_m[0][0], conf_m[0][1], conf_m[0][2], conf_m[0][3]])
#
#
# def read_confusion_matrix():
#     conf_m = []
#     with open("confusion_matrix.csv") as f:
#         reader = csv.DictReader(f, delimiter=',')
#         for line in reader:
#             conf_m.append([line["TP"], line["FP"], line["TN"], line["FN"]])
#     return conf_m
#
#
# def read_doc():
#     conf_m = []
#     c = 0
#     with open("doc.csv") as f:
#         reader = csv.DictReader(f, delimiter=',')
#         for line in reader:
#             if c > 100:
#                 break
#             else:
#                 print(line)
#                 conf_m.append([line["doc"], line["markup"], line["count"], line[" ton"]])
#                 c += 1
#     return conf_m
#
#
# def count_words(text):
#     sentences = nltk.sent_tokenize(text)
#     count_words = sum([len(sentence.split()) for sentence in sentences])
#     print("Words: ", count_words)
#     write_doc(text)
#     return count_words
#
#
# def work_with_dataset(file_name):
#     file = open(file_name)
#     read_tsv = csv.reader(file, delimiter="\t")
#     for line in read_tsv:
#         if line[0]!= "id":
#             write_doc(line[2])
#             formed_data, total_res = form_data(line[2])
#             if int(line[1]) == 1 and total_res > 0:
#                 write_confusion_matrix(0)
#             elif int(line[1]) == 1 and total_res <= 0:
#                 write_confusion_matrix(1)
#             elif int(line[1]) == 0 and total_res < 0:
#                 write_confusion_matrix(2)
#             elif int(line[1]) == 0 and total_res >= 0:
#                 write_confusion_matrix(3)

example = 'Happy? LOVE! The CIA has been not incompetent from its inception. ' \
          'The roster of incompetence includes subversion operations that cost the lives of hundreds of agents and accomplished nothing; ' \
          'CIA-managed coups that backfired, the Bay of Pigs and many others. ' \
          'Even operations that "succeeded" were pyrrhicThe CIA has been incompetent from its inception. ' \
          'I stopped believing in Santa Claus when my mother took me to see him in a department store, and he asked for my autograph. ' \
          'When you write a comic strip, the person on the left always speaks first. ' \
          'I used to jog, but the ice cubes kept falling out of my glass. '
example2 = '<POS> The CIA has been not no without incompetent from its inception. ' \
           'The roster of incompetence includes subversion operations that cost the lives of hundreds of agents and accomplished nothing; CIA-managed coups that backfired, the Bay of Pigs and many others. Even operations that "succeeded" were pyrrhic'
result = algorithm_sa_without_clauses(example)
# print()
# for i in form_data(example):
#     print(i[0], i[1], i[2])

# work_with_dataset("imdb_TrainData.tsv")
