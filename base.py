from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Конфігурація бази даних
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Для зручного доступу до колонок за іменами
    return conn

@app.route('/')
def index():
    # Виведення головної сторінки
    return render_template('index.html')

@app.route('/menu')
def menu():
    # Підключення до бази даних
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Вибірка всіх піц з таблиці
    cursor.execute("SELECT name, ingredients, price FROM pizzas")
    pizzas = cursor.fetchall()
    
    # Закриття підключення
    conn.close()
    
    # Передача даних у шаблон
    return render_template('menu.html', pizzas=pizzas)

# Створення та наповнення таблиці pizzas
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pizzas
                      (id INTEGER PRIMARY KEY,
                       name TEXT,
                       ingredients TEXT,
                       price REAL)''')
    pizzas = [
        ('Pepperoni', 'Піца з пепероні та сиром', 8.99),
        ('Margherita', 'Класична піца з томатами та моцарелою', 7.99),
        ('Hawaiian', 'Піца Гавайська з ананасами та шинкою', 9.99)
    ]
    cursor.executemany('''INSERT INTO pizzas (name, ingredients, price)
                          VALUES (?, ?, ?)''', pizzas)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()  # Ініціалізація бази даних
    app.run(debug=True)
