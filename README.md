# WordWatch-3.0

**Setting up MYSQL**

1. Change db.yaml as necessary
2. CREATE database wordwatchmaster;
3. USE wordwatchmaster
4. CREATE table users( id INT AUTO_INCREMENT PRIMARY KEY, username varchar(100) not null, password varchar(100) not null, first_name varchar(100), last_name varchar(100));
5. CREATE TABLE input_history (
   id INT AUTO_INCREMENT PRIMARY KEY,
   user_id INT,
   text_input TEXT,
   submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, OFF INT,
   FOREIGN KEY (user_id) REFERENCES users(id)
   );

**Running flask app**

* In command line type "set FLASK_APP=app"
* Followed by "set FLASK_ENV=development"
* CMD : flask run -p PORT_NUMBER
