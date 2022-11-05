from flask import Flask, g, request
import sqlite3
import glob
import json

dbname = "test.db"
app = Flask(__name__)


def get_db():
    db = sqlite3.connect(dbname)
    return db


@app.route("/recipes", methods=["POST"])
def post_recipes():
    con = get_db()  # コネクション
    con.row_factory = sqlite3.Row  # カラム名取得
    cur = con.cursor()  # カーソルインスタンスを作成

    recipe = request.json  # POSTメソッド のデータを取得
    try:
        title, making_time, serves, ingredients, cost = recipe.values()
    except ValueError as e:
        print(e)

    try:
        cur.execute(f"""
            INSERT INTO recipes(title, making_time, serves, ingredients, cost)
            VALUES("{title}", "{making_time}", "{serves}", "{ingredients}", "{cost}")
        """)
        con.commit()

        cur2 = con.cursor()  # カーソルインスタンスを作成
        cur2.execute(f"""
            SELECT id, title, making_time, serves, ingredients, cost, created_at, updated_at
            FROM recipes
            WHERE title = '{title}' and
                making_time = '{making_time}' and
                serves = '{serves}' and
                ingredients = '{ingredients}' and
                cost = '{cost}'
            ORDER BY created_at DESC
            LIMIT 1
        """)
        recipes = []
        for row in cur2.fetchall():  # sqlite3.Row オブジェクトを dict に変換
            recipes.append(dict(row))
        response = {
            "message": "Recipe successfully created!",
            "recipe": recipes
        }
        cur2.close()
        return json.dumps(response, indent=2)
    except Exception as e:
        print(e)
        response = {
            "message": "Recipe creation failed!",
            "required": "title, making_time, serves, ingredients, cost"
        }
        return response
    finally:
        cur.close()
        con.close()


@app.route("/recipes", methods=["GET"])
def get_recipes():
    con = get_db()  # db connection
    con.row_factory = sqlite3.Row  # カラム名取得
    cur = con.cursor()  # カーソル取得

    cur.execute("SELECT id, title, making_time, serves, ingredients, cost FROM recipes")
    recipes = []
    for row in cur.fetchall():  # sqlite3.Row オブジェクトを dict に変換
        recipes.append(dict(row))
    cur.close()
    con.close()
    response = {
        "recipes": recipes
    }
    return json.dumps(response, indent=2)


@app.route("/recipes/<id>", methods=["GET"])
def get_specific_recipe(id):
    con = get_db()  # db connection
    con.row_factory = sqlite3.Row  # カラム名取得
    cur = con.cursor()  # カーソル取得

    cur.execute(f"""
        SELECT id, title, making_time, serves, ingredients, cost FROM recipes WHERE id = {id}
    """)
    recipes = []
    for row in cur.fetchall():  # sqlite3.Row オブジェクトを dict に変換
        recipes.append(dict(row))
    cur.close()
    con.close()
    response = {
        "message": "Recipe details by id",
        "recipe": recipes
    }
    return json.dumps(response, indent=2)


@app.route("/recipes/<id>", methods=["PATCH"])
def patch_recipe(id):
    con = get_db()  # コネクション
    cur = con.cursor()  # カーソルインスタンスを作成

    recipe = request.json  # POSTメソッド のデータを取得
    try:
        title, making_time, serves, ingredients, cost = recipe.values()
    except ValueError as e:
        print(e)

    try:
        cur.execute(f"""
            UPDATE recipes SET
                title = '{title}',
                making_time = '{making_time}',
                serves = '{serves}',
                ingredients = '{ingredients}',
                cost = '{cost}'
            WHERE id = {id}
        """)
        con.commit()
        response =   {
            "message": "Recipe successfully updated!",
            "recipe": [
                {
                    "title": title,
                    "making_time": making_time,
                    "serves": serves,
                    "ingredients": ingredients,
                    "cost": cost,
                }
            ]
        }
        return response
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()


@app.route("/recipes/<id>", methods=["DELETE"])
def delete_recipe(id):
    con = get_db()  # コネクション
    cur = con.cursor()  # カーソルインスタンスを作成
    try:
        cur.execute(f"DELETE FROM recipes WHERE id = {id}")
        con.commit()
        response = {
            "message": "Recipe successfully removed!"
        }
        return json.dumps(response, indent=2)
    except Exception as e:
        print(e)
        response = {
            "message":"No Recipe found"
        }
        return json.dumps(response, indent=2)
    finally:
        cur.close()
        con.close()


if __name__ == "__main__":
    app.run()
