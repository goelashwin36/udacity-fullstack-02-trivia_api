import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys
import string
from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin',
                             '*')

        return response

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            "status": 200,
            "message": "Hello World",
        })

    @app.route('/categories', methods=['GET'])
    def get_categories():

        try:
            categories_list = list(map(Category.format, Category.query.all()))

            if(not(categories_list)):
                abort(404)
            return jsonify({
                "status": 200,
                "success": True,
                "message": "question successfully created",
                "data": {
                    "categories": categories_list
                }
            })
        except:
            abort(422)

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        categories = list(map(Category.format, Category.query.all()))
        questions_query = Question.query.paginate(
            page, QUESTIONS_PER_PAGE, False)
        questions = list(map(Question.format, questions_query.items))
        if(len(questions) > 0):
            return jsonify({
                "code": 200,
                "success": True,
                "data": {
                    "questions": questions,
                    "total_questions": len(questions),
                    "categories": categories,
                    "current_category": None
                }
            })
        else:
            abort(404)

    @app.route('/questions/<int:ques_id>', methods=['DELETE'])
    def delete_question(ques_id):

        question = Question.query.filter(
            Question.id == ques_id).one_or_none()
        if(question is None):
            abort(404)
        Question.delete(question)
        return jsonify({
            "status": 200,
            "success": True,
            "message": "question successfully deleted"
        })

    @app.route('/questions/create', methods=['POST'])
    def create_question():

        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        try:
            # Match category id with the database. Abort if not there
            category_query = Category.query.filter(Category.id == category).one_or_none()
            if(category_query is None):
                abort(422)

            new_question = Question(question, answer, category, difficulty)
            Question.insert(new_question)
            return jsonify({
                "code": 200,
                "success": True,
                "message": "Question successfully created",
                "data": {
                    "question": Question.format(new_question)
                }
            })
        except:
            # db.session.rollback()
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_question():

        body = request.get_json()
        query = body.get('searchTerm')

        if(not(query)):
            abort(422)

        page = 1
        if request.args.get('page'):
            page = int(request.args.get('page'))

        questions_query = Question.query.filter(
            Question.question.ilike(
                '%'+query+'%')).paginate(page, QUESTIONS_PER_PAGE, False)
        questions_list = list(
            map(Question.format, questions_query.items))
        if(len(questions_list) > 0):
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Questions found",
                "data": {
                    "questions": questions_list,
                    "current_category": None,
                    "total_questions": questions_query.total
                }
            })
        abort(404)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):

        current_category = Category.query.filter(
            Category.id == category_id).one_or_none()
        page = 1
        if request.args.get('page'):
            page = int(request.args.get('page'))
        questions_query = Question.query.filter(
            Question.category == category_id).paginate(page, QUESTIONS_PER_PAGE, False)
        questions = list(map(Question.format, questions_query.items))
        if(len(questions) > 0 and current_category):
            return jsonify({
                "code": 200,
                "success": True,
                "data": {
                    "total_questions": questions_query.total,
                    "questions": questions,
                    "current_category": Category.format(current_category)
                }
            })
        else:
            abort(404)

    @app.route("/quizzes", methods=['POST'])
    def get_question_for_quiz():

        body = request.get_json()
        category = body.get('quiz_category')
        previous_questions = []
        if(body.get('previous_questions')):
            previous_questions = body.get(
                'previous_questions')  # List of Question IDs

        # Filter by category if it exists
        if("id" in category):

            if(Category.query.filter(Category.id == category['id']).one_or_none() is None):
                abort(404)
            questions_query = Question.query.filter_by(category=category['id']).filter(
                Question.id.notin_(previous_questions)).all()
            length_questions = len(questions_query)

            if(length_questions > 0):
                ques = Question.format(
                    questions_query[random.randrange(0, length_questions)])
            else:
                ques = None

        else:
            questions_query = Question.query.filter(
                Question.id.notin_(previous_questions)).all()
            length_questions = len(questions_query)

            if(length_questions > 0):
                ques = Question.format(
                    questions_query[random.randrange(0, length_questions)])
            else:
                ques = None

        return jsonify({
            "code": 200,
            "success": True,
            "data": {
                "question": ques
            }
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app
