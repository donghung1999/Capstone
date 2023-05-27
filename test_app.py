import os
import unittest
import json
from app import create_app

CASTING_ASSISTANT_ACCESS_TOKEN = os.getenv('CASTING_ASSISTANT_ACCESS_TOKEN')
CASTING_DIRECTOR_ACCESS_TOKEN = os.getenv('CASTING_DIRECTOR_ACCESS_TOKEN')
EXECUTIVE_PRODUCER_ACCESS_TOKEN = os.getenv('EXECUTIVE_PRODUCER_ACCESS_TOKEN')

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.casting_assistant_access_token = CASTING_ASSISTANT_ACCESS_TOKEN
        self.casting_director_access_token = CASTING_DIRECTOR_ACCESS_TOKEN
        self.executive_producer_access_token = EXECUTIVE_PRODUCER_ACCESS_TOKEN
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test get Movies

    def testGetMoviesFromDataBaseWithSuccess(self):
        responseFromApi = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer {}".format(self.casting_assistant_access_token)}
        )
        print(json.loads(responseFromApi.data))
        self.assertEqual(json.loads(responseFromApi.data)['success'], True)
    
    def testGetMoviesFromDataBaseWithError(self):
        responseFromApi = self.client().get('/movies',
            headers={"Authorization": "Bearer"})
        self.assertFalse(json.loads(responseFromApi.data)['success'])
        self.assertEqual(responseFromApi.status_code, 401)

    # # Test create Movies

    def testCreateNewMovieInDatabaseWithSuccess1(self):
        responseFromApi = self.client().post('/movies',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.executive_producer_access_token)
                                }, json={
                                    "title": "Mui co chay",
                                    "release_date": "2022-12-04",
                                })
        self.assertEqual(responseFromApi.status_code, 200)
        self.assertTrue(json.loads(responseFromApi.data)['success'])
        self.assertTrue(len(json.loads(responseFromApi.data)['movies']))

    def testCreateNewMovieInDatabaseWithSuccess2(self):
        responseFromApi = self.client().post('/movies',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.executive_producer_access_token)
                                }, json={
                                    "title": "Mui co chay Phan 2",
                                    "release_date": "2022-12-04",
                                })
        self.assertEqual(responseFromApi.status_code, 200)
        self.assertTrue(json.loads(responseFromApi.data)['success'])
        self.assertTrue(len(json.loads(responseFromApi.data)['movies']))

    def testCreateNewMovieInDatabaseWithError1(self):
        movieObject = {}
        responseFromApi = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.executive_producer_access_token)
                                 }, json=movieObject)
        self.assertFalse(json.loads(responseFromApi.data)['success'])
        self.assertEqual(responseFromApi.status_code, 400)

    def testCreateNewMovieInDatabaseWithError2(self):
        responseFromApi = self.client().post('/movies',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_assistant_access_token)
                                }, json={
                                    "title": "Mui co chay",
                                    "release_date": "2022-12-04",
                                })
        self.assertFalse(json.loads(responseFromApi.data)['success'])
        self.assertEqual(responseFromApi.status_code, 403)

    # Test update Movies

    def testUpdateExistMovieInDatabaseWithSuccess(self):
        responseFromApi = self.client().patch('/movies/2',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.executive_producer_access_token)
                                }, json={
                                    "title": "Mui co chay 1",
                                    "release_date": "2022-12-04",
                                })
        self.assertTrue(json.loads(responseFromApi.data)['success'])
        self.assertEqual(200, responseFromApi.status_code)

    def testUpdateExistMovieInDatabaseWithError1(self):
        responseFromApi = self.client().patch('/movies/999999',
                                 headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_director_access_token)
                                }, json={
                                    "title": "Mui co chay",
                                    "release_date": "2022-12-04",
                                })
        self.assertFalse(json.loads(responseFromApi.data)['success'])
        self.assertEqual(404, responseFromApi.status_code)

    def testUpdateExistMovieInDatabaseWithError2(self):
        responseFromApi = self.client().patch('/movies/2',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_assistant_access_token)
                                }, json={
                                    "title": "Mui co chay",
                                    "release_date": "2022-12-04",
                                })
        self.assertFalse(json.loads(responseFromApi.data)['success'])
        self.assertEqual(403, responseFromApi.status_code)

    # Test delete Movies

    def testDeleteMovieInDatabaseWithSuccess(self):
        responseFromApi = self.client().delete('/movies/1',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.executive_producer_access_token)
                                })
        self.assertTrue(json.loads(responseFromApi.data)['success'])
        self.assertEqual(json.loads(responseFromApi.data)['delete'], '1')
        self.assertEqual(200, responseFromApi.status_code)

    def testDeleteMovieInDatabaseWithError1(self):
        responseFromApi = self.client().delete('/movies/999999',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.executive_producer_access_token)
                                })
        self.assertFalse(json.loads(responseFromApi.data)['success'])
        self.assertEqual(404, responseFromApi.status_code)

    def testDeleteMovieInDatabaseWithError2(self):
        responseFromApi = self.client().delete('/movies/0',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_assistant_access_token)
                                })
        self.assertFalse(json.loads(responseFromApi.data)['success'])
        self.assertEqual(403, responseFromApi.status_code)

    # Test get Actors
    def testGetActorsFromDataBaseWithSuccess(self):
        responseFromApi = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer {}".format(self.casting_assistant_access_token)}
        )
        self.assertEqual(json.loads(responseFromApi.data)['success'], True)

    def testGetActorsFromDataBaseWithError1(self):
        responseFromApi = self.client().get('/actors')
        self.assertFalse(json.loads(responseFromApi.data)['success'])
        self.assertEqual(401, responseFromApi.status_code)

    # Test post Actors

    def testCreateNewActorsInDatabaseWithSuccess1(self):
        responseFromApi = self.client().post('/actors',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_director_access_token)
                                }, json={
                                    "name": "Dong Hung 01",
                                    "gender": "male",
                                    "age": 24,
                                })
        self.assertEqual(responseFromApi.status_code, 200)
        self.assertTrue(json.loads(responseFromApi.data)['success'])
        self.assertTrue(len(json.loads(responseFromApi.data)['actors']))

    def testCreateNewActorsInDatabaseWithSuccess2(self):
        responseFromApi = self.client().post('/actors',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.executive_producer_access_token)
                                }, json={
                                    "name": "Dong Hung 02",
                                    "gender": "male",
                                    "age": 24,
                                })
        self.assertEqual(responseFromApi.status_code, 200)
        self.assertTrue(json.loads(responseFromApi.data)['success'])
        self.assertTrue(len(json.loads(responseFromApi.data)['actors']))
    
    def testCreateNewActorsInDatabaseWithError1(self):
        responseFromApi = self.client().post('/actors',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_assistant_access_token)
                                }, json={
                                    "name": "Dong Hung",
                                    "gender": "male",
                                    "age": 24,
                                })
        self.assertFalse(json.loads(responseFromApi.data)['success'])
        self.assertEqual(responseFromApi.status_code, 403)

    def testCreateNewActorsInDatabaseWithError2(self):
        responseFromApi = self.client().post('/actors',
                                headers={
                                    "Authorization": "Bearer"
                                }, json={
                                    "name": "Dong Hung",
                                    "gender": "male",
                                    "age": 24,
                                })
        self.assertFalse(json.loads(responseFromApi.data)['success'])
        self.assertEqual(responseFromApi.status_code, 401)

    # Test update Actors

    def testUpdateExistActorsInDatabaseWithSuccess(self):
        responseFromApi = self.client().patch('/actors/2',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.executive_producer_access_token)
                                }, json={
                                    "name": "Dong Hung",
                                    "gender": "male",
                                    "age": 24,
                                })
        self.assertTrue(json.loads(responseFromApi.data)['success'])
        self.assertEqual(200, responseFromApi.status_code)

    def testUpdateExistActorsInDatabaseWithError1(self):
        responseFromApi = self.client().patch('/actors/2',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_assistant_access_token)
                                }, json= {
                                    "name": "Dong Hung",
                                    "gender": "male",
                                    "age": 24,
                                })
        self.assertFalse(json.loads(responseFromApi.data)['success'])
        self.assertEqual(responseFromApi.status_code, 403)

    def testUpdateExistActorsInDatabaseWithError2(self):
        responseFromApi = self.client().patch('/actors/2',
                                headers={
                                    "Authorization": "Bearer"
                                }, json={
                                    "name": "Dong Hung",
                                    "gender": "male",
                                    "age": 24,
                                })
        self.assertFalse(json.loads(responseFromApi.data)['success'])
        self.assertEqual(responseFromApi.status_code, 401)

    # Test delete Actors

    def testDeleteActorsInDatabaseWithSuccess(self):
        responseFromApi = self.client().delete('/actors/1',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_director_access_token)
                                })
        self.assertTrue(json.loads(responseFromApi.data)['success'])
        self.assertEqual(json.loads(responseFromApi.data)['delete'], '1')
        self.assertEqual(200, responseFromApi.status_code)

    def testDeleteActorsInDatabaseWithError1(self):
        responseFromApi = self.client().delete('/actors/9999',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_director_access_token)
                                })
        self.assertFalse(json.loads(responseFromApi.data)['success'])
        self.assertEqual(responseFromApi.status_code, 404)

    def testDeleteActorsInDatabaseWithError2(self):
        responseFromApi = self.client().delete('/actors/1',
                                headers={
                                    "Authorization": "Bearer"
                                })
        self.assertFalse(json.loads(responseFromApi.data)['success'])
        self.assertEqual(responseFromApi.status_code, 401)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()