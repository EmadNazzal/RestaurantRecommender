import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'; 
import { useZoneForCurrentTime } from '../../apiServices/useService'; 
import styles from './MapCharts.module.css'; 

const MapCharts = () => {
  const [dateTime, setDateTime] = useState('2024-08-01T12:00:00');
  const [chartData, setChartData] = useState([]);
  const { response, error, loading } = useZoneForCurrentTime(dateTime);

  useEffect(() => {
    if (response && response.predictions) {
        console.log('API Response:', response); 
      const formattedData = response.predictions.map(item => ({
        zone: item.zone,
        busyness: item.predicted_value * 100 
      }));
      setChartData(formattedData);
    }
  }, [response]); 

  const handleDateTimeChange = (e) => {
    setDateTime(e.target.value);
  };

  if (loading) return <div className={styles.loadingMessage}>Loading...</div>;
  if (error) return <div className={styles.errorMessage}>Error loading data: {error.message}</div>;

  return (
    <div className={styles.container}>
      <h1 className={styles.header}>Busyness Score Visualization</h1>
      <div className={styles.datetimeSelector}>
        <label className={styles.inputLabel}>
          DateTime:
          <input
            type="datetime-local"
            value={dateTime}
            onChange={handleDateTimeChange}
            className={styles.inputField}
          />
        </label>
      </div>
      <div className={styles.chartContainer}>
        <h2>Busyness Score by Zone</h2>
        <LineChart
          width={800}
          height={400}
          data={chartData}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="zone" label={{ value: 'Zone', position: 'insideBottomRight', offset: -10 }} />
          <YAxis label={{ value: 'Busyness Score (%)', angle: -90, position: 'insideLeft' }} />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="busyness"
            stroke="#8884d8" 
            dot={{ fill: '#8884d8' }} 
          />
        </LineChart>
      </div>
    </div>
  );
};

export default MapCharts;
