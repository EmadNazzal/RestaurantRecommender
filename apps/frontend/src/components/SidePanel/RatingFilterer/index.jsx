import React from 'react';
import styles from '../SidePanel.module.css'; // Import the CSS module

function RatingFilterer({ ratings, onRatingSelection }) {
  return (
    <select
      onChange={onRatingSelection}
      className={`${styles.selectBase} ${styles.ratingFilterSelect}`} // Apply the base class and specific class
    >
      <option disabled selected>
        Rating
      </option>
      {ratings.map((rating) => (
        <option key={rating.label} value={rating.label}>
          {rating.label}
        </option>
      ))}
    </select>
  );
}

export default RatingFilterer;
