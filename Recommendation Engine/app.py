# # Import libraries
try:
	import pandas as pd
	import streamlit as st
	import numpy as np
	import matrix_factorization
except Exception as e:
	st.write(f'Error loading dependencies {e}')

@st.cache(allow_output_mutation=True)
def load_data():
	try:
		movies_rating_df = pd.read_csv('data/user_ratings.csv')
		ratings = pd.read_csv('data/user_ratings.csv')
		movies_df = pd.read_csv('data/movies.csv')
	except Exception as e:
		st.write(f"Error reading data {e}")
	movies_rating_df = movies_rating_df[['title', 'genres', 'userId', 'movieId', 'rating']]

	# movies that was seen by just a user should be dropped
	# hence any movie with less than 40 views will be dropped
	popular_movie = movies_rating_df['movieId'].value_counts()
	movie_popularity = popular_movie[popular_movie > 40].index

	movies_rating_df = movies_rating_df[movies_rating_df['movieId'].isin(movie_popularity)]
	# movies_rating_df['seenCounts'] = movies_rating_df.groupby('title')['title'].transform('count')

	# Create Sparse Matrix (UserID x MovieNames)
	user_ratings_df = pd.pivot_table(movies_rating_df, index='userId', columns='movieId', values='rating')

	# Matrix Factorization to get U x M
	U, M = matrix_factorization.low_rank_matrix_factorization(user_ratings_df.values, num_features=11, regularization_amount=1.1)


	return movies_rating_df, movies_df, ratings, U, M, user_ratings_df


movies_rating_df, movies_df, ratings, U, M, user_ratings_df = load_data()

# Predict all user ratings
predicted_ratings = np.matmul(U,M)

## Most Highly Rated ###
def highestRated():
    st.write('Here are the 40 highest rated movies:')
    highest_ratings = pd.DataFrame(movies_rating_df.groupby('movieId')['rating'].mean())
    a = ratings.drop('rating', axis=1)
    highest_ratings = highest_ratings.join(a, on = 'movieId')
    highest_ratings = highest_ratings.sort_values('rating', ascending = False)
    st.dataframe(highest_ratings[['title', 'genres', 'rating']].head(40))


### Recommended for You ###

def userRecommendations():
    ## Prompt User to Choose user_id to search
    min_user_id = movies_rating_df.userId.min()
    max_user_id = movies_rating_df.userId.max()

    st.write('Enter a user_id between ' + str(min_user_id) + ' and ' + str(max_user_id) + ':')
    search_user_id = (st.number_input('user_id', min_value=1, max_value=610))

    ## Show previously watched movies
    if search_user_id:
	    st.write('Movies previously watched by user_id ' + str(search_user_id) + ':')
	    watched_movies = movies_rating_df[movies_rating_df['userId'] == search_user_id]
	    watched_movies = watched_movies.merge(movies_df, on = 'movieId', how='left')
	    st.write(watched_movies.title_x)

	    ## Show recommended movies
	    st.write("Here are some recommended movies based on past movie ratings:")

	    # Merging predicted user ratings with movie list
	    user_ratings = predicted_ratings[search_user_id - 1]
	    movies_df['rating'] = pd.Series(user_ratings)

	    # Removing movies that have already been watched
	    already_watched = watched_movies['movieId']
	    recommended_movies = movies_df[movies_df.index.isin(already_watched) == False]

	    # Sort recommended movies from highest to lowest rating
	    recommended_movies = recommended_movies.sort_values(by='rating', ascending = False)
	    recommended_movies['rating'] = np.clip(recommended_movies['rating'], a_min=1, a_max=5)
	    st.dataframe(recommended_movies[['movieId', 'title', 'genres', 'rating']].head(10))

### Explore and find similar favourites ###

def similarMovies(M=M):
    # Prompt user for movie id
    st.dataframe(movies_df[['movieId', 'title', 'genres']].head(10))
    st.write('Choose a movie to find similar movies to the selected movie (USE MOVIE ID #): ')
    movie_id = st.number_input('Enter a movie id', min_value=1, max_value=600)
    if movie_id:
	    movie_info = movies_df.loc[movie_id]

	    st.write("We are finding movies similar to this movie:")
	    st.write("Movie title: {}".format(movie_info.title))
	    st.write("Genre: {}".format(movie_info.genres))

	    ## Find similar movies
	    # 1) Get features for movie
	    M = np.transpose(M)
	    movie_features = M[movie_id - 1]

	    # 2) Subtract current movie features from every other movie features and take absolute value
	    difference = M - movie_features
	    absolute_difference = np.abs(difference)

	    # 3) Sum all features to get a 'total difference score' for each movie
	    total_difference = np.sum(absolute_difference, axis=1)

	    # 4) Create a new column with difference score for each movie
	    movies_df['difference_score'] = pd.Series(total_difference)

	    # 5) Sort movies from least different to most different and show results
	    sorted_movie_list = movies_df.sort_values('difference_score', ascending = True)
	    st.write('How many movies would you like the system to recommend?')
	    number  = st.number_input(label='No of Recommendation', min_value=5, max_value=40)
	    st.write('The top ' + str(number)+' most similar movies are: ')
	    st.dataframe(sorted_movie_list[['title', 'genres', 'difference_score']][0:number])

### Main ###
def main():
	st.title('Movie Recommendation Engine')
	st.subheader('Dataset is based on MovieLens Database')
	st.markdown("""<style>
						body{
							background-color:#abceac;
							color: #091021;
							font-color: #896524;
							}
					</style>""", unsafe_allow_html=True)

	options = ['See Highest Rated Movies', 'Find Recommended Movies based on User', 'Find Recommended Movies based on Movie']
	choice = st.selectbox('Menu', options)
  
	if choice == 'See Highest Rated Movies':
		highestRated()
	elif choice == 'Find Recommended Movies based on User':
		userRecommendations()
	elif choice == 'Find Recommended Movies based on Movie':
		similarMovies()


if __name__ == '__main__':
	main()