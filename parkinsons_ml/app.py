from flask import Flask, render_template, request, redirect, session, url_for
import json, os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USERS_FILE = 'auth/users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()

        email = request.form['email']
        if email in users:
            return "User already exists"

        users[email] = {
            "name": request.form['name'],
            "password": request.form['password'],
            "age": int(request.form['age']),
            "gender": request.form['gender'],
            "hand": request.form['hand'],
            "onset_years": request.form.get('onset_years', 0),
            "role": request.form['role']
        }

        save_users(users)
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        email = request.form['email']
        password = request.form['password']
        
        if email in users:
            user = users[email]
            if user.get('password') == password:
                session['username'] = user.get('name', 'Guest')  # 🟢 changed from 'username' to 'name'
                session['role'] = user.get('role', 'user')
                return redirect('/dashboard')
            else:
                return "Incorrect password"
        else:
            return "User not found"
    
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    return render_template('dashboard.html', user=session['username'], role=session['role'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
