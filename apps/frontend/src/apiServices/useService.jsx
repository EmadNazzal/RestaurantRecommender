import { useState, useEffect } from "react";
import * as apiService from "./apiService";

// remember for later, function logic is same except for import names, maybe make one CLASS which includes all of them, and make apiServices.{DynamicValue}
export const useRegister = (data) => {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (data) {
      setLoading(true);
      apiService
        .registerUser(data)
        .then((res) => {
          setResponse(res.data);
          setLoading(false);
        })
        .catch((err) => {
          setError(err);
          setLoading(false);
        });
    }
  }, [data]);

  return { response, error, loading };
};

export const useContactUs = () => {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const contactUs = async (data) => {
    setLoading(true);
    try {
      const res = await apiService.contactUs(data);
      setResponse(res.data);
      setLoading(false);
    } catch (error) {
      setError(error);
      setLoading(false);
      throw error;
    }
  };

  return { response, error, loading, contactUs };
};

export const useLogin = (data) => {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (data) {
      setLoading(true);
      apiService
        .loginUser(data)
        .then((res) => {
          setResponse(res.data);
          setLoading(false);
        })
        .catch((err) => {
          setError(err);
          setLoading(false);
        });
    }
  }, [data]);

  return { response, error, loading };
};

export const useAllRestaurants = () => {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    apiService
      .getAllRestaurants()
      .then((res) => {
        setResponse(res.data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err);
        setLoading(false);
      });
  }, []);

  return { response, error, loading };
};

export const useFreeTextRestaurantSearch = (query) => {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (query) {
      setLoading(true);
      apiService
        .restuarantFreeTextEntry(query)
        .then((res) => {
          setResponse(res.data);
          // console.log(res.data)
          setLoading(false);
        })
        .catch((err) => {
          setError(err);
          setLoading(false);
        });
    }
  }, [query]);

  return { response, error, loading };
};


export function useZoneForCurrentTime(currentTime) {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await apiService.getZoneForCurrentTime();
        setResponse(result.data);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [currentTime]); 

  return { response, loading, error };
}


export const useResetPassword = (data) => {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (data) {
      setLoading(true);
      apiService
        .resetPassword(data)
        .then((res) => {
          setResponse(res.data);
          setLoading(false);
        })
        .catch((err) => {
          setError(err);
          setLoading(false);
        });
    }
  }, [data]);

  return { response, error, loading };
};
// from here we can create all the api endpoints really fast "SEPERATION OF LOGIC " for better preformance and understanding and testing.
