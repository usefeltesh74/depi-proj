import csv
import pandas as pd
from utils.data_loader import load_cleaned_users, load_cleaned_ratings

def get_users_df():
    return load_cleaned_users()

def get_ratings_df():
    return load_cleaned_ratings()

users_df = get_users_df()
ratings_df = get_ratings_df()

def add_new_user(user_name, password, user_id, loc="Unknown", Age=None, path='data/processed/users_cleaned.csv'):
    """Adding a new user to user's dataset"""
    users_df = load_cleaned_users()
    
    if (user_name in users_df["User-Name"].values) or (user_id in users_df.values):
        print("User already exists")
        return False

    if len(password) < 4:
        print("Password must be at least 4 characters")
        return False

    new_user_row = [user_id, user_name, loc, Age, password]
    with open(path, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(new_user_row)
        print("User added successfully")
    return True

def add_rating(user_id: int, isbn: str, rating: int, path='data/processed/ratings_cleaned.csv'):
    """Appending a new rating row to ratings_cleaned.csv"""
    ratings_df = load_cleaned_ratings()
    user_isbns_df = ratings_df.groupby("User-ID")["ISBN"].unique()

    if (user_id in user_isbns_df) and (isbn in user_isbns_df.loc[user_id]):
        print("User already rated that book")
        return False

    with open(path, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([int(user_id), str(isbn), float(rating)])
        print("Rating added successfully")
    return True

if __name__ == "__main__":
    pass