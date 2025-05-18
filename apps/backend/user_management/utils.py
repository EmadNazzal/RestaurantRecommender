"""This file contains utility functions for the user management app."""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore

from .models import Preference, UserLikedRestaurant, UserPreference  # type: ignore


def get_all_preferences():
    """Return a list of all preference IDs that are selectable."""
    # Return a list of all preference IDs that are selectable.
    return list(Preference.objects.filter(is_selectable=True).values_list("id", flat=True))


def user_preferences_to_vector(user, all_preferences):
    """Return a vector of 1s and 0s representing the user's preferences.

    0 means the user does not have the specified preference, and 1 means the user has the specified preference.

    Args:
        user (User): The user whose preferences to convert to a vector.
        all_preferences (list): A list of all preference IDs.

    Returns:
        list: A list of 1s and 0s representing the user's preferences.
    """
    # Get the preference IDs of the user's preferences.
    user_preferences = set(UserPreference.objects.filter(
        user=user).values_list("preference_id", flat=True))
    # Return a list of 1s and 0s representing the user's preferences.
    return [1 if pref_id in user_preferences else 0 for pref_id in all_preferences]


def calculate_cosine_similarity(vector1, vector2):
    """Calculate the cosine similarity between two vectors."""
    # Convert the vectors to numpy arrays and reshape them.
    # The arrays are reshaped to have 1 row and as many columns as needed.
    # This is because cosine_similarity expects the vectors to be in the form of a matrix.
    # This allows the vectors to be compared element-wise.
    # Vector1 is the user's preferences vector, and vector2 is the similar user's preferences vector.
    vector1 = np.array(vector1).reshape(1, -1)
    vector2 = np.array(vector2).reshape(1, -1)

    # Calculate the cosine similarity between the two vectors and return the result.
    return cosine_similarity(vector1, vector2)[0][0]


def get_liked_restaurants_matrix(similar_users, all_restaurants):
    """Return a matrix of liked restaurants for similar users.

    The matrix is weighted by similarity, where the similarity score is the cosine similarity
    between the user's preferences and the similar user's preferences.

    Args:
        similar_users (list): A list of similar users.
        all_restaurants (list): A list of all restaurant IDs.

    Returns:
        numpy.ndarray: A matrix of liked restaurants for similar
        users weighted by similarity.
    """
    # Get the number of similar users and restaurants.
    user_count = len(similar_users)
    restaurant_count = len(all_restaurants)
    # Create a matrix to store the liked restaurants for similar users.
    liked_matrix = np.zeros((user_count, restaurant_count), dtype=float)

    # For each index and user in the similar users list:
    for i, user in enumerate(similar_users):
        # Get the user's similarity score.
        similarity_score = user["similarity"]
        # Get the user's liked restaurants.
        liked_restaurants = UserLikedRestaurant.objects.filter(
            user__email=user["email"])

        # For each liked restaurant in the user's liked restaurants:
        for liked_restaurant in liked_restaurants:
            # Get the index of the restaurant in the list of all restaurants.
            restaurant_id = liked_restaurant.restaurant.id
            # Weight the similarity score by the similarity.
            restaurant_index = all_restaurants.index(restaurant_id)
            # Store the similarity score in the liked matrix.
            # This is weighted by similarity.
            liked_matrix[i, restaurant_index] = similarity_score

    return liked_matrix
