# dataset contains imdb id
# no login or anything, state for current user is always persisted
# starts off with list of random movies, you rate each one out of 5 stars?
# then we start to display the recommnedations to you
# 'reset profile' button at the top of the page that removes all information being held on the current user


from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint
 
app = Flask(__name__, static_url_path='/static')
 
@app.route("/")
def index():
    return "Flask App!"
 
#@app.route("/hello/<string:name>")
@app.route("/hello/<string:name>/")
def hello(name):
#    return name
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
        'template.html',**locals())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)