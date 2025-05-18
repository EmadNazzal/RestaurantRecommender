import { useEffect, useState } from "react";
import { Box, Typography, CircularProgress } from "@mui/material";
import WbSunnyIcon from "@mui/icons-material/WbSunny";
import CloudIcon from "@mui/icons-material/Cloud";
import OpacityIcon from "@mui/icons-material/Opacity";
import AcUnitIcon from "@mui/icons-material/AcUnit";
import ThunderstormIcon from "@mui/icons-material/Thunderstorm";

const weatherIcons = {
  Clear: <WbSunnyIcon sx={{ color: "#4a87ed" }} />,
  Clouds: <CloudIcon sx={{ color: "#4a87ed" }} />,
  Rain: <OpacityIcon sx={{ color: "#4a87ed" }} />,
  Snow: <AcUnitIcon sx={{ color: "#4a87ed" }} />,
  Thunderstorm: <ThunderstormIcon sx={{ color: "#4a87ed" }} />,
};

const ReactOpenWeather = ({ lat, lng }) => {
  const [weather, setWeather] = useState(null);

  useEffect(() => {
    const fetchWeather = async () => {
      const response = await fetch(
        `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lng}&appid=${
          import.meta.env.VITE_OPENWEATHER_API_KEY
        }`
      );
      const data = await response.json();
      setWeather(data);
    };

    fetchWeather();
  }, [lat, lng]);

  if (!weather) {
    return (
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          height: "90px",
          padding: "0 20px",
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  const temperature = Math.round(weather.main.temp - 273.15);
  const weatherIcon = weatherIcons[weather.weather[0].main] || <WbSunnyIcon />;

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        height: "80px",
        padding: "0 20px",
      }}
    >
      <Typography variant="h6" component="div" sx={{ marginRight: "10px", color:"#4a87ed" }}>
        {temperature}°C
      </Typography>
      {weatherIcon}
    </Box>
  );
};

export default ReactOpenWeather;
