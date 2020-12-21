## Movie Recommendation System

### The dataset for this project was gotten from movielens

The approach were simple
1. Hihgly Rated
	Movies will be recommended based on ratings from all the users in the dataset. The data has been cleaned to remove bias for instance if a movie has only been rated by just one user and has a very high rating, such case has been removed and only movies that has been seen and rated more than 40 times are left in the data. Data Cleaning Approach

2. User Recommendation
	Movies will be recommended based on user's choice. Say a previous user liked and rated a movie before and wants a new recommendation, such user just input his/her userId and gets top 10 similar movies to previously seen movies. Movies are predicted based on genres and ratings.

3. Movie Based Recommendation
	Here, movies are recommended using a low rank matrix multiplication. The user input an id of movie he/she has previously seen and wants another movie similar to that. The steps include::
	
		a. Get features for movie
		b. Subtract current movie features from every other movie features and take absolute value
		c. Sum all features to get a 'total difference score' for each movie
		d. Create a new column with difference score for each movie
		e. Sort movies from least different to most different and show results
