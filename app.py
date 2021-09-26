from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token, get_jwt_identity, jwt_required)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


import datetime
import random
import sqlite3
import bcrypt


app = Flask(__name__)
CORS(app)


#==============================================================#
#config database


app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'some_random_jwt_secret_key'

db = SQLAlchemy(app)
app.secret_key = 'random secret key'

jwt = JWTManager(app)



"""


DATABASES:
===========================


Passangers: id, phone, first_name, Last_name, email, password, ref

Owners: id, phone, first_name, Last_name, email, password,ref

Crew: id, phone, first_name, last_name, email, password, ref

Vehicle: id, reg_no, sacco, capacity, owner_ref

Payments: id, ref, reg_no, amount, passanger_phone, crew_ref

Top-Up; id, mpesa, phone, amount,

Withdraw: id, mpesa, phone, service_charge ,amount, amount_received, owner_ref

Crew_bookmark: id, reg_no, alias, crew_ref

Report: id, ref, reg_no, alias, report,


PASSANGERS:
==========================
Enter reg no and amount to pay ride
Top up using phone number as account number to paybill
view payment and deposit history
view ride details, reg_no and sacco
Report matatu
Edit profile


OWNER:
==========================
Register vehicle
Withdraw funds
view payments per vehicle and withdraws
view reposts per vehicle
Edit profile


CREW:
==========================
Enter userphone and amount to pay ride
view payment history as per vehicle
Edit profile



"""





#===============================#
#       DATABASE MODELS         #
#===============================#




#Passengers class db model
class Passengers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String, unique=True)
    ref = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    created_at = db.Column(db.String)



    def __init__(self,first_name,last_name,email,phone,ref,password,created_at):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.ref = ref
        self.password = password
        self.created_at = created_at


#owners class db model
class Owners(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String, unique=True)
    ref = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    created_at = db.Column(db.String)



    def __init__(self,first_name,last_name,email,phone,ref,password,created_at):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.ref = ref
        self.password = password
        self.created_at = created_at


#owner class db model
class Crew(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String, unique=True)
    ref = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    created_at = db.Column(db.String)



    def __init__(self,first_name,last_name,email,phone,ref,password,created_at):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.ref = ref
        self.password = password
        self.created_at = created_at


#vehicle class db model
class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    reg_no = db.Column(db.String, unique=True)
    sacco = db.Column(db.String)
    capacity = db.Column(db.Integer)
    owner_ref = db.Column(db.String)
    created_at = db.Column(db.String)


    def __init__(self,reg_no, sacco, capacity, owner_ref, created_at):
        self.reg_no = reg_no
        self.sacco = sacco
        self.capacity = capacity
        self.owner_ref = owner_ref
        self.created_at = created_at


#payments class and db model
class Payments(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    ref = db.Column(db.String, unique=True)
    reg_no = db.Column(db.String)
    amount= db.Column(db.Integer)
    pass_phone = db.Column(db.String)
    crew_ref = db.Column(db.String)
    owner_ref = db.Column(db.String)
    created_at = db.Column(db.String)


    def __init__(self,ref,reg_no, amount, pass_phone, crew_ref,owner_ref, created_at):
        self.ref = ref
        self.reg_no = reg_no
        self.amount = amount
        self.pass_phone = pass_phone
        self.crew_ref = crew_ref
        self.owner_ref = owner_ref
        self.created_at = created_at


#top up class
class Topups(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    mpesa_code = db.Column(db.String, unique=True)
    amount= db.Column(db.Integer)
    pass_phone = db.Column(db.String)
    status = db.Column(db.String)
    created_at = db.Column(db.String)



    def __init__(self,mpesa_code, amount, pass_phone,status,created_at):
        self.mpesa_code = mpesa_code
        self.amount = amount
        self.status = status
        self.pass_phone = pass_phone
        self.created_at = created_at


#withdraw class
class Withdraws(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    mpesa_code = db.Column(db.String, unique=True)
    amount= db.Column(db.Integer)
    owner_phone = db.Column(db.String)
    service_charge = db.Column(db.Integer)
    amount_received = db.Column(db.Integer)
    status = db.Column(db.String)
    owner_ref = db.Column(db.String)
    created_at = db.Column(db.String)

    def __init__(self,mpesa_code, amount, owner_phone,service_charge,amount_received,status,owner_ref,created_at):
        self.mpesa_code = mpesa_code
        self.amount = amount
        self.owner_phone = owner_phone
        self.service_charge = service_charge
        self.amount_received = amount_received
        self.status = status
        self.owner_ref = owner_ref
        self.created_at = created_at


#crew bookmark
class CrewBookmarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.Integer)
    alias = db.Column(db.String)
    crew_ref = db.Column(db.String)
    created_at = db.Column(db.String)     

    def __init__(self,reg_no, alias,crew_ref, created_at):
        self.reg_no = reg_no
        self.alias = alias
        self.crew_ref = crew_ref  
        self.created_at = created_at 


#reports class and db model
class Reports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.Integer, unique=True)
    reg_no = db.Column(db.Integer)
    alias = db.Column(db.String)
    report = db.Column(db.String)
    created_at = db.Column(db.String)    

    def __init__(self, ref, reg_no, alias, report, created_at):
        self.ref = ref
        self.reg_no = reg_no
        self.alias = alias
        self.report = report
        self.created_at = created_at




#=======================================#
#   PASSANGER: 
#             register ...|
#             login ... |
#             forget password ...|
#             reset password ... |
#             view profile ...|
#             edit profile ... |
#             pay ride ... |
#             top up ride ... |
#             view payments [7 days, 30 days, all] ...|
#             view top ups [7 days, 30 days, all]  ...|
#             view ride details, reg_no and sacco
#             report matatu ... |
#             view balance  ... |  
#========================================#     

@app.route('/')
def metro_card():
    return 'metro card'

#pass register
@app.route('/pass/register', methods=['POST'])
def pass_register():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    phone = request.json['phone']
    password = request.json['password']
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    ref_seed = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
    random.shuffle(ref_seed)
    ref_seed_empty = "" 
    ref_gen = ref_seed_empty.join(ref_seed)
    ref = ref_gen[:5]

    x = datetime.datetime.now()
    current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
    current_date = str(current_time)
    created_at = current_date


    try:
        new_pass = Passengers(first_name,last_name, email, phone, ref, password_hashed, created_at)
        db.session.add(new_pass)
        db.session.commit()

        user_profile = Passengers.query.filter_by(email=email).first()
        access_token = create_access_token(identity={"ref": user_profile.ref})

        return {"access_token":access_token},201
    except:
        return 'Email already exists', 406



#pass login
@app.route('/pass/login', methods=['POST'])
def pass_login():  
   
    try:
        email = request.json['email']
        password = request.json['password']
        user_profile = Passengers.query.filter_by(email=email).first()
        password_hash = bcrypt.checkpw(password.encode('utf-8'), user_profile.password)

        if(password_hash == True):
            
            access_token = create_access_token(identity={"ref": user_profile.ref})

            return {"access_token":access_token, "message":"ok"}, 200

        else:

            return {"message":"Authentication failed"}, 200    
    except:
        return 'Something went wrong', 409



#pass forget password
@app.route('/pass/forgot-password', methods=['PUT'])
def pass_forgot_password():
    try:
        email = request.json['email']
        user_email = Passengers.query.filter_by(email=email).first()
        email=user_email.email
        e = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        random.shuffle(e)
        easy_password = "" 
        password_gen = easy_password.join(e)
        password = password_gen[:7]
        password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user_email.password = password_hashed
        db.session.commit()  
 
            
        return  (password) , 200
        #return jsonify(email=user_email.email)

    except:
        return 'Email does not exist'



#pass change password
@app.route('/pass/change-password', methods=['PUT'])
@jwt_required()
def pass_edit_password():
    try:
        users = get_jwt_identity()
        ref = users['ref'] 
        user = Passengers.query.filter_by(ref=ref).first()
        new_password = request.json['new_password']
        confirm_password = request.json['confirm_password']

        if(new_password == confirm_password):
            password_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.password = password_hashed
            db.session.commit()
            return 'Password Successfully Changed'
        else:
            return 'Error: Passwords do not match'
    except:
        return 'login to change password'



#pass profile
@app.route('/pass/profile', methods=['GET'])
@jwt_required()
def pass_profile():
    try:
        users = get_jwt_identity()
        ref = users['ref'] 
        user = Passengers.query.filter_by(ref=ref).first()

        #return session["user_id"]
    
        return jsonify(        
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone, 
            email=user.email  
            )
    except:
       return {"message":"Please Login"}, 200    



#pass edit names
@app.route('/pass/edit', methods=['PUT'])
@jwt_required()
def pass_edit_names():
    try:
        users = get_jwt_identity()
        ref = users['ref'] 
        user = Passengers.query.filter_by(ref=ref).first()
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        user.first_name = first_name
        user.last_name = last_name
        db.session.commit()
        return 'record updated'
    except:
        return 'login to edit profile'



#top up account
@app.route('/pass/topup', methods=['POST'])
@jwt_required()
def pass_topup():
    try:
        users = get_jwt_identity()
        ref = users['ref'] 
        user = Passengers.query.filter_by(ref=ref).first()
        pass_phone = user.phone
        amounts = request.json['amount']
        amount = int(amounts)
        status = 'Complete'
        #mpesa_code = 'Pending12'

        x = datetime.datetime.now()
        current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
        current_date = str(current_time)
        created_at = current_date

       
        e = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        random.shuffle(e)
        easy_password = "" 
        mpesa_gen = easy_password.join(e)
        mpesa_code = mpesa_gen[:7]
    
        new_topup = Topups(mpesa_code,amount,pass_phone,status,created_at)
        db.session.add(new_topup)
        db.session.commit()

              

        return 'Top Up successful'





    except:
        return 'Something went wrong or mpesa code exists'
        


#account pay trip
@app.route('/pass/pay', methods=['POST'])
@jwt_required()
def pass_pay(): 
    try:
        users = get_jwt_identity()
        ref = users['ref'] 

        
        reg_no = request.json['reg_no']
        crew_ref = 'App'

        amount = request.json['amount']  

        owner = Vehicles.query.filter_by(reg_no=reg_no).first()
        owner_ref = owner.owner_ref


        passenger = Passengers.query.filter_by(ref=ref).first()
        pass_phone = passenger.phone

        ref_seed = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
        random.shuffle(ref_seed)
        ref_seed_empty = "" 
        ref_gen = ref_seed_empty.join(ref_seed)
        ref = ref_gen[:5]



        x = datetime.datetime.now()
        current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
        current_date = str(current_time)
        created_at = current_date

     

        conn = sqlite3.connect('database.db')
        conn_sum_topups = conn.cursor()
        conn_sum_topups.execute("SELECT SUM(amount) from topups WHERE pass_phone = '"+ pass_phone +"'")
        total_topups = conn_sum_topups.fetchall()
        topup = total_topups[0][0]


        conn_sum_payments = conn.cursor()
        conn_sum_payments.execute("SELECT SUM(amount) from payments WHERE pass_phone = '"+ pass_phone +"'")
        total_payment = conn_sum_payments.fetchall()

        #total_balance = int(total_topups[0][0]) - int(total_payment[0][0])


        payment = str(total_payment[0][0])

        #payment = 100

        
        if(payment == None ):
            payment = 0   
        

        balance = int(topup) - int(payment)

        if (balance >= int(amount) > 0):
             new_payment = Payments(ref,reg_no,int(amount), pass_phone, crew_ref,owner_ref, created_at)
             db.session.add(new_payment)
             db.session.commit()

             return {"message":"payment successful"},200
            
        else:

            return {"message":"no money in wallet"},200


    except:
        return {"message":"payment failed"},200



#report matatu
@app.route('/report', methods=['POST'])
def report():
    try:
        reg_no = request.json['reg_no'] 
        alias = request.json['alias'] 
        report = request.json['report'] 

        ref_seed = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
        random.shuffle(ref_seed)
        ref_seed_empty = "" 
        ref_gen = ref_seed_empty.join(ref_seed)
        ref = ref_gen[:5]



        x = datetime.datetime.now()
        current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
        current_date = str(current_time)
        created_at = current_date

        new_report = Reports(ref,reg_no, alias, report, created_at)
        db.session.add(new_report)
        db.session.commit()

        return 'Report submited'
    except:
        return 'Something went wrong'


#pass view balance
@app.route('/pass/balance', methods=['GET'])
@jwt_required()
def pass_balance():
    try:
        users = get_jwt_identity()
        ref = users['ref'] 


        passenger = Passengers.query.filter_by(ref=ref).first()
        pass_phone = passenger.phone

        
        conn = sqlite3.connect('database.db')
        conn_sum_topups = conn.cursor()
        conn_sum_topups.execute("SELECT SUM(amount) from topups WHERE pass_phone = '"+ pass_phone +"'")
        total_topups = conn_sum_topups.fetchall()
        topup = total_topups[0][0]

        
        conn_sum_payments = conn.cursor()
        conn_sum_payments.execute("SELECT SUM(amount) from payments WHERE pass_phone = '"+ pass_phone +"'")
        total_payment = conn_sum_payments.fetchall()
        

        payment = str(total_payment[0][0])

        #payment = 100

        
        if(payment == None ):
            payment = 0   
        
        if(topup == None):
            topup = 0

        balance = int(topup) - int(payment)

        return jsonify(balance=balance)


    except:

        return 'something went wrong'



#pass view all payments
@app.route('/pass/all-payments', methods=['GET'])
@jwt_required()
def pass_all_payments():
    user = get_jwt_identity()
    pass_ref = user['ref']
    pass_details = Passengers.query.filter_by(ref=pass_ref).first()
    pass_phone = pass_details.phone

    pass_payments = Payments.query.filter_by(pass_phone=pass_phone).all()

    output =[]
    for pass_payment in pass_payments:
            pass_data={}
            pass_data['id']=pass_payment.id
            pass_data['ref']=pass_payment.ref
            pass_data['reg_no']=pass_payment.reg_no
            pass_data['amount']=pass_payment.amount
            pass_data['created_at']=pass_payment.created_at
            output.append(pass_data)

    return jsonify({"pass_payments":output})



#pass view all deposits
@app.route('/pass/all-topup', methods=['GET'])
@jwt_required()
def pass_all_topup():
    user = get_jwt_identity()
    pass_ref = user['ref']
    pass_details = Passengers.query.filter_by(ref=pass_ref).first()
    pass_phone = pass_details.phone

    pass_payments = Topups.query.filter_by(pass_phone=pass_phone).all()

    output =[]
    for pass_payment in pass_payments:
            pass_data={}
            pass_data['id']=pass_payment.id
            pass_data['mpesa_code']=pass_payment.mpesa_code
            pass_data['amount']=pass_payment.amount
            pass_data['status']=pass_payment.status
            pass_data['created_at']=pass_payment.created_at
            output.append(pass_data)

    return jsonify({"pass_topups":output})



#=======================================#
#   OWNER: 
#             forget password ...|
#             reset password ...|
#             view profile ...|
#             edit profile ...|
#             register vehicle ...|
#             edit vehicle
#             view vehicle ... |
#             transfer vehicle [change owner_ref]  ...|
#             withdraw cash ...|
#             view payments per vehicle [7 days, 30 days, all] ...|
#             view deposits [7 days, 30 days, all] ...|
#             view withdraws [7 days, 30 days, all] ...|
#             view balance  ...|
#             view reports matatu
#========================================# 


#owner register
@app.route('/owner/register', methods=['POST'])
def owner_register():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    phone = request.json['phone']
    password = request.json['password']
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    ref_seed = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
    random.shuffle(ref_seed)
    ref_seed_empty = "" 
    ref_gen = ref_seed_empty.join(ref_seed)
    ref = ref_gen[:5]

    x = datetime.datetime.now()
    current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
    current_date = str(current_time)
    created_at = current_date


    try:
        new_owner = Owners(first_name,last_name, email, phone, ref, password_hashed, created_at)
        db.session.add(new_owner)
        db.session.commit()

        user_profile = Owners.query.filter_by(email=email).first()
        access_token = create_access_token(identity={"ref": user_profile.ref})

        return {"access_token":access_token},201
    except:
        return 'Email already exists', 406


#owner login
@app.route('/owner/login', methods=['POST'])
def owner_login():  
   
    try:
        email = request.json['email']
        password = request.json['password']
        user_profile = Owners.query.filter_by(email=email).first()
        password_hash = bcrypt.checkpw(password.encode('utf-8'), user_profile.password)

        if(password_hash == True):
            
            access_token = create_access_token(identity={"ref": user_profile.ref})

            return {"access_token":access_token}, 200

        else:

            return 'Authentication failed', 400    
    except:
        return 'Something went wrong', 409


#forget password
@app.route('/owner/forgot-password', methods=['PUT'])
def owner_forgot_password():
    try:
        email = request.json['email']
        user_email = Owners.query.filter_by(email=email).first()
        email=user_email.email
        e = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        random.shuffle(e)
        easy_password = "" 
        password_gen = easy_password.join(e)
        password = password_gen[:7]
        password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user_email.password = password_hashed
        db.session.commit()  
 
            
        return  (password) , 200
        #return jsonify(email=user_email.email)

    except:
        return 'Email does not exist'


#owner change password
@app.route('/owner/change-password', methods=['PUT'])
@jwt_required()
def owner_edit_password():
    try:
        users = get_jwt_identity()
        ref = users['ref'] 
        user = Owners.query.filter_by(ref=ref).first()
        new_password = request.json['new_password']
        confirm_password = request.json['confirm_password']

        if(new_password == confirm_password):
            password_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.password = password_hashed
            db.session.commit()
            return 'Password Successfully Changed'
        else:
            return 'Error: Passwords do not match'
    except:
        return 'login to change password'



#owner profile
@app.route('/owner/profile', methods=['GET'])
@jwt_required()
def owner_profile():
    try:
        users = get_jwt_identity()
        ref = users['ref'] 
        user = Owners.query.filter_by(ref=ref).first()

        #return session["user_id"]
    
        return jsonify(        
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone, 
            email=user.email  
            )
    except:
        return 'Please login'



#owner edit names
@app.route('/owner/edit', methods=['PUT'])
@jwt_required()
def owner_edit_names():
    try:
        users = get_jwt_identity()
        ref = users['ref'] 
        user = Owners.query.filter_by(ref=ref).first()
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        user.first_name = first_name
        user.last_name = last_name
        db.session.commit()
        return 'record updated'
    except:
        return 'login to edit profile'



#owner add vehicle
@app.route('/owner/add-vehicle', methods=['POST'])
@jwt_required()
def owner_add_vehicle():
    try:
        users = get_jwt_identity()
        ref = users['ref'] 

        reg_no = request.json['reg_no']
        
        sacco = request.json['sacco']
        capacity = request.json['capacity']
        owner_ref = ref

        x = datetime.datetime.now()
        current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
        current_date = str(current_time)
        created_at = current_date

        new_vehicle = Vehicles(reg_no,sacco,capacity,owner_ref,created_at)
        db.session.add(new_vehicle)
        db.session.commit()

        return 'Vehicle added'

    except:
        return 'Something went wrong'



#edit vehicle
@app.route('/owner/vehicle/<id>', methods=['PUT'])
@jwt_required()
def owner_edit_vehicle(id):
    try:
        users = get_jwt_identity()
        owner_ref = users['ref'] 
        vehicle = Vehicles.query.filter_by(owner_ref=owner_ref,id=id).first()
        sacco = request.json['sacco']
        capacity = request.json['capacity']
        vehicle.sacco = sacco
        vehicle.capacity = capacity
        db.session.commit()
        return 'record updated'
    except:
        return 'login to edit profile'




#view vehicle
@app.route('/owner/vehicle', methods=['GET'])
@jwt_required()
def owner_view_vehicle():
    user = get_jwt_identity()
    owner_ref = user['ref']
    reg_no = request.json['reg_no']
    vehicle_details = Vehicles.query.filter_by(owner_ref=owner_ref,reg_no=reg_no ).first()

    return jsonify(        
        reg_no=vehicle_details.reg_no,
        sacco=vehicle_details.sacco,
        capacity= vehicle_details.capacity
            )


#view all vehicles
@app.route('/owner/vehicles', methods=['GET'])
@jwt_required()
def owner_view_all_vehicle():
    user = get_jwt_identity()
    owner_ref = user['ref']
    vehicle_details = Vehicles.query.filter_by(owner_ref=owner_ref ).all()

   
    output =[]
    for vehicle_detail in vehicle_details:
            vehicle_data={}
            vehicle_data['reg_no']=vehicle_detail.reg_no
            vehicle_data['capacity']=vehicle_detail.capacity
            vehicle_data['sacco']=vehicle_detail.sacco
            vehicle_data['id']=vehicle_detail.id
           
            output.append(vehicle_data)
    return jsonify({"vehicles":output})


#transfer vehicle

@app.route('/owner/transfer', methods=['PUT'])
@jwt_required()
def owner_transfers():
    try:
        users = get_jwt_identity()
        ref = users['ref'] 
        new_owner_email = request.json['email']
        reg_no = request.json['reg_no']
        

        search_new_owner_email = Owners.query.filter_by(email=new_owner_email).first()
        new_owner_email = search_new_owner_email.email
        new_owner_ref = search_new_owner_email.ref

        search_reg_no = Vehicles.query.filter_by(reg_no=reg_no, owner_ref=ref).first()
        found_reg_no = search_reg_no.reg_no
    
        if( new_owner_email == None ):
            
            return 'Email not found'

        elif (found_reg_no == None):

            return 'Vehicle Registration number not found'

        else:  
            update_vehicle = Vehicles.query.filter_by(reg_no=found_reg_no).first()
            update_vehicle.owner_ref = new_owner_ref
            db.session.commit()      
        
            return 'Transfer successful '

    except:

        return 'Error: Email/ Reg number might not be in the system or This user is not the owner of the vehicle'


#withdraw cash
@app.route('/owner/withdraw', methods=['POST'])
@jwt_required()
def owner_withdraw():
    users = get_jwt_identity()
    owner_ref = users['ref']
    amount = request.json['amount']
    owner_phone = request.json['owner_phone']
    service_charge = int(amount) * (3.5/100)
    amount_received = int(amount) - int(service_charge)
    status = 'Pending'

    if( int(amount) < 0):
        amount = 0
        service_charge = 0
        amount_received = 0        
    

    ref_seed = ['0','1','2','3','4','5','6','7','8','9','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
    random.shuffle(ref_seed)
    ref_seed_empty = "" 
    ref_gen = ref_seed_empty.join(ref_seed)
    mpesa_code = ref_gen[:10]

    x = datetime.datetime.now()
    current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
    current_date = str(current_time)
    created_at = current_date


    conn = sqlite3.connect('database.db')
    conn_sum_withdraws = conn.cursor()
    conn_sum_withdraws.execute("SELECT SUM(amount) from withdraws WHERE owner_ref = '"+ owner_ref +"'")        
    total_withdraws = conn_sum_withdraws.fetchall()
    withdraws = total_withdraws[0][0]

    if(withdraws == None):
        withdraws = 0
      

        
    conn_sum_payments = conn.cursor()
    conn_sum_payments.execute("SELECT SUM(amount) from payments WHERE owner_ref = '"+ owner_ref +"'")
    total_payment = conn_sum_payments.fetchall()
    payment = total_payment[0][0]

        #payment = 100

        
    if(payment == None ):
        payment = 0  
    else: 
        payment = total_payment[0][0]
        

    balance = payment - withdraws
        


    try:
        if(balance >= int(amount) > 0):
            new_owner = Withdraws(mpesa_code, amount, owner_phone,service_charge,amount_received,status,owner_ref,created_at)
            db.session.add(new_owner)
            db.session.commit()
            return " withdraw successful",201
            
        else:
            return 'No enough money to withdraw'

      

        
    except:
        return 'Withdraw failed', 406



#view balance
@app.route('/owner/balance', methods=['GET'])
@jwt_required()
def owner_balance():
    try:
        users = get_jwt_identity()
        ref = users['ref'] 
       
        conn = sqlite3.connect('database.db')
        conn_sum_withdraws = conn.cursor()
        conn_sum_withdraws.execute("SELECT SUM(amount) from withdraws WHERE owner_ref = '"+ ref +"'")
        total_withdraws = conn_sum_withdraws.fetchall()
        withdraws = total_withdraws[0][0]

        if(withdraws == None):
            withdraws = 0
      

        
        conn_sum_payments = conn.cursor()
        conn_sum_payments.execute("SELECT SUM(amount) from payments WHERE owner_ref = '"+ ref +"'")
        total_payment = conn_sum_payments.fetchall()
        payment = total_payment[0][0]

        #payment = 100

        
        if(payment == None ):
            payment = 0  
        else: 
            payment = total_payment[0][0]
        

        balance = payment - withdraws
        
        return jsonify(balance=balance)


    except:

        return 'something went wrong'


#view deposits
@app.route('/owner/all-deposits', methods=['GET'])
@jwt_required()
def owner_all_deposits():
    user = get_jwt_identity()
    owner_ref = user['ref']
    owner_deposits = Payments.query.filter_by(owner_ref=owner_ref).all()

    output =[]
    for owner_deposit in owner_deposits:
            owner_data={}
            owner_data['ref']=owner_deposit.ref
            owner_data['reg_no']=owner_deposit.reg_no
            owner_data['amount']=owner_deposit.amount
            owner_data['created_at']=owner_deposit.created_at
            output.append(owner_data)

    return jsonify({"owner_deposits":output})



#view withdraws
@app.route('/owner/all-withdraws', methods=['GET'])
@jwt_required()
def owner_all_withdraws():
    user = get_jwt_identity()
    owner_ref = user['ref']
    owner_withdraws = Withdraws.query.filter_by(owner_ref=owner_ref).all()

    output =[]
    for owner_withdraw in owner_withdraws:
            owner_data={}
            owner_data['mpesa_code']=owner_withdraw.mpesa_code
            owner_data['owner_phone']=owner_withdraw.owner_phone
            owner_data['amount']=owner_withdraw.amount
            owner_data['service_charge']=owner_withdraw.service_charge
            owner_data['amount_received']=owner_withdraw.amount_received
            owner_data['status']=owner_withdraw.status
            owner_data['created_at']=owner_withdraw.created_at
            output.append(owner_data)

    return jsonify({"owner_withdraws":output})



#view payments per vehicle
@app.route('/owner/vehicle/payment/<id>', methods=['GET'])
@jwt_required()
def owner_all_payments_per_vehicle(id):
    try:
        user = get_jwt_identity()
        owner_ref = user['ref']
        vehicle = Vehicles.query.filter_by(id=id,owner_ref=owner_ref).first()
        reg_no=vehicle.reg_no
        owner_deposits = Payments.query.filter_by(owner_ref=owner_ref,reg_no=reg_no ).all()

        output =[]
        for owner_deposit in owner_deposits:
                owner_data={}
                owner_data['ref']=owner_deposit.ref
                owner_data['reg_no']=owner_deposit.reg_no
                owner_data['amount']=owner_deposit.amount
                owner_data['created_at']=owner_deposit.created_at
                output.append(owner_data)

        return jsonify({"vehicle_payments":output})

    except:
        return 'Something went wrong'




#=======================================#
#   CREW: 
#             register ...|
#             login ...|
#             forget password ...|
#             reset password ...|
#             view profile ...|
#             edit profile ...|
#             view payments per vehicle [7 days, 30 days, all] ...|
#             create bookmark ...|
#             view bookmark ... |
#             delete bookmark
#             enter payment userphone number and amount ... |
#========================================# 


#cew register
@app.route('/crew/register', methods=['POST'])
def crew_register():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    phone = request.json['phone']
    password = request.json['password']
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    ref_seed = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
    random.shuffle(ref_seed)
    ref_seed_empty = "" 
    ref_gen = ref_seed_empty.join(ref_seed)
    ref = ref_gen[:5]

    x = datetime.datetime.now()
    current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
    current_date = str(current_time)
    created_at = current_date


    try:
        new_crew = Crew(first_name,last_name, email, phone, ref, password_hashed, created_at)
        db.session.add(new_crew)
        db.session.commit()

        user_profile = Crew.query.filter_by(email=email).first()
        access_token = create_access_token(identity={"ref": user_profile.ref})

        return {"access_token":access_token},201
    except:
        return 'Email already exists', 406


#crew login
@app.route('/crew/login', methods=['POST'])
def crew_login():  
   
    try:
        email = request.json['email']
        password = request.json['password']
        user_profile = Crew.query.filter_by(email=email).first()
        password_hash = bcrypt.checkpw(password.encode('utf-8'), user_profile.password)

        if(password_hash == True):
            
            access_token = create_access_token(identity={"ref": user_profile.ref})

            return {"access_token":access_token}, 200

        else:

            return 'Authentication failed', 400    
    except:
        return 'Something went wrong', 409


#crew forget password
@app.route('/crew/forgot-password', methods=['PUT'])
def crew_forgot_password():
    try:
        email = request.json['email']
        user_email = Crew.query.filter_by(email=email).first()
        email=user_email.email
        e = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        random.shuffle(e)
        easy_password = "" 
        password_gen = easy_password.join(e)
        password = password_gen[:7]
        password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user_email.password = password_hashed
        db.session.commit()  
 
            
        return  (password) , 200
        #return jsonify(email=user_email.email)

    except:
        return 'Email does not exist'



#crew change password
@app.route('/crew/change-password', methods=['PUT'])
@jwt_required()
def crew_edit_password():
    try:
        users = get_jwt_identity()
        ref = users['ref'] 
        user = Crew.query.filter_by(ref=ref).first()
        new_password = request.json['new_password']
        confirm_password = request.json['confirm_password']

        if(new_password == confirm_password):
            password_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.password = password_hashed
            db.session.commit()
            return 'Password Successfully Changed'
        else:
            return 'Error: Passwords do not match'
    except:
        return 'login to change password'



#crew profile
@app.route('/crew/profile', methods=['GET'])
@jwt_required()
def crew_profile():
    try:
        users = get_jwt_identity()
        ref = users['ref'] 
        user = Crew.query.filter_by(ref=ref).first()

        #return session["user_id"]
    
        return jsonify(        
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone, 
            email=user.email  
            )
    except:
        return 'Please login'



#crew edit names
@app.route('/crew/edit', methods=['PUT'])
@jwt_required()
def crew_edit_names():
    try:
        users = get_jwt_identity()
        ref = users['ref'] 
        user = Crew.query.filter_by(ref=ref).first()
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        user.first_name = first_name
        user.last_name = last_name
        db.session.commit()
        return 'record updated'
    except:
        return 'login to edit profile'



#crew create bookmark
@app.route('/crew/bookmark', methods=['POST'])
@jwt_required()
def crew_create_bookmark():
    try:
        users = get_jwt_identity()
        crew_ref = users['ref'] 
        reg_no= request.json['reg_no']
        alias = request.json['alias']

        x = datetime.datetime.now()
        current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
        current_date = str(current_time)
        created_at = current_date
        
        vehicle_search = Vehicles.query.filter_by(reg_no=reg_no).first()
        vehicle_reg = vehicle_search.reg_no
        #if(vehicle_search.ref_no == reg_no):

        new_bookmark = CrewBookmarks(reg_no, alias, crew_ref, created_at)
        db.session.add(new_bookmark)
        db.session.commit()

        return 'Bookmark successful'
    except:
        return 'Vehicle Registration number no in the system'


#crew view bookmarks -all
@app.route('/crew/bookmark', methods=['GET'])
@jwt_required()
def crew_view_all_bookmark():
    try:
        users = get_jwt_identity()
        crew_ref = users['ref'] 
        
        bookmarks = CrewBookmarks.query.filter_by(crew_ref=crew_ref).all()

        output =[]
        for bookmark in bookmarks:
            bookmark_data={}
            bookmark_data['reg_no']=bookmark.reg_no
            bookmark_data['alias']=bookmark.alias
           
            output.append(bookmark_data)

        return jsonify({"bookmarks":output})

    except:
        return 'Vehicle Registration number no in the system'


#crew view all payments
@app.route('/crew/payments', methods=['GET'])
@jwt_required()
def crew_view_all_payments():
    try:
        users = get_jwt_identity()
        crew_ref = users['ref'] 
        
        payments = Payments.query.filter_by(crew_ref=crew_ref).all()

        output =[]
        for payment in payments:
            payment_data={}
            payment_data['ref']=payment.ref
            payment_data['reg_no']=payment.reg_no
            payment_data['amount']=payment.amount
            payment_data['created_at']=payment.created_at
           
            output.append(payment_data)

        return jsonify({"payments":output})

    except:
        return 'Vehicle Registration number no in the system'


#crew view all payments per vehicle
@app.route('/crew/payment/<id>', methods=['GET'])
@jwt_required()
def crew_view_all_payments_per_vehicle(id):
    try:
        users = get_jwt_identity()
        crew_ref = users['ref'] 
        bookmark = CrewBookmarks.query.filter_by(id=id).first()
        reg_no = bookmark.reg_no

        payments = Payments.query.filter_by(crew_ref=crew_ref, reg_no=reg_no ).all()

        output =[]
        for payment in payments:
            payment_data={}
            payment_data['ref']=payment.ref
            payment_data['reg_no']=payment.reg_no
            payment_data['amount']=payment.amount
            payment_data['created_at']=payment.created_at
           
            output.append(payment_data)

        return jsonify({"payments":output})

    except:
        return 'Vehicle Registration number no in the system'



#crew view bookmark
@app.route('/crew/bookmark/<id>', methods=['GET'])
@jwt_required()
def crew_view_bookmark(id):
    try:
        users = get_jwt_identity()
        crew_ref = users['ref'] 


        bookmark = CrewBookmarks.query.filter_by(id=id).first()
        bookmark_reg = bookmark.reg_no
        bookmark_alias = bookmark.alias

        return jsonify(
            crew_ref=crew_ref,
            reg_no = bookmark_reg,
            alias =bookmark_alias
        )
    except:
        return 'login to change password'


#crew collect payment using bookmark
@app.route('/crew/bookmark/<id>', methods=['POST'])
@jwt_required()
def crew_add_payment_using_bookmark(id): 
    try:
        users = get_jwt_identity()
        bookmark = CrewBookmarks.query.filter_by(id=id).first()
        reg_no = bookmark.reg_no
        crew_ref = bookmark.crew_ref


        amount = request.json['amount']
        pass_phone = request.json['pass_phone']
        
        ref_seed = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
        random.shuffle(ref_seed)
        ref_seed_empty = "" 
        ref_gen = ref_seed_empty.join(ref_seed)
        ref = ref_gen[:5]


        x = datetime.datetime.now()
        current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
        current_date = str(current_time)
        created_at = current_date


        

        owner = Vehicles.query.filter_by(reg_no=reg_no).first()
        owner_ref = owner.owner_ref
        

        conn = sqlite3.connect('database.db')
        conn_sum_topups = conn.cursor()
        conn_sum_topups.execute("SELECT SUM(amount) from topups WHERE  pass_phone = '"+ pass_phone +"'")
        total_topups = conn_sum_topups.fetchall()
        topup = total_topups[0][0]

    

        conn_sum_payments = conn.cursor()
        conn_sum_payments.execute("SELECT SUM(amount) from payments WHERE pass_phone = '"+ pass_phone +"'")
        total_payment = conn_sum_payments.fetchall()
        payment = total_payment[0][0]

        total_balance = int(topup) - int(payment)
        #"""
        if (total_balance >= int(amount) > 0):
             new_payment = Payments(ref,reg_no, amount, pass_phone, crew_ref,owner_ref, created_at)
             db.session.add(new_payment)
             db.session.commit()

             return 'Payment successful'
            
        else:

            return 'No enough money in wallet'
        #"""
        #return str(total_balance)
    except:
        return 'Error: Phone Number or Registration number is not in the system'




#crew view payments per vehicle all




#crew view  payments per vehicle 7 days



#crew view payments per vehicle 30 days




if __name__ == "__main__":
    
    app.run(debug=True)
