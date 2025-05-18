import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import DashboardNav from './DashboardNav/DashboardNav';
import DrawerSidePanel from './DrawerSidePanel/DrawerSidePanel';
import MapWithRestaurants from './MapGoogle/MapWithRestaurants';
import styles from './dashboard.module.css';
import MainPanel from '../MainPanel';
import { FavoriteProvider } from './FavoriteContext';
import { MapProvider } from './MapGoogle/MapContext';
import FilterPopup from '../FilterPopUp/FilterPopup';
import Tour from 'reactour';
import { Button, Tooltip, IconButton } from '@mui/material';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import navStyles from './DashboardNav/dashboardNav.module.css'
import sideIcons from './DrawerSidePanel/drawerSidePanel.module.css'
import mapStyles from './MapGoogle/MapWithRestaurants.module.css'
import restaurantCardStyles from '../RestaurantCard/RestaurantCard.module.css';
import panelStyles  from '../FilterPopUp/FilterPopup.module.css'
const Dashboard = () => {
  const [originalRestaurants, setOriginalRestaurants] = useState([]);
  const [restaurants, setRestaurants] = useState([]);
  const [cuisines, setCuisines] = useState([]);
  const [prices, setPrices] = useState([]);
  const [zones, setZones] = useState([]);
  const [ratings, setRatings] = useState([]);
  const [foodRatings, setFoodRatings] = useState([]);
  const [aspects, setAspects] = useState([]);
  const [compareRestaurants, setCompareRestaurants] = useState([]);
  const [isTourOpen, setIsTourOpen] = useState(true); // State to manage tour visibility

  const ratingRanges = [
    { label: '0-1', min: 0, max: 1 },
    { label: '1-2', min: 1, max: 2 },
    { label: '2-3', min: 2, max: 3 },
    { label: '3-4', min: 3, max: 4 },
    { label: '4-5', min: 4, max: 5 },
  ];

  const [filters, setFilters] = useState({
    sort: null,
    cuisine: null,
    price: null,
    zone: null,
    ratingRange: null,
    foodRating: null,
    aspects: [],
  });

  useEffect(() => {
    axios.get('https://nibble.rest/api/all-restaurants/')
      .then((response) => {
        const data = response.data;
        setOriginalRestaurants(data);
        setRestaurants(data);
        setCuisines([...new Set(data.map(r => r.primary_cuisine))].sort());
        setPrices([...new Set(data.map(r => r.price))].sort());
        setZones([...new Set(data.map(r => r.zone))].sort());
        setRatings([...new Set(data.map(r => r.overall_rating))].sort());
        setFoodRatings([...new Set(data.map(r => r.food_rating))].sort());
        setAspects([...new Set(data.flatMap(r => r.aspects.map(a => a.aspect)))].sort());
      })
      .catch((error) => { 
        console.error('Error fetching restaurants:', error);
      });
  }, []);

  const filterRestaurants = useCallback(() => {
    let filtered = [...originalRestaurants];

    if (filters.cuisine) {
      filtered = filtered.filter(r => r.primary_cuisine === filters.cuisine);
    }

    if (filters.price) {
      filtered = filtered.filter(r => r.price === filters.price);
    }

    if (filters.zone) {
      filtered = filtered.filter(r => r.zone === filters.zone);
    }

    if (filters.ratingRange) {
      const [min, max] = filters.ratingRange.split('-').map(Number);
      filtered = filtered.filter(r => r.overall_rating > min && r.overall_rating <= max);
    }

    if (filters.foodRating) {
      filtered = filtered.filter(r => r.food_rating === filters.foodRating);
    }

    if (filters.aspects.length > 0) {
      filtered = filtered.filter(r => 
        filters.aspects.every(filterAspect => 
          r.aspects.some(rAspect => rAspect.aspect === filterAspect)
        )
      );
    }

    switch (filters.sort) {
      case 'alphabetical':
        filtered.sort((a, b) => (a.restaurant_name ?? '').localeCompare(b.restaurant_name ?? ''));
        break;
      case 'rating':
        filtered.sort((a, b) => (b.overall_rating ?? 0) - (a.overall_rating ?? 0));
        break;
      case 'cuisine':
        filtered.sort((a, b) => (a.primary_cuisine ?? '').localeCompare(b.primary_cuisine ?? ''));
        break;
      case 'zone':
        filtered.sort((a, b) => (a.zone ?? '').localeCompare(b.zone ?? ''));
        break;
      case 'price':
        filtered.sort((a, b) => (a.price ?? '').localeCompare(b.price ?? ''));
        break;
      default:
        break;
    }

    setRestaurants(filtered);
  }, [filters, originalRestaurants]);

  useEffect(() => {
    filterRestaurants();
  }, [filters, filterRestaurants]);

  const handleSortSelection = (e) => {
    setFilters((prevFilters) => ({ ...prevFilters, sort: e.target.value }));
  };

  const handleCuisineSelection = (e) => {
    setFilters((prevFilters) => ({ ...prevFilters, cuisine: e.target.value }));
  };

  const handlePriceSelection = (e) => {
    setFilters((prevFilters) => ({ ...prevFilters, price: e.target.value }));
  };

  const handleZoneSelection = (e) => {
    setFilters((prevFilters) => ({ ...prevFilters, zone: e.target.value }));
  };

  const handleRatingSelection = (e) => {
    setFilters((prevFilters) => ({ ...prevFilters, ratingRange: e.target.value }));
  };

  const handleFoodRatingSelection = (e) => {
    setFilters((prevFilters) => ({ ...prevFilters, foodRating: e.target.value }));
  };

  const handleAspectSelection = (selectedAspects) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      aspects: selectedAspects,
    }));
  };

  const handleResetFilters = () => {
    setFilters({
      sort: null,
      cuisine: null,
      price: null,
      zone: null,
      ratingRange: null,
      foodRating: null,
      aspects: [],
    });
  };

  const handleCompare = (restaurant) => {
    if (compareRestaurants.length <= 2) {
      setCompareRestaurants((prevCompareRestaurants) => [...prevCompareRestaurants, restaurant]);
    }
  };

  const handleResetComparison = () => {
    setCompareRestaurants([]);
  };

  // Define the steps for the tour
  const tourSteps = [
    {
      selector: `.${navStyles.mainContainerDashNav}`, 
      content: 'Welcome to the Dashboard! Here you can find all the restaurants in the Nibbler database.',
    },
    {
      selector: `.${mapStyles.mapDiv}`, 
      content: 'Click on the markers on the map to view more information about the restaurant. For route planning, right click on the map to set the starting and ending points.',
    },
    {
      selector: `.${restaurantCardStyles.cardContainer}`, 
      content: 'The cards display the restaurant name, cuisine, price, and overall rating. You can add restaurants to your favorites list by clicking the heart icon on the opposite side of the card.',
    },
    {
      selector: `.${sideIcons.compareIcon}`, 
      content: 'To compare two restauratns, click on them on the map and add them to be compared using the "Compare" button. Then click on the compare icon in the left panel to view the comparison.',
    },
    {
      selector: `.${sideIcons.leftSideIcons}`, 
      content: 'The icons on the left provide various ways to filter and search for restaurants.',
    },
    {
      selector: `.${panelStyles.openButton}`, 
      content: 'Click on the filter icon to open the filter panel, where you can filter restaurants based on various criteria.',
    },
    {
      selector: `.${mapStyles.viewLayer}`, 
      content: 'Visualize and view the busyness from the dropdown menu.',
    },
    {
      selector: `.${navStyles.sideNavInfo}`, 
      content: 'Manage your account and change your information in the management account section.',
    },
  ];

  return (
    <FavoriteProvider>
      <MapProvider>
        <div className={styles.first}>
          <DashboardNav />
          <DrawerSidePanel
            cuisines={cuisines}
            restaurants={restaurants}
            onSortSelection={handleSortSelection}
            onCuisineSelection={handleCuisineSelection}
            prices={prices}
            onPriceSelection={handlePriceSelection}
            zones={zones}
            onZoneSelection={handleZoneSelection}
            ratings={ratingRanges}
            onRatingSelection={handleRatingSelection}
            foodRatings={foodRatings}
            onFoodRatingSelection={handleFoodRatingSelection}
            aspects={aspects}
            onAspectSelection={handleAspectSelection}
            compareRestaurants={compareRestaurants}
            onResetComparison={handleResetComparison}
            onResetFilters={handleResetFilters} // New reset filters handler
          />
          <div className={styles.MapAndLeftDivContainer}>
            <div className={styles.leftSideDiv}>
              <div className={styles.sidePanelAndMainPanel}>
                <FilterPopup
                  cuisines={cuisines}
                  onSortSelection={handleSortSelection}
                  onCuisineSelection={handleCuisineSelection}
                  prices={prices}
                  onPriceSelection={handlePriceSelection}
                  zones={zones}
                  onZoneSelection={handleZoneSelection}
                  ratings={ratingRanges}
                  onRatingSelection={handleRatingSelection}
                  foodRatings={foodRatings}
                  onFoodRatingSelection={handleFoodRatingSelection}
                  aspects={aspects}
                  onAspectSelection={handleAspectSelection}
                  onResetFilters={handleResetFilters}
                />
                <MainPanel restaurants={restaurants} />
              </div>
            </div>
            <MapWithRestaurants
              restaurants={restaurants}
              onCompare={handleCompare}
              className={styles.mapComponent}
            />
          </div>
        </div>
        <Tour
          steps={tourSteps}
          isOpen={isTourOpen}
          onRequestClose={() => setIsTourOpen(false)}
          styles={{
            tooltip: (base) => ({
              ...base,
              borderRadius: '5px', 
            }),
            popover: (base) => ({
              ...base,
              borderRadius: '5px',
            }),
            arrow: (base) => ({
              ...base,
              borderRadius: '10px',
            }),
          }}
        />
        <Tooltip title="Quick Tour Guide">
          <IconButton
            onClick={() => setIsTourOpen(true)}
            className={styles.helpButton}
            aria-label="Quick Tour Guide"
          >
            <HelpOutlineIcon />
          </IconButton>
        </Tooltip>
      </MapProvider>
    </FavoriteProvider>
  );
};

export default Dashboard;
