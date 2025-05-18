import React from 'react';
import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  Chip,
  Rating,
  Button,
  IconButton,
} from '@mui/material';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import LanguageIcon from '@mui/icons-material/Language';
import staticCard from '../../assets/images/stock-restaurant.jpg';
import styles from './RestaurantCard.module.css';
import { useFavorites } from '../DashboardPage/FavoriteContext'; // Adjust import path

function RestaurantCard({ restaurant, onShowOnMap }) {
  const { addFavorite, isFavorite } = useFavorites(); // Get the functions from context

  const positiveAspects = restaurant.aspects
    ? restaurant.aspects.filter((aspect) => aspect.rating_type === 'positive').slice(0, 3)
    : [];
  const negativeAspects = restaurant.aspects
    ? restaurant.aspects.filter((aspect) => aspect.rating_type === 'negative').slice(0, 3)
    : [];

  const handleFavoriteClick = () => {
    addFavorite(restaurant); // Add or remove favorite
  };

  return (
    <div className={styles.cardContainer}>
      <div className={styles.card}>
        <div className={styles.cardFront}>
          <div className={styles.cardMediaContainer}>
            <CardMedia
              component="img"
              image={restaurant.photo_url ? restaurant.photo_url[0] : staticCard}
              alt="Restaurant"
              className={styles.cardImage}
            />
          </div>
          <CardContent className={styles.cardContent}>
            <Typography variant="h6" component="div" className={styles.cardTitle}>
              {restaurant.restaurant_name}
              <Chip
                label="NEW"
                sx={{
                  backgroundColor: '#31bff0',
                  color: 'white',
                  '& .MuiChip-label': {
                    fontWeight: 'bold',
                  },
                }}
              />
            </Typography>
            <div className={styles.cardActions}>
              <Chip label={restaurant.price} className={styles.badgeOutline} />
              <Chip label={restaurant.primary_cuisine} className={styles.badgeOutline} />
              <Chip label={restaurant.zone} className={styles.badgeOutline} />
              <Rating
                name="read-only size-medium"
                value={restaurant.overall_rating}
                precision={0.1}
                readOnly
                className={styles.rating}
              />
            </div>
          </CardContent>
        </div>
        <div className={styles.cardBack}>
          <CardContent className={styles.cardContentBack}>
            <div className={styles.aspectList}>
              <Typography variant="body2" component="div">
                Positive Aspects:
              </Typography>
              <div className={styles.aspectChips}>
                {positiveAspects.map((aspect) => (
                  <Chip
                    key={aspect.id}
                    label={aspect.aspect}
                    color="success"
                    className={styles.aspectChip}
                  />
                ))}
              </div>
            </div>
            <div className={styles.aspectList}>
              <Typography variant="body2" component="div">
                Negative Aspects:
              </Typography>
              <div className={styles.aspectChips}>
                {negativeAspects.map((aspect) => (
                  <Chip
                    key={aspect.id}
                    label={aspect.aspect}
                    color="error"
                    className={styles.aspectChip}
                  />
                ))}
              </div>
            </div>
            <div className={styles.cardActionsBack}>
              <Button
                variant="contained"
                color="primary"
                onClick={() => onShowOnMap(restaurant)}
                className={styles.mapButton}
              >
                Show
              </Button>
              <IconButton
                aria-label="website"
                href={restaurant.website}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.websiteButton}
              >
                <LanguageIcon />
              </IconButton>
              <IconButton
                aria-label="add to favorites"
                className={styles.favoriteButton}
                onClick={handleFavoriteClick} // Handle click event
                style={{ color: isFavorite(restaurant.id) ? 'red' : 'inherit' }} // Conditionally style the icon
              >
                {isFavorite(restaurant.id) ? <FavoriteIcon /> : <FavoriteBorderIcon />} {/* Switch icons */}
              </IconButton>
            </div>
          </CardContent>
        </div>
      </div>
    </div>
  );
}

export default RestaurantCard;
