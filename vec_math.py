from numpy import dot
from numpy.linalg import norm


# add 2 vectors
def add(coord1, coord2):
    return [c1 + c2 for c1, c2 in zip(coord1, coord2)]


# subtract 2 vectors
def sub(coord1, coord2):
    return [c1 - c2 for c1, c2 in zip(coord1, coord2)]


# average vectors
def mean(vectors):
    no_of_vec = len(vectors)
    resultant = [0] * len(vectors[0])
    for v in vectors:
        resultant = add(resultant, v)
    return [x/no_of_vec for x in resultant]


# cosine similarity between vectors
def cos(v1, v2):
    if norm(v1) > 0 and norm(v2) > 0:
        return dot(v1, v2) / (norm(v1) * norm(v2))
    else:
        return 0.0
