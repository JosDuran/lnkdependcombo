from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm 
from wtforms import SelectField
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

DEFAULT_PATH = '/home/rufus/pyapps/dependentcombo/test.db'

def db_connect(db_path=DEFAULT_PATH, detect_types=sqlite3.PARSE_DECLTYPES):  
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row # its key
    return con

class Form(FlaskForm):
    state = SelectField('state', choices=[('CA', 'California'), ('NV', 'Nevada')]) 
    city = SelectField('city', choices=[])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    cone = db_connect()
    cur = cone.cursor()
    astate = 'CA'
    ssql = 'SELECT * from city WHERE STATE = "%s"' % (astate)
    print( 'ssql= '+ ssql)

    cur.execute(ssql)
   
    for row in cur:
        form.city.choices += [(row['id'], row['name'] )]
    

    if request.method == 'POST':
        cone = db_connect()
        cur = cone.cursor()
        ssql = 'SELECT * FROM CITY WHERE ID = "%s"'  %(form.city.data)
        cur.execute(ssql)
        row = cur.fetchone()
        aname = row['name']
        return '<h1>State: {}, City: {}</h1>'.format(form.state.data, aname)

    return render_template('index.html', form=form)

@app.route('/city/<state>')
def city(state):
    cone = db_connect()
    cur = cone.cursor()
    ssql = 'select * from city where state = "%s"' %(state)
    cur.execute(ssql)
    cityArray = []

    for row in cur:
        cityObj = {}
        cityObj['id'] = row['id']
        cityObj['name'] = row['name']
        cityArray.append(cityObj)

    return jsonify({'cities' : cityArray})

if __name__ == '__main__':
    app.run(debug=True)
