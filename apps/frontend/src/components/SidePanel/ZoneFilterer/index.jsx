import React from 'react';
import styles from '../SidePanel.module.css'; // Import the CSS module

function ZoneFilterer({ zones, onZoneSelection }) {
  return (
    <select
      onChange={onZoneSelection}
      className={`${styles.selectBase} ${styles.zoneFilterSelect}`} // Apply the base class and specific class
    >
      <option disabled selected>
         Zone
      </option>
      {zones.map((zone) => (
        <option key={zone} value={zone}>
          {zone}
        </option>
      ))}
    </select>
  );
}

export default ZoneFilterer;
