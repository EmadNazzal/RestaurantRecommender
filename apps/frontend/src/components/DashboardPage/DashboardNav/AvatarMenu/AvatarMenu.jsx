import React from "react";
import { Avatar, Menu, MenuItem, ListItemIcon, Dialog, DialogTitle, DialogContent, IconButton, Slide } from "@mui/material";
import { Person, Favorite, ExitToApp, Close } from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import FavoriteRestaurants from "../../../FavoriteRestaurants/FavoriteRestaurants";

// Transition component for the dialog
const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const AvatarMenu = ({ avatarImg, username }) => {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [openFavorites, setOpenFavorites] = React.useState(false);
  const navigate = useNavigate();

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleManageAccount = () => {
    handleClose();
    navigate("/manageaccount");
  };

  const handleOpenFavorites = () => {
    handleClose();
    setOpenFavorites(true);
  };

  const handleCloseFavorites = () => {
    setOpenFavorites(false);
  };

  const handleLogout = async () => {
    const accessToken = localStorage.getItem("access_token");
    const refreshToken = localStorage.getItem("refresh_token");

    const response = await fetch("https://nibble.rest/api/logout/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ access: accessToken, refresh: refreshToken }),
    });

    if (response.ok) {
      // Clear tokens from storage
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");

      // Redirect to home page
      navigate("/");
    } else {
      console.error("Failed to log out");
    }

    handleClose();
  };

  return (
    <>
      <Avatar
        alt="User Avatar"
        src={avatarImg}
        sx={{ width: 56, height: 56, margin: "0px 20px", cursor: "pointer" }}
        onClick={handleClick} // Open menu on avatar click
      />
      {/* Menu for avatar */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
        transformOrigin={{ vertical: "top", horizontal: "right" }}
        PaperProps={{
          elevation: 1,
          sx: {
            mt: 1,
          },
        }}
      >
        <MenuItem onClick={handleManageAccount}>
          <ListItemIcon>
            <Person fontSize="small" />
          </ListItemIcon>
          Manage Account
        </MenuItem>
        <MenuItem onClick={handleOpenFavorites}>
          <ListItemIcon>
            <Favorite fontSize="small" />
          </ListItemIcon>
          Favorites
        </MenuItem>
        <MenuItem onClick={handleLogout}>
          <ListItemIcon>
            <ExitToApp fontSize="small" />
          </ListItemIcon>
          Logout
        </MenuItem>
      </Menu>

      {/* Favorites Modal */}
      <Dialog
        open={openFavorites}
        onClose={handleCloseFavorites}
        TransitionComponent={Transition}
        fullWidth
        maxWidth="sm"
        PaperProps={{
          sx: {
            padding: 2,
            borderRadius: 3
          },
        }}
      >
        <DialogTitle color={"#4c83ed"}>
          Your Favorite Restaurants 
          <IconButton
            edge="end"
            color="inherit"
            onClick={handleCloseFavorites}
            aria-label="close"
            sx={{ position: 'absolute', right: 8, top: 8 }}
          >
            <Close />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          <FavoriteRestaurants />
        </DialogContent>
      </Dialog>
    </>
  );
};

export default AvatarMenu;
