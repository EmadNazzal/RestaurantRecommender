import React from 'react';
import styles from '../SidePanel.module.css'; // Import the CSS module

function Sorter({ onSortSelection }) {
  return (
    <select
      onChange={onSortSelection}
      className={`${styles.selectBase} ${styles.sorterSelect}`} // Apply the base class and specific class
      name="selectedSort"
    >
      <option disabled selected>
        Sort by
      </option>
      <option value="alphabetical">A-Z</option>
      <option value="rating">Rating</option>
      <option value="cuisine">Cuisine</option>
      <option value="neighborhood">Neighborhood</option>
      <option value="zone">Zone</option>
    </select>
  );
}

export default Sorter;
