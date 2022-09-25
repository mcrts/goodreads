import os
import json
from collections import Counter
from itertools import islice

from whoosh.fields import Schema, TEXT, STORED, ID, NUMERIC
from whoosh import index


def get_schema():
    schema = Schema(
        asin=ID(stored=True),
        isbn=ID(stored=True),
        isbn13=ID(stored=True),
        kindle_asin=ID(stored=True),
        book_id=ID(stored=True, unique=True),
        work_id=ID(stored=True),
        title=TEXT(stored=True),
        title_without_series=TEXT(stored=True),
        description=TEXT(stored=True),
        average_rating=NUMERIC(stored=True),
        ratings_count=NUMERIC(stored=True),
        text_reviews_count=NUMERIC(stored=True),
        image_url=STORED,
        goodreads_url=STORED,
    )
    return schema

def init_index(indexdir):
    os.makedirs(indexdir, exist_ok=True)
    ix = index.create_in(indexdir, schema=get_schema())
    return ix

def add_documents(indexdir, documents):
    ix = index.open_dir(indexdir)
    with ix.writer() as writer:
        for d in documents:
            if d.get("average_rating", None):
                average_rating = float(d.get("average_rating", None))
            else:
                average_rating = None

            if d.get("ratings_count", None):
                ratings_count = float(d.get("ratings_count", None))
            else:
                ratings_count = None

            if d.get("text_reviews_count", None):
                text_reviews_count = float(d.get("text_reviews_count", None))
            else:
                text_reviews_count = None

            writer.add_document(
                asin=d.get("asin", None),
                isbn=d.get("isbn", None),
                isbn13=d.get("isbn13", None),
                kindle_asin=d.get("kindle_asin", None),
                book_id=d.get("book_id", None),
                work_id=d.get("work_id", None),
                title=d.get("title", None),
                title_without_series=d.get("title_without_series", None),
                description=d.get("description", None),
                average_rating=average_rating,
                ratings_count=ratings_count,
                text_reviews_count=text_reviews_count,
                image_url=d.get("image_url", None),
                goodreads_url=d.get("link", None),
            )

def add_source_file(indexdir, src):
    with open(src, "r") as fp:
        print(f"Add {src} documents to {indexdir} index.")
        documents = (json.loads(l) for l in fp.readlines())
        add_documents(indexdir, documents)


def find_most_active_users(interactions_file):
    with open(interactions_file, "r") as fp:
        documents = (json.loads(l) for l in fp.readlines())
        documents = filter(lambda d: d.get('is_read'), documents)
        documents = (d.get('user_id') for d in documents)
        counter = Counter(documents)
    return counter

def find_reviews(indexdir, interactions_file, user):
    ix = index.open_dir(indexdir)
    with open(interactions_file, "r") as fp, ix.searcher() as searcher:
        documents = (json.loads(l) for l in fp.readlines())
        documents = filter(lambda d: d.get('is_read'), documents)
        documents = filter(lambda d: d.get('user_id') == user, documents)
        documents = ((searcher.document(book_id=d.get('book_id')).get('title'), d.get('rating')) for d in documents)
        documents = list(documents)
    return documents

