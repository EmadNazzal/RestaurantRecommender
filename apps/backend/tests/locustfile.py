"""This file contains the locust test cases for the backend API."""

from locust import HttpUser, TaskSet, between, tag, task

TWO_HUNDRED = 200


class UserBehavior(TaskSet):
    """User behavior for the locust tests."""

    @tag("login")
    @task
    def login(self):
        """Login task for the locust tests."""
        response = self.client.post(
            "/api/login/", json={"email": "han@example.com", "password": "secure3password"})
        if response.status_code == TWO_HUNDRED:
            try:
                response_json = response.json()
                self.access_token = response_json.get("access")
                self.refresh_token = response_json.get("refresh")
                self.client.headers.update(
                    {"Authorization": f"Bearer {self.access_token}"})
                print(f"Successfully logged in. Token: {self.access_token}")
            except ValueError:
                print(f"Failed to decode JSON. Response text: {response.text}")
        else:
            print(
                f"Login failed with status code {response.status_code}. Response text: {response.text}")

    @task(1)
    def view_profile(self):
        response = self.client.get("/api/profiles/82/")
        print(
            f"View Profile Response: {response.status_code}, {response.text}")

    @task(2)
    def view_bookmarks(self):
        """View bookmarks task for the locust tests."""
        response = self.client.get("/api/bookmarks/")
        print(
            f"View Bookmarks Response: {response.status_code}, {response.text}")

    @task(1)
    def create_bookmark(self):
        """Create bookmark task for the locust tests."""
        response = self.client.post(
            "/api/bookmarks/", json={"restaurant_ids": [4500]})
        print(
            f"Create Bookmark Response: {response.status_code}, {response.text}")

    @task(1)
    def contact_us(self):
        """Contact us task for the locust tests."""
        response = self.client.post(
            "/api/contact-us/",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "subject": "Not happy at all",
                "message": "Should be happier!",
            },
        )
        print(f"Contact Us Response: {response.status_code}, {response.text}")

    @task(1)
    def register_user(self):
        """Register user task for the locust tests."""
        response = self.client.post(
            "/api/register/",
            json={
                "first_name": "Testingagain",
                "surname": "Willtestingeverend",
                "email": "testusertestuser@example.com",
                "password": "password123123",
                "confirm_password": "password123123",
            },
        )
        print(
            f"Register User Response: {response.status_code}, {response.text}")

    @task(1)
    def reset_password_request(self):
        """Reset password request task for the locust tests."""
        response = self.client.post(
            "/api/reset-password/", json={"email": "testuser@example.com"})
        print(
            f"Reset Password Request Response: {response.status_code}, {response.text}")

    @task(1)
    def reset_password_confirm(self):
        """Reset password confirm task for the locust tests."""
        response = self.client.post(
            "/api/reset-password/confirm/valid_token/", json={"token": "valid_token", "new_password": "new_password123"}
        )
        print(
            f"Reset Password Confirm Response: {response.status_code}, {response.text}")

    @task(1)
    def logout_user(self):
        """Logout user task for the locust tests."""
        response = self.client.post(
            "/api/logout/", json={"refresh": self.refresh_token})
        print(f"Logout Response: {response.status_code}, {response.text}")


class RestaurantRecommenderTasks(TaskSet):
    """TaskSet for the restaurant recommender API."""

    @task(1)
    def get_all_restaurants(self):
        """Get all restaurants task for the locust tests."""
        response = self.client.get("/api/all-restaurants/")
        print(
            f"Get All Restaurants Response: {response.status_code}, {response.text}")

    @task(2)
    def free_text_restaurant_search(self):
        """Free text restaurant search task for the locust tests."""
        response = self.client.get(
            "/api/free-text-restaurant-search/", params={"query": "Pizza"})
        print(
            f"Free Text Restaurant Search Response: {response.status_code}, {response.text}")

    @task(1)
    def predict_busyness(self):
        """Predict busyness task for the locust tests."""
        response = self.client.get("/api/2024-07-07T12:00:00/zone/")
        print(
            f"Predict Busyness Response: {response.status_code}, {response.text}")


class WebsiteUser(HttpUser):
    """Website user for the locust tests."""

    tasks = [UserBehavior, RestaurantRecommenderTasks]
    wait_time = between(1, 5)
    host = "https://nibble.rest"

    def on_start(self):
        """on_start is called when a Locust user starts."""
        self.client.headers.update({"Content-Type": "application/json"})


if __name__ == "__main__":
    import subprocess

    subprocess.run(["locust", "-f", "locustfile.py",
                   "--host=https://nibble.rest"])
