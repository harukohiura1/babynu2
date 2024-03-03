from flaskr import app
from flask import render_template, request, jsonify, redirect, url_for
import sqlite3
DATABASE = 'database.db'

@app.route('/')
def today():
    con = sqlite3.connect(DATABASE)
    db_foods = con.execute('SELECT * FROM foods').fetchall()
    con.close()

    foods = []
    for row in db_foods:
        foods.append({'id':row[0], 'name':row[1], 'protein':row[2], 'fat':row[3], 'carbohydrate':row[4]})

    # レーダーチャートのデータ
    title = row[1]
    labels = ['protein', 'fat', 'carbohydrate']
    values = [row[2], row[3], row[4]]

    return render_template(
        'today.html',
        foods = foods, title=title, labels=labels, values=values
    )

@app.route('/meal')
def meal():
    dish_id = []
    dish_name = []
    con = sqlite3.connect(DATABASE)
    db_meals = con.execute('SELECT * FROM dishes').fetchall()
    combined_list = zip(dish_id, dish_name)

    for row in db_meals:
        dish_id.append(row[0])
        dish_name.append(row[1])

    return render_template(
        'meal.html', combined_list=combined_list
    )

@app.route('/dish/<dish_id>')
def dish(dish_id):
    con = sqlite3.connect(DATABASE)
    db_dishes = con.execute('SELECT * FROM dishes WHERE dish_id =?', (int(dish_id),)).fetchone()
    db_foods_dishes = con.execute('SELECT * FROM foods_dishes WHERE dish_id =?', (int(dish_id),)).fetchall()
    dishes_name = db_dishes[1]

    ingredients = []
    total_protein = 0
    total_fat = 0
    total_carbohydrate = 0
    for sublist in db_foods_dishes:
        foods_dishes_food_id = sublist[2]
        db_foods = con.execute('SELECT * FROM foods WHERE food_id =?', (int(foods_dishes_food_id),)).fetchall()
        foods_name = db_foods[0][1]
        ingredients.append(foods_name)
        protein = db_foods[0][2]
        fat = db_foods[0][3]
        carbohydrate = db_foods[0][4]
        total_protein += protein
        total_fat += fat
        total_carbohydrate += carbohydrate
    con.close()

    title = dishes_name
    labels = ['protein', 'fat', 'carbohydrate']
    values_int = [total_protein, total_fat, total_carbohydrate]
    values = [str(value) for value in values_int]

    return render_template(
        'dish.html',
        ingredients = ingredients, title = title, labels = labels, values = values
    )

@app.route('/food_form')
def food_form():
    return render_template(
        'food_form.html'
    )

@app.route('/food_form_register', methods=['POST'])
def food_form_register():
    food_name = request.form['food_name']
    protein = request.form['protein']
    fat = request.form['fat']
    carbohydrate = request.form['carbohydrate']

    con = sqlite3.connect(DATABASE)
    con.execute("INSERT INTO foods (food_name, protein, fat, carbohydrate) VALUES (?, ?, ?, ?)",
                (food_name, protein, fat, carbohydrate))
    con.commit()
    con.close()
    return redirect(url_for('today'))

@app.route('/dish_form')
def dish_form():
    return render_template('dish_form.html')

@app.route('/dish_form_suggest', methods=['GET'])
def dish_form_suggest():
    con = sqlite3.connect(DATABASE)
    cursor = con.cursor()
    cursor.execute("SELECT food_id, food_name FROM foods")
    rows = cursor.fetchall()
    cursor.close()
    con.close()
    matched_candidates = []
    keyword = request.args.get('keyword', '')
    for row in rows:
        if keyword in row[1]:
            matched_candidates.append({'food_id': row[0], 'food_name': row[1]})
    return jsonify(matched_candidates)

@app.route('/dish_form_register', methods=['POST'])
def dish_form_register():
    dish_name = request.form['dish_name']
    food_ids = request.form.getlist('food_ids[]')
    quantities = request.form.getlist('quantities[]')
    food_names = request.form.getlist('food_names[]') # food_idを取得できたのでfood_nameの使い道がなくなったがひとまずこのまま。後で使うかも？
    print(dish_name, food_ids, quantities)

    con = sqlite3.connect(DATABASE)
    # 料理名がすでに存在するかどうかを検索
    existing_dish = con.execute('SELECT dish_id FROM dishes WHERE dish_name = ?', (dish_name,)).fetchone()
    print(existing_dish, 'existing_dish')
    # existing_dishがNoneでない場合、料理名がすでに存在する
    if existing_dish:
        dish_id = existing_dish[0]
    else:
        con.execute("INSERT INTO dishes (dish_name) VALUES (?)", (dish_name,))
        dish_id = con.execute('SELECT dish_id FROM dishes WHERE dish_name = ?', (dish_name,)).fetchone()[0]
        con.commit()
        con.close()

    # food_idごとに、同じdish_idで行を追加できるるようにする
    for food_id, quantity in zip(food_ids, quantities):
        con = sqlite3.connect(DATABASE)
        con.execute("INSERT INTO foods_dishes (food_id, quantity, dish_id) VALUES (?, ?, ?)", (food_id, quantity, dish_id))
        con.commit()
    con.close()

    return redirect(url_for('dish_form'))

@app.route('/jquery_practice')
def jquery_practice():
    return render_template(
        'jquery_practice.html'
    )
