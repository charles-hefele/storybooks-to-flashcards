import json
import timeit
import nltk
from HanTa import HanoverTagger as ht
from word import *
import os
from nltk.corpus import stopwords
from spacy.lang.de.stop_words import STOP_WORDS

BOOK = 'books/12mo/Meine Sachen.txt'
# BOOK = 'books/18mo/Gute Nacht, kleiner Löwe!.txt'
# BOOK = 'books/12mo/Mein Zoo Gucklochbuch.txt'
# BOOK = 'books/unrated/Der Kleine König - Teddy ist weg.txt'
# BOOK = 'books/novels/kasperle_auf_reisen_ch1.txt'
# BOOK = 'books/novels/kasperle_auf_reisen.txt'
# BOOK = 'books/novels/test.txt'

STOP_WORDS_SET = 'spacy'
# STOP_WORDS_SET = 'nltk'

# open and read the book
file = open(BOOK, 'rt')
corpus = file.read()

# get the list of POS codes
with open('lookup/pos_codes_hanta.json', 'r') as f:
    pos_codes = json.load(f)

# init the words list
words = []

# create the tagger
tagger = ht.HanoverTagger('morphmodel_ger.pgz')

# start a timer
start_time = timeit.default_timer()

# sentenize the corpus
sentences = nltk.sent_tokenize(corpus)

for sentence in sentences:

    # tokenize the sentence
    tokenizer = nltk.RegexpTokenizer(r'[a-zA-ZäÄüÜöÖß\']+')
    tokens = tokenizer.tokenize(sentence)

    if STOP_WORDS_SET == 'spacy':
        tokens = [t for t in tokens if not t.lower() in STOP_WORDS]  # spacy stop words
    else:
        stop_words = set(stopwords.words('german'))
        tokens = [t for t in tokens if not t.lower() in stop_words]  # nltk stop words

    # generate POS and lemmata for the tokens
    tags = tagger.tag_sent(tokens, taglevel=1)

    for tag in tags:
        text = tag[0]
        lemma = tag[1]
        pos = tag[2]

        # remove certain parts of speech
        pos_list = ['ART', 'CARD', 'FM', 'ITJ', 'KON', 'KOUS', 'NE', 'PDAT', 'PDS', 'PIAT', 'PIS', 'PRELS', 'PTKA',
                    'PTKANT', 'PWS', 'XY']
        if pos in pos_list:
            continue

        # skip any tokens where the lemma contains an apostrophe
        if '\'' in lemma:
            continue

        # fix capitalization
        if pos != 'NN':
            text = text.lower()

        # replace sentence newlines with spaces
        sentence = sentence.replace('\n', ' ')

        # map the data into a custom Word object
        word = Word(text, lemma, f'{pos}: {pos_codes.get(pos)}')

        # add this word to the list
        if word in words:
            words[words.index(word)].add_new_sentence(sentence)
            words[words.index(word)].increase_count()
        else:
            word.add_new_sentence(sentence)
            words.append(word)

# set the vocabulary word list
vocab = Vocabulary(words)

# write the vocabulary to a json file
book_name = os.path.splitext(BOOK)[0].rpartition('/')[2]
with open(f'vocab/{book_name}.json', 'w') as f:
    f.write(VocabularySchema().dumps(vocab))

# write a human-readable version of the vocabulary
with open(f'vocab/{book_name}.txt', 'w') as f:
    [f.write(word.shorthand()) for word in vocab.words]

corpus_split_len = len(corpus.split())
print(f'Generated {len(words)} flashcards out of {corpus_split_len} words ({len(words)/corpus_split_len:.0%})')

elapsed = timeit.default_timer() - start_time
print(f'Time for flashcard creation: {elapsed:.2f} seconds')
