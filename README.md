# Recipe-Database
- A simple application to demonstrate the use of Flask and SQLlite3 libraries in Python.

## Features:
- Add new recipes with ingredients and instructions
- Edit existing recipes
- Delete recipes
- View a list of all recipes
- View details of a specific recipe

## Requirements:
```
Flask, Python 3.x (my version is 3.1x)
```

## Clone the repository
```
git clone [repo_url]
cd recipe-database
```

## Create a virtual environment
```
python -m venv recipe_env
recipe_env\Scripts\activate
```
- Or
Use ``` source venv/bin/activate ```

## Install requirements
```
pip install flask
```

## Usage
1. Initialize the database
```
python init_db.py
```

2. Run the Flask application
```
python app.py
```
3. Open your web browser and go to `http://127.0.0.1:5000/`.

4. Using the interface:
- To add a new recipe, click on "Add a new recipe" on the home page.
- To view a recipe, click on the recipe title on the home page.
- To edit a recipe, click on "Edit" on the recipe detail page.
- To delete a recipe, click on "Delete" on the recipe detail page.

5. Then press Ctrl+C in your Command Prompt/Terminal to terminate the local server.

