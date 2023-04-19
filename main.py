from app import app, mongo
from flask import render_template
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/add', methods=['GET','POST'])
def add_user():
    if request.method=='POST':
        _name = request.form['name']
        _email = request.form['email']
        _password = request.form['pwd']
        _hashed_password = generate_password_hash(_password)
        id = mongo.db.person.insert_one({'name': _name, 'email': _email, 'pwd': _hashed_password})
        #resp = jsonify('User added successfully!')
        #resp.status_code = 200
        #return resp
    return render_template('index.html')


@app.route('/')
def users():
	users = mongo.db.person.find()
	#resp = dumps(users)
	return render_template('all_users.html',users=users)

@app.route('/user/<id>',methods=['GET'])
def user(id):
    if request.method=='GET':
	    use = mongo.db.person.find_one({'_id': ObjectId(str(id))},{'_id':0})
	    #resp = dumps(use)
	    #return resp
    return render_template('specific_user.html',user=use)

@app.route('/update/', methods=['POST','GET'])
def update_user():
    if request.method=='POST':
        #_json = request.json
        print("Updation")
        #_id = request.form['_id']
        _name = request.form['name']
        _email = request.form['email']
        _password = request.form['pwd']		
        _hashed_password = generate_password_hash(_password)
# save edits
        mongo.db.person.update_one({'email':_email}, {'$set': {'name': _name,  'pwd': _hashed_password}})
#resp = jsonify('User updated successfully!')
#resp.status_code = 200
        print("Updation Done!!")
        #__email=request.args.get('email')
        users = mongo.db.person.find()
        return render_template('all_users.html',users=users)
        #return render_template('update.html')
    #print(request.args.get('arg1'))
    return render_template('update.html')

@app.route('/edit/<email>/<name>/<password>',methods=['POST','GET'])
def edit(email,name,password):
        if request.method=='POST':
                _name = request.form['name']
                _email = request.form['email']
                _password = request.form['pwd']		
                _hashed_password = generate_password_hash(_password)
                mongo.db.person.update_one({'email':email}, {'$set': {'name': _name,  'pwd': _hashed_password}})
                users = mongo.db.person.find()
                return render_template('all_users.html',users=users) 
        print('running!')
        return render_template('update.html',_email=email,_name=name,_pwd=password)
        
                
@app.route('/sure/<email>',methods=['GET',"POST"])
def sure(email):
    return render_template('sure.html',email=email)		
@app.route('/delete/<email>', methods=['DELETE','GET'])
def delete_user(email):
    mongo.db.person.delete_one({'email': email})
    #resp = jsonify('User deleted successfully!')
    #resp.status_code = 20
    users = mongo.db.person.find()
    #print("hello")
    return render_template('all_users.html',users=users) 
    #return resp 

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run(debug=True)
