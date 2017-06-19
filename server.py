from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')
@app.route('/')
def index():
    query = "SELECT * FROM friends"
    friends = mysql.query_db(query)
    print friends
    return render_template('index.html', all_friends=friends)
    
@app.route('/friends', methods=['POST']) #THIS MAKES YOUR DATABASE ENTRY SHOW ON THE PAGE!!
def create():
    print request.form['name']
    print request.form['age']
    print request.form['time']
    # add a friend to the database!
    #we want to insert into our query
    query = "INSERT INTO friends(name,age,time,updated_at) VALUES (:name, :age, :time, NOW())"
    # We'll then create a dictionary of data from the POST data received.

    data = {
        'name': request.form['name'],
        'age': request.form['age'],
        'time': request.form['time']
    }
    # Run query, with dictionary values injected into the query
    mysql.query_db(query,data)
    return redirect('/')

@app.route('/friends/<friend_id>')
def show(friend_id):
    # Write query to select specific user by id. At every point where
    # we want to insert data, we write ":" and variable name.
    query = "SELECT * FROM friends WHERE id = {}".format(friend_id)
    # Run query with inserted data.
    friends = mysql.query_db(query)
    print friends
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias one_friend.
    return render_template('index.html', one_friend=friends[0])

#CREATE ANOTHER PAGE TO UPDATE A SPECIFIC RECORD
#Create another page and add a form that would submit to the following route
@app.route('/update_friend/<friend_id>', methods=['POST'])
def update(friend_id):
    query = "UPDATE friends SET name = :name, age = :age, time = :time, WHERE id = :id"
    data = {
             'name': request.form['name'],
             'age':  request.form['age'],
             'time': request.form['time'],
             'id': friend_id
           }
    mysql.query_db(query, data)
    return redirect('/')

#DELETES RECORDS
@app.route('/remove_friend/<friend_id>', methods=['POST'])
def delete(friend_id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': friend_id}
    mysql.query_db(query, data)
    return redirect('/')


app.run(debug=True)