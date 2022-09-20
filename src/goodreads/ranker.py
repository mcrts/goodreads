
import random

def score_document(userid, document):
    return random.random()

def rank_documents(userid, documents):
    ranked_documents = []
    for d in documents:
        d.affinity = score_document(userid, d)
        ranked_documents.append(d)
    return sorted(ranked_documents, key=lambda d: d.affinity, reverse=True)
