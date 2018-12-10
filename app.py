# dataset contains imdb id
# no login or anything, state for current user is always persisted
# starts off with list of random movies, you rate each one out of 5 stars?
# then we start to display the recommnedations to you
# 'reset profile' button at the top of the page that removes all information being held on the current user

# how to pass in a parameter `name` that we can then use as local var
# @app.route("/hello/<string:name>/")
# def func(name):
# // use name in the method

from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory
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
    title = "Movie Recommendations - Login"
    return render_template(
        'login.html',**locals())
 
@app.route("/")
def hello():
    name = "moviename that is very long indeed"
    tot_num_movies = predictor.number_movies
    username = ""
    got_username = 'user' in request.cookies
    if got_username:
        username = request.cookies['user']
        username = unquote(username)
    lang = "en"
    if 'lang' in request.cookies:
        lang = request.cookies['lang']
        lang = unquote(lang)
    print("lang is",lang)
    numrecs = 150
    remark = "a lot"
    if numrecs>100:
        if lang=="en":
            remark = "That is a lot of movies!"
        else:
            remark = "C'est beaucoup de films!"
    elif numrecs>50:
        if lang=="en":
            remark = "That is quite a few movies!"
        else:
            remark = "C'est pas mal de films!"
    elif numrecs>25:
        if lang =="en":
            remark = "That is not many movies!"
        else:
            remark = "Ce n'est pas beaucoup de films!"
    else:
        if lang=="en":
            remark = "That is disappointing!"
        else:
            remark = "C'est décevant!"
    title = "Movie Recommendations"
    quotes = [ "'If people do not believe that mathematics is simple, it is only because they do not realize how complicated life is.' -- John Louis von Neumann ",
               "'Computer science is no more about computers than astronomy is about telescopes' --  Edsger Dijkstra ",
               "'To understand recursion you must first understand recursion..' -- Unknown",
               "'You look at things that are and ask, why? I dream of things that never were and ask, why not?' -- Unknown",
               "'Mathematics is the key and door to the sciences.' -- Galileo Galilei",
               "'Not everyone will understand your journey. Thats fine. Its not their journey to make sense of. Its yours.' -- Unknown"  ]
    card_backgrounds = ["card-bg-"+col for col in ["purple","blue","pink","green","red","orange","yellow","gray","darkGray","lightBlue"]]
    randomNumber = randint(0,len(quotes)-1) 
    #quote = quotes[randomNumber] 
 
    return render_template(
        'cards.html',**locals())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)