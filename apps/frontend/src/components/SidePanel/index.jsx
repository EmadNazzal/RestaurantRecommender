import React from 'react';
import Sorter from "./Sorter";
import CuisineFilterer from "./CuisineFilterer";
import PriceFilterer from "./PriceFilterer";
import ZoneFilterer from "./ZoneFilterer";
import RatingFilterer from "./RatingFilterer";
import FoodRatingFilterer from "./FoodRatingFilterer/FoodRatingFilterer";
import AspectFilterer from "./AspectFilterer/AspectFilterer";
import PropTypes from "prop-types";
import styles from './SidePanel.module.css';

function SidePanel({
  cuisines,
  onSortSelection,
  onCuisineSelection,
  prices,
  onPriceSelection,
  zones,
  onZoneSelection,
  ratings,
  onRatingSelection,
  foodRatings,
  onFoodRatingSelection,
  aspects,
  onAspectSelection,
  onResetFilters,
}) {
  return (
    <div className={styles.sidePanel}>
      <Sorter onSortSelection={onSortSelection} />
      <CuisineFilterer cuisines={cuisines} onCuisineSelection={onCuisineSelection} />
      <PriceFilterer prices={prices} onPriceSelection={onPriceSelection} />
      <ZoneFilterer zones={zones} onZoneSelection={onZoneSelection} />
      <RatingFilterer ratings={ratings} onRatingSelection={onRatingSelection} />
      <FoodRatingFilterer foodRatings={foodRatings} onFoodRatingSelection={onFoodRatingSelection} />
      <AspectFilterer aspects={aspects} onAspectSelection={onAspectSelection} />
      <button className={styles.resetButton} onClick={onResetFilters}>Reset Filters</button>
    </div>
  );
}

SidePanel.propTypes = {
  cuisines: PropTypes.array.isRequired,
  onSortSelection: PropTypes.func.isRequired,
  onCuisineSelection: PropTypes.func.isRequired,
  prices: PropTypes.array.isRequired,
  onPriceSelection: PropTypes.func.isRequired,
  zones: PropTypes.array.isRequired,
  onZoneSelection: PropTypes.func.isRequired,
  ratings: PropTypes.array.isRequired,
  onRatingSelection: PropTypes.func.isRequired,
  foodRatings: PropTypes.array.isRequired,
  onFoodRatingSelection: PropTypes.func.isRequired,
  aspects: PropTypes.array.isRequired,
  onAspectSelection: PropTypes.func.isRequired,
  onResetFilters: PropTypes.func.isRequired, 
};

export default SidePanel;
