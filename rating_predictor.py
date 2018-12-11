# bradley mackey
# web technology assignment 2018/19

import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
import time
import random

class RatingPredictor(object):
    """
    loads files from disk and performs ratings predictions for a given user
    """

    def __init__(self):
        # print("reading database files in...")
        self.__read_files()
        self.__update_model()

    def __read_files(self):
        """
        reads the static, unchanging files from the movie database
        """
        self.existing_ratings_data = pd.read_csv("ml-latest-small/ratings.csv")
        self.movie_names = pd.read_csv("ml-latest-small/movies.csv")
        self.number_movies = self.movie_names.shape[0]
        self.movie_links = pd.read_csv("ml-latest-small/links.csv")
        self.custom_ratings_data = pd.read_csv("users.csv")
        self.combined_ratings_data = self.existing_ratings_data.append(self.custom_ratings_data, ignore_index=False)
        
    def __update_model(self):
        """
        calculates the latest predictions for all users, making use of the latest user ratings data from our system
        """
        # update the whole movie data table before we can calculate
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

    def user_rate(self,username,movie,stars):
        """
        user has rated a movie, model should be updated
        """
        t = time.gmtime()
        timestamp = int(time.mktime(t))
        new = pd.DataFrame([[username,movie,stars,timestamp]], columns=["userId","movieId","rating","timestamp"])
        new['timestamp'] = new['timestamp'].apply(int)
        new['movieId'] = new['movieId'].apply(int)
        new['rating'] = new['rating'].apply(float)
        # print("TYPES")
        # print(self.custom_ratings_data.dtypes)
        # print("MERGING TYPES")
        # print(new.dtypes)
        new_values = new.values
        # print("THE NEW VALUES:")
        # print(new_values)
        new_userId = new_values[0][0]
        new_movieId = new_values[0][1]
        self.custom_ratings_data = self.custom_ratings_data[(self.custom_ratings_data.userId != new_userId) | (self.custom_ratings_data.movieId != new_movieId)]
        self.combined_ratings_data = self.combined_ratings_data[(self.combined_ratings_data.userId != new_userId) | (self.combined_ratings_data.movieId != new_movieId)]
        self.custom_ratings_data = self.custom_ratings_data.append(new)
        self.combined_ratings_data = self.combined_ratings_data.append(new)
        # print(self.custom_ratings_data.head())
        self.custom_ratings_data.to_csv("users.csv", index=False)

        # now we have added a new entry to the dataset, we need to recompute all of the ratings!
        self.__update_model()

    def user_predictions(self,username,number=250):
        """
        returns top 150 movie predictions for a given user for a given model state
        returned in format [(userId, movieId, rating, title, [genres])]
        """
        user_regex = "^" + username + "$"
        predicted_for_user = self.prediction_df.filter(axis=0, regex=user_regex).T
        # if there are no current ratings for this user, show them a random user (1-10's stuff, so we can get an idea of what they like)
        pd.set_option('display.max_columns', None) 
        if predicted_for_user.empty:
            user_to_use = str(random.randint(1,10))
            print("user has no ratings currently. showing user",user_to_use,"preferences instead")
            predicted_for_user = self.prediction_df.filter(axis=0, regex="^"+user_to_use+"$").T
        predicted_for_user = predicted_for_user.unstack(level=0).sort_values(ascending=False).reset_index()
        # predicted_for_user = (predicted_for_user - min_value) / (max_value - min_value)
        predicted_for_user = pd.merge(predicted_for_user, self.movie_names, on="movieId")
         
        # print(predicted_for_user.head())
        results = [tuple(row) for row in predicted_for_user.values][0:number]
        values = [tup[2] for tup in results]
        max_val = max(values)
        min_val = min(values)
        itr = 0
        for userId, movieId, rating, title, genres in results:
            # turn the results into a list of strings instead of concat list
            genre_list = genres.split("|")
            norm_rating = (rating - min_val)/(max_val-min_val)
            # print(userId,movieId,norm_rating*5,title)
            results[itr] = (userId,movieId,norm_rating*5,title,genre_list)
            itr += 1
        return results
