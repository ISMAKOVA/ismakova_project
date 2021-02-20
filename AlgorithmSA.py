import nltk


#adding symbols to start and replacing an end
def replace_end_symbols(text):
    return ' '.join(['<S>', text.replace('.', '</S>').replace('!', '<EM>').replace('?', '<QM>').replace('!?', '<QM>')])


#replacing symbols in inner part
def replace_inner_symbols(text):
    return text.replace('"', '<Q>').replace(',', '<Z>').replace(':', '<Z>').replace(';', '<Z>').replace('-', '<Z>')\
        .replace('and', 'CJ').replace('or', 'CJ')


example = 'The CIA has been incompetent from its inception. ' \
          'The roster of incompetence includes subversion operations that cost the lives of hundreds of agents and accomplished nothing; ' \
          'CIA-managed coups that backfired, the Bay of Pigs and many others. ' \
          'Even operations that "succeeded" were pyrrhicThe CIA has been incompetent from its inception. ' \
          'The roster of incompetence includes subversion operations that cost the lives of hundreds of agents and accomplished nothing; ' \
          'CIA-managed coups that backfired, the Bay of Pigs and many others. ' \
          'Even operations that "succeeded" were pyrrhic'
sentences = nltk.sent_tokenize(example)
tagged_end_text = [replace_end_symbols(sentence) for sentence in sentences]
print(tagged_end_text)
tagged_inner_text = [replace_inner_symbols(sentence) for sentence in tagged_end_text]
print(tagged_inner_text)
