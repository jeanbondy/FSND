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
        self.database_path = "postgresql://postgres@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'What time is it',
            'answer': 'too late',
            'category': 1,
            'difficulty': 1
        }

        self.search_term = {'searchTerm': 'hank'}

        self.quizzes = {'previous_questions': [13,14],
                        'quiz_category': {'type': 'click',
                                          'id': 0}
                        }
    
    def tearDown(self):
        """Executed after each test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_quizzes(self):
        res = self.client().post('/quizzes', json=self.quizzes)
        data = json.loads(res.data)
        print(f'res data is {data}')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_400_quizzes_malformed(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)
        print(f'res data is {data}')

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


# working tests
'''
        def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['currentCategory'])

    def test_404_get_paginated_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_post_new_question_malformed(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


    def test_search_question(self):
        res = self.client().post('/questions', json=self.search_term)
        data = json.loads(res.data)

        print(res.status_code)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])

    def test_delete_question(self):
        res = self.client().delete('/questions/11')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'resource deleted')
        
    def test_404_delete_missing_question(self):
        res = self.client().delete('/questions/11')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['currentCategory'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])

    def test_404_questions_by_category(self):
        res = self.client().get('/categories/95/questions')
        data = json.loads(res.data)

        print(f'res data is {data}')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        


'''
