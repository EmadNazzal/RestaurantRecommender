import React, { useEffect, useState } from "react";
import { useZoneForCurrentTime } from "../../../../apiServices/useService";
import { InfoWindow } from "@vis.gl/react-google-maps";
import Slider from "react-slick";
import { Card, CardContent, Typography, Rating, IconButton, Button, Chip } from "@mui/material";
import RestaurantMenuIcon from '@mui/icons-material/RestaurantMenu';
import { Close as CloseIcon, ArrowForward as ArrowForwardIcon } from "@mui/icons-material";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import styles from "./RestaurantInfoWindow.module.css";

function RestaurantInfoWindow({ restaurant, onClose, onCompare }) {
  const [timestamp, setTimestamp] = useState(null);
  const [busynessScore, setBusynessScore] = useState(null);
  const [isAdded, setIsAdded] = useState(false);
  const { response: busynessData, loading, error } = useZoneForCurrentTime(timestamp);

  useEffect(() => {
    if (timestamp && busynessData) {
      const score = busynessData?.predictions.find(
        (prediction) => prediction.zone === restaurant.zone
      )?.predicted_value;
      setBusynessScore(score);
    }
  }, [timestamp, busynessData, restaurant.zone]);

  useEffect(() => {
    if (timestamp === null) {
      const currentTimestamp = new Date().toISOString();
      setTimestamp(currentTimestamp);
    }
  }, [timestamp]);

  const handleCompareClick = () => {
    setIsAdded(true);
    onCompare(restaurant);
  };

  const getAspectColor = (aspect) => {
    return aspect.rating_type === 'positive' ? 'green' : 'red';
  };

  const photoUrls = restaurant.photo_url;

  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true
  };

  return (
    <InfoWindow position={restaurant.location} onCloseClick={onClose}>
      <Card className={styles.card}>
        <CardContent className={styles.cardContent}>
          <IconButton edge="end" color="inherit" onClick={onClose} className={styles.closeButton}>
            <CloseIcon />
          </IconButton>
          <div className={styles.imageContainer}>
            <Slider {...settings}>
              {photoUrls.map((url, index) => (
                <div key={index} className={styles.imageSlide}>
                  <img src={url} alt={`${restaurant.restaurant_name} ${index + 1}`} className={styles.image} />
                </div>
              ))}
            </Slider>
          </div>
          <div className={styles.infoContainer}>
            <Typography variant="h6" component="h2" className={styles.title}>
              {restaurant.restaurant_name}
            </Typography>
            <Typography variant="body2" color="textSecondary" className={styles.detail}>
              {restaurant.address}
            </Typography>
            <Typography variant="body2" color="textSecondary" className={styles.detail}>
              Neighborhood: {restaurant.neighborhood}
            </Typography>
            <Typography variant="body2" color="textSecondary" className={styles.detail}>
              Zone: {restaurant.zone}
            </Typography>
            <Typography variant="body2" color="textSecondary" className={styles.detail}>
              Primary Cuisine: {restaurant.primary_cuisine}
            </Typography>
            <Typography variant="body2" color="textSecondary" className={styles.detail}>
              Price Range: {restaurant.price}
            </Typography>
            <div className={styles.ratingContainer}>
              <Typography variant="body2" color="textSecondary" className={styles.detail}>
                Overall Rating:
              </Typography>
              <Rating value={restaurant.overall_rating} precision={0.1} readOnly />
            </div>
            <div className={styles.ratingContainer}>
              <Typography variant="body2" color="textSecondary" className={styles.detail}>
                Ambience Rating:
              </Typography>
              <Rating value={restaurant.ambience_rating} precision={0.1} readOnly />
            </div>
            <div className={styles.ratingContainer}>
              <Typography variant="body2" color="textSecondary" className={styles.detail}>
                Food Rating:
              </Typography>
              <Rating value={restaurant.food_rating} precision={0.1} readOnly />
            </div>
            <div className={styles.ratingContainer}>
              <Typography variant="body2" color="textSecondary" className={styles.detail}>
                Service Rating:
              </Typography>
              <Rating value={restaurant.service_rating} precision={0.1} readOnly />
            </div>
            <div className={styles.ratingContainer}>
              <Typography variant="body2" color="textSecondary" className={styles.detail}>
                Value Rating:
              </Typography>
              <Rating value={restaurant.value_rating} precision={0.1} readOnly />
            </div>
            <div className={styles.busynessScore}>
              <Typography variant="body2" color="textSecondary">
                Busyness Score:
              </Typography>
              <Typography variant="body2" color={loading ? "textSecondary" : "error"}>
                {loading ? "Loading..." : busynessScore ? `${busynessScore.toFixed(2)} people / sqft` : "No Data"}
              </Typography>
            </div>
            <div className={styles.aspects}>
              <Typography variant="body2" color="textSecondary" className={styles.detail}>
                Aspects:
              </Typography>
              {restaurant.aspects.map((aspect) => (
                <Chip
                  key={aspect.id}
                  label={aspect.aspect}
                  color={aspect.rating_type === 'positive' ? 'success' : 'error'}
                  className={styles.aspectChip}
                />
              ))}
            </div>
          </div>
          <div className={styles.btnHolderForTwo}>
            <Button 
              variant="contained" 
              color="primary" 
              className={styles.exploreButton} 
              href={restaurant.website}
              target="_blank"
              rel="noopener"
              endIcon={<ArrowForwardIcon />}
              sx={{marginRight:"7px"}}
            >
              Explore
            </Button>
            <Button 
              variant="outlined" 
              color="primary" 
              className={styles.compareButton}
              startIcon={<RestaurantMenuIcon />}
              onClick={handleCompareClick}
              disabled={isAdded}
            >
              {isAdded ? "Added" : "Compare"}
            </Button> 
          </div>
        </CardContent>
      </Card>
    </InfoWindow>
  );
}

export default RestaurantInfoWindow;
