import os
import logging
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    print("Creating Falsk app...")
    app = Flask(__name__)
    logging.basicConfig(level=logging.DEBUG)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after
    completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow - DONE
    """
    @app.after_request  # used to modify the response object before it is sent to the client
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Cntrol-Allow-Headers",
            "Content-Type,Authorization")
        response.headers.add(
            "Access-Control-ALlow-Methods",
            "GET,PUT,POST,DELETE,OPTIONS")
        return response

    @app.route('/')
    def index():
        urls = {}
        for rule in app.url_map.iter_rules():
            urls[rule.rule] = list(rule.methods)
        return jsonify(urls)

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            categories_dict = {
                category.id: category.type for category in categories
            }

            return jsonify({
                'success': True,
                'categories': categories_dict
            })
        except Exception as e:
            print(e)
            return jsonify({
                'success': False,
                'error': 500,
                'message': 'An error occured while fetching categories.'
            }), 500

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for
    three pages. Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET', 'POST'])
    def questions():
        if request.method == 'GET':
            page = request.args.get('page', 1, type=int)
            questions = Question.query.paginate(page, per_page=10, error_out=False)

            try:
                formatted_questions = [question.format() for question in questions.items]
                categories = {category.id: category.type for category in Category.query.all()}

                return jsonify({
                    'success': True,
                    'questions': formatted_questions,
                    'total_questions': questions.total,
                    'categories': categories
                })
            except Exception as e:
                print(e)
                return jsonify({
                    'success': False,
                    'error': 500,
                    'message': 'An error occurred while fetching the questions'
                }), 500

        elif request.method == 'POST':
            try:
                data = request.get_json()

                if not data:
                    abort(400, 'Request body cannot be empty')

                question = data.get('question', None)
                answer = data.get('answer', None)
                difficulty = data.get('difficulty', None)
                category = data.get('category', None)

                if not all([question, answer, difficulty, category]):
                    abort(422, 'Request data is incomplete')

                new_question = Question(
                    question=question,
                    answer=answer,
                    difficulty=difficulty,
                    category=category,
                )

                db.session.add(new_question)
                db.session.commit()

                return jsonify({
                    'success': True,
                    'created': new_question.question,
                    'question_id': new_question.id
                }), 201

            except Exception as e:
                db.session.rollback()
                print(f'error: {e}')
                abort(500, 'An error occurred while creating the question.')
            finally:
                db.session.close()

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['GET', 'DELETE'])
    def delete_question(question_id):
        if request.method == 'GET':
            question = Question.query.get(question_id)
            if not question:
                return jsonify({
                    'success': False,
                    'error': 404,
                    'message': 'Question not found'
                }), 404

        elif request.method == 'DELETE':
            try:
                question = Question.query.get(question_id)
                if not question:
                    return jsonify({
                        'success': False,
                        'error': 404,
                        'message': 'Question not found'
                    }), 404

                db.session.delete(question)
                db.session.commit()

                return jsonify({
                    'success': True,
                    'deleted': question_id
                }), 200
            except Exception as e:
                db.session.rollback()
                print(e)
                return jsonify({
                    'success': False,
                    'error': 500,
                    'message': 'An error occurred while deleting the question.'
                }), 500
            finally:
                db.session.close()

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last
    page of the questions list in the "List" tab.

    This was added to /questions
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            data = request.get_json()
            search_term = data.get('searchTerm', '')

            questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')
            ).all()
            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(questions)
            }), 200

        except Exception as e:
            print(f'Error: {e}')
            abort(500, 'An error occured while searching for quesions.')

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            abort(404, 'Category not found')

        questions = Question.query.filter(
            Question.category == category_id).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'current_category': category.type
        }), 200

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            data = request.get_json()
            quiz_category = data.get('quiz_category')
            previous_questions = data.get('previous_questions', [])

            if quiz_category['type'] == 'All':
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)
                ).all()
            else:
                questions = Question.query.filter(
                    Question.category == quiz_category['id'],
                    Question.id.notin_(previous_questions)
                ).all()

            if len(questions) > 0:
                question = random.choice(questions).format()
            else:
                question = None

            return jsonify({
                'success': True,
                'question': question
            }), 200

        except Exception as e:
            print(f'Error: {e}')
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    for rule in app.url_map.iter_rules():
        print(rule)

    print("Flask app created successfully")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
