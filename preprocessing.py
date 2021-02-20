import nltk
import spacy
nlp = spacy.load("en_core_web_sm")

para = '''Either the well was very deep, or she fell very slowly, for she had
plenty of time as she went down to look about her and to wonder what was going
to happen next. First, she tried to look down and make out what she was coming to,
but it was too dark to see anything; then she looked at the sides of the well, and
noticed that they were filled with cupboards and book-shelves; here and there she
saw maps and pictures hung upon pegs. She took down a jar from one of the shelves
as she passed; it was labelled 'ORANGE MARMALADE', but to her great disappointment it
was empty: she did not like to drop the jar for fear of killing somebody, so managed
to put it into one of the cupboards as she fell past it. Hello my friend, it is me, the man from France!'''


def prep(text):
    lemm_token_text = []
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        lemm_words = [word.lemma_ for word in nlp(sentence)]
        lemm_sent = " ".join(lemm_words)
        lemm_token_text.append(lemm_sent)
    return lemm_token_text


def adding_start_end_tags(sentences_arr):
    sent_with_tags = [' '.join(['<S>', sent.replace('.', '</S>')
                            .replace('!', '<!/S>').replace('?', '<?/S>')
                            .replace('!?', '<?!/S>')])
                      for sent in sentences_arr]

    return sent_with_tags



sentences_arr = prep(para)
print(sentences_arr)
sent_with_tags = adding_start_end_tags(sentences_arr)
print(sent_with_tags)