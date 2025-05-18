import React from 'react';
import { Button, Card, CardContent, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import { useTheme } from '@mui/material/styles';

function CompareRestaurants({ restaurants, onReset }) {
  const theme = useTheme();

  if (restaurants.length < 2) return <Typography>No restaurants to compare.</Typography>;

  const [rest1, rest2] = restaurants;

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" component="h2" color={"#4c83ed"} sx={{textAlign:"center", padding:"10px"}}>
          Compare Restaurants
        </Typography>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell color='#d32f2f'>Name</TableCell>
                <TableCell>{rest1.restaurant_name}</TableCell>
                <TableCell>{rest2.restaurant_name}</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell>Address</TableCell>
                <TableCell>{rest1.address}</TableCell>
                <TableCell>{rest2.address}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Primary Cuisine</TableCell>
                <TableCell>{rest1.primary_cuisine}</TableCell>
                <TableCell>{rest2.primary_cuisine}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Price Range</TableCell>
                <TableCell>{rest1.price}</TableCell>
                <TableCell>{rest2.price}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Overall Rating</TableCell>
                <TableCell>{rest1.overall_rating}</TableCell>
                <TableCell>{rest2.overall_rating}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Ambience Rating</TableCell>
                <TableCell>{rest1.ambience_rating}</TableCell>
                <TableCell>{rest2.ambience_rating}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Food Rating</TableCell>
                <TableCell>{rest1.food_rating}</TableCell>
                <TableCell>{rest2.food_rating}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Service Rating</TableCell>
                <TableCell>{rest1.service_rating}</TableCell>
                <TableCell>{rest2.service_rating}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Value Rating</TableCell>
                <TableCell>{rest1.value_rating}</TableCell>
                <TableCell>{rest2.value_rating}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Noise Level</TableCell>
                <TableCell>{rest1.noise_level}</TableCell>
                <TableCell>{rest2.noise_level}</TableCell>
              </TableRow>
              {/* Add more rows as needed */}
            </TableBody>
          </Table>
        </TableContainer>
        <Button variant="outlined" color="primary" onClick={onReset} style={{ marginTop: theme.spacing(2) }}>
          Reset
        </Button>
      </CardContent>
    </Card>
  );
}

export default CompareRestaurants;
