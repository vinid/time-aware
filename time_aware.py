from scipy.spatial.distance import cosine
import numpy as np
import itertools
import gensim

model_y = gensim.models.KeyedVectors.load_word2vec_format("model_of_years")
model_c = gensim.models.word2vec.Word2Vec.load("model_of_entites")


def compute_min_max_sim():
    """
    Compute normalization values for temporal representation of years
    :return:
    """
    vocab = [k for k in model_y.wv.vocab]
    comb = itertools.combinations(vocab, 2)
    list_of_similarities = list(map(lambda x: model_y.similarity(x[0], x[1]), comb))
    return max(list(list_of_similarities)), min(list(list_of_similarities))

def most_representative_year(entity, topn=1):
    """
    Get most representative year for an entity
    :param entity:
    :param topn:
    :return:
    """
    res = list(map(int, [k[0] for k in model_y.most_similar([model_c[entity]], topn=topn)]))
    return np.average(res)


def time_aware_flattened_similarity(entity_a, entity_b, alpha=0.5):
    """
    :param entity_a:
    :param entity_b:
    :param alpha:
    :return:
    """
    entity_array_a = model_c[entity_a]
    entity_array_b = model_c[entity_b]

    year_a = np.average(list(map(int, ([k[0] for k in model_y.most_similar(positive=[entity_array_a], topn=1)]))))
    year_b = np.average(list(map(int, ([k[0] for k in model_y.most_similar(positive=[entity_array_b], topn=1)]))))

    year_array_a = model_y[str(year_a).split(".")[0]]
    year_array_b = model_y[str(year_b).split(".")[0]]

    # return alpha* (1 - cosine(entity_array_a, entity_array_b)) + (1 - alpha)*(1/(1 - cosine(year_array_a, year_array_b)))
    a = (1 - cosine(entity_array_a, entity_array_b))
    b = (1 - (cosine(year_array_a, year_array_b)))

    maxed, mined = compute_min_max_sim()

    new_b = (b - mined) / (maxed - mined)

    return alpha * a - (1 - alpha) * (new_b), a, new_b, year_a, year_b



