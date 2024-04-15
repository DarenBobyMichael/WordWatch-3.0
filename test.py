from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'Darens-MacBook-Pro.local'
app.config['MYSQL_USER'] = 'root'# Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'Trvc1@6w'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'wordwatchmaster'  # Replace with your MySQL database name

mysql = MySQL(app)

@app.route('/')
def check_mysql_connection():
    try:
        # Attempt to connect to MySQL
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        return 'MySQL connection successful!'
    except Exception as e:
        return f'MySQL connection failed: {e}'

if __name__ == '__main__':
    app.run(debug=True,port=5050)
