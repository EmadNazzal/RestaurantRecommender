import { useState, useEffect } from "react";
import { Modal, Box, Typography, TextField, Button, MenuItem, Select, FormControl, InputLabel, Checkbox, ListItemText, OutlinedInput } from "@mui/material";
import PropTypes from "prop-types";
import styles from "./ModalPopUp.module.css";
import { useLogin, useRegister, useResetPassword } from "../../apiServices/useService";
import { useNavigate } from "react-router-dom";
import { useAllRestaurants } from "../../apiServices/useService"; // Adjust the import path as needed

const ModalPopUp = ({ open, handleClose }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [surname, setSurname] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [isForgotPassword, setIsForgotPassword] = useState(false);
  const [selectedPrice, setSelectedPrice] = useState([]);
  const [selectedCuisine, setSelectedCuisine] = useState([]);

  const [loginData, setLoginData] = useState(null);
  const [registerData, setRegisterData] = useState(null);
  const [resetPasswordData, setResetPasswordData] = useState(null);

  const navigate = useNavigate();
  const { response: loginResponse, error: loginError, loading: loginLoading } = useLogin(loginData);
  const { response: registerResponse, error: registerError, loading: registerLoading } = useRegister(registerData);
  const { response: resetPasswordResponse, error: resetPasswordError, loading: resetPasswordLoading } = useResetPassword(resetPasswordData);

  const { response: restaurantsResponse, loading: restaurantsLoading, error: restaurantsError } = useAllRestaurants();

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (isForgotPassword) {
      setResetPasswordData({ email });
    } else if (isLogin) {
      setLoginData({ email, password });
    } else {
      if (password !== passwordConfirm) {
        alert("Passwords do not match.");
        return;
      }
      const preferences = [...selectedPrice, ...selectedCuisine];
      setRegisterData({ email, first_name: firstName, surname, password, password_confirm: passwordConfirm, preferences });
    }
  };

  const toggleForm = () => {
    setIsLogin(!isLogin);
    setIsForgotPassword(false);
    setEmail("");
    setPassword("");
    setFirstName("");
    setSurname("");
    setPasswordConfirm("");
    setRememberMe(false);
    setSelectedPrice([]);
    setSelectedCuisine([]);
  };

  const toggleForgotPassword = () => {
    setIsForgotPassword(true);
    setIsLogin(false);
    setEmail("");
    setPassword("");
    setFirstName("");
    setSurname("");
    setPasswordConfirm("");
    setRememberMe(false);
    setSelectedPrice([]);
    setSelectedCuisine([]);
  };

  const backToLogin = () => {
    setIsForgotPassword(false);
    setIsLogin(true);
    setEmail("");
    setPassword("");
    setFirstName("");
    setSurname("");
    setPasswordConfirm("");
    setRememberMe(false);
    setSelectedPrice([]);
    setSelectedCuisine([]);
  };

  useEffect(() => {
    if (loginResponse) {
      const { access, refresh } = loginResponse;
      if (rememberMe) {
        localStorage.setItem("access_token", access);
        localStorage.setItem("refresh_token", refresh);
      } else {
        sessionStorage.setItem("access_token", access);
        sessionStorage.setItem("refresh_token", refresh);
      }
      navigate("/dashboard");
      handleClose();
    }
    if (registerResponse) {
      setIsLogin(true); // Switch to login form after successful sign-up
    }
    if (resetPasswordResponse) {
      alert("Password reset email sent. Please check your email.");
      setIsLogin(true);
      setIsForgotPassword(false);
    }
  }, [loginResponse, registerResponse, resetPasswordResponse, rememberMe, handleClose, navigate]);

  const priceOptions = restaurantsResponse ? [...new Set(restaurantsResponse.map(restaurant => restaurant.price))] : [];
  const cuisineOptions = restaurantsResponse ? [...new Set(restaurantsResponse.map(restaurant => restaurant.primary_cuisine))] : [];

  return (
    <Modal open={open} onClose={handleClose}>
      <Box className={styles.modalBox}>
        <div className={styles.circle1}></div>
        <div className={styles.circle2}></div>
        <div className={styles.box3}></div>
        <div className={styles.textHolder}>
          <h2 className={styles.welcomeNibbler}>Welcome, Nibbler !</h2>
          <p className={styles.yourFoodAdvisor}>
            Your Best Food Advisor,
            <br />
            Find your meal at your own convenience
          </p>
        </div>
        <div className={styles.loginFields}>
          <h3 className={styles.loginText}>
            {isForgotPassword ? "Reset Password" : isLogin ? "Login" : "Sign Up"}
          </h3>
          {(loginError || registerError || resetPasswordError) && (
            <Typography color="error">
              {loginError?.message || registerError?.message || resetPasswordError?.message || "Something went wrong."}
            </Typography>
          )}
          <form onSubmit={handleSubmit}>
            <TextField
              label="Email"
              variant="outlined"
              fullWidth
              margin="normal"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            {!isLogin && !isForgotPassword && (
              <>
                <TextField
                  label="First Name"
                  variant="outlined"
                  fullWidth
                  margin="normal"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                />
                <TextField
                  label="Surname"
                  variant="outlined"
                  fullWidth
                  margin="normal"
                  value={surname}
                  onChange={(e) => setSurname(e.target.value)}
                />
                <TextField
                  label="Confirm Password"
                  type="password"
                  variant="outlined"
                  fullWidth
                  margin="normal"
                  value={passwordConfirm}
                  onChange={(e) => setPasswordConfirm(e.target.value)}
                />
              </>
            )}
            {!isForgotPassword && (
              <TextField
                label="Password"
                type="password"
                variant="outlined"
                fullWidth
                margin="normal"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            )}
            {isLogin && (
              <div className={styles.rememberMeContainer}>
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                />
                <label className={styles.rememberMeText}>Remember Me</label>
              </div>
            )}
            {!isLogin && !isForgotPassword && (
              <>
                <FormControl fullWidth margin="normal">
                  <InputLabel>Price</InputLabel>
                  <Select
                    multiple
                    value={selectedPrice}
                    onChange={(e) => setSelectedPrice(e.target.value)}
                    input={<OutlinedInput label="Price" />}
                    renderValue={(selected) => selected.join(', ')}
                  >
                    {priceOptions.map((price) => (
                      <MenuItem key={price} value={price}>
                        <Checkbox checked={selectedPrice.indexOf(price) > -1} />
                        <ListItemText primary={price} />
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <FormControl fullWidth margin="normal">
                  <InputLabel>Cuisine</InputLabel>
                  <Select
                    multiple
                    value={selectedCuisine}
                    onChange={(e) => setSelectedCuisine(e.target.value)}
                    input={<OutlinedInput label="Cuisine" />}
                    renderValue={(selected) => selected.join(', ')}
                  >
                    {cuisineOptions.map((cuisine) => (
                      <MenuItem key={cuisine} value={cuisine}>
                        <Checkbox checked={selectedCuisine.indexOf(cuisine) > -1} />
                        <ListItemText primary={cuisine} />
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </>
            )}
            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              sx={{ marginBottom: "10px", marginTop: "8px" }}
              disabled={loginLoading || registerLoading || resetPasswordLoading}
            >
              {isForgotPassword ? "Send Reset Link" : isLogin ? "Sign In" : "Sign Up"}
            </Button>
            {isForgotPassword && (
              <Button
                variant="outlined"
                color="primary"
                size="medium"
                sx={{ margin: "10px auto"}}
                onClick={backToLogin}
              >
                Back to Sign In
              </Button>
            )}
          </form>
          {isLogin && !isForgotPassword && (
            <h5 className={styles.forgotPassword} onClick={toggleForgotPassword}>Forgot Password?</h5>
          )}
          {!isForgotPassword && (
            <button onClick={toggleForm} className={styles.signUpBtn}>
              {isLogin ? "Sign Up" : "Sign In"}
            </button>
          )}
        </div>
      </Box>
    </Modal>
  );
};

ModalPopUp.propTypes = {
  open: PropTypes.bool.isRequired,
  handleClose: PropTypes.func.isRequired,
};

export default ModalPopUp;
