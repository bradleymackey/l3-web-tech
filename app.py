# dataset contains imdb id
# no login or anything, state for current user is always persisted
# starts off with list of random movies, you rate each one out of 5 stars?
# then we start to display the recommnedations to you
# 'reset profile' button at the top of the page that removes all information being held on the current user

# how to pass in a parameter `name` that we can then use as local var
# @app.route("/hello/<string:name>/")
# def func(name):
# // use name in the method

from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory, jsonify
from random import randint
import os
from urllib.parse import unquote
from dataset import update_dataset
from rating_predictor import RatingPredictor

print("updating movie dataset to latest version...")
update_dataset()
print("dataset updated!")
print()
print("creating rating predictor...")
predictor = RatingPredictor()
print("predictor created!")
print()
print("starting flask app...")


def get_remark(lang,numrecs):
    """
    gets a localised remark for a given number of movies
    """
    if numrecs>100:
        if lang=="en":
            return "That is a lot of movies!"
        else:
            return "C'est beaucoup de films!"
    elif numrecs>50:
        if lang=="en":
            return "That is quite a few movies!"
        else:
            return "C'est pas mal de films!"
    elif numrecs>25:
        if lang =="en":
            return "That is not many movies!"
        else:
            return "Ce n'est pas beaucoup de films!"
    else:
        if lang=="en":
            return "That is disappointing!"
        else:
            return "C'est décevant!"

app = Flask(__name__, static_url_path='/static')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route("/login/")
def login():
    got_username = 'user' in request.cookies
    username = ""
    if got_username:
        username = request.cookies['user']
        username = unquote(username)
    lang = "en"
    if 'lang' in request.cookies:
        lang = request.cookies['lang']
        lang = unquote(lang)
    return render_template(
        'login.html',**locals())
 
@app.route("/")
def hello():
    name = "moviename that is very long indeed"
    tot_num_movies = predictor.number_movies
    username = ""
    predictions = []
    got_username = 'user' in request.cookies
    if got_username:
        print("GOT COOKIE")
        # get user predictions from the model
        username = unquote(request.cookies['user'])
        predictions = predictor.user_predictions(username,number=250)
    else:
        print("NO COOKIE!")
        # if there is no user logged in, just show the recommendations for a random person
        predictions = predictor.user_predictions("khsfkjhsfkdh",number=250)
    # are these ratings relevant to this user?
    # if not, we have no ratings for them, so we can't show relevant ratings yet
    # we should not show the 'match' thing in the UI
    this_user_ratings = len(predictions)>0
    if len(predictions)>0:
        ratings_for_user = predictions[0][0] # look at userId of the first prediction
        print("ratings for user",ratings_for_user)
        print("username",username)
        if ratings_for_user!=username:
            print("NO MATCH!")
            this_user_ratings = False
    print("number of predictions for",username,":",len(predictions))
    lang = "en"
    if 'lang' in request.cookies:
        lang = request.cookies['lang']
        lang = unquote(lang)
    numrecs = 250
    remark = get_remark(lang,numrecs)

    card_backgrounds = ["card-bg-"+col for col in ["purple","blue","pink","green","red","orange","yellow","gray","darkGray","lightBlue"]]
    itr = 0
    for userId, movieId, rating, title, genres in predictions:
        background = card_backgrounds[abs(hash(title)) % len(card_backgrounds)]
        predictions[itr] = (userId,movieId,rating,title,genres,background)
        itr += 1
 
    return render_template(
        'cards.html',**locals())

@app.route('/review/<movie_id>', methods = ['POST'])
def user(movie_id):
    username = request.form['user']
    stars_to_rate = request.form['stars']
    predictor.user_rate(username,movie_id,stars_to_rate)
    good = {'status':'good'}
    return jsonify(good)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)