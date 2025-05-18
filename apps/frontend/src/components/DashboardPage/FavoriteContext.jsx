// FavoriteContext.js
import React, { createContext, useState, useContext } from 'react';

const FavoriteContext = createContext();

export const FavoriteProvider = ({ children }) => {
  const [favoriteRestaurants, setFavoriteRestaurants] = useState([]);

  const addFavorite = (restaurant) => {
    setFavoriteRestaurants((prevFavorites) => {
      // Check if the restaurant is already in favorites
      if (prevFavorites.some(fav => fav.id === restaurant.id)) {
        return prevFavorites.filter(fav => fav.id !== restaurant.id); // Remove if already favorited
      }
      return [...prevFavorites, restaurant]; // Add if not favorited
    });
  };

  const removeFavorite = (id) => {
    setFavoriteRestaurants((prevFavorites) => 
      prevFavorites.filter((restaurant) => restaurant.id !== id)
    );
  };

  const isFavorite = (id) => {
    return favoriteRestaurants.some((restaurant) => restaurant.id === id);
  };

  return (
    <FavoriteContext.Provider value={{ favoriteRestaurants, addFavorite, removeFavorite, isFavorite }}>
      {children}
    </FavoriteContext.Provider>
  );
};

export const useFavorites = () => useContext(FavoriteContext);
