import spacy
from word import *
import json
import os
from google_trans_new import google_translator
import timeit

# BOOK = 'books/12mo/Meine Sachen.txt'
# BOOK = 'books/18mo/Gute Nacht, kleiner Löwe!.txt'
# BOOK = 'books/12mo/Mein Zoo Gucklochbuch.txt'
# BOOK = 'books/unrated/Der Kleine König - Teddy ist weg.txt'
BOOK = 'books/novels/kasperle_auf_reisen_ch1.txt'
# BOOK = 'books/novels/kasperle_auf_reisen.txt'

# get the list of POS codes
with open('lookup/pos_codes.json', 'r') as f:
    pos_codes = json.load(f)

# get the German to English dictionary
with open('lookup/german_english.json', 'r') as f:
    german_english = json.load(f)

# open and read the book
file = open(BOOK, 'rt')
corpus = file.read()

# init the words list
words = []

# init the translator
translator = google_translator()

# start a timer
start_time = timeit.default_timer()

# load the language model
# nlp = spacy.load('de_dep_news_trf')    # accuracy
nlp = spacy.load('de_core_news_sm')    # efficiency

# run the pipeline
doc = nlp(corpus)

# for every tokenized word
for token in doc:

    # remove stop words
    if token.is_stop:
        continue

    # remove certain parts of speech
    pos_list = ['INTJ', 'NUM', 'PRON', 'PROPN', 'PUNCT', 'SPACE', 'X']
    if token.pos_ in pos_list:
        continue

    # before translating, make the German text and lemma lowercase unless it's a noun
    case_list = ['NOUN', 'PROPN']
    if token.pos_ in case_list:
        text_case_filtered = token.text
        lemma_case_filtered = token.lemma_
    else:
        text_case_filtered = token.text.lower()
        lemma_case_filtered = token.lemma_.lower()

    # translate it using Google Translate
    translation = translator.translate(text_case_filtered, lang_src='de', lang_tgt='en')
    translation = translation.rstrip()

    # after translating, make the English text lowercase unless it's a proper noun
    case_list = ['PROPN']
    if token.pos_ in case_list:
        translation_case_filtered = translation
    else:
        translation_case_filtered = translation.lower()

    # translate it using the German-to-English dictionary
    translation_simple = german_english.get(text_case_filtered, 'NULL')
    translation_simple_lemma = german_english.get(lemma_case_filtered, 'NULL')

    # map the data into a custom Word object
    word = Word(text_case_filtered, lemma_case_filtered, f'{pos_codes[token.pos_]} ({token.pos_})', token.tag_,
                token.dep_, token.shape_, token.is_alpha, token.is_stop, token.lang_, translation_case_filtered,
                translation_simple, translation_simple_lemma, 1)

    # add this word to the list
    if word in words:
        words[words.index(word)].increase_count()
    else:
        words.append(word)

# set the vocabulary word list
vocab = Vocabulary(words)

# write a json file, to be read by the flashcards app
book_name = os.path.splitext(BOOK)[0].rpartition('/')[2]
with open(f'vocab/{book_name}.json', 'w') as f:
    f.write(VocabularySchema().dumps(vocab))

# write a human-readable version of the vocabulary
with open(f'vocab/{book_name}.txt', 'w') as f:
    [f.write(f'{word.text}, {word.lemma}, {word.translation}, {word.translation_simple}, {word.translation_simple_lemma}, {word.pos}\n') for word in vocab.words]

# log the total time it took
elapsed = timeit.default_timer() - start_time
print(f'Time: {elapsed:.2f} seconds')
