# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Endpoints

### GET /categories

- Description: Fetches the list of categories

- Parameters: None

- Returns: List of Categories. Every category is represented as a dictionary with keys `id` and `type`

- Sample Response

```
{
  "data": {
    "categories": [
      {
        "id": 1,
        "type": "Science"
      },
      {
        "id": 2,
        "type": "Art"
      },
      {
        "id": 3,
        "type": "Geography"
      }
    ]
  },
  "message": "question successfully created",
  "status": 200,
  "success": true
}
```

### GET /questions?page=<page_number>

- Description: Fetches the list of categories and questions

- Parameters: page_number

- Returns: List of categories and questions which are paginated(10 per page) according to the page number(default=1)

- Sample Response

```
{
  "code": 200,
  "data": {
    "categories": [
      {
        "id": 1,
        "type": "Science"
      },
      {
        "id": 2,
        "type": "Art"
      },
      {
        "id": 3,
        "type": "Geography"
      }
    ],
    "current_category": null,
    "questions": [
      {
        "answer": "Muhammad Ali",
        "category": 1,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
      },
      {
        "answer": "Apollo 13",
        "category": 3,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      }
    ],
    "total_questions": 2
  },
  "success": true
}
```

### DELETE /questions/<int:question_id>

- Description: Deletes question with the given question_id

- Parameters: question_id

- Returns: True if question is successfully deleted

- Sample Response

```
{
  "message": "question successfully deleted",
  "status": 200,
  "success": true
}
```

### POST /questions/create

- Description: Creates a new question

- Parameters: question, answer, category, difficulty

- Returns: True along with the question if it is successfully created

- Sample Request Body

```
{
    "question": "Is this a new question?",
    "answer": "Yes it is!!",
    "category": 2,
    "difficulty": 4
}
```

- Sample Response

```
{
  "code": 200,
  "data": {
    "question": {
      "answer": "Yes it is!!",
      "category": 2,
      "difficulty": 4,
      "id": 35,
      "question": "Is this a new question?"
    }
  },
  "message": "Question successfully created",
  "success": true
}
```

### POST /questions/search

- Description: Performs a case insensitive search on all the questions. The questions are paginated(10 per page) according to the page number(default=1)

- Parameters: searchTerm, page

- Returns: List of questions that matches the searchTerm

- Sample Request Body

```
{
    "searchTerm": "What is"
}
```

- Sample Response

```
{
  "data": {
    "current_category": null,
    "questions": [
      {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
      },
      {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
      }
    ],
    "total_questions": 2
  },
  "message": "Questions found",
  "status": 200,
  "success": true
}
```

### GET /categories/<int:category_id>/questions

- Description: Fetches a list of questions having the given category. The questions are paginated(10 per page) according to the page number(default=1)

- Parameters: category_id, page

- Returns: List of questions, total_questions, current_category

- Sample Response

```
{
  "code": 200,
  "data": {
    "current_category": {
      "id": 3,
      "type": "Geography"
    },
    "questions": [
      {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
      },
      {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
      }
    ],
    "total_questions": 2
  },
  "success": true
}
```

### POST /quizzes

- Description: Get questions to play the quiz

- Parameters: quiz_category, previous_questions

- Returns: A random question which belongs to the quiz_category and is not in previous_questions

- Sample Request Body

```
{
    "quiz_category": {
        "id": 3,
        "Type": "Geography"
    },
    "previous_questions": [
        13
    ]
}
```

- Sample Response

```
{
  "code": 200,
  "data": {
    "question": {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  },
  "success": true
}
```