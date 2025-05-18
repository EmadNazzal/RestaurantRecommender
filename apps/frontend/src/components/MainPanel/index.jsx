import React, { useContext, useState } from 'react';
import RestaurantCard from '../RestaurantCard';
import { Pagination } from '@mui/material';
import styles from './MainPanel.module.css';
import MapContext from '../DashboardPage/MapGoogle/MapContext';

function MainPanel({ restaurants }) {
  const [currentPage, setCurrentPage] = useState(1);
  const { selectRestaurant } = useContext(MapContext);
  const restaurantsPerPage = 20;

  const indexOfLastRestaurant = currentPage * restaurantsPerPage;
  const indexOfFirstRestaurant = indexOfLastRestaurant - restaurantsPerPage;
  const currentRestaurants = restaurants.slice(
    indexOfFirstRestaurant,
    indexOfFirstRestaurant + restaurantsPerPage
  );

  const handlePageChange = (event, value) => {
    setCurrentPage(value);
  };

  return (
    <div className={styles.mainContainer}>
      <div className={styles.container}>
        {currentRestaurants.map((restaurant) => (
          <RestaurantCard
            key={restaurant.id}
            restaurant={restaurant}
            onShowOnMap={selectRestaurant}
          />
        ))}
      </div>
      <div className={styles.pagination}>
        <Pagination
          count={Math.ceil(restaurants.length / restaurantsPerPage)}
          page={currentPage}
          onChange={handlePageChange}
          color="primary"
          variant="outlined"
          shape="rounded"
          size="small"
          sx={{
            button: {
              minWidth: '30px',
              padding: '4px 8px',
              marginBottom: '10px',
            },
          }}
        />
      </div>
    </div>
  );
}

export default MainPanel;
