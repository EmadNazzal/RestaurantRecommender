"""This file contains the functions to make predictions for restaurant busyness."""

import pickle  # noqa: S403
from datetime import datetime
import numpy as np
import xgboost as xgb
from django.core.cache import cache

from restaurant_recommender.models import PredictionModel, Restaurant, WeatherData  # type: ignore


def cos_transformer(period):
    """Returns a function that calculates the cosine transformation of a given value.

    Args:
        period: The period over which to calculate the transformation.

    Returns:
        function: A function that takes a value and returns its cosine transformation.
    """
    return lambda x: np.cos(x / period * 2 * np.pi)


def sin_transformer(period):
    """Returns a function that calculates the sine transformation of a given value.

    Args:
        period (int): The period over which to calculate the transformation.

    Returns:
        function: A function that takes a value and returns its sine transformation.
    """
    return lambda x: np.sin(x / period * 2 * np.pi)


def make_predictions(time):  # noqa: PLR0914, PLR0915
    """
    Make predictions for restaurant busyness based on the input data.

    Args:
        time: The time in '%Y-%m-%dT%H:%M:%S' format.

    Returns:
        dict: A dictionary containing the predictions or an error message.
    """
    try:
        # Generate a cache key based on the time and weather data
        cache_key = f"busyness_prediction_{time}"
        cached_result = cache.get(cache_key)
        if cached_result:
            print(f"Retrieved cached prediction for time: {time}")
            return cached_result

        # Try to get the model from the cache
        model = cache.get("prediction_model")
        if not model:
            prediction_model = PredictionModel.objects.filter(is_active=True).latest("updated_at")
            print(f"Prediction model loaded: {prediction_model.model_name}")

            if not prediction_model.pickle_file:
                print("Warning: pickle_file is None or empty")
                return {"error": "No active prediction model found"}

            model = pickle.loads(prediction_model.pickle_file)  # noqa: S301
            # Cache for 1 hour
            cache.set("prediction_model", model, timeout=3600)
            print("Prediction model successfully loaded from pickle and cached")

        # Parse the time to datetime format
        selected_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        print(f"Selected time: {selected_time}")

        # Extract features from the selected time
        day_of_week = selected_time.weekday() + 1
        month = selected_time.month
        hour = selected_time.hour
        minute = selected_time.minute
        print(f"Extracted features - Day of week: {day_of_week}, Month: {month}, Hour: {hour}, Minute: {minute}")

        # Apply cosine and sine transformations to time features
        month_cos = cos_transformer(12)(month)
        hour_cos = cos_transformer(24)(hour)
        minute_cos = cos_transformer(60)(minute)
        dow_cos = cos_transformer(7)(day_of_week)
        month_sin = sin_transformer(12)(month)
        hour_sin = sin_transformer(24)(hour)
        minute_sin = sin_transformer(60)(minute)
        dow_sin = sin_transformer(7)(day_of_week)
        print("Cosine and sine transformations applied.")

        # Fetch weather data from cache
        temp = cache.get("temperature")
        dwpt = cache.get("dewpoint")
        prcp = cache.get("precipitation")

        if temp is None or dwpt is None or prcp is None:
            weather_data = WeatherData.objects.latest("timestamp")
            temp = weather_data.temperature
            dwpt = weather_data.dewpoint
            prcp = weather_data.precipitation
            # Cache weather for an hour
            cache.set("temperature", temp, timeout=3600)
            cache.set("dewpoint", dwpt, timeout=3600)
            cache.set("precipitation", prcp, timeout=3600)
            print("Weather data fetched from database and cached")

        # Retrieve all unique zones
        zones_and_locations = Restaurant.objects.values_list("zone", "location_id").distinct()
        print(f"Retrieved zones and location_ids: {zones_and_locations}")

        predictions = []
        for zone, location_id in zones_and_locations:
            DOLocationID = location_id  # noqa: N806
            input_features = np.array([
                DOLocationID,
                temp,
                dwpt,
                prcp,
                day_of_week,
                month_cos,
                hour_cos,
                minute_cos,
                dow_cos,
                month_sin,
                hour_sin,
                minute_sin,
                dow_sin,
            ]).reshape(1, -1)
            print(f"Input features for location_id {location_id} in zone {zone}: {input_features}")

            feature_names = [
                "DOLocationID",
                "temp",
                "dwpt",
                "prcp",
                "day_of_week",
                "month_cos",
                "hour_cos",
                "minute_cos",
                "dow_cos",
                "month_sin",
                "hour_sin",
                "minute_sin",
                "dow_sin",
            ]
            dmatrix_input = xgb.DMatrix(input_features, feature_names=feature_names)
            print("Converted input features to DMatrix.")
            predicted_value = model.predict(dmatrix_input)
            print(f"Prediction for zone {zone} with location_id {location_id}: {predicted_value}")

            predicted_value = float(predicted_value[0])
            predictions.append({"zone": zone, "predicted_value": predicted_value})

        result = {"predictions": predictions}
        # Cache time for 10 minutes
        cache.set(cache_key, result, timeout=600)
        print(f"Cached prediction result for time: {time}")

        return result  # noqa: TRY300

    except PredictionModel.DoesNotExist:
        print("No active prediction model found.")
        return {"error": "No active prediction model found"}
    except ValueError as e:
        print(f"Error during prediction: {e!s}")
        return {"error": str(e)}
