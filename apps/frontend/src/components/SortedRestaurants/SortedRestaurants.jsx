import React from 'react';
import { useLocation } from 'react-router-dom';

const SortedRestaurants = () => {
    const location = useLocation();
    const restaurants = location.state?.restaurants || [];

    return (
        <div>
            <h1>Sorted Recommended Restaurants</h1>
            <ul>
                {restaurants.length > 0 ? (
                    restaurants.map(restaurant => (
                        <li key={restaurant.id}>{restaurant.name}</li>
                    ))
                ) : (
                    <p>No restaurants found.</p>
                )}
            </ul>
        </div>
    );
};

export default SortedRestaurants;