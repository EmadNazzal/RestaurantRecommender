import React from 'react';
import styles from '../SidePanel.module.css'; // Import the CSS module

function FoodRatingFilterer({ foodRatings, onFoodRatingSelection }) {
  return (
    <select onChange={onFoodRatingSelection} className={styles.selectBase}>
      <option disabled selected>Food Rating</option>
      {foodRatings.map((rating) => (
        <option key={rating} value={rating}>{rating}</option>
      ))}
    </select>
  );
}

export default FoodRatingFilterer;
