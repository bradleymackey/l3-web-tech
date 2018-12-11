# bradley mackey
# web technology assignment 2018/19

"""
manages the updating of the dataset
"""

DATASET_LOCATION = "http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"

import requests
import zipfile
import io
import time

def update_dataset():
    """
    updates the dataset files
    """
    r = requests.get(DATASET_LOCATION, stream=True)
    if r.ok:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        print("dataset updated at: {:.1f}".format(time.time()))
    else:
        print("[NETWORK ERROR] - could not update dataset")

