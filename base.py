from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/menu')
def menu():

    conn = get_db_connection()
    cursor = conn.cursor()
    

    cursor.execute("SELECT name, ingredients, price FROM pizzas")
    pizzas = cursor.fetchall()
    

    conn.close()
    

    return render_template('menu.html', pizzas=pizzas)


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




@app.route('/')
def home():
    return 'Головна сторінка'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



if __name__ == '__main__':
    init_db()  # Ініціалізація бази даних
    app.run(debug=True)
