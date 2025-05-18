import { useEffect, useMemo } from "react";
import { useMap } from "@vis.gl/react-google-maps";

function GeoJsonLayer({ data, predictions }) {
  const map = useMap();

  const getColorFromPrediction = (value) => {
    if (value >= 2.5) return '#FF0000'; // Red for very busy areas
    if (value >= 1.5 && value < 2.5) return '#FFA500'; // Orange for busy areas
    if (value >= 0.5 && value < 1.5) return '#FFFF00'; // Yellow for moderately busy areas
    if (value >= 0.2 && value < 0.5) return '#00FF00'; // Green for less busy areas
    if (value < 0.2) return '#0000FF'; // Blue for not busy areas
  };

  const processedData = useMemo(() => {
    if (!data || !predictions) return data;

    const predictionMap = predictions.reduce((acc, prediction) => {
      acc[prediction.zone] = prediction.predicted_value;
      return acc;
    }, {});

    return {
      ...data,
      features: data.features.map((feature) => {
        const zoneName = feature.properties.zone;
        const predictedValue = predictionMap[zoneName] || 0;
        return {
          ...feature,
          properties: {
            ...feature.properties,
            predictedValue,
          },
        };
      }),
    };
  }, [data, predictions]);

  useEffect(() => {
    if (!map || !processedData) return;

    const geoJsonLayer = new google.maps.Data();
    geoJsonLayer.addGeoJson(processedData);

    geoJsonLayer.setStyle((feature) => {
      const predictedValue = feature.getProperty('predictedValue');
      const color = getColorFromPrediction(predictedValue);

      return {
        strokeColor: '#4B2E2A',
        strokeWeight: 0.5,
        fillColor: color,
        fillOpacity: 0.5,
      };
    });

    geoJsonLayer.setMap(map);

    return () => {
      geoJsonLayer.setMap(null);
    };
  }, [map, processedData]);

  return null;
}

export default GeoJsonLayer;
