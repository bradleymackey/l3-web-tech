import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds

class RatingPredictor(object):
    """
    loads files from disk and performs ratings predictions for a given user
    """

    def __init__(self):
        print("reading database files in...")
        self.read_files()
        self.update_for_user_rating()



    def read_files(self):
        """
        reads the static, unchanging files from the movie database
        """
        self.existing_ratings_data = pd.read_csv("ml-latest-small/ratings.csv")
        self.movie_names = pd.read_csv("ml-latest-small/movies.csv")
        self.movie_links = pd.read_csv("ml-latest-small/links.csv")
        
    def update_for_user_rating(self):
        """
        calculates the latest predictions for all users, making use of the latest user ratings data from our system
        """
        self.custom_ratings_data = pd.read_csv("ml-latest-small/users.csv")
        self.combined_ratings_data = self.existing_ratings_data.append(self.custom_ratings_data, ignore_index=False, sort=True)
        # all mereged movie and rating data
        movie_data = pd.merge(self.combined_ratings_data, self.movie_names, on="movieId")
        self.movie_data = pd.merge(movie_data, self.movie_links, on="movieId")

        # calculate estimated ratings for each user!
        R_df = self.movie_data.pivot(index="userId",columns="movieId",values="rating").fillna(0)
        R = R_df.values # numpy array
        user_ratings_mean = np.mean(R,axis=1)
        R_demeaned = R - user_ratings_mean.reshape(-1,1)

        # doing the estimate to find out who is the most likley to like each movie
        U, sigma, Vt = svds(R_demeaned, k=50) # k = heuristic based on how many latent factors we want to consider
        sigma = np.diag(sigma)
        all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1,1)
        self.prediction_df = pd.DataFrame(all_user_predicted_ratings, columns=R_df.columns, index=R_df.index)

    def user_predictions(self,username):
        """
        returns top 150 movie predictions for a given user for a given model state
        returned in format [((username,movieId), estimated star rating)]
        """
        user_regex = "^" + username + "$"
        predicted_for_user = self.prediction_df.filter(axis=0, regex=user_regex).T
        predicted_for_user = predicted_for_user.unstack(level=0).sort_values(ascending=False)
        return zip(predicted_for_user.index[0:100],predicted_for_user[0:100])


pred = RatingPredictor()
pred.update_for_user_rating()
for i in pred.user_predictions("1"):
    print(i)