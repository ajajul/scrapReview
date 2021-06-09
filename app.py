from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from scrap import fetchReviews
import yaml

app = Flask(__name__)
db_config = yaml.load(open('database.yaml'))
app.config['SQLALCHEMY_DATABASE_URI'] = db_config['uri'] 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

class GoodleReviews(db.Model):
    __tablename__ = "google_reviews"

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review_time = db.Column(db.String())
    reviewer_name = db.Column(db.String())
    rating = db.Column(db.Integer)
    review_text = db.Column(db.String)

    def __init__(self, review_time, reviewer_name, rating, review_text):
        self.review_time = review_time
        self.reviewer_name = reviewer_name,
        self.rating = rating,
        self.review_text = review_text

    def __repr__(self):
        return '%s/%s/%s/%s/%s' % (self.review_id, self.review_time, self.reviewer_name, self.rating, self.review_text)

@app.route('/')
def index():
    return redirect(url_for('allReviews'))


@app.route("/get-reviews")
def getReviews():
    all_reviews = fetchReviews()
    for reviews in all_reviews:
        goodle_reviews = GoodleReviews(review_time=reviews['review_time'],reviewer_name=reviews['reviewer_name'],rating=reviews['rating'],review_text=reviews['review_text'])
        db.session.add(goodle_reviews)
        db.session.commit()
    return redirect(url_for('allReviews'))


@app.route("/all-reviews")
def allReviews():
    all_reviews = GoodleReviews.query.all()
    print(" \n\n\n\n======================   : ", len(all_reviews))
    return render_template("home.html", data=all_reviews)

if __name__ == '__main__':
    app.debug = True
    app.run()
