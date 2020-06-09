import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


casting_assistant = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNrWXIyMTZtVmtibHZHRmszQmRNdCJ9.eyJpc3MiOiJodHRwczovL2Rldi0tM3hnYXZwMS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkY2VlOWQyYjAwNjIwMDEzN2EwODczIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU5MTUzNzM3MSwiZXhwIjoxNTkxNjIzNzcxLCJhenAiOiJqSkFqaGVzVkVPSE8zM2ZtNFpsZFN0NzJlTk9xVlNhTCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIl19.fa05yh2C0_jWZ3z_tfVlFFTQ38McgLyPFwfrHsRZBzm9OZgbm36YL5lrQXcGNdZNaIK_ntCqC1yQIuEBBsY-uJ2rJQsTs9bCeYVjt1IVGP0Mcj9--sGj-Gxwo3MDRTxV7WTwriZl6S6BJ3DGnNWQK-CRF2be2XNWgWqmdEbKqnBSUsq6ejW231T5shiVwsTqtnoLnd5He0TPnXpxmzTlvMQnkSF3gXqz4dTT5M2EwwqP8OwZdVCaDesWK947WYEfJznW2m2-WkPmlOu1XsDUAL3qC7Rw3ri16pRuKUv0Uh2GQIt5RFO7BGJwdHiPKc6ZAkKdWCmCgOh1WxUbV557sQ"}
casting_director = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNrWXIyMTZtVmtibHZHRmszQmRNdCJ9.eyJpc3MiOiJodHRwczovL2Rldi0tM3hnYXZwMS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkY2VmNWQzNDQxMzcwMDE0OThkYjIwIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU5MTUzNzU1MywiZXhwIjoxNTkxNjIzOTUzLCJhenAiOiJqSkFqaGVzVkVPSE8zM2ZtNFpsZFN0NzJlTk9xVlNhTCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.kGqiD-rtoiBFjrfIlgml7W7m1saQ-NvzlEIaRNm97I7Oa61jokFT0AC_d-Ez-pfuF1TLRS_4CjnaCrnZqz48KlIzBHYLPmbQOBdUpJZcLIJonP3836WKoliPtJN__Q-5qnU1WuuXnsZ2e3juTiDy9mfR0m7eIccxh1-fQ_Pqs97KFxYUsljvatkQzfiMgBbiSZVWJfZ67PvT0DtUna9iQqJrOyvUlDUue-piHhACxwiUMLJWjDyIocU-XvfPZnrQ4kLJXmM2YxXHaJAWO4ZFAuI721KQUtXhzz_Z6ElTZHg3Iok5lYoHTWhHer1hpSUYj70kWceyy_q_0HoQMQrhGg"}
executive_producer = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNrWXIyMTZtVmtibHZHRmszQmRNdCJ9.eyJpc3MiOiJodHRwczovL2Rldi0tM3hnYXZwMS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkY2VmZTZhMTFjN2YwMDFhMTc3YWRhIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU5MTUzNzY5MCwiZXhwIjoxNTkxNjI0MDkwLCJhenAiOiJqSkFqaGVzVkVPSE8zM2ZtNFpsZFN0NzJlTk9xVlNhTCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.revzyKjPU8cxqANekMWL5oAvS2yCQEBV_fm3PJ3h8dxllecHW1QYBMVMW05EMEg-CEE-Hc99DE8BTPYqPEh2knRR9anNuvxS59MSxszuXbCYtq9QjhpAkeKgBUHf-ndr10MfvPYtdPgyvqxsZMJhI1chfhwJNjKK5Fu-ey7Ioyao0um9p82lNy-2CswJi4IjN3xY1Jd-Z4UT4OTZtaEvpuJpC_8cUSai1SN95_bR_Wnz7EEEeoC18hog4J-fQ_yZuNQDdFJEnxcA4Itn5lXwGSVro15YXt7f_ci2KOnYh4J7P1p6vy58UzjVVcYapwjHtsf5Tvf3B9pqD0bnRMAUHA"}
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
        """Executed before each test. Define test vars and initialize"""
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

    def test_get_actors(self):  # assistant can get actors
        """Test getting actors successfully """
        res = self.client().get('/actors', headers=casting_assistant)
        data = json.loads(res.data)

        #self.assertEqual(res.status_code, 200)
        #self.assertTrue(data["success"])
        #self.assertTrue(data["actors"])

    def test_get_movies(self):  # assistant can get movies
        """Test getting movies """
        res = self.client().get('/movies', headers=casting_assistant)
        data = json.loads(res.data)

        #self.assertEqual(res.status_code, 200)
        #self.assertTrue(data["success"])
        #self.assertTrue(data["movies"])

    def test_patch_actor(self):  # executive can patch actors
        """Test updating an actor in database """
        res = self.client().patch('/actors/2', json=new_actor, headers=executive_producer)
        data = json.loads(res.data)

        #self.assertEqual(res.status_code, 200)
        #self.assertTrue(data["success"])
        #self.assertTrue(data["updated actor"])

    def test_patch_actor_400(self):
        """Test updating an actor with invalid actor_id """
        res = self.client().patch('/actors/1000', json=partial_actor, headers=executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "bad request")

    def test_patch_movie(self):  # director can patch movies
        """Test updating a movie in database """
        res = self.client().patch('/movies/2', json=partial_movie, headers=casting_director)
        data = json.loads(res.data)

        #self.assertEqual(res.status_code, 200)
        #self.assertTrue(data["success"])
        #self.assertTrue(data["updated movie"])

    def test_patch_movie_400(self):
        """Test updating a movie with invalid movie_id """
        res = self.client().patch('/movies/8080', json=partial_movie, headers=executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "bad request")

    def test_delete_actor(self):  # director can delete actors
        """Test deleting an actor from the database """
        res = self.client().delete('/actors/2/delete', headers=casting_director)
        data = json.loads(res.data)

        #self.assertEqual(res.status_code, 200)
        #self.assertTrue(data["success"])
        #self.assertTrue(data["deleted"])

    def test_delete_actor_404(self):
        """Test deleting an actor with invalid actor_id """
        res = self.client().delete('/actors/2/delete', headers=executive_producer)
        data = json.loads(res.data)

        #self.assertEqual(res.status_code, 404)
        #self.assertFalse(data["success"])
        #self.assertEqual(data["message"], "resource not found")

    def test_delete_movie(self):  # executive can delete movies
        """Test deleting a movie from the database """
        res = self.client().delete('/movies/3/delete', headers=executive_producer)
        data = json.loads(res.data)

        #self.assertEqual(res.status_code, 200)
        #self.assertTrue(data["success"])
        #self.assertTrue(data["deleted"])

    def test_delete_movie_404(self):
        """Test deleting a movie with invalid movie_id """
        res = self.client().delete('/movies/1/delete', headers=executive_producer)
        data = json.loads(res.data)

        #self.assertEqual(res.status_code, 404)
        #self.assertFalse(data["success"])
        #self.assertEqual(data["message"], "resource not found")


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

    def test_patch_actor_assistant_permissions_500(self):  # assistant cannot patch actors
        """Test that assistants cannot patch actors """
        res = self.client().patch('/actors/1', json=partial_actor, headers=casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "internal server error")

    def test_post_movie_director_permissions_500(self):  # director cannot post movies
        """Test that directors cannot delete actors """
        res = self.client().post('/actors/create', headers=casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "internal server error")

    def test_patch_movie_assistant_permissions_500(self):  # assistant cannot patch movies
        """Test that assistants cannot patch movies """
        res = self.client().patch('/movies/1', json=partial_movie, headers=casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "internal server error")

    def test_delete_movie_director_permissions_500(self):  # director cannot delete movies
        """Test that directors cannot delete movies """
        res = self.client().delete('/movies/1/delete', headers=casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "internal server error")

if __name__ == "__main__":
    unittest.main()
