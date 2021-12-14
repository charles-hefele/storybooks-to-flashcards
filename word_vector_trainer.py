from tqdm import tqdm
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from gensim.models import word2vec
import timeit
import nltk
from spacy.lang.de.stop_words import STOP_WORDS
from HanTa import HanoverTagger as ht
import pandas as pd
# credit https://www.kaggle.com/jeffd23/visualizing-word-vectors-with-t-sne/notebook

# BOOK = 'books/12mo/Meine Sachen.txt'
# BOOK = 'books/18mo/Gute Nacht, kleiner Löwe!.txt'
# BOOK = 'books/12mo/Mein Zoo Gucklochbuch.txt'
# BOOK = 'books/unrated/Der Kleine König - Teddy ist weg.txt'
# BOOK = 'books/novels/Kasperle auf Reisen - Chapter 1.txt'
BOOK = 'books/novels/Kasperle auf Reisen.txt'
# BOOK = 'books/novels/Vom Mars zur Erde.txt'

POS_EXCLUSIONS = ['ART', 'CARD', 'FM', 'ITJ', 'KON', 'KOUS', 'NE', 'PDAT', 'PDS', 'PIAT', 'PIS', 'PRELS', 'PTKA',
                  'PTKANT', 'PWS', 'XY']

# open and read the book
file = open(BOOK, 'rt')
corpus = file.read()

# create the tagger
tagger = ht.HanoverTagger('morphmodel_ger.pgz')

# tokenize the sentences
print('tokenizing the sentences')
sentences = nltk.sent_tokenize(corpus)

# build sentence arrays (e.g. [['dog', 'says', 'woof'], ['cat', 'says', 'meow']])
print('building sentence arrays')
sentence_arrays = []
for sentence in tqdm(sentences):
    # tokenize it
    tokenizer = nltk.RegexpTokenizer(r'[a-zA-ZäÄüÜöÖß\']+')  # can't use '\w+' here b/c it tokenizes words ending in ''s' into 's' as its own word
    tokens = tokenizer.tokenize(sentence)

    # remove stop words
    tokens = [t for t in tokens if not t.lower() in STOP_WORDS]

    # generate tags
    tags = tagger.tag_sent(tokens, taglevel=1)

    # only keep certain parts of speech
    tags = [t[0] for t in tags if t[2] not in POS_EXCLUSIONS]

    # add the new tokens to the list
    sentence_arrays.append(tags)

# generate the word vectors
print('generating word vectors')
start_time = timeit.default_timer()
model = word2vec.Word2Vec(sentence_arrays, vector_size=50, min_count=5, window=5, workers=4)
print(f'generated {len(model.wv)} word vectors')
elapsed = timeit.default_timer() - start_time
print(f'time for word vector training: {elapsed:.2f} seconds')

# save the model
model.save('output/storybook_word_vectors')

# export the model as CSV
vectors = [(v, model.wv[v]) for v in model.wv.index_to_key]
vectors_df = pd.DataFrame(vectors)
vectors_df = pd.DataFrame(vectors_df[1].to_list(), index=vectors_df[0])
vectors_df.index.name = 'word'
vectors_df.to_csv('output/storybook_word_vectors.csv', encoding='utf-8-sig')    # need the encoding to render the foreign characters correctly in Excel

# split the vectors into tokens and labels
tokens = []
labels = []
for key in model.wv.index_to_key:
    tokens.append(model.wv[key])
    labels.append(key)

# generate a t-SNE model out of the vectors
print('generating t-SNE model')
start_time = timeit.default_timer()
tsne_model = TSNE(perplexity=30, n_components=2, init='pca', n_iter=2500, random_state=23)
new_values = tsne_model.fit_transform(tokens)
elapsed = timeit.default_timer() - start_time
print(f'time for t-SNE model creation: {elapsed:.2f} seconds')

# split t-SNE result into x and y arrays for plotting
x = []
y = []
for value in new_values:
    x.append(value[0])
    y.append(value[1])

# plot the t-SNE model
print('plotting the t-SNE model')
start_time = timeit.default_timer()
plt.figure(figsize=(7, 7))
for i in tqdm(range(len(x))):
    plt.scatter(x[i],y[i])
    plt.annotate(labels[i],
                 xy=(x[i], y[i]),
                 xytext=(5, 2),
                 textcoords='offset points',
                 ha='right',
                 va='bottom')
elapsed = timeit.default_timer() - start_time
print(f'Time for plot generation: {elapsed:.2f} seconds')
plt.savefig('output/book_vocab_using_custom_vectors.png')
plt.show()

