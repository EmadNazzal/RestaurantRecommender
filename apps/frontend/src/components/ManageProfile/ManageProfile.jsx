import { useState, useEffect } from "react";
import {
  TextField,
  Button,
  Avatar,
  MenuItem,
  Checkbox,
  ListItemText,
  Select,
  FormControl,
  InputLabel,
  Box,
  Typography,
  Grid,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import styles from "./ManageProfile.module.css";
import { useAllRestaurants } from "../../apiServices/useService";
import { useAuth } from "../DashboardPage/AuthContext";
import stopSign from '../../assets/images/stop.jpg'

const ManageProfile = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const [userData, setUserData] = useState({
    first_name: "",
    surname: "",
    email: "",
    avatar: "",
  });

  const [selectedPreferences, setSelectedPreferences] = useState([]);
  const [selectedAdditionalPreferences, setSelectedAdditionalPreferences] = useState([]);

  const { response: restaurants, loading, error } = useAllRestaurants();

  useEffect(() => {
    if (!user) {
      // If the user is not authenticated, don't fetch user data
      return;
    }

    // Fetch user data if authenticated
    axios.get("https://nibble.rest/api/profiles/").then((response) => {
      setUserData(response.data);
    });
  }, [user]);

  const handleSignInClick = () => {
    navigate("/");
  };

  if (!user) {
    return (
      <div className={styles.restrictedContainer}>
        <img src={stopSign} alt="Not Allowed" style={{width:"250px", height:"250px", padding:"15px"}}/>
        <Typography variant="h4" component="h1" className={styles.restrictedTitle}>
          Access Restricted
        </Typography>
        <Typography variant="body1" className={styles.restrictedMessage}>
          You must be signed in to view this page. Please sign in to access the Manage Profile page.
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={handleSignInClick}
          sx={{ backgroundColor: "#3ba9ee", marginTop: "20px" }}
        >
          Sign In
        </Button>
      </div>
    );
  }

  const handleInputChange = (e) => {
    setUserData({ ...userData, [e.target.name]: e.target.value });
  };

  const handleAvatarChange = (e) => {
    setUserData({ ...userData, avatar: e.target.files[0] });
  };

  const handlePreferencesChange = (e) => {
    setSelectedPreferences(e.target.value);
  };

  const handleAdditionalPreferencesChange = (e) => {
    setSelectedAdditionalPreferences(e.target.value);
  };

  const handleSaveChanges = async () => {
    const formData = new FormData();
    formData.append("first_name", userData.first_name);
    formData.append("surname", userData.surname);
    if (userData.avatar) {
      formData.append("avatar", userData.avatar);
    }

    try {
      const response = await axios.post("https://nibble.rest/api/profiles/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("User data updated:", response.data);
    } catch (error) {
      console.error("Error updating user data:", error);
    }
  };

  const handleBackToDashboard = () => {
    navigate("/dashboard");
  };

  const uniqueCuisines = restaurants ? [...new Set(restaurants.map(restaurant => restaurant.primary_cuisine))] : [];
  const uniquePrices = restaurants ? [...new Set(restaurants.map(restaurant => restaurant.price))] : [];

  return (
    <div className={styles.parentContainer}>
      <div className={styles.container}>
        <Typography variant="h4" component="h1" className={styles.title}>
          Manage Account
        </Typography>
        <Grid container spacing={4} className={styles.section}>
          <Grid item xs={12} md={4} className={styles.avatarContainer}>
            <Avatar
              src={userData.avatar ? URL.createObjectURL(userData.avatar) : userData.avatar}
              alt="User Avatar"
              sx={{ width: 120, height: 120 }}
            />
            <input type="file" onChange={handleAvatarChange} className={styles.avatarInput} />
          </Grid>
          <Grid item xs={12} md={8}>
            <TextField
              label="First Name"
              name="first_name"
              value={userData.first_name}
              onChange={handleInputChange}
              variant="outlined"
              fullWidth
              margin="normal"
            />
            <TextField
              label="Surname"
              name="surname"
              value={userData.surname}
              onChange={handleInputChange}
              variant="outlined"
              fullWidth
              margin="normal"
            />
            <TextField
              label="Email"
              name="email"
              value={userData.email}
              onChange={handleInputChange}
              variant="outlined"
              fullWidth
              margin="normal"
              disabled
            />
          </Grid>
        </Grid>
        <Box className={styles.buttonsContainer}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleSaveChanges}
            sx={{ backgroundColor: "#3ba9ee", margin: "20px 0" }}
          >
            Save Changes
          </Button>
          <Button
            variant="outlined"
            color="primary"
            onClick={handleBackToDashboard}
            sx={{ borderColor: "#498aed", color: "#498aed", margin: "20px" }}
          >
            Back to Dashboard
          </Button>
        </Box>
      </div>
    </div>
  );
};

export default ManageProfile;
