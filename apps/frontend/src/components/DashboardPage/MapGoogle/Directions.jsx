import { useEffect, useState } from "react";
import { useMap, useMapsLibrary } from "@vis.gl/react-google-maps";
import styles from "./MapWithRestaurants.module.css";

function Directions({ start, end, reset }) {
  const map = useMap();
  const routesLibrary = useMapsLibrary("routes");
  const [directionsService, setDirectionsService] = useState(null);
  const [directionsRenderer, setDirectionsRenderer] = useState(null);
  const [routes, setRoutes] = useState([]);
  const [routeIndex, setRouteIndex] = useState(0);
  const selected = routes[routeIndex];
  const leg = selected?.legs[0];

  useEffect(() => {
    if (!routesLibrary || !map) return;
    setDirectionsService(new routesLibrary.DirectionsService());
    const renderer = new routesLibrary.DirectionsRenderer({ map });
    setDirectionsRenderer(renderer);
    
    // Clean up the renderer when component unmounts
    return () => {
      if (renderer) {
        renderer.setMap(null);
      }
    };
  }, [routesLibrary, map]);

  useEffect(() => {
    if (!directionsService || !directionsRenderer) return;

    directionsService
      .route({
        origin: start,
        destination: end,
        travelMode: google.maps.TravelMode.DRIVING,
        provideRouteAlternatives: true,
      })
      .then((response) => {
        directionsRenderer.setDirections(response);
        setRoutes(response.routes);
      });
  }, [directionsService, directionsRenderer, start, end]);

  useEffect(() => {
    if (!directionsRenderer) return;
    directionsRenderer.setRouteIndex(routeIndex);
  }, [routeIndex, directionsRenderer]);

  const handleReset = () => {
    if (directionsRenderer) {
      directionsRenderer.setDirections(null); // Clear directions from the map
    }
    setRoutes([]);
    setRouteIndex(0);
    reset(); // Call the provided reset function
  };

  if (!leg) return null;

  return (
    <div className={styles.card}>
      <h2 className={styles.cardTitle}>{selected.summary}</h2>
      <p className={styles.cardText}>
        {leg.start_address.split(",")[0]} to {leg.end_address.split(",")[0]}
      </p>
      <p className={styles.cardText}>Distance: {leg.distance?.text}</p>
      <p className={styles.cardText}>Duration: {leg.duration?.text}</p>
      <h2 className={styles.cardTitle}>Alternative Routes:</h2>
      <ul className={styles.cardList}>
        {routes.map((route, index) => (
          <li key={route.summary} className={styles.cardListItem}>
            <button
              className={styles.cardButton}
              onClick={() => setRouteIndex(index)}
            >
              {route.summary}
            </button>
          </li>
        ))}
      </ul>
      <button onClick={handleReset} className={styles.cardButton}>
        Reset
      </button>
    </div>
  );
}

export default Directions;
