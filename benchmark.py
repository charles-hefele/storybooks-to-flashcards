import spacy
import timeit
import nltk
from HanTa import HanoverTagger as ht
from pprint import pprint

# BOOK = 'books/12mo/Meine Sachen.txt'
# BOOK = 'books/18mo/Gute Nacht, kleiner Löwe!.txt'
# BOOK = 'books/12mo/Mein Zoo Gucklochbuch.txt'
# BOOK = 'books/unrated/Der Kleine König - Teddy ist weg.txt'
BOOK = 'books/novels/kasperle_auf_reisen_ch1.txt'
# BOOK = 'books/novels/kasperle_auf_reisen.txt'

# open and read the book
file = open(BOOK, 'rt')
corpus = file.read()

# HanTa
tagger = ht.HanoverTagger('morphmodel_ger.pgz')
start_time = timeit.default_timer()
tokens = nltk.word_tokenize(corpus, 'german')
lemmata = tagger.tag_sent(tokens, taglevel=1)
# pprint(lemmata)
elapsed = timeit.default_timer() - start_time
print(f'Time for HanTa: {elapsed:.1f} seconds')

# spaCy - efficiency
start_time = timeit.default_timer()
nlp = spacy.load('de_core_news_sm')
doc = nlp(corpus)
# pprint(doc)
elapsed = timeit.default_timer() - start_time
print(f'Time for spaCy efficiency: {elapsed:.1f} seconds')

# spaCy - accuracy
start_time = timeit.default_timer()
nlp = spacy.load('de_dep_news_trf')
doc = nlp(corpus)
# pprint(doc)
elapsed = timeit.default_timer() - start_time
print(f'Time for spaCy accuracy: {elapsed:.1f} seconds')
