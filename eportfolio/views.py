from flask import Flask, render_template, url_for, redirect, session, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from forms import LoginForm, AddSubjectForm, SearchSubjectForm, PortfolioForm
import dataaccess as da
import os
import logging
import traceback

app = Flask(__name__)
bs = Bootstrap(app)
app.config["SECRET_KEY"] = os.urandom(32)
app.config["WTF_CSRF_SECRET_KEY"] = os.urandom(32)
csrf = CSRFProtect(app)

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = da.validate_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            logging.debug(f"User logged in: {username}")
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
            logging.debug("Invalid credentials provided")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    logging.debug("User logged out")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        logging.debug("User not logged in, redirecting to login page")
        return redirect(url_for('login'))
    return render_template('dashboard.html', role=session['role'])

@app.route('/add_subject', methods=['GET', 'POST'])
def add_subject_route():
    if 'username' not in session:
        logging.debug("User not logged in, redirecting to login page")
        return redirect(url_for('login'))
    form = AddSubjectForm()
    if form.validate_on_submit():
        subjectname = form.subjectname.data
        teacher_id = session['user_id']
        student_id = form.student_id.data
        logging.debug(f"Adding subject: {subjectname}, teacher_id: {teacher_id}, student_id: {student_id}")
        try:
            da.add_subject(subjectname, teacher_id, student_id)
            flash('Subject added successfully', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            logging.error(f"Error adding subject: {e}")
            flash('Failed to add subject', 'danger')
    return render_template('add_subject.html', form=form, role=session['role'])

@app.route('/search_subject', methods=['GET', 'POST'])
def search_subject_route():
    if 'username' not in session:
        logging.debug("User not logged in, redirecting to login page")
        return redirect(url_for('login'))
    form = SearchSubjectForm()
    subjects = []
    if form.validate_on_submit():
        search_term = form.search_term.data
        logging.debug(f"Searching subjects with term: {search_term}")
        try:
            subjects = da.search_subjects(session['user_id'], search_term)
            logging.debug(f"Found subjects: {subjects}")
        except Exception as e:
            logging.error(f"Error searching subjects: {e}")
            flash('Failed to search subjects', 'danger')
    return render_template('search_subject.html', form=form, subjects=subjects, role=session['role'])

@app.route('/portfolio/<int:subject_id>', methods=['GET', 'POST'])
def portfolio(subject_id):
    if 'username' not in session:
        logging.debug("User not logged in, redirecting to login page")
        return redirect(url_for('login'))
    form = PortfolioForm()
    if form.validate_on_submit():
        entry = form.entry.data
        user_id = session['user_id']
        logging.debug(f"Adding portfolio entry: {entry}, for subject_id: {subject_id}, user_id: {user_id}")
        try:
            da.add_portfolio_entry(subject_id, user_id, entry)
            flash('Portfolio entry added successfully', 'success')
            logging.debug("Portfolio entry added successfully")
            return redirect(request.url)
        except Exception as e:
            logging.error(f"Error adding portfolio entry: {e}")
            traceback.print_exc()
            flash('Failed to add portfolio entry', 'danger')
    entries = da.get_portfolio_entries(subject_id)
    logging.debug(f"Portfolio entries retrieved: {entries}")
    return render_template('portfolio.html', form=form, entries=entries, role=session['role'], subject_id=subject_id)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)