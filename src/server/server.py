from flask import Flask, render_template, request
import random

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    args = request.args
    print(args)
    
    items = []
    data = {
        'title': "Ms. Marvel, Vol. 1: No Normal",
        'imgurl': "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1413031883l/20898019.jpg",
        'relevance': 1.0,
        'affinity': random.random(),
        'rating': random.randint(1, 5),
    }

    items.extend([data for _ in range(16)])
    return render_template("index.html", items=items)
