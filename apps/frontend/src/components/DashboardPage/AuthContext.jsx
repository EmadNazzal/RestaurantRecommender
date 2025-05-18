import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      // Clear any previous errors
      setError(null);
      setLoading(true);

      // Retrieve the token from localStorage or sessionStorage
      const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
      // console.log('Token from authContext:', token);

      // Check if token is available
      if (!token) {
        console.warn('No token found in localStorage or sessionStorage.');
        setLoading(false);
        setUser(null);
        return;
      }

      try {
        const response = await fetch('https://nibble.rest/api/profiles/', {
          headers: { Authorization: `Bearer ${token}` }
        });

        // Check if the response is okay
        if (response.ok) {
          const userData = await response.json();
          console.log('Fetched user data:', userData);
          setUser(userData);
        } else {
          // Log and set error state if response is not okay
          console.error('Error fetching user data:', response.status, response.statusText);
          setError(`Error: ${response.status} ${response.statusText}`);
          setUser(null);
        }
      } catch (err) {
        // Log and set error state for any other errors
        console.error('Error fetching user data:', err);
        setError('An unexpected error occurred.');
        setUser(null);
      } finally {
        // Set loading to false after attempt
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, error }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook for using authentication context
export const useAuth = () => useContext(AuthContext);
