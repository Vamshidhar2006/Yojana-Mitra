from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


embedding_function = DefaultEmbeddingFunction()


def create_embeddings(texts):
    return embedding_function(texts)