import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import and_
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # @TODO: Set up CORS. Allow ' * ' for origins. Delete the sample route after completing the TODOs
    CORS(app, resources={r"*": {"origins": "*"}})

    # @TODO: Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, DELETE')
        return response

    # @TODO: Create an endpoint to handle GET requests for all available categories.

    @app.route('/categories', methods=['GET'])
    def categories():
        categories_query = Category.query.all()
        categories = {}
        for category in categories_query:
            categories[category.id] = category.type
        return jsonify({'categories': categories})

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  '''

    @app.route('/questions', methods=['GET'])
    def questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        questions_query = Question.query.all()
        questions = [question.format() for question in questions_query]
        categories_query = Category.query.all()
        categories = {}
        for category in categories_query:
            categories[category.id] = category.type
        # todo: how to get current category?
        return jsonify({
            'currentCategory': 'History',
            'totalQuestions': len(questions_query),
            'categories': categories,
            'questions': questions[start:end]
        })
    '''
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter_by(id=question_id).one_or_none()
        if question is None:
            abort(404)
        else:
            try:
                #Question.delete(question)
                return jsonify({'message': 'success'})
            except:
                pass
            finally:
                pass

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    @app.route('/questions', methods=['POST'])
    def search_questions():
        request_body = request.get_json()
        new_question = Question(question=request_body['question'],
                                answer=request_body['answer'],
                                category=request_body['category'],
                                difficulty=request_body['difficulty'])
        new_question.insert()
        return jsonify({
            'message': 'looks good'
        })
    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @app.route('/questions', methods=['POST'])
    def search_questions():
        request_body = request.get_json()
        search_term = (request_body['searchTerm'])
        questions_query = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
        questions = [question.format() for question in questions_query]
        return jsonify({
            'totalQuestions': len(questions_query),
            'questions': questions
        })
    '''
    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def questions_by_category(category_id):
        questions_query = Question.query.filter_by(category=category_id).all()
        category = Category.query.filter_by(id=category_id).one_or_none()
        if category is None:
            abort(404)
        else:
            questions = [question.format() for question in questions_query]
            return jsonify({
                'currentCategory': category.type,
                'totalQuestions': len(questions_query),
                'questions': questions
            })


    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
    
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        request_body = request.get_json()
        previous_questions = request_body['previous_questions']
        quiz_category = request_body['quiz_category']
        quizzes_query = Question.query.filter(and_(~Question.id.in_(previous_questions)), Question.category==quiz_category)
        all_questions = [question.format() for question in quizzes_query]
        all_question_ids = [question.id for question in quizzes_query]
        random_pick = random.randrange(len(all_question_ids))
        random_question = all_questions[random_pick]
        return jsonify({
            'question': random_question
        })

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
