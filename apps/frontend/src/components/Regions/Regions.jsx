import React from "react";
import styles from "./regions.module.css";
import { useState } from "react";
import { useAllRestaurants } from "../../apiServices/useService";
import Rating from "@mui/material/Rating";
import Box from "@mui/material/Box";

export const Regions = () => {
  const { response: restaurants, error, loading } = useAllRestaurants();
  const [selectedNeighborhood, setSelectedNeighborhood] = useState("");

  const handleSelection = (e) => {
    setSelectedNeighborhood(e.target.value);
  };

  // Extract unique zones from restaurant data
  const zones = restaurants
    ? [...new Set(restaurants.map((restaurant) => restaurant.zone))]
    : [];

  return (
    <div className={styles.regionsContainer}>
      <label htmlFor="region">Choose a region:</label>
      <select
        id="region"
        name="region"
        onChange={handleSelection}
        value={selectedNeighborhood}
      >
        <option value="">Select a neighborhood</option>
        {zones.map((neighborhood, index) => (
          <option key={index} value={neighborhood}>
            {neighborhood}
          </option>
        ))}
      </select>

      <h3>
        The restaurants you selected in that neighborhood are now pinned on the
        map with details about them.
      </h3>

      {loading && <div className={styles.loading}>Loading...</div>}
      {error && <div className={styles.error}>Error: {error.message}</div>}
      {selectedNeighborhood && (
        <ul>
          {restaurants
            .filter(
              (restaurant) => restaurant.zone === selectedNeighborhood
            )
            .map((restaurant) => (
              <li key={restaurant.id}>
                <span>{restaurant.restaurant_name}</span>
                <span>{restaurant.primary_cuisine}</span>
                <Box
                  component="fieldset"
                  mb={1}
                  borderColor="transparent"
                  sx={{ display: 'flex', alignItems: 'center' }}
                >
                  <Rating
                    name="read-only"
                    value={restaurant.overall_rating}
                    readOnly
                    precision={0.5}
                    size="small"
                    sx={{ color: '#007bff' }} // Set star color
                  />
                </Box>
              </li>
            ))}
        </ul>
      )}
    </div>
  );
};
