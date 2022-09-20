from flask import Flask, render_template, request

from .search import search_document, Document
from .ranker import rank_documents

PAGELEN = 16
app = Flask(__name__)


MOCKDOCUMENT = Document('No Results', 'https://t4.ftcdn.net/jpg/04/73/25/49/360_F_473254957_bxG9yf4ly7OBO5I0O5KABlN930GwaMQz.jpg', 0, 0, 0)

@app.route("/", methods=["GET"])
def index():
    args = request.args
    print(args)

    indexdir = app.config["INDEXDIR"]
    userid = args.get("userid", default=0, type=int)
    querystring = args.get("q", default="captain america", type=str)

    search_results = search_document(indexdir, querystring, PAGELEN)
    ranked_results = rank_documents(userid, search_results)
    if len(ranked_results) < PAGELEN:
        ranked_results.extend([MOCKDOCUMENT for _ in range(PAGELEN - len(ranked_results))])

    return render_template("index.html", items=ranked_results)
