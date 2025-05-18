import React from 'react';
import styles from '../SidePanel.module.css'; // Import the CSS module

function CuisineFilterer({ cuisines, onCuisineSelection }) {
  return (
    <select
      onChange={onCuisineSelection}
      className={styles.selectBase} // Apply the base class
    >
      <option disabled selected>
        Cuisine
      </option>
      {cuisines.map((cuisine) => (
        <option key={cuisine} value={cuisine}>
          {cuisine}
        </option>
      ))}
    </select>
  );
}

export default CuisineFilterer;
