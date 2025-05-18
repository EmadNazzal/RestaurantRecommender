import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const SignUp = () => {
    const navigate = useNavigate();
    const [userData, setUserData] = useState({
        first_name: '',
        surname: '',
        email: '',
        password: '',
        password_confirm: '',
    });
    const [preferences, setPreferences] = useState([]);
    const [selectedPreferences, setSelectedPreferences] = useState([]);
    const [similarUsers, setSimilarUsers] = useState([]);
    const [recommendedRestaurants, setRecommendedRestaurants] = useState([]);

    useEffect(() => {
        axios.get('/api/api/preferences/')
            .then(response => {
                setPreferences(response.data);
            })
            .catch(error => {
                console.error('Error fetching preferences:', error);
            });
    }, []);

    const handleInputChange = (e) => {
        setUserData({ ...userData, [e.target.name]: e.target.value });
    };

    const handlePreferenceChange = (preferenceId) => {
        setSelectedPreferences(prev =>
            prev.includes(preferenceId)
                ? prev.filter(id => id !== preferenceId)
                : [...prev, preferenceId]
        );
    };

    const handleSignUp = async () => {
        const registrationData = {
            ...userData,
            preferences: selectedPreferences
        };

        try {
            await axios.post('/api/api/register/', registrationData);
            alert('User registered successfully.');

            // Ensure user is logged in
            const loginResponse = await axios.post('/api/api/login/', {
                email: userData.email,
                password: userData.password
            });
            const { access, refresh } = loginResponse.data;
            localStorage.setItem('token', access);
            document.cookie = `access_token=${access}; path=/; SameSite=None; Secure`;
            document.cookie = `refresh_token=${refresh}; path=/; SameSite=None; Secure`;

            await fetchSimilarUsers();
            const recommendedRestaurantsData = await fetchRecommendedRestaurants();
            setRecommendedRestaurants(recommendedRestaurantsData);

            const sortedRestaurants = recommendedRestaurantsData.sort((a, b) => a.rating - b.rating);

            navigate('/sorted-restaurants', { state: { restaurants: sortedRestaurants } });
        } catch (error) {
            console.error('Error registering user:', error);
        }
    };

    const fetchSimilarUsers = async () => {
        try {
            const response = await axios.get('/api/api/users/similar/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            setSimilarUsers(Array.isArray(response.data) ? response.data : []);
        } catch (error) {
            console.error('Error fetching similar users:', error);
            setSimilarUsers([]); // Set to empty array in case of error
        }
    };

    const fetchRecommendedRestaurants = async () => {
        try {
            const response = await axios.get('/api/api/restaurants/recommend/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            console.log("Fetched Recommended Restaurants:", response.data);
            return Array.isArray(response.data) ? response.data : [];
        } catch (error) {
            console.error('Error fetching recommended restaurants:', error);
            return [];
        }
    };

    return (
        <div>
            <h1>Sign Up</h1>
            <input
                type="text"
                name="first_name"
                placeholder="First Name"
                value={userData.first_name}
                onChange={handleInputChange}
            />
            <input
                type="text"
                name="surname"
                placeholder="Surname"
                value={userData.surname}
                onChange={handleInputChange}
            />
            <input
                type="email"
                name="email"
                placeholder="Email"
                value={userData.email}
              onChange={handleInputChange}
            />
            <input
                type="password"
                name="password"
                placeholder="Password"
                value={userData.password}
                onChange={handleInputChange}
            />
            <input
                type="password"
                name="password_confirm"
                placeholder="Confirm Password"
                value={userData.password_confirm}
                onChange={handleInputChange}
            />
            <h2>Select Your Preferences</h2>
            <ul>
                {preferences.map(preference => (
                    <li key={preference.id}>
                        <label>
                            <input
                                type="checkbox"
                                checked={selectedPreferences.includes(preference.id)}
                                onChange={() => handlePreferenceChange(preference.id)}
                            />
                            {preference.description}
                        </label>
                    </li>
                ))}
            </ul>
            <button onClick={handleSignUp}>Sign Up</button>

            {similarUsers.length > 0 && (
                <div>
                    <h2>Similar Users</h2>
                    <ul>
                        {similarUsers.map(user => (
                            <li key={user.email}>
                                {user.email} (Similarity: {user.similarity.toFixed(2)})
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {recommendedRestaurants.length > 0 && (
                <div>
                    <h2>Recommended Restaurants</h2>
                    <ul>
                        {recommendedRestaurants.map(restaurant => (
                            <li key={restaurant.id}>{restaurant.name}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default SignUp;