import os
import random
import itertools as it
import json
from dataclasses import dataclass, field
from typing import Sequence
import pickle

from bidict import bidict
from scipy.sparse import coo_array, save_npz, load_npz


def score_document(userid, document):
    return random.random()

def rank_documents(userid, documents):
    ranked_documents = []
    for d in documents:
        d.affinity = score_document(userid, d)
        ranked_documents.append(d)
    return sorted(ranked_documents, key=lambda d: d.affinity, reverse=True)

@dataclass
class TokenIndex:
    index: bidict = field(default_factory=bidict)
    id_sequence: Sequence[int] = field(default_factory=lambda :it.count(0))

    def get_id(self, token):
        if token not in self.index:
            idx = next(self.id_sequence)
            self.index[token] = idx
        else:
            idx = self.index[token]
        return idx

    def get_token(self, idx):
        return self.index.inverse[idx]


def reviews_to_coo(reviews):
    userids = []
    bookids = []
    ratings = []
    for userid, bookid, rating in reviews:
        userids.append(userid)
        bookids.append(bookid)
        ratings.append(rating)
    
    coo = coo_array((ratings, (userids, bookids)), dtype=int)
    return coo


class Ranker:
    def __init__(self, rankdir):
        self.rankdir = rankdir
        self.matrixpath = self.rankdir / "interactions.npz"
        self.userindexpath = self.rankdir / "userindex.pkl"
        self.bookindexpath = self.rankdir / "bookindex.pkl"
        self.user_index = TokenIndex()
        self.book_index = TokenIndex()
        self.csr_matrix = None
        self.initialize()
    
    def initialize(self):
        os.makedirs(self.rankdir, exist_ok=True)
        if self.matrixpath.exists():
            self.csr_matrix = load_npz(self.matrixpath.as_posix())
            with open(self.userindexpath, 'rb') as fp:
                self.user_index = pickle.load(fp)
            with open(self.bookindexpath, 'rb') as fp:
                self.book_index = pickle.load(fp)
        else:
            self.csr_matrix = coo_array((0, 0), dtype=int)
            save_npz(self.matrixpath.as_posix(), self.csr_matrix)
            with open(self.userindexpath, 'wb') as fp:
                pickle.dump(self.user_index, fp)
            with open(self.bookindexpath, 'wb') as fp:
                pickle.dump(self.book_index, fp)
    
    def get_userid(self, user):
        return self.user_index.get_id(user)
    
    def get_user(self, userid):
        return self.user_index.get_token(userid)

    def get_bookid(self, book):
        return self.book_index.get_id(book)
    
    def get_book(self, bookid):
        return self.book_index.get_token(bookid)
    
    def add_reviews(self, src):
        with open(src, "r") as fp:
            documents = (json.loads(l) for l in fp.readlines())
            documents = filter(lambda d: d.get('is_read'), documents)
            reviews = ((self.get_userid(d.get('user_id')), self.get_bookid(d.get('book_id')), int(d.get('rating'))) for d in documents)
            coo = reviews_to_coo(reviews)
        fname = self.matrixpath.as_posix()
        save_npz(fname, coo)
        with open(self.userindexpath, 'wb') as fp:
            pickle.dump(self.user_index, fp)
        with open(self.bookindexpath, 'wb') as fp:
            pickle.dump(self.book_index, fp)
