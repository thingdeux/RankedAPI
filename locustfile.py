# This is a locust definition file.
# (http://docs.locust.io/)
#
# It is not intended that this is run on a any of the servers so please do *not* include
# Locust as a dependency in requirements.txt.  It comes with a number of unnecessary libraries
# And should only be run locally.

# To Install -> pip install locustio==0.8a2
# To Run -> locust --host=http://api.goranked.com
# Navigate to http://127.0.0.1:8089 

from locust import HttpLocust, TaskSet, task
import json
import random
from math import floor

class FastConsumingWideCoverageUserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()
        random.seed()

    def login(self):
        response = self.client.post("/api/v1/users/auth/token/", {"username": "TylerWilliams",
                                           "password": "TylerWilliams11",
                                           "client_id": "j7jhdBmo7jqw6CjZoBvgHK0FjZ0vzag8iypDs7x6",
                                           "grant_type": "password"})
        try:
            if response.status_code == 200:
                json_response = json.loads(response.content)
                self.auth_token = json_response['access_token']
        except Exception as e:
            # Auth Failed - Use non-expiring token.
            self.auth_token = "ObZx00UNXBPnnPYew9pD9VldlDRogW"
            # print("Auth Failure w/ Status {}".format(response))
            response.failure('AUTH FAILED')

    def get_header(self):
        try:
            return self.auth_token or "ObZx00UNXBPnnPYew9pD9VldlDRogW"
        except AttributeError:
            return "ObZx00UNXBPnnPYew9pD9VldlDRogW"

    @task(2)
    def index(self):
        self.client.get("/api/v1/videos/", headers={ "Authorization": 'Bearer {}'.format(self.get_header()) })

    @task(4)
    def profile(self):
        self.client.get("/api/v1/users/me/", headers={"Authorization": 'Bearer {}'.format(self.get_header())})

        random_id = floor(random.randint(1, 54))
        self.client.get("/api/v1/users/{}/followers/".format(random_id), headers={"Authorization": 'Bearer {}'.format(self.get_header())})
        random_id = floor(random.randint(1, 54))
        self.client.get("/api/v1/users/{}/followers/".format(random_id), headers={"Authorization": 'Bearer {}'.format(self.get_header())})
        random_id = floor(random.randint(1, 54))
        self.client.get("/api/v1/users/{}/following/".format(random_id), headers={"Authorization": 'Bearer {}'.format(self.get_header())})

    @task(5)
    def search(self):
        random_id = floor(random.randint(1, 60))
        self.client.get("/api/v1/search/?category={}".format(random_id), headers={"Authorization": 'Bearer {}'.format(self.get_header())})
        self.client.get("/api/v1/search/explore/?category={}&name=thing".format(random_id),
                        headers={"Authorization": 'Bearer {}'.format(self.get_header())})

    @task(5)
    def video_detail(self):
        random_id = floor(random.randint(1, 1300))
        self.client.get("/api/v1/videos/{}/".format(random_id), headers={"Authorization": 'Bearer {}'.format(self.get_header())})
        random_id = floor(random.randint(1, 1300))
        self.client.get("/api/v1/videos/{}/".format(random_id), headers={"Authorization": 'Bearer {}'.format(self.get_header())})
        random_id = floor(random.randint(1, 1300))
        self.client.get("/api/v1/videos/{}/".format(random_id), headers={"Authorization": 'Bearer {}'.format(self.get_header())})


class WebsiteUser(HttpLocust):
    task_set = FastConsumingWideCoverageUserBehavior

    min_wait = 3000
    max_wait = 8000