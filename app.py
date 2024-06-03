# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return render_template('index.html', recipes=recipes)

@app.route('/add', methods=('GET', 'POST'))
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        instructions = request.form['instructions']
        category = request.form['category']
        ingredients = request.form.getlist('ingredients')
        quantities = request.form.getlist('quantities')

        conn = get_db_connection()
        
        conn.execute('''
        INSERT OR IGNORE INTO categories (name) VALUES (?)
        ''', (category,))
        
        category_id = conn.execute('''
        SELECT id FROM categories WHERE name = ?
        ''', (category,)).fetchone()[0]
        
        conn.execute('''
        INSERT INTO recipes (title, instructions, category_id) VALUES (?, ?, ?)
        ''', (title, instructions, category_id))
        
        recipe_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

        for name, quantity in zip(ingredients, quantities):
            conn.execute('''
            INSERT INTO ingredients (recipe_id, name, quantity) VALUES (?, ?, ?)
            ''', (recipe_id, name, quantity))
        
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_recipe.html')

@app.route('/edit/<int:recipe_id>', methods=('GET', 'POST'))
def edit_recipe(recipe_id):
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
    ingredients = conn.execute('SELECT * FROM ingredients WHERE recipe_id = ?', (recipe_id,)).fetchall()
    category = conn.execute('SELECT name FROM categories WHERE id = ?', (recipe['category_id'],)).fetchone()['name']
    
    if request.method == 'POST':
        title = request.form['title']
        instructions = request.form['instructions']
        category = request.form['category']
        ingredient_names = request.form.getlist('ingredients')
        quantities = request.form.getlist('quantities')

        conn.execute('''
        INSERT OR IGNORE INTO categories (name) VALUES (?)
        ''', (category,))
        
        category_id = conn.execute('SELECT id FROM categories WHERE name = ?', (category,)).fetchone()[0]

        conn.execute('UPDATE recipes SET title = ?, instructions = ?, category_id = ? WHERE id = ?',
                     (title, instructions, category_id, recipe_id))
        
        conn.execute('DELETE FROM ingredients WHERE recipe_id = ?', (recipe_id,))
        
        for name, quantity in zip(ingredient_names, quantities):
            conn.execute('INSERT INTO ingredients (recipe_id, name, quantity) VALUES (?, ?, ?)',
                         (recipe_id, name, quantity))
        
        conn.commit()
        conn.close()
        return redirect(url_for('recipe', recipe_id=recipe_id))
    
    conn.close()
    return render_template('edit_recipe.html', recipe=recipe, ingredients=ingredients, category=category)

@app.route('/delete/<int:recipe_id>', methods=('POST',))
def delete_recipe(recipe_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM ingredients WHERE recipe_id = ?', (recipe_id,))
    conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
    ingredients = conn.execute('SELECT * FROM ingredients WHERE recipe_id = ?', (recipe_id,)).fetchall()
    category = conn.execute('SELECT name FROM categories WHERE id = ?', (recipe['category_id'],)).fetchone()['name']
    conn.close()
    return render_template('recipe.html', recipe=recipe, ingredients=ingredients, category=category)

if __name__ == '__main__':
    app.run(debug=True)
