from flask import Flask, request, jsonify
from models import init_db, seed_exercises, add_user, get_user, get_exercises_by_level, get_motivational_message

app = Flask(__name__)


@app.route('/')
def index():
    return "Ласкаво просимо до Fitness App!"


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    level = data.get('level')

    if not username or not password or not level:
        return jsonify({"error": "Всі поля обов'язкові"}), 400

    result = add_user(username, password, level)
    if result:
        return jsonify({"message": "Користувача зареєстровано"}), 201
    else:
        return jsonify({"error": "Користувач з таким іменем вже існує"}), 409


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = get_user(username, password)
    if user:
        return jsonify({"message": "Вхід успішний", "user": {"id": user[0], "username": user[1], "level": user[3]}})
    else:
        return jsonify({"error": "Неправильний логін або пароль"}), 401


@app.route('/exercises/<level>', methods=['GET'])
def exercises_level(level):
    print(f"Параметр рівня: {level}")
    exercises = get_exercises_by_level(level)
    if exercises:
        motivational_message = get_motivational_message()
        return jsonify(exercises, motivational_message)
    else:
        return jsonify({"error": "Немає вправ для цього рівня"}), 404


if __name__ == '__main__':
    init_db()
    seed_exercises()
    app.run(debug=True)
