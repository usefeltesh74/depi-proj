import streamlit as st
import pandas as pd
import random
import requests
from PIL import Image
from io import BytesIO
import os
from datetime import datetime
from app_helpers import add_new_user, add_rating
from utils.data_loader import load_cleaned_users, load_cleaned_ratings

# Set page config
st.set_page_config(
    page_title="Book Rating App",
    page_icon="📚",
    layout="wide"
)

# Load the books data
@st.cache_data
def load_books():
    return pd.read_csv('data/processed/books_cleaned.csv')

# Function to get a random sample of books
def get_random_books(books_df, n=5):
    return books_df.sample(n=n)

# Function to display book with rating
def display_book(book, index):
    # Create a container for the book display
    with st.container():
        # Create two columns: left for image, right for details and rating
        col1, col2 = st.columns([1, 2], gap="large")
        with col2:
            # Book details and rating
            st.markdown(f"### {book['Book-Title']}")
            st.markdown(f"**Author:** {book['Book-Author']}")
            st.markdown(f"**Year:** {book['Year-Of-Publication']}")
            st.markdown(f"**Publisher:** {book['Publisher']}")
            st.markdown("---")
            st.markdown("#### Rate this book")
            rating = st.slider(
                "Rating (1-10)",
                min_value=1,
                max_value=10,
                value=5,
                key=f"rating_{index}"
            )
            st.markdown(f"**Your rating:** {rating}/10")
            # For height calculation
            st.markdown('<div id="book-details-bottom"></div>', unsafe_allow_html=True)
        with col1:
            # Use CSS to make the image fill the vertical space of the right column
            st.markdown("""
                <style>
                .book-image-vertical {
                    display: flex;
                    flex-direction: column;
                    justify-content: flex-start;
                    height: 350px;
                }
                .book-image-vertical img {
                    height: 100%;
                    width: auto;
                    max-width: 100%;
                    object-fit: contain;
                }
                </style>
            """, unsafe_allow_html=True)
            # Use a placeholder if image is missing or fails
            image_url = book['Image-URL-M'] if pd.notna(book['Image-URL-M']) and book['Image-URL-M'].strip() else f"https://picsum.photos/150/220?random={index}"
            st.markdown(f'<div class="book-image-vertical"><img src="{image_url}" alt="Book Cover" onerror="this.onerror=null;this.src=\'https://picsum.photos/150/220?random={index}\';"></div>', unsafe_allow_html=True)
        return rating

def authenticate_user(username, password):
    users_df = load_cleaned_users()
    user = users_df[
        (users_df['User-Name'] == username) & 
        (users_df['Password'] == password)
    ]
    if not user.empty:
        return user.iloc[0]['User-ID']
    return None

# Main app
def main():
    st.title("📚 Book Rating App")
    st.write("Sign in or register to rate books!")
    
    # Session state initialization
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    # Authentication section
    if not st.session_state.username:
        tab1, tab2 = st.tabs(["Sign In", "Register"])
        
        with tab1:
            st.subheader("Sign In")
            signin_username = st.text_input("Username:", key="signin_username")
            signin_password = st.text_input("Password:", type="password", key="signin_password")
            
            if st.button("Sign In"):
                if signin_username.strip() and signin_password.strip():
                    user_id = authenticate_user(signin_username.strip(), signin_password.strip())
                    if user_id:
                        st.session_state.username = signin_username.strip()
                        st.session_state.user_id = user_id
                        st.success(f"Welcome back, {st.session_state.username}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please enter both username and password")
        
        with tab2:
            st.subheader("Register")
            col1, col2 = st.columns(2)
            with col1:
                reg_username = st.text_input("Enter your username:", key="reg_username")
                reg_password = st.text_input("Enter your password:", type="password", key="reg_password")
            with col2:
                location = st.text_input("Enter your location:", key="reg_location")
                age = st.number_input("Enter your age:", min_value=1, max_value=120, value=25, key="reg_age")
            
            if st.button("Register"):
                if reg_username.strip() and reg_password.strip():
                    if len(reg_password) < 4:
                        st.error("Password must be at least 4 characters long")
                    elif reg_username in load_cleaned_users()["User-Name"].values:
                        st.error("Username already exists")
                    else:
                        users_df = load_cleaned_users()
                        user_id = users_df.iloc[-1,0] + 1
                        if add_new_user(reg_username.strip(), reg_password.strip(), user_id, location.strip(), age):
                            st.session_state.username = reg_username.strip()
                            st.session_state.user_id = user_id
                            st.success(f"Welcome, {st.session_state.username}! Your user ID is {user_id}")
                            
                            print("\n=== DEBUG INFO ===")
                            print("Current users in database:")
                            users_df = load_cleaned_users()
                            print(users_df)
                            print("\nUsers dataframe tail:")
                            print(users_df.tail())
                            print("\nRatings dataframe info:")
                            ratings_df = load_cleaned_ratings()
                            print("Shape:", ratings_df.shape)
                            print("Columns:", ratings_df.columns.tolist())
                            print("\nLast 4 ratings:")
                            print(ratings_df.tail().to_string())
                            print("\n==================\n")
                            
                            st.rerun()
                else:
                    st.error("Please enter both username and password")
        st.stop()

    # Display user info at the top
    st.info(f"**Logged in as:** {st.session_state.username}  |  **User ID:** {st.session_state.user_id}")
    
    # Add a sign out button
    if st.button("Sign Out"):
        st.session_state.username = ''
        st.session_state.user_id = None
        st.rerun()

    # Load books
    books_df = load_books()
    
    # Get random books
    if 'random_books' not in st.session_state:
        st.session_state.random_books = get_random_books(books_df)
    
    # Display books and collect ratings
    ratings = []
    for i, book in st.session_state.random_books.iterrows():
        st.markdown("---")
        rating = display_book(book, i)
        ratings.append({
            'ISBN': book['ISBN'],
            'Title': book['Book-Title'],
            'Image-URL': book['Image-URL-M'],
            'Rating': rating
        })
    
    # Submit button
    if st.button("Submit Ratings"):
        success = True
        for r in ratings:
            try:
                if not add_rating(st.session_state.user_id, r['ISBN'], r['Rating']):
                    st.error(f"Error saving rating for {r['Title']}")
                    success = False
            except Exception as e:
                st.error(f"Error saving rating for {r['Title']}: {str(e)}")
                success = False
        
        if success:
            st.success("Thank you for your ratings! They have been saved.")
            st.write("Your ratings:")
            for r in ratings:
                st.write(f"{r['Title']}: {r['Rating']}/10")
            
            print("\n=== DEBUG INFO ===")
            print("Current users in database:")
            users_df = load_cleaned_users()
            print(users_df)
            print("\nUsers dataframe tail:")
            print(users_df.tail())
            print("\nRatings dataframe info:")
            ratings_df = load_cleaned_ratings()
            print("Shape:", ratings_df.shape)
            print("Columns:", ratings_df.columns.tolist())
            print("\nLast 4 ratings:")
            print(ratings_df.tail().to_string())
            print("\n==================\n")
            
            # Option to get new books
            if st.button("Rate More Books"):
                st.session_state.random_books = get_random_books(books_df)
                st.rerun()

if __name__ == "__main__":
    main()
