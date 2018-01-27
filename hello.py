from flask import Flask, render_template, request, json
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'goldy'
app.config['MYSQL_DATABASE_PASSWORD'] = 'goldy'
app.config['MYSQL_DATABASE_DB'] = 'sample_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/showSignUp')
def showSignUp():
	return render_template('sample_signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
	_name = request.form['inputName']
	_branch = request.form['inputBranch']
	_cgpa = request.form['inputCgpa']
	
	if _name and _branch and _cgpa:
		return json.dumps({'html':'<span>All fields good!</span>'})
	else:
		return json.dumps({'html':'<span>Enter the required fields</span>'})
		
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.callproc('sp_createUser', (_name, _branch, _cgpa))

	data = cursor.fetchall()
	if len(data) is 0:
		conn.commit()
		return json.dumps({'message':'User created successfully!'})
	else:
		return json.dumps({'error':str[data(0)]})


if __name__ == "__main__":
    app.run()
