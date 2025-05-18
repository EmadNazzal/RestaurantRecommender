import React, { useState, useEffect } from 'react';
import { TextField, Autocomplete, CircularProgress } from '@mui/material';
import logoimg from '../../../assets/images/cutlery1.png';
import appStyles from '../../../App.module.css';
import AvatarMenu from './AvatarMenu/AvatarMenu'; // Import the AvatarMenu component
import styles from './dashboardNav.module.css';
import avatarImg from '../../../assets/images/UCD_Dublin.png';
import { useAllRestaurants } from '../../../apiServices/useService'; // Adjust import path accordingly
import ReactOpenWeather from '../../ReactWeather/ReactOpenWeather';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../DashboardPage/AuthContext'; 
const defaultCenter = { lat: 40.7831, lng: -73.9712 };

const DashboardNav = ({ onRestaurantSelect }) => {
  const { response: restaurants, error, loading } = useAllRestaurants();
  const [searchValue, setSearchValue] = useState('');
  const [options, setOptions] = useState([]);
  const navigate = useNavigate(); // Initialize useNavigate
  const { user } = useAuth(); // Use authentication context


  useEffect(() => {
    if (restaurants) {
      const updatedOptions = restaurants.map(restaurant => ({
        id: restaurant.id,
        label: `${restaurant.restaurant_name} (${restaurant.price}, ${restaurant.zone})`,
        rating: restaurant.overall_rating,
        location: { lat: restaurant.latitude, lng: restaurant.longitude },
      }));
      setOptions(updatedOptions);
    }
  }, [restaurants]);

  const handleChange = (event, value) => {
    if (value && value.id) {
      // Notify parent component about selected restaurant
      onRestaurantSelect(value.location);
    }
    setSearchValue(value ? value.label : '');
  };

  const handleLogoClick = () => {
    navigate('/'); // Navigate to home page
  };

  return (
    <div className={`${styles.mainContainerDashNav} ${appStyles.mainContainer}`}>
      <div className={styles.logoContainer}>
        <img src={logoimg} alt="Logo Image" style={{ width: "80px", cursor:"pointer" }}  onClick={handleLogoClick}/>
        <p className={styles.dashboardText}>Nibbler Navigator</p>
      </div>
      <Autocomplete
        freeSolo
        options={options}
        getOptionLabel={(option) => option.label}
        onChange={handleChange}
        renderOption={(props, option) => (
          <li {...props} key={option.id}>{option.label}</li>
        )}
        renderInput={(params) => (
          <TextField
            {...params}
            label="Search"
            variant="outlined"
            InputProps={{
              ...params.InputProps,
              endAdornment: (
                <>
                  {loading ? <CircularProgress color="inherit" size={20} /> : null}
                </>
              ),
              style: {
                width: '400px', // Set fixed width
              },
            }}
          />
        )}
      />
      <div className={styles.sideNavInfo}>
        <ReactOpenWeather lat={defaultCenter.lat} lng={defaultCenter.lng} />
        <AvatarMenu avatarImg={user ? user.profilePicture : avatarImg} username={user ? user.username : 'Guest'} />
        <div className={styles.userDetails}>

          <p className={styles.emad}>{user ? user.firt_name : 'Guest'}</p>

          <p className={styles.user}>{user ? 'User' : ''}</p>

        </div>
      </div>
    </div>
  );
};

export default DashboardNav;
