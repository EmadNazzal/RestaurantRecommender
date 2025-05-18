import React, { useState } from 'react';
import Modal from 'react-modal';
import SidePanel from '../SidePanel/index'
import styles from './FilterPopup.module.css';

Modal.setAppElement('#root'); // This is important for accessibility

const FilterPopup = ({
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
}) => {
  const [modalIsOpen, setModalIsOpen] = useState(false);

  const openModal = () => {
    setModalIsOpen(true);
  };

  const closeModal = () => {
    setModalIsOpen(false);
  };

  return (
    <div style={{display:"flex", justifyContent:"center", alignItems:"center"}}>
      <button className={styles.openButton} onClick={openModal}>Open Filters</button>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        contentLabel="Filter Modal"
        className={styles.modal}
        overlayClassName={styles.overlay}
      >
        <button className={styles.closeButton} onClick={closeModal}>Close</button>
        <SidePanel
          cuisines={cuisines}
          onSortSelection={onSortSelection}
          onCuisineSelection={onCuisineSelection}
          prices={prices}
          onPriceSelection={onPriceSelection}
          zones={zones}
          onZoneSelection={onZoneSelection}
          ratings={ratings}
          onRatingSelection={onRatingSelection}
          foodRatings={foodRatings}
          onFoodRatingSelection={onFoodRatingSelection}
          aspects={aspects}
          onAspectSelection={onAspectSelection}
          onResetFilters={onResetFilters}
        />
      </Modal>
    </div>
  );
};

export default FilterPopup;
