from flask import Flask, render_template, request

from .search import search_document, Document
from .ranker import Ranker

PAGELEN = 16
app = Flask(__name__)


MOCKDOCUMENT = Document('No Results', 'https://t4.ftcdn.net/jpg/04/73/25/49/360_F_473254957_bxG9yf4ly7OBO5I0O5KABlN930GwaMQz.jpg', 0, 0, 0)

@app.route("/", methods=["GET"])
def index():
    indexdir = app.config["INDEXDIR"]
    rankdir = app.config["RANKDIR"]
    args = request.args

    querystring = args.get("q", default=None, type=str)
    if querystring:
        print("there is a query :", querystring)
        search_results = search_document(indexdir, querystring, 4*PAGELEN)
    else:
        print("no query")
        search_results = search_document(indexdir, "", 4*PAGELEN)

    user = args.get("userid", default=None, type=str)
    if user:
        print("there is a user :", user)
        ranker = Ranker(rankdir)
        for d in search_results:
            d.affinity = ranker.rank_book(user, d.bookid)
        ranked_results = sorted(search_results, key=lambda d: d.affinity, reverse=True)
    else:
        print("no user")
        ranked_results = search_results

    if len(ranked_results) < PAGELEN:
        ranked_results.extend([MOCKDOCUMENT for _ in range(PAGELEN - len(ranked_results))])
    else:
        ranked_results = ranked_results[:PAGELEN]

    res = render_template("index.html", items=ranked_results, userid=user, q=querystring)
    return res
