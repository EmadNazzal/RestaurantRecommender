import React from 'react';
import styles from '../SidePanel.module.css'; // Import the CSS module

function PriceFilterer({ prices, onPriceSelection }) {
  return (
    <select
      onChange={onPriceSelection}
      className={styles.selectBase} // Apply the base class
    >
      <option disabled selected>
        Price
      </option>
      {prices.map((price) => (
        <option key={price} value={price}>
          {price}
        </option>
      ))}
    </select>
  );
}

export default PriceFilterer;
