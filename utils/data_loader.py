import pandas as pd
from scipy.sparse import load_npz
import json
import os
import pickle
import numpy as np
from scipy.sparse import csr_matrix

def load_books(path = r'..\data\raw\Books.csv'):
    books = pd.read_csv(path,sep=';',on_bad_lines='skip',encoding = 'latin-1', low_memory=False)
    return books

def load_users(path = r'..\data\raw\Users.csv'):
    users = pd.read_csv(path,sep=';',on_bad_lines='skip',encoding='latin-1')
    return users

def load_ratings(path = r'..\data\raw\Ratings.csv'):
    ratings = pd.read_csv(path,sep=';',on_bad_lines='skip',encoding='latin-1')
    return ratings

def load_cleaned_books(path = 'data/processed/books_cleaned.csv'):
    return pd.read_csv(path)

def load_cleaned_users(path = 'data/processed/users_cleaned.csv'):
    return pd.read_csv(path)

def load_cleaned_ratings(path = 'data/processed/ratings_cleaned.csv'):
    return pd.read_csv(path)

def load_user_item_matrix(path = 'data/processed/user_item.npz'):
    return csr_matrix(np.load(path)['arr_0'])

def load_mappers(path = 'data/processed/mappers.json'):
    with open(path, 'r') as f:
        return json.load(f)

def load_trained_model(path = r'..\models\collaborative_filtering_model.pkl'):
    with open(path,'rb') as f:
        model = pickle.load(f)

    return model