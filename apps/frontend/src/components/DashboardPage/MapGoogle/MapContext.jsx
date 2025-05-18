import React, { createContext, useState } from 'react';

const MapContext = createContext();

export const MapProvider = ({ children }) => {
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);

  const selectRestaurant = (restaurant) => {
    setSelectedRestaurant(restaurant);
  };

  return (
    <MapContext.Provider value={{ selectedRestaurant, selectRestaurant }}>
      {children}
    </MapContext.Provider>
  );
};

export default MapContext;
