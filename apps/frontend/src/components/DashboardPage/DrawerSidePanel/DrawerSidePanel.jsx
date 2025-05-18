import React, { useState } from "react";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import Tooltip from "@mui/material/Tooltip";
import IconButton from "@mui/material/IconButton";
import {
  LocationOnOutlined,
  RestaurantOutlined,
  ThumbUpOutlined,
  MapOutlined,
} from "@mui/icons-material";
import CompareArrowsRoundedIcon from "@mui/icons-material/CompareArrowsRounded";
import Typography from "@mui/material/Typography";
import Badge from "@mui/material/Badge";
import { useNavigate } from "react-router-dom";
import { Regions } from "../../Regions/Regions";
import { Restaurants } from "../../Restaurants/Restaurants";
import MapCharts from "../../MapCharts/MapCharts";
import CompareRestaurants from "../../CompareRestaurants/CompareRestaurants";
import styles from "./drawerSidePanel.module.css";

const sideBarList = [
  { label: "Regions", icon: <LocationOnOutlined /> },
  { label: "Restaurants", icon: <RestaurantOutlined /> },
  { label: "Compare", icon: <CompareArrowsRoundedIcon /> },
  { label: "Recommendations", icon: <ThumbUpOutlined /> },
  { label: "Charts", icon: <MapOutlined /> },
];

function DrawerSidePanel({ compareRestaurants, onResetComparison }) {
  const [modalOpen, setModalOpen] = useState(null);
  const navigate = useNavigate();

  const handleModalOpen = (label) => {
    setModalOpen(label);
  };

  const handleModalClose = () => {
    setModalOpen(null);
  };

  const modalContent = {
    Regions: <Regions />,
    Restaurants: <Restaurants />,
    Compare: (
      <CompareRestaurants
        restaurants={compareRestaurants}
        onReset={onResetComparison}
      />
    ),
    Recommendations: "Content for Recommendations",
    Charts: <MapCharts />,
  };

  return (
    <Box
      sx={{
        position: "fixed",
        top: "50%",
        left: 0,
        transform: "translateY(-50%)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        zIndex: 1300,
        paddingLeft: 1,
      }}
      className={styles.leftSideIcons}
    >
      {sideBarList.map((item, index) => (
        <Tooltip title={item.label} placement="right" key={index} >
          <IconButton
            sx={{
              color: "#ffffff",
              margin: "10px 0",
              backgroundColor: "#2e6ce8",
              "&:hover": {
                backgroundColor: "#1d4db8",
              },
            }}
            onClick={() => handleModalOpen(item.label)}
          >
            {item.label === "Compare" ? (
              <Badge badgeContent={compareRestaurants.length} color="error" className={styles.compareIcon}>
                {item.icon}
              </Badge>
            ) : (
              item.icon
            )}
          </IconButton>
        </Tooltip>
      ))}

      {sideBarList.map((item, index) => (
        <Modal
          key={index}
          open={modalOpen === item.label}
          onClose={handleModalClose}
          aria-labelledby={`${item.label}-modal-title`}
          aria-describedby={`${item.label}-modal-description`}
        >
          <Box className={styles.modalBox}>
            <Typography
              id={`${item.label}-modal-title`}
              variant="h6"
              component="h2"
            >
              {item.label}
            </Typography>
            <Box id={`${item.label}-modal-description`} sx={{ mt: 2 }}>
              {modalContent[item.label]}
            </Box>
          </Box>
        </Modal>
      ))}
    </Box>
  );
}

export default DrawerSidePanel;
