from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

# Config DB
f = open('database.json', 'r')
data = json.load(f)
app.config['MYSQL_HOST'] = data['MYSQL_HOST']
app.config['MYSQL_USER'] = data['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = data['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = data['MYSQL_DB']

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST": # TODO fix clean form fields
        details = request.form
        email = details['email']
        region = details['region']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Users(email, region, verified) VALUES (%s, %s, FALSE)", (email, region))
        mysql.connection.commit()
        cur.close()
        return render_template('success.html')
    return render_template('testindex.html', content="Ost")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
