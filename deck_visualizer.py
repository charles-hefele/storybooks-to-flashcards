import spacy
from word import VocabularySchema
from spacy_vec_ops import SpacyVecOps
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import timeit
# credit https://www.kaggle.com/jeffd23/visualizing-word-vectors-with-t-sne/notebook

# BOOK = 'Meine Sachen'
# BOOK = 'Mein Zoo Gucklochbuch'
# BOOK = 'Der Kleine König - Teddy ist weg'
# BOOK = 'Kasperle auf Reisen - Chapter 1'
BOOK = 'Kasperle auf Reisen'
VOCAB_INPUT = f'vocab/{BOOK}.json'

MINIMUM_WORD_COUNT = 10

# start timer
start_time = timeit.default_timer()

# read the data
with open(VOCAB_INPUT, 'r') as file:
    contents = file.read()
    vocab = VocabularySchema().loads(contents)

# load the model
nlp = spacy.load('de_core_news_lg')  # using the largest word vector set from spaCy
ops = SpacyVecOps(nlp)

# init containers
labels = []
tokens = []

# generate data for t-SNE
num_points = 0
for word in vocab.words:
    if word.count >= MINIMUM_WORD_COUNT:
        tokens.append(nlp.vocab[word.text].vector)
        labels.append(word.text)
        num_points += 1
print('total points is', num_points)

# run t-SNE
tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
new_values = tsne_model.fit_transform(tokens)

# end timer
elapsed = timeit.default_timer() - start_time
print(f'Time to run t-SNE: {elapsed:.2f} seconds')

# extract new values from t-SNE run
x = []
y = []
for value in new_values:
    x.append(value[0])
    y.append(value[1])

# plot it
plt.figure(figsize=(7, 7))
for i in range(len(x)):
    plt.scatter(x[i],y[i])
    plt.annotate(labels[i],
                 xy=(x[i], y[i]),
                 xytext=(5, 2),
                 textcoords='offset points',
                 ha='right',
                 va='bottom')
plt.savefig('output/book_vocab_using_spaCy_vectors.png')
plt.show()


