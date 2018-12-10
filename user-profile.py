import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds

class RatingPredictor(object):
    """
    loads files from disk and performs ratings predictions for a given user
    """

    def __init__(self):
        pass

# users.csv is where we maintain all the user profiles
users_data = pd.read_csv("ml-latest-small/users.csv")

ratings_data = pd.read_csv("ml-latest-small/ratings.csv")
ratings_data = ratings_data.append(users_data, ignore_index=False, sort=True)
print(ratings_data.tail())
movie_names = pd.read_csv("ml-latest-small/movies.csv")
movie_links = pd.read_csv("ml-latest-small/links.csv")

# all mereged movie and rating data
movie_data = pd.merge(ratings_data, movie_names, on="movieId")
movie_data = pd.merge(movie_data, movie_links, on="movieId")
print(movie_data.head())

# most loved movies
mean_ratings = movie_data.groupby('title')['rating'].mean().sort_values(ascending=False)
#print(mean_ratings.head())

# calculate estimated ratings for each user!
R_df = movie_data.pivot(index="userId",columns="movieId",values="rating").fillna(0)
print(R_df.head())
R = R_df.values # numpy array
user_ratings_mean = np.mean(R,axis=1)
R_demeaned = R - user_ratings_mean.reshape(-1,1)

# doing the estimate to find out who is the most likley to like each movie
U, sigma, Vt = svds(R_demeaned, k=50) # k = heuristic based on how many latent factors we want to consider
sigma = np.diag(sigma)
all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1,1)
preds_df = pd.DataFrame(all_user_predicted_ratings, columns=R_df.columns, index=R_df.index)

print(preds_df.filter(axis=0, regex="^crackio weener$"))

