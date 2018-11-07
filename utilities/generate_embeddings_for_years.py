from collections import Counter
import os
import numpy as np
import argparse
from gensim.models import word2vec

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-embedded_model_location', '--embeded', help="Location of the embedded model you want to learn temporal embeddings from", type=str)
    parser.add_argument('-dimension_of_the_embeddings', '--dim', help="Dimensionality of the previous embedding", type=str)
    parser.add_argument('-year_embeddings', '--em', help="Output location for the embedded years", type=str)
    parser.add_argument('-year_annotated', '--an', help="Location Folder of the annotated years", type=str)

    args = parser.parse_args()

    folder = args.an
    model_e = word2vec.Word2Vec.load(args.embedded_model_location)

    with open(args.em, "w") as text_file:
        num_files = len(os.listdir(folder))
        dimensions = args.dimension_of_the_embeddings

        text_file.write(str(num_files) + " " + str(dimensions) + " " + "\n")
        for ff in os.listdir(folder):

            name = ff
            path = (os.path.join(folder, ff))
            with open(path, "r") as filino:
                coso = filino.readlines()
                entities = set(coso[0].split())
                summing = []

                for entity in entities:
                    try:
                        summing.append(model_e[entity])
                    except Exception as e:
                        continue
                concatenated_array = np.average(summing, axis=0)
                concatenated_list = concatenated_array.tolist()
                string_to_save = ' '.join(map(str, concatenated_list))
                a = text_file.write(str(name) + " " + string_to_save + "\n")