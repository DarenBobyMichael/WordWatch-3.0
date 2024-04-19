from flask import Flask, render_template, request, redirect, url_for, session
from saraswati.malayalam_predict_new import predict
from saraswati.malayalam_predict_video_new import predict_video# Corrected module name
from flask_mysqldb import MySQL
from flask import flash
from functools import wraps
import yaml
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'nannayiVarum'

db_config = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['ALLOWED_EXTENSIONS']= {'mp4', 'avi', 'mov', 'mpeg', 'mkv'}
app.config['UPLOAD_FOLDER'] = 'saraswati/uploads'
app.config['MYSQL_HOST'] = db_config['mysql_host']
app.config['MYSQL_USER'] = db_config['mysql_user']
app.config['MYSQL_PASSWORD'] = db_config['mysql_password']
app.config['MYSQL_DB'] = db_config['mysql_db']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session or not session['loggedin']:
            flash("Please log in to view that page", "info")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def login():
    failed = request.args.get('failed', 'False') == 'True'
    return render_template('login.html',failed=failed)
     
@app.route('/auth', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    account = cur.fetchone()
    session['loggedin'] = False
    if account:
        session['loggedin'] = True
        session['username'] = username
        session['id'] = account[0]
        session['first_name'] = account[3]
        session['last_name'] = account[4]
        return redirect(url_for('predict_malayalam'))
    else:
        return redirect(url_for('login')+'?failed=True')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        cur = mysql.connection.cursor()

        # Check if username already exists
        cur.execute("SELECT id FROM users WHERE username=%s", (username,))
        account = cur.fetchone()
        if account:
            flash('Username already exists. Choose a different one.')
        else:
            cur.execute("INSERT INTO users (username, password,first_name,last_name) VALUES (%s, %s,%s,%s)", (username, password,first_name,last_name))
            mysql.connection.commit()
            return redirect(url_for('login'))
    return render_template('register.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload_file():
    predicted_text = None
    off_rating = None
    text_content = None
    ratings=None
    labels_data=None
    upload_status=0
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
    text_to_predict=predict_video(filename)
    if text_to_predict == '':
                flash("Text input is empty", 'error')
                return redirect(url_for('predict_malayalam'))
    text_content, predicted_text, labels_data,ratings = predict(text_to_predict)
    cur=mysql.connection.cursor()
    user_id=session['id']
    Name=session['first_name']+" "+session['last_name']
    cur.execute("SELECT text_input, submission_time,OFF FROM input_history WHERE user_id=%s ORDER BY submission_time DESC", (user_id,))
    history = cur.fetchall()
    cur.close()
    return render_template('video.html', Name=Name, history=history,text_content=text_content, predicted_text=predicted_text, ratings=ratings,labels_data=labels_data)

    



@app.route('/video', methods=['GET', 'POST'])
def video():
    text_content=None
    predicted_text=None
    ratings=None
    labels_data=None
    # GET request or post-upload logic
    user_id = session['id']
    Name = session['first_name'] + " " + session['last_name']
    cur = mysql.connection.cursor()
    cur.execute("SELECT text_input, submission_time,OFF FROM input_history WHERE user_id=%s ORDER BY submission_time DESC", (user_id,))
    history = cur.fetchall()
    cur.close()
    # Assuming mysql connection setup, and other database interaction remains the same...
    return render_template('video.html', Name=Name, history=history,text_content=text_content, predicted_text=predicted_text, ratings=ratings,labels_data=labels_data)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def predict_malayalam():
    if 'loggedin' not in session or not session['loggedin']:
        # If user is not loggedin, redirect to login page with a message
        flash("Please log in to view that page", "info")
        return redirect(url_for('login'))
    predicted_text = None
    off_rating = None
    text_content = None
    ratings=None
    labels_data=['Abusive','Not in intended language','Off target ind','Off target group','Profanity','Normal']
    cur = mysql.connection.cursor()
    user_id=session['id']
    Name=session['first_name']+" "+session['last_name']
    cur.execute("SELECT text_input, submission_time,OFF FROM input_history WHERE user_id=%s ORDER BY submission_time DESC", (user_id,))
    history = cur.fetchall()
    cur.close()
    if request.method == 'POST':
        text_to_predict = request.form['text_to_predict']
        if text_to_predict == '':
                flash("Text input is empty", 'error')
                return redirect(url_for('predict_malayalam'))
        text_content, predicted_text, labels_data,ratings = predict(text_to_predict)
        cur = mysql.connection.cursor()

        try:
            
            cur.execute("INSERT INTO input_history (user_id, text_input, OFF) VALUES (%s, %s, %s)", (user_id, text_to_predict,off_rating))
            mysql.connection.commit()  # Commit the transaction
            flash("Data inserted successfully into input_history table")
            cur.execute("SELECT text_input, submission_time,OFF FROM input_history WHERE user_id=%s ORDER BY submission_time DESC", (user_id,))
            history = cur.fetchall()# Flash message for success
        except Exception as e:
            flash(f"Error inserting data into input_history table: {e}", 'error')  # Flash message for error
            mysql.connection.rollback()  # Rollback the transaction in case of error
        finally:
            cur.close() 
    # Ensure the HTML content is stored in a template file, e.g., `home.html` under the `templates` directory.
    return render_template("home.html", Name=Name, history=history, text_content=text_content, predicted_text=predicted_text, ratings=ratings,labels_data=labels_data)
