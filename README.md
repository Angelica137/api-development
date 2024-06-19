# Trivia App

This project is a full-stack web application for the API Development and Documentation modeule of the Full Stack Nanodegree from Udacity.

The backend is built with Flask and SQLAlchemy, and the frontend is built with React. The application allows users to view questions, add new questions, search for questions, play a quiz game, and delete questions.

## Getting Started
### Prerequisites

- Python 3.7 or later
- Node.js and npm (for frontend development)

### Installing Dependencies
#### Backend Dependencies

- Create a new virtual environment:

```bash
Python -m venv env
source env/bin/activate  # on Windows, use `env\Scripts\activate`
```

- Install the required packages:

```bash
pip install -r requirements.txt
```

#### Frontend Dependencies

- Navigate to the frontend directory:

```bash
cd frontend
```

- Install the required packages:

```bash
npm install
```

### Starting the Server
#### Backend Server

From the root directory, start the backend server:

```bash
export FLASK_APP=backend/flaskr/__init__.py
export FLASK_ENV=development
flask run
```

The backend server will start running on http://localhost:5000/ by default.


#### Frontend Server

Navigate to the frontend directory:

```bash
cd frontend
```

Start the frontend server:

```bash
npm start
```

The frontend server will start running on http://localhost:3000/ by default.


## API Endpoints

### GET /categories

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key-value pairs.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

### GET /questions

- Fetches a list of questions, including pagination (every 10 questions).
- Request Arguments: page (optional, default is 1)
- Returns: An object with the following keys:
  -  success: Boolean indicating if the request was successful
  - questions: A list of question objects
  - total_questions: The total number of questions
  - categories: An object of id: category_string key-value pairs

```json
{
  "success": true,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    }
  ],
  "total_questions": 20,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

### DELETE /questions/<int:question_id>

- Deletes a question based on the provided question ID.
- Request Arguments: question_id (required)
- Returns: An object with the following keys:
  - success: Boolean indicating if the request was successful
  - deleted: The ID of the deleted question

```json
{
  "success": true,
  "deleted": 10
}
```

### POST /questions

- Creates a new question.
- Request Body:
  - question: String (required)
  - answer: String (required)
  - difficulty: Integer (required)
  - category: Integer (required)
- Returns: An object with the following keys:
  - success: Boolean indicating if the request was successful
  - created: The question text of the created question
  - question_id: The ID of the created question

```json
{
  "success": true,
  "created": "What is the capital of France?",
  "question_id": 25
}
```

### POST /questions/search

- Searches for questions based on a search term.
- Request Body:
  - searchTerm: String (required)
- Returns: An object with the following keys:
  - success: Boolean indicating if the request was successful
  - questions: A list of question objects that match the search term
  - total_questions: The total number of questions that match the search term
  - current_category: The category of the questions (if applicable)

```json
{
  "success": true,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "total_questions": 1,
  "current_category": null
}
```

### GET /categories/<int:category_id>/questions

- Fetches questions for a specific category.
- Request Arguments: category_id (required)
- Returns: An object with the following keys:
  - success: Boolean indicating if the request was successful
  - questions: A list of question objects for the specified category
  - total_questions: The total number of questions for the specified category
  - current_category: The name of the current category

```json
{
  "success": true,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    }
  ],
  "total_questions": 2,
  "current_category": "History"
}
```

### POST /quizzes
- Fetches a random question for the quiz game, excluding previously displayed questions.
- Request Body:
  - quiz_category: An object with the following keys:
    - type: String (required, either a category type or 'All')
    - id: Integer (required, the category ID, or 0 for 'All')
  - previous_questions: A list of question IDs (required)
- Returns: An object with the following keys:
  - success: Boolean indicating if the request was successful
  - question: A random question object (if available)

```json
{
  "success": true,
  "question": {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  }
}
