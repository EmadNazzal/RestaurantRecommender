import { useState } from "react";
import { useFreeTextRestaurantSearch } from "../../apiServices/useService";
import { TextField, Paper, Typography, Chip, CircularProgress, Box, Card, CardMedia, CardContent, Grid } from "@mui/material";
import { green, red } from "@mui/material/colors";
import { styled } from "@mui/material/styles";

const ChipPositive = styled(Chip)(({ theme }) => ({
  backgroundColor: green[500],
  color: theme.palette.getContrastText(green[500]),
}));

const ChipNegative = styled(Chip)(({ theme }) => ({
  backgroundColor: red[500],
  color: theme.palette.getContrastText(red[500]),
}));

const RestaurantCard = styled(Card)(({ theme }) => ({
  marginBottom: theme.spacing(3),
}));

export const Restaurants = () => {
  const [query, setQuery] = useState("");
  const { response, error, loading } = useFreeTextRestaurantSearch(query);

  const handleSearch = (e) => {
    if (e.key === "Enter") {
      setQuery(e.target.value);
    }
  };

  return (
    <Box sx={{ padding: 2, maxWidth: 800, margin: "0 auto" }}>
      <TextField
        fullWidth
        label="Search for restaurants"
        variant="outlined"
        onKeyDown={handleSearch}
        sx={{ marginBottom: 3 }}
      />
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: 2 }}>
          <CircularProgress />
        </Box>
      )}
      {error && (
        <Typography color="error" sx={{ marginTop: 2 }}>
          Error: {error.message}
        </Typography>
      )}
      {response && response.length > 0 && (
        <Grid container spacing={3}>
          {response.map((restaurant) => (
            <Grid item xs={12} sm={6} md={4} key={restaurant.id}>
              <RestaurantCard>
                <CardMedia
                  component="img"
                  height="140"
                  image={JSON.parse(restaurant.photo_url)[0]}
                  alt={restaurant.restaurant_name}
                />
                <CardContent>
                  <Typography variant="h5" gutterBottom sx={{ color: "#4c83ed" }}>
                    {restaurant.restaurant_name}
                  </Typography>
                  <Typography variant="body1" paragraph>
                    <strong>Cuisine:</strong> {restaurant.primary_cuisine}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Overall Rating: {restaurant.overall_rating}
                  </Typography>
                  <Box sx={{ marginTop: 2 }}>
                    <Typography variant="h6">Positive Aspects:</Typography>
                    <Box sx={{ marginTop: 1 }}>
                      {restaurant.aspects
                        .filter((aspect) => aspect.rating_type === "positive")
                        .map((aspect) => (
                          <ChipPositive key={aspect.id} label={aspect.aspect} sx={{ margin: 0.5 }} />
                        ))}
                    </Box>
                  </Box>
                  <Box sx={{ marginTop: 2 }}>
                    <Typography variant="h6">Negative Aspects:</Typography>
                    <Box sx={{ marginTop: 1 }}>
                      {restaurant.aspects
                        .filter((aspect) => aspect.rating_type === "negative")
                        .map((aspect) => (
                          <ChipNegative key={aspect.id} label={aspect.aspect} sx={{ margin: 0.5 }} />
                        ))}
                    </Box>
                  </Box>
                </CardContent>
              </RestaurantCard>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};
