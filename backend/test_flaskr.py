import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'ash', 'ashsha', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["data"]["categories"]))

    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data']['questions'], True)
        self.assertTrue(data['data']['total_questions'], True)
        self.assertTrue(data['data']['categories'], True)

    def test_404_get_paginated_questions(self):
        res = self.client().get('/questions?page=99999999999999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "resource not found")

    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'], "question successfully deleted")

    def test_404_delete_question(self):
        res = self.client().delete('/questions/89736452')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "resource not found")

    def test_create_questions(self):
        res = self.client().post('/questions/create', json={
            "question": "New question",
            "answer": "New answer",
            "category": 2,
            "difficulty": 4
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data']['question'], True)

    def test_422_create_questions(self):
        res = self.client().post('/questions/create', json={
            "question": "New question",
            "answer": "New answer",
            "category": 4398593475345,
            "difficulty": 3
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "unprocessable")

    def test_search_questions(self):
        res = self.client().post('/questions/search', json={
            "searchTerm": "what"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data']['questions'], True)
        self.assertTrue(data['data']['total_questions'], True)

    def test_422_search_questions(self):
        res = self.client().post('/questions/search', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "unprocessable")

    def test_404_search_questions(self):
        res = self.client().post('/questions/search',
                                 json={"searchTerm": "reghbusbgosuybgagagig"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "resource not found")

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data']['questions'], True)
        self.assertTrue(data['data']['total_questions'], True)
        self.assertTrue(data['data']['current_category'], True)

    def test_404_get_questions_by_category(self):
        res = self.client().get('/categories/3894759347693/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "resource not found")

    def test_get_questions_for_quiz(self):
        res = self.client().post('/quizzes', json={
            "quiz_category": {"id":2},
            "previous_questions": [17,18,19]
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data']['question'], True)

    def test_404_get_questions_for_quiz(self):
        res = self.client().post('/quizzes', json={
            "quiz_category": {"id":298346598346},
            "previous_questions": [12]
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "resource not found")




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
