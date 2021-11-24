import timeit
from google_trans_new import google_translator
from tqdm import tqdm
from word import *
import os

# BOOK = 'Meine Sachen'
# BOOK = 'Mein Zoo Gucklochbuch'
# BOOK = 'Der Kleine König - Teddy ist weg'
# BOOK = 'Kasperle auf Reisen - Chapter 1'
BOOK = 'Kasperle auf Reisen'

VOCAB_INPUT = f'vocab/{BOOK}.json'

# read the data
with open(VOCAB_INPUT, 'r') as file:
    contents = file.read()
    vocab = VocabularySchema().loads(contents)

# init the translator
translator = google_translator()

# start a timer
start_time = timeit.default_timer()

# start the count
translated = 0

try:
    # for every word in the vocab
    for word in tqdm(vocab.words):

        # translate both the original text and the lemma
        text_trans = translator.translate(word.text, lang_src='de', lang_tgt='en')
        lemma_trans = translator.translate(word.lemma, lang_src='de', lang_tgt='en')

        # fix capitalization
        text_trans = text_trans.lower()
        lemma_trans = lemma_trans.lower()

        # trim whitespace
        text_trans = text_trans.rstrip()
        lemma_trans = lemma_trans.rstrip()

        # set the fields
        word.text_trans = text_trans
        word.lemma_trans = lemma_trans

        # increment the count
        translated += 1

except Exception as err:
    print(f"Unexpected {err=}, {type(err)=}")

# write the vocabulary to a json file
book_name = os.path.splitext(BOOK)[0].rpartition('/')[2]
with open(f'vocab/{book_name}.json', 'w') as f:
    f.write(VocabularySchema().dumps(vocab))

# write a human-readable version of the vocabulary
with open(f'vocab/{book_name}.txt', 'w') as f:
    [f.write(word.shorthand()) for word in vocab.words]

elapsed = timeit.default_timer() - start_time
print(f'Translated: {translated} of {len(vocab.words)} ({translated/len(vocab.words):.0%})')
print(f'Time for translation: {elapsed:.1f} seconds')
