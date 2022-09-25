from whoosh import index, qparser, scoring


class Document:
    def __init__(self, bookid, title, imgurl, relevance, rating, affinity=0):
        self.bookid = bookid
        self.title = title
        self.imgurl = imgurl
        self.relevance = relevance
        self.rating = rating
        self.affinity = 0

    @classmethod
    def fromHit(cls, hit):
        data = hit.fields()
        doc = cls(
            bookid=data.get("book_id", ""),
            title=data.get("title", ""),
            imgurl=data.get("image_url", ""),
            relevance=hit.score,
            rating=data.get("average_rating", 0),
        )
        return doc

def search_document(indexdir, querystring, pagelen):
    ix = index.open_dir(indexdir)
    qp = qparser.MultifieldParser(
        ["title", "title_without_series", "description"], schema=ix.schema
    )
    q = qp.parse(querystring)
    with ix.searcher(weighting=scoring.TF_IDF()) as s:
        results = s.search_page(
            q, 1, pagelen=pagelen
        )
        docs = [Document.fromHit(h) for h in results]
    return docs