--------- ABOUT ----------
a rating predictor for movies
allows users to login, uses rated movies to inform future predictions
done in the form of a website

---------- TO RUN ----------
`python3 app.py`

runs A FLASK WEB APP
web app will run on http://localhost:80/
please use a (reasonably) modern browser

---------- DEPENDENCIES ----------
pandas, urllib, flask, numpy, requests, scipy

---------- COMMENTS ----------
- movielens dataset is used as source (~ 9742 movies total) (~ 600 users with reviews)
- (the larger movielens dataset is ~250mb, which I deemed too large for this small-scale assignment)
- dataset is automatically updated each time before web app is run
- friendly website user interface, with large, clear tiles showing the movies. 
- HTML,CSS,JS and AJAX (to flask web app) for a dynamic experience
- language selection option on website (english & french)
- login/logout as users (CaSe SeNsItIvE), logging in again restores all previous preferences just as they were left
- personalised message tells users how many ratings they have today, the state of their account (are they logged in or not? are their any recommendations at the moment?)
- user profiling - as users rate movies, suggestions dynamically update - with each rating AJAX request updates the central rating respoitory
- SVD recommendation algorithm realised in pandas, which is normalised before showing to users (ensures there are always matches in the range 0-5 stars, which makes the most sense to users)
- user ratings stored in `users.csv`, which is merged with main ratings when starting server, file is also backed up again with each new rating into the system
