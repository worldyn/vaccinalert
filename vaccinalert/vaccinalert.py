from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import json
import re

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
        print("POST")
        details = request.form
        email = details['email']
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$' # email regex
        if not re.search(regex, email):
            print("not an email ")
            return render_template('error.html')
        #region = details['region']
        region = "stockholm"
        try:
            print("trying connection")
            cur = mysql.connection.cursor()
            print(" executing..")
            cur.execute("SELECT * FROM Users WHERE email = %s", (email,))
            print(" fetching all")
            res = cur.fetchall()
            if len(res) > 0: # email exists
                print("email exists")
                cur.close()
                return render_template('error.html')
            print("email not exist, execute insert")

            cur.execute("INSERT INTO Users(email, region, verified) VALUES (%s, %s, FALSE)", (email, region))
            print("commit")
            mysql.connection.commit()
            cur.close()
            # send email verification
            return render_template('success.html')
        except:
            print("server error mysql...")
            return render_template('error.html')
    print("getting...")
    return render_template('testindex.html')

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.run(host='0.0.0.0')
