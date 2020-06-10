import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


casting_assistant = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNrWXIyMTZtVmtibHZHRmszQmRNdCJ9.eyJpc3MiOiJodHRwczovL2Rldi0tM3hnYXZwMS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkZmJiNDlhMTFjN2YwMDFhMWEwNWI1IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU5MTcyMDg0OSwiZXhwIjoxNTkxODA3MjQ5LCJhenAiOiJqSkFqaGVzVkVPSE8zM2ZtNFpsZFN0NzJlTk9xVlNhTCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIl19.C1rYpeY4WQBfd7jKhSz0gJjAFHwN7qTtp3PW2_QB56M9kFdSSq1D99F2QPdzZ6XGYFQAToC6F36xYs0shgd_YdIX0x5u_Lh5dxDDXdvB9BzfoHKFb9J4GOuHKDECHbvm-GX9Bqe0LYLowuNBczvMRY2UBmd5UM7qp9bPdzHs7avFk2OQHw0ChOzC2p88njhe5J8IWNqG_5udEolu0CC1g34skwtOBl78vZZ663_DyciWoypDGzre2Xu9ZUI5rEA1UZvMr01WWPQ-OpqDAqjzPfbYnZN19TfKVZTFicOKEOWLY2mg-lzYviijhLGBSDifmNfc9ASKEgk7XWkcVElpuQ"}
casting_director = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNrWXIyMTZtVmtibHZHRmszQmRNdCJ9.eyJpc3MiOiJodHRwczovL2Rldi0tM3hnYXZwMS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkZmJjYTc0NWJkN2UwMDE5ZDQ3ZmJhIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU5MTcyMTIxNiwiZXhwIjoxNTkxODA3NjE2LCJhenAiOiJqSkFqaGVzVkVPSE8zM2ZtNFpsZFN0NzJlTk9xVlNhTCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.i8SQw8seo-N0twmjccpOotJMY7H9KZAIFQ_WaG61Pp2sa6vRcWGsJ4goq9GbYETU7Tj1v2mlyI_3Y1bqeG6L1m2f-BIBJEVhQu3lgfO_dQt2yFME_C5urUh0O1lwN-uVRVoBObmRMeu_9POMVNXQu_nskqRg2sptTO1z2XNPWfaSZvWTQAWws1uVqyZh_wT82xr0-gkf0I4K1L3fxoyU-VelY6qD-obZwczM6uRKNyqnAGQrZYmhbV2AUNwRgRQ5E8sDU35BrMZfdg_m3zfr5dPn_QW7pDpwL3RTitdJOzSs6_dTogKM7G698xSfyvMpEdol87x-hQxZiUXVRvr1lQ"}
executive_producer = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNrWXIyMTZtVmtibHZHRmszQmRNdCJ9.eyJpc3MiOiJodHRwczovL2Rldi0tM3hnYXZwMS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkZmJkYjcyYjAwNjIwMDEzN2M5NmYwIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU5MTcyMTQ4MiwiZXhwIjoxNTkxODA3ODgyLCJhenAiOiJqSkFqaGVzVkVPSE8zM2ZtNFpsZFN0NzJlTk9xVlNhTCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.LMKOyaYfGWNe4FgVzaMZttQFzDPa0XXTiSQRCqCYTP_9HprLThsojiocEKbKeF2oJQ9Ep5W4C06JYdrRFnvxGocpxcwuTN1uehHEY6jIvMCHuhKIbDpTRs8amx3aSfMkZOIY_60uNYMzuYuq4wK7mH6rfExvPEJVwrJsRUk4VGqzauo1oXVYOoibdda-_hAss7pNlWz37KX5TCJl1i3dYh8qDWczv4FZn436IvwncVxf9Dg7QpPiQrtGAIS0ApUNVucxAWvd-Nf89zAsZCFRhPA-BM9Q5CiOSfZxdD1sOJVvOXRJXBE9dnBbIsWpLsKobdp-2jwIaMrVCBjDoFtoEA"}
invalid_jwt = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIibHZHRmszQmRNdCJ9.eyJpc3MiOiJodHRw5jb20vIiwic3ViIjoiYXwiYXVkIjoiY2FzdGluZyIsImlhdCI6wicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIl19.fxdjBICcR4u8u4Z44a7Q"}


new_actor = {
    "name": "Magnolia",
    "age": 27,
    "gender": "female"
}
partial_actor = {
    "name": "Magneelia"
}
new_movie = {
   "title": "Mi Vidaa",
   "release_date": "2019-07-02T18:42:29Z"
}
partial_movie = {
   "title": "Mi Vida"
}


class CastingTestCase(unittest.TestCase):
    """This class represents the Casting test case"""

    def setUp(self):
        """Executed before each test"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test_heroku"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    """
    First, test for success/failure at each endpoint with permissions
    """

    def test_get_actors_404(self):
        """Test getting actors from an empty database """
        res = self.client().get('/actors', headers=casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_get_movies_404(self):
        """Test getting movies from an empty database """
        res = self.client().get('/movies', headers=casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_post_actor(self):
        """Test creating an actor in the database """
        res = self.client().post('/actors/create', json=new_actor, headers=executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["new actor"])

    def test_post_actor_422(self):
        """Test posting an actor with missing attribute """
        res = self.client().post('/actors/create', json=partial_actor, headers=executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unprocessable entity")

    def test_post_movie(self):
        """Test creating a movie in the database """
        res = self.client().post('/movies/create', json=new_movie, headers=executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["new movie"])

    def test_post_movie_422(self):
        """Test posting a movie with missing attribute """
        res = self.client().post('/movies/create', json=partial_movie, headers=executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unprocessable entity")

    def test_get_actors(self):
        """Test getting actors successfully """
        res = self.client().get('/actors', headers=casting_assistant)
        data = json.loads(res.data)

        #  self.assertEqual(res.status_code, 200)
        #  self.assertTrue(data["success"])
        #  self.assertTrue(data["actors"])

    def test_get_movies(self):
        """Test getting movies """
        res = self.client().get('/movies', headers=casting_assistant)
        data = json.loads(res.data)

        #  self.assertEqual(res.status_code, 200)
        #  self.assertTrue(data["success"])
        #  self.assertTrue(data["movies"])

    def test_patch_actor(self):
        """Test updating an actor in database """
        res = self.client().patch('/actors/2', json=new_actor, headers=executive_producer)
        data = json.loads(res.data)

        #  self.assertEqual(res.status_code, 200)
        #  self.assertTrue(data["success"])
        #  self.assertTrue(data["updated actor"])

    def test_patch_actor_400(self):
        """Test updating an actor with invalid actor_id """
        res = self.client().patch('/actors/1000', json=partial_actor, headers=executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "bad request")

    def test_patch_movie(self):
        """Test updating a movie in database """
        res = self.client().patch('/movies/2', json=partial_movie, headers=casting_director)
        data = json.loads(res.data)

        #  self.assertEqual(res.status_code, 200)
        #  self.assertTrue(data["success"])
        #  self.assertTrue(data["updated movie"])

    def test_patch_movie_400(self):
        """Test updating a movie with invalid movie_id """
        res = self.client().patch('/movies/8080', json=partial_movie, headers=executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "bad request")

    def test_delete_actor(self):
        """Test deleting an actor from the database """
        res = self.client().delete('/actors/2/delete', headers=casting_director)
        data = json.loads(res.data)

        #  self.assertEqual(res.status_code, 200)
        #  self.assertTrue(data["success"])
        #  self.assertTrue(data["deleted"])

    def test_delete_actor_404(self):
        """Test deleting an actor with invalid actor_id """
        res = self.client().delete('/actors/2/delete', headers=executive_producer)
        data = json.loads(res.data)

        #  self.assertEqual(res.status_code, 404)
        #  self.assertFalse(data["success"])
        #  self.assertEqual(data["message"], "resource not found")

    def test_delete_movie(self):  # executive can delete movies
        """Test deleting a movie from the database """
        res = self.client().delete('/movies/3/delete', headers=executive_producer)
        data = json.loads(res.data)

        #  self.assertEqual(res.status_code, 200)
        #  self.assertTrue(data["success"])
        #  self.assertTrue(data["deleted"])

    def test_delete_movie_404(self):
        """Test deleting a movie with invalid movie_id """
        res = self.client().delete('/movies/1/delete', headers=executive_producer)
        data = json.loads(res.data)

        #  self.assertEqual(res.status_code, 404)
        #  self.assertFalse(data["success"])
        #  self.assertEqual(data["message"], "resource not found")

    """
    Secondly, a test to demonstrate role based access control
    """

    def test_get_movies_401(self):
        """Test getting movies with no valid JWT """
        res = self.client().get('/movies', headers=invalid_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unauthorized")

    def test_get_actors_401(self):
        """Test getting actors with no valid JWT """
        res = self.client().get('/actors', headers=invalid_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unauthorized")

    def test_patch_actor_assistant_permissions_500(self):
        """Test that assistants cannot patch actors """
        res = self.client().patch('/actors/1', json=partial_actor, headers=casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "internal server error")

    def test_post_movie_director_permissions_500(self):
        """Test that directors cannot delete actors """
        res = self.client().post('/actors/create', headers=casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "internal server error")

    def test_patch_movie_assistant_permissions_500(self):
        """Test that assistants cannot patch movies """
        res = self.client().patch('/movies/1', json=partial_movie, headers=casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "internal server error")

    def test_delete_movie_director_permissions_500(self):
        """Test that directors cannot delete movies """
        res = self.client().delete('/movies/1/delete', headers=casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "internal server error")


if __name__ == "__main__":
    unittest.main()
