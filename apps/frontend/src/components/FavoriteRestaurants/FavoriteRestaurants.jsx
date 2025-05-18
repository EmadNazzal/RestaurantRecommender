// FavoriteRestaurants.jsx
import React from 'react';
import { Card, CardContent, CardMedia, Typography, IconButton, Rating, Grid } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import styles from './FavoriteRestaurants.module.css';
import { useFavorites } from '../DashboardPage/FavoriteContext'; // Import the useFavorites hook

const FavoriteRestaurants = () => {
  const { favoriteRestaurants, removeFavorite } = useFavorites(); // Get data and functions from context

  return (
    <div className={styles.container}>
      <Grid container spacing={2}>
        {favoriteRestaurants.map((restaurant) => (
          <Grid item xs={12} sm={6} md={4} key={restaurant.id}>
            <Card className={styles.card}>
              <CardMedia
                component="img"
                image={restaurant.photo_url[0] || 'default-image-url.jpg'}
                alt="Restaurant"
                sx={{ height: 150, width: 150 }}
              />
              <CardContent>
                <Typography variant="h6">{restaurant.restaurant_name}</Typography>
                <Rating
                  name="read-only"
                  value={restaurant.overall_rating}
                  precision={0.1}
                  readOnly
                />
                <Typography variant="body2">{restaurant.address}</Typography>
                <Typography variant="body2">{restaurant.price}</Typography>
                <Typography variant="body2">{restaurant.zone}</Typography>
                <IconButton
                  aria-label="remove from favorites"
                  onClick={() => removeFavorite(restaurant.id)} // Call removeFavorite from context
                >
                  <DeleteIcon />
                </IconButton>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </div>
  );
};

export default FavoriteRestaurants;
