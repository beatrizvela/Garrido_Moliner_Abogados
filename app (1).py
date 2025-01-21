
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Crear la base de datos
def init_db():
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT,
                    email TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS cases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER,
                    case_number TEXT NOT NULL,
                    type TEXT,
                    status TEXT,
                    FOREIGN KEY (client_id) REFERENCES clients (id)
                )''')
    conn.commit()
    conn.close()

# Rutas
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/clients')
def clients():
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    c.execute("SELECT * FROM clients")
    clients = c.fetchall()
    conn.close()
    return render_template('clients.html', clients=clients)

@app.route('/add_client', methods=['POST'])
def add_client():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    c.execute("INSERT INTO clients (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
    conn.commit()
    conn.close()
    return redirect(url_for('clients'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Aquí puedes agregar funcionalidad para guardar o enviar el mensaje
        return render_template('thank_you.html', name=name)
    return render_template('contact.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
