import { useCallback } from 'react';
import { AdvancedMarker, useMap } from '@vis.gl/react-google-maps';
import customMadeMarker from '../../../assets/images/restaurant-icon.png';

function RestaurantMarkers({ locations, onMarkerClick }) {
  const map = useMap();

  const handleClick = useCallback(
    (ev, location) => {
      if (!map) return;
      if (!ev.latLng) return;
      map.panTo(ev.latLng);
      map.setZoom(18); // Zoom in on click

      // Call onMarkerClick if it's a function
      if (typeof onMarkerClick === 'function') {
        console.log('Marker clicked:', location); // Add logging
        onMarkerClick(location); // This will trigger the InfoWindow
      } else {
        console.error('onMarkerClick is not a function');
      }
    },
    [map, onMarkerClick]
  );

  // console.log('RestaurantMarkers locations:', locations); // Debugging line

  return (
    <>
      {locations.map((location) => (
        <AdvancedMarker
          key={location.id}
          position={location.location}
          clickable={true}
          onClick={(ev) => handleClick(ev, location)}
        >
          <img
            src={customMadeMarker}
            width={30}
            height={30}
            alt="Restaurant Marker"
          />
        </AdvancedMarker>
      ))}
    </>
  );
}

export default RestaurantMarkers;
