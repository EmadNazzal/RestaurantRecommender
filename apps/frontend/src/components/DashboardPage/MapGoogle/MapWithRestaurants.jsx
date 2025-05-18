import React, { useContext, useEffect, useState, useCallback } from 'react';
import { APIProvider, Map } from '@vis.gl/react-google-maps';
import Directions from './Directions';
import GeoJsonLayer from './GeoJsonLayer';
import RestaurantInfoWindow from './RestaurantInfoWindow/RestaurantInfoWindow';
import { FormControl, InputLabel, MenuItem, Select } from '@mui/material';
import RestaurantMarkers from './RestaurantMarkers';
import { useZoneForCurrentTime } from '../../../apiServices/useService';
import mapStyle from './MapWithRestaurants.module.css';
import MapContext from './MapContext';

const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
const GOOGLE_MAP_ID = import.meta.env.VITE_GOOGLE_MAPS_ID_KEY;

const defaultCenter = { lat: 40.7831, lng: -73.9712 };
const defaultZoom = 13;
const restaurantZoom = 19; // Define the zoom level for a selected restaurant

function MapWithRestaurants({ restaurants, onCompare }) {
  const [locations, setLocations] = useState([]);
  const [view, setView] = useState('all-restaurants');
  const [zonesGeoJson, setZonesGeoJson] = useState(null);
  const [startLocation, setStartLocation] = useState(null);
  const [endLocation, setEndLocation] = useState(null);
  const [directionsRequested, setDirectionsRequested] = useState(false);
  const [currentHour, setCurrentHour] = useState(new Date().getHours());
  const { selectedRestaurant, selectRestaurant } = useContext(MapContext);

  const { response: predictions, loading: predictionsLoading, error: predictionsError } = useZoneForCurrentTime(currentHour);



  useEffect(() => {
    if (restaurants) {
      const locationsData = restaurants.map((restaurant) => ({
        ...restaurant,
        location: { lat: restaurant.latitude, lng: restaurant.longitude },
      }));
      updateLocations(locationsData);
    }
  }, [restaurants]);

  useEffect(() => {
    fetch('/zonesGeoJson.json')
      .then((response) => response.json())
      .then((data) => setZonesGeoJson(data))
      .catch((error) => console.error('Error loading GeoJSON:', error));
  }, []);

  useEffect(() => {
    updateLocations(locations);
  }, [view]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCurrentHour(new Date().getHours());
    }, 120000); // Update every 2 minutes

    return () => clearInterval(intervalId);
  }, []);

  const updateLocations = (data) => {
    let filteredLocations;
    switch (view) {
      case 'color-coded-zones':
        filteredLocations = data; // Placeholder for actual filtering logic
        break;
      default:
        filteredLocations = data;
    }
    setLocations(filteredLocations);
  };

  const handleViewChange = (event) => {
    setView(event.target.value);
  };

  const handleRightClick = (e) => {
    const latLng = e.detail.latLng;
    if (!startLocation) {
      setStartLocation(latLng);
    } else if (!endLocation) {
      setEndLocation(latLng);
      setDirectionsRequested(true);
    } else {
      setStartLocation(latLng);
      setEndLocation(null);
      setDirectionsRequested(false);
    }
  };

  // Determine the map center and zoom level
  const mapCenter = selectedRestaurant
    ? { lat: selectedRestaurant.latitude, lng: selectedRestaurant.longitude }
    : defaultCenter;

  const mapZoom = selectedRestaurant ? restaurantZoom : defaultZoom;

  return (
    <APIProvider apiKey={GOOGLE_MAPS_API_KEY}>
      <div style={{ height: 'calc(100vh - 90px)', width: '100%', position: 'relative' }} className={mapStyle.mapDiv}>
        <Map
          apiKey={GOOGLE_MAPS_API_KEY}
          defaultCenter={mapCenter}
          defaultZoom={mapZoom}
          mapContainerStyle={{ width: '100%', height: '100%' }}
          mapId={GOOGLE_MAP_ID}
          onContextmenu={handleRightClick}
        >
          {view === 'all-restaurants' && (
            <RestaurantMarkers
              locations={locations}
              onMarkerClick={selectRestaurant}
            />
          )}
          {view === 'color-coded-zones' && zonesGeoJson && predictions && !predictionsLoading && !predictionsError && (
            <GeoJsonLayer data={zonesGeoJson} predictions={predictions.predictions} />
          )}
          {selectedRestaurant && (
            <RestaurantInfoWindow
              restaurant={selectedRestaurant}
              onClose={() => selectRestaurant(null)}
              onCompare={onCompare}
            />
          )}
          <div style={{ position: 'absolute', bottom: 20, right: 20, zIndex: 1000, backgroundColor: '#fff', padding: '10px', boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)', borderRadius: '4px' }}>
            {startLocation && endLocation && directionsRequested && (
              <Directions
                start={startLocation}
                end={endLocation}
                reset={() => {
                  setStartLocation(null);
                  setEndLocation(null);
                  setDirectionsRequested(false);
                }}
              />
            )}
          </div>
          <div className={mapStyle.colorScale}>
            <div className={mapStyle.scaleContainer}>
              <div className={mapStyle.scaleBar}></div>
              <div className={mapStyle.labels}>
                <span>Not Busy</span>
                <span>Less Busy</span>
                <span>Moderately Busy</span>
                <span>Busy</span>
                <span>Very Busy</span>
              </div>
            </div>
          </div>
        </Map>
        <div style={{ position: 'absolute', top: 60, left: 10, zIndex: 1000 }} className={mapStyle.viewLayer}>
          <FormControl variant="filled" sx={{ width: '180px', backgroundColor: 'rgb(153 182 240)', borderRadius: '5px', color: 'white' }}>
            <InputLabel id="map-view-select-label">See Layers :</InputLabel>
            <Select
              labelId="map-view-select-label"
              id="map-view-select"
              value={view}
              onChange={handleViewChange}
            >
              <MenuItem value="all-restaurants">All Restaurants</MenuItem>
              <MenuItem value="color-coded-zones">Color-Coded Zones</MenuItem>
            </Select>
          </FormControl>
        </div>
      </div>
    </APIProvider>
  );
}

export default MapWithRestaurants;
