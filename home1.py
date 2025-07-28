from flask import *
from flask_mysqldb import MySQL
from datetime import datetime
import MySQLdb.cursors
import re
from fpdf import FPDF
date=datetime.now()

app=Flask(__name__)
app.secret_key="SHRI"



app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='mysql'
app.config['MYSQL_DB']='dairy_project'
app.config['MYSQL_PORT']=3307

mysql=MySQL(app)

l=datetime.today()
now=l.strftime('%Y-%m-%d')

@app.route('/404.html')
def home():
	return render_template("404.html")

@app.route('/index.html')
def index():
	l=datetime.today()
	print(l.strftime('%Y-%m-%d'))
	# now=datetime.strptime(l, '%Y-%m-%d')
	# print(now)
	return render_template("index.html")

@app.route('/product.html')
def product():
	return render_template("product.html")

@app.route('/contact.html')
def contact():
	return render_template("contact.html")

@app.route('/about.html')
def about():
	return render_template("about.html")

@app.route('/gallery.html')
def gallery():
	return render_template("gallery.html")

@app.route('/service.html')
def service():
	return render_template("service.html")

@app.route('/login.html', methods=['GET','POST'])
def login():
		msg=''
		if request.method == "POST" and 'phone' in request.form and 'password' in request.form:
			session['phone']=request.form['phone']
			session['password']=request.form['password']

			phone=session['phone']
			password=session['password']

			cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			if cursor.execute("SELECT * FROM dairy_project.register WHERE phone=%s AND password=%s AND cust_type='sell'", (phone,password)):
				data=cursor.fetchone()
				if data:
					session['loggedin']=True
					session['phone']=data['phone']
					msg='Logged in Successfully !!'
					return redirect(url_for('selldashboard'))
				else:
					msg="Incorrect username/password !! "
			elif cursor.execute("SELECT * FROM dairy_project.register WHERE phone=%s AND password=%s AND cust_type='buy'", (phone,password)):
				data=cursor.fetchone()
				if data:
					session['loggedin']=True
					session['phone']=data['phone']
					msg='Logged in Successfully !!'
					return redirect(url_for('buydashboard'))
				else:
					msg="Incorrect username/password !! "

			elif cursor.execute("SELECT * FROM dairy_project.adminregister WHERE phone=%s AND password=%s", (phone,password)):
				data=cursor.fetchone()
				if data:
					session['loggedin']=True
					session['phone']=data['phone']
					msg='Logged in Successfully !!'
					return redirect(url_for('admindashboard'))
				else:
					msg="Incorrect username/password !! "
		return render_template('login.html',msg=msg)


@app.route('/forget.html',methods=['GET','POST'])
def forget():
    if request.method =='POST' and 'phone' in request.form and 'password' in request.form:
        print('hi')
        phone = request.form['phone']
        password = request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from dairy_project.register where phone=%s",(phone,))
        account=cursor.fetchone()
        print('hi')
        if account:
            cursor.execute("update dairy_project.register set password=%s where phone=%s" ,(password,phone,))
            mysql.connection.commit()
            return redirect(url_for('login'))
        else:
            msg='Incorrect user id / password !'
    return render_template('forget.html')

@app.route('/selldashboard.html')
def selldashboard():
	phone=session['phone']
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * FROM register WHERE phone=%s and cust_type='sell' ",(phone,))
	user=cursor.fetchall()

	session['user']=user
	print(user)
	name=user[0][1]
	cursor.execute("SELECT round(SUM(amount),2) as sum1, round(SUM(quantity),2) as sum2 FROM dairy_project.collection WHERE userid=%s",(user[0][0],))
	collection=cursor.fetchall()
	# (0.166, 2)
	milk=(collection[0][0])
	quan=(collection[0][1])
	print(collection)
	cursor.execute("SELECT  round(SUM(amount),0)  as sum2 FROM dairy_project.cattlefeedsell WHERE userid=%s",(user[0][0],))
	cattlefeed=cursor.fetchall()
	print(cattlefeed)
	cursor.execute("SELECT round(SUM(advance),0) as sum2 FROM dairy_project.advance_entry WHERE userid=%s",(user[0][0],))
	advance=cursor.fetchall()
	print(advance)
	cursor.close()
	return render_template('selldashboard.html',milk=milk,quan=quan,cattle=cattlefeed[0][0],advn=advance[0][0])

@app.route('/customerprofile.html', methods=["POST","GET"])
def customerprofile():
	user=session['user']
	userid=user[0][0]
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * from dairy_project.register where userid=%s",(userid,))
	user=cursor.fetchall()
	return render_template('customerprofile.html',data=user)

@app.route('/updatecust1.html', methods=['POST','GET'])
def updatecust1():
	user=session['user']
	userid=user[0][0]
	print('hii')
	data1=''
	if request.method =="POST" and 'cname' in request.form:
		cname=request.form['cname']
		address=request.form['address']
		print('hello')
		# print(name)
		cursor=mysql.connection.cursor()
		cursor.execute("UPDATE dairy_project.register SET name=%s, address=%s where userid=%s",(cname,address,userid,))
		cursor.connection.commit()
		cursor.execute("SELECT * from dairy_project.register where userid=%s",(userid,))
		data1=cursor.fetchall()
	return redirect(url_for('customerprofile'))

@app.route('/custregister.html', methods=["POST","GET"])
def custregister():
	l=datetime.today()
	now=l.strftime('%Y-%m-%d')
	msg=''
	phone=session['phone']
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT userid FROM register WHERE phone=%s",(phone,))
	data1=cursor.fetchone()
	
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * FROM collection WHERE userid=%s",(data1,))
	data=cursor.fetchall()
	return render_template('custregister.html',data=data,msg=msg)

@app.route('/date.html', methods=['POST','GET'])
def date():
	msg=''
	collectiondata=''
	phone=session['phone']
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT userid FROM register WHERE phone=%s",(phone,))
	data1=cursor.fetchone()
	
	# if request.method == 'POST':
	# 	msg='Please fill out the form'

	if request.method == 'POST' and 'from_date' in request.form and 'to_date' in request.form:
		session['from_date']=request.form['from_date']
		session['to_date']=request.form['to_date']

		from_date=session['from_date']
		to_date=session['to_date']
		cursor=mysql.connection.cursor()
		cursor.execute("SELECT * FROM collection WHERE userid=%s and day between %s and %s",(data1,from_date,to_date))
		collectiondata=cursor.fetchall()
		session['collectiondata']=collectiondata
	return render_template('custregister.html',data=collectiondata,msg=msg)

@app.route('/buydashboard.html')
def buydashboard():
	phone=session['phone']
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * FROM register WHERE phone=%s and cust_type='buy' ",(phone,))
	user=cursor.fetchall()

	session['user']=user
	print(user)
	name=user[0][1]
	cursor.execute("SELECT round(SUM(amount),2) as sum1, round(SUM(quantity),2) as sum2 FROM dairy_project.selling WHERE userid=%s",(user[0][0],))
	collection=cursor.fetchall()
	milk=(collection[0][0])
	quan=(collection[0][1])
	print(collection)
	cursor.close()
	return render_template('buydashboard.html',name=name,milk=milk,quan=quan)

@app.route('/buycustprofile.html', methods=["POST","GET"])
def buycustprofile():
	user=session['user']
	userid=user[0][0]
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * from dairy_project.register where userid=%s",(userid,))
	user=cursor.fetchall()
	return render_template('buycustprofile.html',data=user)


@app.route('/updatecust.html', methods=['POST','GET'])
def updatecust():
	user=session['user']
	userid=user[0][0]
	print('hii')
	data1=''
	if request.method =="POST" and 'cname' in request.form:
		cname=request.form['cname']
		address=request.form['address']
		print('hello')
		# print(name)
		cursor=mysql.connection.cursor()
		cursor.execute("UPDATE dairy_project.register SET name=%s, address=%s where userid=%s",(cname,address,userid,))
		cursor.connection.commit()
		cursor.execute("SELECT * from dairy_project.register where userid=%s",(userid,))
		data1=cursor.fetchall()
	return redirect(url_for('buycustprofile'))


@app.route('/custadvance.html',methods=['POST','GET'])
def custadvance():
	user=session['user']
	userid=user[0][0]
	print('hii')
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * from dairy_project.advance_entry where userid=%s",(userid,))
	advance1=cursor.fetchall()
	cursor.execute("SELECT * from dairy_project.advance where userid=%s",(userid,))
	advance2=cursor.fetchall()
	return render_template('custadvance.html',data=advance1,data1=advance2)

@app.route('/custcattlefeed.html',methods=['POST','GET'])
def custcattlefeed():
	user=session['user']
	userid=user[0][0]
	print('hii')
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * from dairy_project.cattlefeedsell where userid=%s",(userid,))
	cattle1=cursor.fetchall()
	cursor.execute("SELECT * from dairy_project.cattlefeed where userid=%s",(userid,))
	cattle2=cursor.fetchall()
	return render_template('custcattlefeed.html',data=cattle1,data1=cattle2)

@app.route('/buycustregister.html', methods=["POST","GET"])
def buycustregister():
	l=datetime.today()
	now=l.strftime('%Y-%m-%d')
	msg=''
	phone=session['phone']
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT userid FROM register WHERE phone=%s",(phone,))
	data1=cursor.fetchone()
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * FROM selling WHERE userid=%s",(data1,))
	data=cursor.fetchall()
	return render_template('buycustregister.html',data=data,msg=msg)

@app.route('/buycust.html',methods=['POST','GET'])
def buycust():
	phone=session['phone']
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT userid FROM register WHERE phone=%s",(phone,))
	data1=cursor.fetchone()
	
	if request.method=="POST":
		session['from_date']=request.form['from_date']
		session['to_date']=request.form['to_date']

		from_date=session['from_date']
		to_date=session['to_date']

		cursor.execute("SELECT * FROM selling WHERE userid=%s and day between %s and %s",(data1,from_date,to_date))
		data=cursor.fetchall()
	return render_template('buycustregister.html',data=data)



# @app.route('/customerbill2.html', methods=["POST","GET"])
# def buycustbill():
# 	phone=session['phone']
# 	cursor=mysql.connection.cursor()
# 	cursor.execute("SELECT userid FROM register WHERE phone=%s",(phone,))
# 	data=cursor.fetchone()
# 	# data=data[0]
# 	# print(data)
# 	if request.method=="POST" and "from_date" in request.form and 'to_date' in request.form:
# 		session['from_date']=request.form['from_date']
# 		session['to_date']=request.form['to_date']
# 		from_date=session['from_date']
# 		to_date=session['to_date']	
# 	return render_template('buycustbill.html')


# @app.route('/bothdashboard.html')
# def bothdashboard():
# 	phone=session['phone']
# 	cursor=mysql.connection.cursor()
# 	cursor.execute("SELECT * FROM register WHERE phone=%s and cust_type='both' ",(phone,))
# 	data=cursor.fetchall()

# 	session['data']=data
# 	cursor.close()
# 	return render_template('bothdashboard.html')


@app.route('/register.html', methods=['GET','POST'])
def register():
	l=datetime.today()
	now=l.strftime('%Y-%m-%d')
	msg=''
	reduction=0
	balance_amount=0
	bal=0
	if request.method == "POST" and 'name' in request.form and 'address' in request.form and 'pincode' in request.form  and 'phone' in request.form and  'cust_type' in request.form and 'password' in request.form:
		details=request.form
		session['name']=details['name']
		session['address']=details['address']
		session['pincode']=details['pincode']
		session['phone']=details['phone']
		session['cust_type']=details['cust_type']
		session['password']=details['password']

		name=session["name"]
		address=session["address"]
		pincode=session["pincode"]
		phone=session["phone"]
		cust_type=session["cust_type"]
		password=session["password"]

		cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM dairy_project.register WHERE phone=%s AND password=%s',(phone, password))
		data=cursor.fetchone()
		if data:
			msg="Account Already Exists !!"
		elif  not name or not address or not pincode  or not phone or not cust_type or not password:
			msg="Please Fill Out The Form !!"
		elif not re.match(r'[0-9]+',phone):
			msg = 'Mobile No must contain only  numbers !'
		else:

			cursor.execute('INSERT INTO dairy_project.register VALUES(null,%s,%s, %s, %s, %s, %s)',(name,address,pincode,phone,cust_type,password))
			cursor.execute('INSERT INTO dairy_project.advance VALUES(%s,null,%s, %s)',(now,reduction,balance_amount,))
			cursor.execute('INSERT INTO dairy_project.cattlefeed VALUES(%s,null,%s,%s)',(now,reduction,balance_amount,))
			mysql.connection.commit()
			msg='You have Successfully Registered'
			return redirect (url_for('login'))
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html',msg=msg)	


app.route('/logout.html')
def logout():
	session.pop('loggedin',None)
	session.pop('phone',None)
	session.pop('password',None)
	return redirect(url_for('login'))


@app.route('/collection.html',methods=['POST','GET'])
def collection():
	rate=0
	amount=0
	snf=0
	fat=0
	quantity=0
	l=datetime.today()
	now=l.strftime('%Y-%m-%d')

	user=''
	msg=''

	day=session.get('day')
	userid3=session.get('userid3') 
	daytime=session.get('daytime')
	milk_type=session.get('milk_type')
	snf=session.get('snf')
	degree=session.get('degree')
	rate=session.get('rate')
	amount=session.get('amount')
	fat=session.get('fat')
	quantity=session.get('quantity')
	print("Q=",quantity)
	print("Q=",fat)
	print("Q=",snf)
	print(rate)
	print(amount)

	if userid3==None or quantity==None or fat==None or snf==None or degree==None or rate==None or amount==None or day==None or daytime==None or milk_type==None:
		msg="Please Fill The form"
		# flash('Please Fill The Form')

	else:
		cursor=mysql.connection.cursor()
		cursor.execute("INSERT INTO dairy_project.collection VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(day,userid3,daytime,milk_type,quantity,fat,snf,degree,rate,amount))
		mysql.connection.commit()
		session.pop('user', None)
		session.pop('quantity', None)
		session.pop('userid3', None)
		session.pop('fat', None)
		session.pop('snf', None)
		session.pop('degree', None)
		session.pop('rate', None)
		session.pop('amount', None)
		session.pop('ans', None)				
	return render_template('collection.html',user=user,rate=rate,amount=amount,now=now,msg=msg)

@app.route('/greet1', methods=['POST','GET'])
def greet():
	# n=''
	if 'userid' in request.form:
		session['userid3'] = request.form['userid']
		userid3=session['userid3']
		print(userid3)
		cursor=mysql.connection.cursor()
		cursor.execute("SELECT * FROM dairy_project.register WHERE userid=%s AND cust_type='sell' ",(userid3,))
		user=cursor.fetchall()
		print(user)
		user=user[0][1]
		session['user']=user
		return jsonify(message1=f'{user}')
	return '', 400

@app.route('/greet4', methods=['POST','GET'])
def greet4():
	# n=''
	if 'day' in request.form and 'daytime' in request.form and 'milk_type' in request.form and 'snf' in request.form and 'fat' in request.form and 'quantity' in request.form and 'degree' in request.form:
		session['day']=request.form['day']
		session['daytime']=request.form['daytime']
		session['milk_type']=request.form['milk_type']
		session['snf'] = request.form['snf']
		session['degree'] = request.form['degree']
		session['fat'] = request.form['fat']
		session['quantity'] = request.form['quantity']

		quantity=session['quantity']
		fat=session['fat']
		degree=session['degree']
		snf=session['snf']
		milk_type=session['milk_type']
		day=session['day']
		daytime=session['daytime']

		print(milk_type)

		fat1=[]
		snf1=[]
		cow_rate1=[]
		buffallo_rate1=[]
		cursor=mysql.connection.cursor()
		cursor.execute("SELECT * FROM dairy_project.snfpurchase")
		data=cursor.fetchall()
		# print(type(data))
		def add_values_in_dict(sample_dict, key, list_of_values):
			if key not in sample_dict:
				sample_dict[key] = list()
			sample_dict[key].extend(list_of_values)
			return sample_dict
		for i,a in enumerate(data):
			for i,b in enumerate(a):
				if i==1:
					fat1.append(b)
				elif i==2:
					snf1.append(b)
				elif i==3:
					cow_rate1.append(b)
				elif i==4:
					buffallo_rate1.append(b)		
	
		bill={}
		t=0
		for i in range(len(fat1)):
			if  milk_type=="cow":
				f=fat1[i]
				s=snf1[i]
				k=[f,s]
				# print(k)
				m=(cow_rate1[i])

			elif  milk_type=="buffallo":
				print(milk_type)
				f=fat1[i]
				s=snf1[i]
				k=[f,s]
				# print(k)
				m=(buffallo_rate1[i])
			else:
				m=0
				k=0

			ms=str(m)
			alpha=str(i)
			mp=ms+'*'+alpha
			bill = add_values_in_dict(bill, (mp), (k))

		c3=float(fat)
		c4=float(snf)
		print(c3)
		print(c4)
	# Get list of keys that contains the given value
		list_of_keys = [key for key, list_of_values in bill.items() if c3 in list_of_values if c4 in list_of_values]
		if list_of_keys:
			print("list:-",list_of_keys)
		else:
			print('Value does not exist in the dictionary')
		ans=list_of_keys[0]
		if ans[4]=='*':
			ans=ans[0:4]
		else:
			ans=ans[0:5]

		ans=float(ans)
		rate=ans
		print(ans)
		session['rate']=rate
		rate=session['rate']

		amount=float(ans)*float(quantity)

		session['amount']=amount 
		amount=session['amount']
		print("answer:-",ans)
		return jsonify(message4=f'{ans}',message5=f'{amount}')
	return '', 400


@app.route('/greet6', methods=['POST','GET'])
def greet6():
	# n=''
	if 'userid' in request.form:
		session['userid'] = request.form['userid']
		userid1=session['userid']
		print(userid1)
		cursor=mysql.connection.cursor()
		cursor.execute("SELECT * FROM dairy_project.register WHERE userid=%s AND cust_type='buy' ",(userid1,))
		user=cursor.fetchall()
		user=user[0][1]
		session['user']=user
		return jsonify(message7=f'{user}')
	return '', 400

@app.route('/selling.html',methods=['POST','GET'])
def selling():
	user=''
	msg=''
	amount=''
	data=''
	rate=0
	day=session.get('day')
	userid1=session.get('userid')
	daytime=session.get('daytime')
	milk_type=session.get('milk_type')
	quantity=session.get('quantity')
		
	if quantity==None or day==None or userid1==None or daytime==None or milk_type==None:
			msg="Please Fill The form"
	else:
		cursor=mysql.connection.cursor()
		cursor.execute("SELECT * FROM dairy_project.local_milk_rate")
		data=cursor.fetchall()
		if milk_type=="buffallo":
			rate=data[0][3]
		elif milk_type=="cow":
			rate=data[0][2]
		print(rate)
		amount=float(rate)*float(quantity)
		cursor.execute("INSERT INTO dairy_project.selling VALUES(%s,%s,%s,%s,%s,%s,%s)",(day,userid1,daytime,milk_type,quantity,rate,amount))
		mysql.connection.commit()
		session.pop('day', None)
		session.pop('userid1', None)
		session.pop('daytime', None)
		session.pop('milk_type', None)
		session.pop('quantity', None)
		session.pop('rate', None)
		session.pop('amount', None)
	return render_template('selling.html',msg=msg,now=now)


@app.route('/greet7', methods=['POST','GET'])
def greet7():
	if request.method=='POST' and  'day' in request.form and 'daytime' in request.form and 'milk_type' in request.form and 'quantity' in request.form:
		print("hiii")
		session['day']=request.form['day']
		session['daytime']=request.form['daytime']
		session['milk_type']=request.form['milk_type']
		session['quantity'] = request.form['quantity']

		quantity=session['quantity']
		day=session['day']
		userid1=session['userid']
		daytime=session['daytime']
		milk_type=session['milk_type']
		print(day)
		print(userid1)
		print(daytime)
		print(milk_type)
		print(quantity)

		cursor=mysql.connection.cursor()
		cursor.execute("SELECT * FROM dairy_project.local_milk_rate")
		data=cursor.fetchall()
		if milk_type=="buffallo":
			rate=data[0][3]
		elif milk_type=="cow":
			rate=data[0][2]
		print(rate)
		amount=float(rate)*float(quantity)
		return jsonify(message8=f'{rate}',message9=f'{amount}')
	return '', 400

@app.route('/bill1', methods=['POST','GET'])
def bill1():
	if request.method=="POST" and "from_date" in request.form and 'to_date' in request.form and 'data' in request.form:
		session['from_date']=request.form['from_date']
		session['to_date']=request.form['to_date']
		session['data']=request.form['data']
		from_date=session['from_date']
		to_date=session['to_date']
		data=session['data']
		
		
		cursor1=mysql.connection.cursor()
		print(data)
		cursor1.execute("SELECT userid,SUM(amount) as sum,SUM(quantity) as sum1 FROM dairy_project.collection WHERE (day between %s and %s) and userid=%s",(from_date,to_date,data))
		data_collection=cursor1.fetchall()
		print(data_collection)
		collection=data_collection[0][1]
		quantity1=data_collection[0][2]

		cursor=mysql.connection.cursor()
		cursor.execute('SELECT reduction,balance_amount FROM dairy_project.advance WHERE userid=%s',(data,))
		data_advance1=cursor.fetchall()
		# print(data_advance1)
		reduct_advance=data_advance1[0][0]
		bal_advance=data_advance1[0][1]
		if reduct_advance>=bal_advance:
			cursor.execute('SELECT userid,balance_amount FROM dairy_project.advance WHERE userid=%s',(data,))
			data_advance2=cursor.fetchall()
			advance=data_advance2[0][1]
			if advance==None:
				advance=0
			else:
				advance=float(advance)
		else:
			cursor.execute('SELECT userid,reduction FROM dairy_project.advance WHERE userid=%s',(data,))
			data_advance2=cursor.fetchall()
			advance=data_advance2[0][1]
			if advance==None:
				advance=0
			else:
				advance=float(advance)	

		cursor=mysql.connection.cursor()
		cursor.execute('SELECT reduction,bal FROM dairy_project.cattlefeed WHERE userid=%s',(data,))
		data_cattle1=cursor.fetchall()
		# print(data_cattle1)
		reduct_cattle=data_cattle1[0][0]
		bal_cattle=data_cattle1[0][1]
		if reduct_cattle>=bal_cattle:
			cursor.execute('SELECT userid,bal  FROM dairy_project.cattlefeed WHERE userid=%s',(data,))
			data_cattle2=cursor.fetchall()
			cattle=data_cattle2[0][1]
			if cattle==None:
				cattle=0
			else:
				cattle=float(cattle)
		else:
			cursor.execute('SELECT userid, reduction FROM dairy_project.cattlefeed WHERE  userid=%s',(data,))
			data_cattle2=cursor.fetchall()
			cattle=data_cattle2[0][1]
			if cattle==None:
				cattle=0
			else:
				cattle=float(cattle)


		quantity1=round(quantity1,2)
		print(quantity1)
		collection=round(collection,2)
		advance=round(advance,0)
		cattle=round(cattle,0)
		total=float(collection)-((advance)+(cattle))
		total=round(total,0)

		cursor.execute("SELECT * FROM dairy_project.register WHERE userid=%s",(data,))
		info=cursor.fetchall()
		print(info)
		name=info[0][1]
		address=info[0][2]
		userid=info[0][0]
		phone=info[0][4]

		return jsonify(quantity1=f'{quantity1}',bill=f'{collection}',total=f'{total}',feed=f'{cattle}',advance=f'{advance}',name=f'{name}',address=f'{address}',userid=f'{userid}',phone=f'{phone}',from_date=f'{from_date}',to_date=f'{to_date}')
	return '', 400

@app.route('/customerbill1.html', methods=['POST','GET'])
def collectionbill():
	data=session.get('data')
	from_date=session.get('from_date')
	to_date=session.get('to_date')
	if request.method=="POST":
		# print("t=",total)
		print("hii")
		cursor=mysql.connection.cursor()
		cursor.execute('SELECT reduction,balance_amount FROM dairy_project.advance WHERE userid=%s',(data,))
		data4=cursor.fetchall()
		print(data4)
		reduct=data4[0][0]
		bal=data4[0][1]
		if reduct>bal:
			print(data4)
			cursor.execute("UPDATE dairy_project.advance SET dairy_project.advance.balance_amount=dairy_project.advance.balance_amount-dairy_project.advance.balance_amount, dairy_project.advance.reduction=0 where userid=%s",(data,))
			mysql.connection.commit()
		else:
			print(data4)
			cursor.execute("UPDATE dairy_project.advance SET dairy_project.advance.balance_amount=dairy_project.advance.balance_amount-dairy_project.advance.reduction where userid=%s",(data,))
			mysql.connection.commit()
	return render_template('sellcustbill.html',from_date=from_date,to_date=to_date)

@app.route('/bill2', methods=['POST','GET'])
def bill2():
	msg=''
	
	if  request.method=="POST" and "from_date" in request.form and 'to_date' in request.form and 'data' in request.form:
		session['from_date']=request.form['from_date']
		session['to_date']=request.form['to_date']
		session['data']=request.form['data']
		from_date=session['from_date']
		to_date=session['to_date']
		data=session['data']
			
		
		cursor1=mysql.connection.cursor()
		print(data)
		cursor1.execute("SELECT userid, SUM(amount) as sum, SUM(quantity) as sum1 FROM dairy_project.selling WHERE (day between %s and %s) and userid=%s",(from_date,to_date,data))
		data_selling=cursor1.fetchall()
		print(data_selling)
		selling=data_selling[0][1]
		quantity=round(data_selling[0][2],2)
		cursor1.execute("SELECT * FROM dairy_project.register WHERE userid=%s",(data,))
		info=cursor1.fetchall()
		print(info)
		name=info[0][1]
		address=info[0][2]
		userid=info[0][0]
		phone=info[0][4]

		print("selling:-",selling)
		total=round(float(selling),0)
		print("total",total)

		return jsonify(quantity=f'{quantity}',bill=f'{total}',name=f'{name}',address=f'{address}',userid=f'{userid}',phone=f'{phone}',from_date=f'{from_date}',to_date=f'{to_date}')
	return '', 400

@app.route('/customerbill2.html', methods=['POST','GET'])
def sellingbill():
	return render_template('buycustbill.html')

@app.route('/sanghrate.html',methods=["POST","GET"])
def sanghrate():
	if request.method=="POST":
		day=request.form['day']
		fat=request.form['fat']
		SNF=request.form['SNF']
		cow_rate=request.form['cow_rate']
		buffallo_rate=request.form['buffallo_rate']

		cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("INSERT INTO dairy_project.sanghrate VALUES(%s,%s,%s,%s,%s)",(day,fat,SNF,cow_rate,buffallo_rate))
		mysql.connection.commit()
		cursor.close()	
	return render_template('sanghrate.html')	

@app.route('/customer_rate.html',methods=["POST","GET"])
def customer_rate():
	l=datetime.today()
	now=l.strftime('%Y-%m-%d')
	data=''
	data=''
	# f=0
	# s=0
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * FROM dairy_project.snfpurchase")
	data=cursor.fetchall()
	# print("b=",m)
	# for m in range(10):
	# 	fat=data[m][1]
	# 	print('f=',f)
	# 	snf=data[m][2]
	# 	print('s=',s)
	if request.method=="POST"  and 'cow_rate' in request.form and 'buffallo_rate' in request.form:

		day=request.form['day']
		cow_rate=request.form['cow_rate']
		buffallo_rate=request.form['buffallo_rate']
		fat=request.form['fat']
		SNF=request.form['SNF']
		print(fat)
		print(SNF)
		print(cow_rate)
		print(buffallo_rate)
		cursor=mysql.connection.cursor()
		cursor.execute("UPDATE dairy_project.SNFpurchase SET dairy_project.SNFpurchase.day=%s, dairy_project.SNFpurchase.cow_rate=%s, dairy_project.SNFpurchase.buffallo_rate=%s where cast(dairy_project.SNFpurchase.fat as decimal(5,1))=%s and cast(dairy_project.SNFpurchase.SNF as decimal(5,1))=%s",(day,cow_rate,buffallo_rate,fat,SNF,))
		mysql.connection.commit()
		cursor.execute("SELECT * FROM dairy_project.snfpurchase")
		data=cursor.fetchall()
		print(len(data))
		cursor.close()
	return render_template('customer_rate.html',data=data,now=now)


@app.route('/data',methods=["POST","GET"])
def data():
	ans=''
	c4=0
	c3=0
	if request.method=="POST":
		c1=request.form['c1']
		c2=request.form['c2']

		date=[]
		fat=[]
		snf=[]
		cow_rate=[]
		buffallo_rate=[]
		# bill={}
		cursor=mysql.connection.cursor()
		cursor.execute("SELECT * FROM dairy_project.snfpurchase")
		data=cursor.fetchall()
		# print(type(data))
		def add_values_in_dict(sample_dict, key, list_of_values):
			if key not in sample_dict:
				sample_dict[key] = list()
			sample_dict[key].extend(list_of_values)
			return sample_dict
		for i,a in enumerate(data):
			for i,b in enumerate(a):
				if i==1:
					fat.append(b)
				elif i==2:
					snf.append(b)
				elif i==3:
					cow_rate.append(b)
				# elif i==4:
				# 	buffallo_rate.append(b)		
		# print(date)
		# print(fat)
		# print(snf)
		bill={}
		alpha='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdedghijklmnopqrstuvwxyMNOPQRSTUVWXYZabcdedghijklmnopqrstuvwxyz!@#JKLMNOPQRSTUVWXYZabcdedghijklmnopqrstuvwxyMNOPQRSTUVWXYZabcdedghijklmnopqrstuvwxyz!@#$%^&*()_+ABCDEFGHIJK$%^&*()_+ABCDEFGHIJKLMNOPQRSTUVWXYZabcdedghijklmnopqrstuvwxyz!@#$%^&*()_+'
		t=0
		# print(len(alpha))

		for i in range(len(fat)):
			f=fat[i]
			s=snf[i]
			k=[f,s]
			# print(k)
			m=(cow_rate[i])
			ms=str(m)
			# print(ms)
			mp=ms+alpha[i]
			# print(mp)
			# t=t+1
			bill = add_values_in_dict(bill, (mp), (k))
		# print(bill)
		# print(bill[3.9])
		# print(bill[8.3])

		c3=float(c1)
		c4=float(c2)
	# Get list of keys that contains the given value
		list_of_keys = [key for key, list_of_values in bill.items() if c3 in list_of_values if c4 in list_of_values]
		if list_of_keys:
			print("list:-",list_of_keys)
		else:
			print('Value does not exist in the dictionary')
		ans=list_of_keys[0]
		if len(ans)==5:
			# print(ans[0:4])
			ans=ans[0:4]
		elif len(ans)==6:
			# print(ans[0:5])
			ans=ans[0:5]
		else:
			# print(ans[0:6])
			ans=ans[0:6]

		ans=float(ans)
		print(ans)
		# print(type(ans))
		# print("rate:- ", list(bill.keys()) [list(bill.values()).index(check)])


		# bill={
		# 	'fat':(fat),
		# 	'snf':(snf),
		# 	'cow_rate':(cow_rate),
		# 	'buffallo_rate':(buffallo_rate)}
		# # print(bill)
			
			# print(type(a))
		# result=dict((x , y) for x, y in data)
		# print(result)
		# print(type(data))
		# print(type(data[0]))
		# print(data[0])
		# user=data[0]
		# f=bill['fat']
		# s=bill['snf']
		# c=bill['cow_rate']
		# b=bill['buffallo_rate']
		# # for key,value in bill.items():
		# print(f.index(3.0))

				# if f[i]==3.8:
				# 	print(i)

				# if key==8.2:
				# 	print(bill['cow_rate'])
			# 		print(value)
			# 		print(value(cow_rate))
	return render_template('data.html',ans=ans)
		
@app.route('/sanghreciept.html',methods=["POST","GET"])
def sanghreciept():
	if request.method=='POST'  and 'day' in request.form and 'daytime' in request.form and 'milk_type' in request.form and 'good_quantity' in request.form and 'fat' in request.form and 'snf' in request.form and 'degree'  in request.form and 'spoiled_quantity' in request.form and 'rate' in request.form:

		session['day']=request.form['day']
		session['daytime']=request.form['daytime']
		session['milk_type']=request.form['milk_type']
		session['total_quantity']=request.form['total_quantity']
		session['good_quantity']=request.form['good_quantity']
		session['fat']=request.form['fat']
		session['snf']=request.form['snf']
		session['degree']=request.form['degree']
		session['rate']=request.form['rate']
		session['amount']=request.form['amount']
		session['spoiled_quantity']=request.form['spoiled_quantity']
		session['srate']=request.form['srate']

		day=session['day']
		daytime=session['daytime']
		milk_type=session['milk_type']
		total_quantity=session['total_quantity']
		good_quantity=session['good_quantity']
		fat=session['fat']
		snf=session['snf']
		degree=session['degree']
		rate=session['rate']
		amount=session['amount']
		spoiled_quantity=session['spoiled_quantity']
		srate=session['srate']

		cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("INSERT INTO dairy_project.sanghreciept VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(day,daytime,milk_type,good_quantity,fat,snf,degree,rate,amount,spoiled_quantity,srate,total_quantity))
		mysql.connection.commit()
	elif request.method == 'POST':
		msg='Please fill out the form'
	return render_template('sanghreciept.html')	

@app.route('/cattlefeedentry.html',methods=["POST","GET"])
def cattlefeedentry():
	data=''
	
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * FROM dairy_project.cattlefeedentry")
	data=cursor.fetchall()

	if request.method=="POST" and 'day' in request.form and 'feed_name' in request.form and 'sack_no' in request.form and 'sack_price' in request.form:
		session['day']=request.form['day']
		session['feed_name']=request.form['feed_name']
		session['sack_no']=request.form['sack_no']
		session['sack_price']=request.form['sack_price']

		day=session['day']
		feed_name=session['feed_name']
		sack_no=session['sack_no']
		sack_price=session['sack_price']
		if feed_name=='cotton Seed Cake':
			fid=1
		elif feed_name=='Chaff':
			fid=2
		else:
			fid=3
		print(fid)
		cursor=mysql.connection.cursor()
		if fid==1 or fid==2 or fid==3:
			cursor.execute("INSERT INTO dairy_project.cattlefeedentry2 VALUES(%s,%s,%s,%s,%s)",(fid,feed_name,day,sack_no,sack_price))
			mysql.connection.commit()
			cursor.execute("UPDATE  dairy_project.cattlefeedentry SET dairy_project.cattlefeedentry.day=%s, dairy_project.cattlefeedentry.sack_no=dairy_project.cattlefeedentry.sack_no+%s,dairy_project.cattlefeedentry.sack_price=%s where dairy_project.cattlefeedentry.feed_name=%s",(day,sack_no,sack_price,feed_name))
			mysql.connection.commit()
			cursor=mysql.connection.cursor()
			cursor.execute("SELECT * FROM dairy_project.cattlefeedentry")
			data=cursor.fetchall()
		session.pop('day', None)
		session.pop('sack_no', None)
		session.pop('sack_price', None)
		session.pop('feed_name', None)
		cursor.close()
	elif request.method=="POST":
		msg="Please fill out the Form"
	return render_template('cattlefeedentry.html',now=now,data=data) 
		
@app.route('/retailsell.html',methods=['POST','GET'])
def retailsell():
	msg=''
	day=session.get('day')
	name=session.get('name')
	daytime=session.get('daytime')
	milk_type=session.get('milk_type')
	quantity=session.get('quantity')
	rate=session.get('rate')
	amount=session.get('amount')

	if name==None or quantity==None or day==None  or daytime==None or milk_type==None or rate==None or amount==None:
		msg="Please Fill The form"

	else:
		cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("INSERT INTO dairy_project.retailsell VALUES(%s,%s,%s,%s,%s,%s,%s)",(day,name,daytime,milk_type,quantity,rate,amount))
		mysql.connection.commit()
		session.pop('day', None)
		session.pop('name', None)
		session.pop('daytime', None)
		session.pop('milk_type', None)
		session.pop('quantity', None)
		session.pop('rate', None)
		session.pop('amount', None)
	return render_template('retailsell.html',msg=msg,now=now)


@app.route('/greet2', methods=['POST','GET'])
def greet2():
	# n=''
	if request.method=='POST' and  'day' in request.form and 'daytime' in request.form and 'milk_type' in request.form and 'quantity' in request.form:
		print("hiii")
		session['name']=request.form['name']
		session['day']=request.form['day']
		session['daytime']=request.form['daytime']
		session['milk_type']=request.form['milk_type']
		session['quantity'] = request.form['quantity']

		name=session['name']
		quantity=session['quantity']
		day=session['day']
		userid1=session['userid']
		daytime=session['daytime']
		milk_type=session['milk_type']
		print(day)
		print(userid1)
		print(daytime)
		print(milk_type)
		print(quantity)

		cursor=mysql.connection.cursor()
		cursor.execute("SELECT * FROM dairy_project.local_milk_rate")
		data=cursor.fetchall()
		if milk_type=="buffallo":
			rate=data[0][3]
		elif milk_type=="cow":
			rate=data[0][2]
		print(rate)
		amount=float(rate)*float(quantity)
		session['rate']=rate 
		session['amount']=amount
		return jsonify(message2=f'{rate}',message3=f'{amount}')
	return '', 400

@app.route('/advance_entry.html',methods=['POST','GET'])
def advance_entry():
	msg=''
	reduction=0
	day=session.get('day')
	userid=session.get('userid')
	advance=session.get('advance')
	totalBalance=session.get('totalBalance')

	if userid==None or advance==None or day==None or totalBalance==None  or reduction==None:
		msg="Please Fill The form"


	elif request.method=='POST' and 'reduction' in request.form:
		session['reduction']=request.form['reduction']
		reduction=session['reduction']
		
		cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("INSERT INTO dairy_project.advance_entry VALUES(%s,%s,%s)",(day,userid,advance))
		cursor.execute("UPDATE dairy_project.advance SET dairy_project.advance.day=%s, dairy_project.advance.reduction=%s, dairy_project.advance.balance_amount=%s where dairy_project.advance.userid=%s",(day,reduction,totalBalance,userid,))
		mysql.connection.commit()

	elif request.method == 'POST':
		msg='Please fill out the form'	
	return render_template('advance_entry.html',now=now,msg=msg)

@app.route('/advance', methods=['POST','GET'])
def advance():
	if 'userid' in request.form:
		session['userid'] = request.form['userid']
		userid2=session['userid']
		print(userid2)
		cursor=mysql.connection.cursor()
		cursor.execute("SELECT * FROM dairy_project.register WHERE userid=%s AND cust_type='sell' ",(userid2,))
		user=cursor.fetchall()
		user=user[0][1]
		session['user']=user
		cursor.execute("SELECT * FROM dairy_project.advance WHERE userid=%s",(userid2,))
		data=cursor.fetchall()
		print(data)
		reduction1=data[0][2]
		print(reduction1)
		balance=data[0][3]
		session['balance']=balance
		session['reduction1']=reduction1   
		return jsonify(name=f'{user}',balance=f'{balance}',reduction1=f'{reduction1}')
	return '', 400

@app.route('/advance2', methods=['POST','GET'])
def advance2():
	if 'day' in request.form and 'advance' in request.form:
		session['day'] = request.form['day']
		day=session['day']
		print(day)
		session['advance'] = request.form['advance']
		advance=session['advance']
		print(advance)
		balance=session['balance']
		print(balance)
		totalBalance=int(balance)+int(advance)
		session['totalBalance']=totalBalance 
		return jsonify(totalBalance=f'{totalBalance}')
	return '', 400




@app.route('/cattlefeedsell.html',methods=["POST","GET"])
def cattlefeedsell():
	msg=''
	day=session.get('day')
	reduction1=session.get('reduction1')
	userid3=session.get('userid3')
	name=session.get('user')
	feed_name=session.get('feed_name')
	sacks=session.get('sacks')
	rate=session.get('rate')
	amount=session.get('amount')

	# if userid3==None or reduction1==None or day==None or name==None or feed_name==None or sacks==None or rate==None and amount==None:
	# 	msg="Please Fill The form"

	if request.method=="POST" and 'reduction1' in request.form:
		session['reduction1']=request.form['reduction1']
		reduction1=session['reduction1']
		print(reduction1)

		print("hiii")
		sack=int(sacks)
		cursor=mysql.connection.cursor()
		cursor.execute("SELECT sack_no FROM dairy_project.cattlefeedentry where dairy_project.cattlefeedentry.feed_name=%s",(feed_name,))
		no=cursor.fetchall()
		no_of_sack=no[0][0]
		print(no_of_sack)
		if no_of_sack<=sack:
			msg='Sacks Are Not Available'
		else:
			cursor.execute("INSERT INTO dairy_project.cattlefeedsell VALUES(%s,%s,%s,%s,%s,%s,%s)",(day,userid3,name,feed_name,sacks,rate,amount))
			cursor.execute("UPDATE  dairy_project.cattlefeed SET  dairy_project.cattlefeed.bal=dairy_project.cattlefeed.bal+%s, dairy_project.cattlefeed.reduction=%s where dairy_project.cattlefeed.userid=%s",(amount,reduction1,userid3))
			cursor.execute("UPDATE  dairy_project.cattlefeedentry SET  dairy_project.cattlefeedentry.sack_no=dairy_project.cattlefeedentry.sack_no-%s where dairy_project.cattlefeedentry.feed_name=%s",(sacks,feed_name))
			mysql.connection.commit()
			cursor.close()
		session.pop('reduction1', None)
		session.pop('day', None)
		session.pop('userid3', None)
		session.pop('name', None)
		session.pop('feed_name', None)
		session.pop('sacks', None)
		session.pop('rate', None)
		session.pop('amount', None)

	return render_template('cattlefeedsell.html',now=now,msg=msg)

@app.route('/greet3', methods=['POST','GET'])
def greet3():
	msg=''
	rate=0
	amount=0
	balance1=0
	userid3=session.get('userid3')
	reduction=0
	if request.method=="POST" and 'day' in request.form  and 'feed_name' in request.form and 'sacks' in request.form:
		print("hiii")
		session['day']=request.form['day']
		
		session['feed_name']=request.form['feed_name']
		session['sacks']=request.form['sacks']

		day=session['day']
		
		# name=session['name']
		feed_name=session['feed_name']
		sacks=session['sacks']
		sack=int(sacks)

		cursor=mysql.connection.cursor()
		cursor.execute("SELECT sack_no FROM dairy_project.cattlefeedentry where dairy_project.cattlefeedentry.feed_name=%s",(feed_name,))
		no=cursor.fetchall()
		no_of_sack=no[0][0]
		print(no_of_sack)
		if no_of_sack<=sack:
			msg='Sacks Are Not Available'
			print("hii")
		else:
			cursor.execute("SELECT * FROM dairy_project.cattlefeedentry where dairy_project.cattlefeedentry.feed_name=%s",(feed_name,))
			data=cursor.fetchall()
			print(data)
			rate=data[0][4]
			print(rate)
			session['rate']=rate 
			amount=float(rate)*float(sacks)
			session['amount']=amount
			print(amount)
			cursor=mysql.connection.cursor()
			cursor.execute("SELECT bal FROM dairy_project.cattlefeed where dairy_project.cattlefeed.userid=%s",(userid3,))
			data1=cursor.fetchall()
			print(data1)
			sp=(float(data1[0][0]))
			balance1=float(amount)+sp
			print(balance1)
		print(msg)
		return jsonify(rate=f'{rate}',amount=f'{amount}',balance1=f'{balance1}',cmsg=f'{msg}')
	return '', 400

@app.route('/admindashboard.html')
def admindashboard():
	l=datetime.today()
	now=l.strftime('%Y-%m-%d')
	# now="2023-04-02"
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT count(userid) FROM register WHERE cust_type='sell'")
	sell=cursor.fetchall()
	print(sell)
	cursor.execute("SELECT count(userid) FROM register WHERE cust_type='buy' ")
	buy=cursor.fetchall()
	

	cursor.execute("SELECT round(SUM(quantity),2) as sum1 FROM dairy_project.collection WHERE day=%s and milk_type='buffallo'",(now,))
	collection1=cursor.fetchall()
	print(collection1[0])
	# if collection1[0]==None:
	# 	buffallo=0
	# else:
	buffallo=(collection1[0][0])

	cursor.execute("SELECT round(SUM(quantity),2) as sum2 FROM dairy_project.collection WHERE day=%s and milk_type='cow' ",(now,))
	collection2=cursor.fetchall()
	# if collection2==None:
	# 	cow=0
	# else:
	cow=(collection2[0][0])
	cursor.close()
	return render_template('admindashboard.html',sell=sell[0][0],buy=buy[0][0],cow=cow,buffallo=buffallo)


	return render_template('admindashboard.html')

@app.route('/local_milk_rate.html',methods=["POST","GET"])
def local_milk_rate():
	l=datetime.today()
	now=l.strftime('%Y-%m-%d')
	print("hii")
	if request.method=="POST" and 'day' in request.form and 'cow_rate' in request.form and 'buffallo_rate' in request.form:
		day=request.form['day']
		cow_rate=request.form['cow_rate']
		buffallo_rate=request.form['buffallo_rate']

		cursor=mysql.connection.cursor()
		cursor.execute("UPDATE dairy_project.local_milk_rate SET day=%s, dairy_project.local_milk_rate.cow_rate=%s, dairy_project.local_milk_rate.buffallo_rate=%s where dairy_project.local_milk_rate.id=1",(day,cow_rate,buffallo_rate,))
		mysql.connection.commit()
		cursor.close()
	return render_template('local_milk_rate.html',now=now)
	

@app.route('/milkcollection.html', methods=["POST","GET"])
def milkcollection():
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * FROM dairy_project.collection")
	data=cursor.fetchall()
	cursor.execute("SELECT milk_type,day,round(sum(quantity),2),round(sum(amount),2) FROM dairy_project.collection group by day,milk_type")
	cowdata1=cursor.fetchall()
	print(cowdata1)
	# cursor.execute("SELECT day,round(sum(quantity),2),round(sum(amount),2) FROM dairy_project.collection where milk_type='buffallo' group by day")
	# buffallodata1=cursor.fetchall()
	# bquan=buffallodata1[0][1]
	# bamount=buffallodata1[0][2]
	# cursor.execute("SELECT round(sum(quantity),2),round(sum(amount),2) FROM dairy_project.collection  group by day")
	# totaldata1=cursor.fetchall()
	# tquan=totaldata1[0][0]
	# tamount=totaldata1[0][1]
	# cursor.close()
	return render_template('milkcollection.html',data=data,cowdata1=cowdata1)	

@app.route('/edit_collection/<int:userid>/<day>/<daytime>', methods = ['POST', 'GET'])
def edit_collection(userid,day,daytime):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM dairy_project.collection WHERE userid=%s and  day=%s', (userid,day))
    data = cursor.fetchall()
    print(type(data))
    print(data[0])
    return render_template('editcollection.html', collection = data[0]) 

@app.route('/update_collection/<userid>/<day>/<daytime>', methods = ['POST', 'GET'])
def update_collection(userid,day,daytime):
	rate=0
	amount=0
	snf=0
	fat=0
	quantity=0
	l=datetime.today()
	now=l.strftime('%Y-%m-%d')
	user=''
	msg=''

	# day=session.get('day')
	# userid=session.get('userid') 
	# daytime=session.get('daytime')
	milk_type=session.get('milk_type')
	SNF=session.get('snf')
	degree=session.get('degree')
	rate=session.get('rate')
	amount=session.get('amount')
	fat=session.get('fat')
	quantity=session.get('quantity')
	print("Q=",quantity)
	print("Q=",fat)
	print("Q=",SNF)
	print(rate)
	print(amount)

	# if quantity==None or fat==None or SNF==None or degree==None or rate==None or amount==None or day==None or daytime==None or milk_type==None:
	# 	msg="Please Fill The form"
	# 	print('hii')
		# flash('Please Fill The Form')

	
	cursor = mysql.connection.cursor()
	query='UPDATE dairy_project.collection SET milk_type=%s,quantity=%s,fat=%s,SNF=%s,degree=%s,rate=%s,amount=%s WHERE userid = %s and daytime=%s and day=%s'
	cursor.execute(query,(milk_type,quantity,fat,SNF,degree,rate,amount,userid,daytime,day))
	mysql.connection.commit()
	session.pop('user', None)
	session.pop('quantity', None)
	session.pop('userid3', None)
	session.pop('fat', None)
	session.pop('snf', None)
	session.pop('degree', None)
	session.pop('rate', None)
	session.pop('amount', None)
	session.pop('ans', None)
		# mysql.connection.commit()
	return redirect(url_for('milkcollection'))
    # if request.method == 'POST':
    # 	# userid=request.form['userid']
    # 	name=request.form['name']
    # 	daytime=request.form['daytime']
    # 	day=request.form['day']
    # 	milk_type=request.form['milk_type']
    # 	quantity=request.form['quantity']
    # 	fat=request.form['fat']
    # 	SNF=request.form['SNF']
    # 	degree=request.form['degree']

    # 	cursor = mysql.connection.cursor()
    # 	query='UPDATE dairy_project.collection SET name=%s,daytime=%s, day=%s ,milk_type=%s,quantity=%s,fat=%s,SNF=%s,degree=%s WHERE userid = %s'
    # 	cursor.execute(query,(name,daytime,day,milk_type,quantity,fat,SNF,degree,userid))
    # 	flash('collection Updated Successfully')
    # 	mysql.connection.commit()
    # 	return redirect(url_for('milkcollection'))

@app.route('/delete_collection/<userid>/<day>/<daytime>', methods = ['POST','GET'])
def delete_collection(userid,day,daytime):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM dairy_project.collection WHERE userid=%s and day=%s and daytime=%s', [userid,day,daytime])
    # n={0}
    # print(n)
    # query='DELETE FROM dairy_project.retail_milksell WHERE name = %s'
    mysql.connection.commit()
    flash('User Removed Successfully')
    return redirect(url_for('milkcollection'))


@app.route('/milkselling.html', methods=["POST","GET"])
def milkselling():
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * FROM dairy_project.selling")
	data=cursor.fetchall()
	cursor.execute("SELECT day,round(sum(quantity),2),round(sum(amount),2) FROM dairy_project.selling where milk_type='cow' group by day order by day")
	cowdata1=cursor.fetchall()
	cursor.execute("SELECT day,round(sum(quantity),2),round(sum(amount),2) FROM dairy_project.selling where milk_type='buffallo' group by day order by day")
	buffallodata1=cursor.fetchall()
	bquan=buffallodata1[0][1]
	bamount=buffallodata1[0][2]
	cursor.execute("SELECT round(sum(quantity),2),round(sum(amount),2) FROM dairy_project.selling  group by day order by day")
	totaldata1=cursor.fetchall()
	tquan=totaldata1[0][0]
	tamount=totaldata1[0][1]
	cursor.close()
	return render_template('milkselling.html',data=data,cowdata1=cowdata1,bquan=bquan,bamount=bamount,tquan=tquan,tamount=tamount)	

@app.route('/edit_selling/<int:userid>/<day>/<daytime>', methods = ['POST', 'GET'])
def edit_selling(userid,day,daytime):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM dairy_project.selling WHERE userid=%s and  day=%s and daytime=%s', (userid,day,daytime))
    data = cursor.fetchall()
    print(type(data))
    print(data[0])
    return render_template('editselling.html', selling = data[0])

@app.route('/update_selling/<int:userid>/<day>/<daytime>', methods=['POST','GET'])
def update_selling(userid, day, daytime):
    user = ''
    msg = ''
    amount = ''
    data = ''
    rate = 0
    milk_type = session.get('milk_type')
    quantity = session.get('quantity')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM dairy_project.local_milk_rate")
    data = cursor.fetchall()

    if milk_type == "buffallo":
        rate = data[0][3]
    elif milk_type == "cow":
        rate = data[0][2]

    print(rate)
    amount = float(rate) * float(quantity)
    cursor = mysql.connection.cursor()
    query = '''UPDATE dairy_project.selling 
               SET milk_type=%s, quantity=%s 
               WHERE userid=%s AND day=%s AND daytime=%s'''
    cursor.execute(query, (milk_type, quantity, userid, day, daytime))
    flash('Customer Updated Successfully')
    mysql.connection.commit()
    return redirect(url_for('milkselling'))


@app.route('/delete/<nuserid>', methods = ['POST','GET'])
def delete_student(nuserid):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM dairy_project.selling WHERE userid = {0}'.format(nuserid))
    #query='DELETE FROM db.student WHERE id = %s'
    #cursor.execute(query,(nid))
    mysql.connection.commit()
    flash('User Removed Successfully')
    return redirect(url_for('localmilkselling'))

@app.route('/retailmilkdata.html', methods=["POST","GET"])
def retailmilkdata():
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * FROM dairy_project.retail_milksell")
	data=cursor.fetchall()
	cursor.close()
	return render_template('retailmilkdata.html',output=data)	

@app.route('/edit_retailsell/<name>', methods = ['POST', 'GET'])
def edit_retailsell(name):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM dairy_project.retail_milksell WHERE name LIKE %s', [name])
    data = cursor.fetchall()
    print(type(data))
    print(data[0])
    return render_template('retailedit.html', retaildata = data[0])

@app.route('/update_retailsell/<name>', methods = ['POST', 'GET'])
def update_retailsell(name):
    if request.method == 'POST':
    	# name = request.form['name']
    	day = request.form['day']
    	daytime=request.form['daytime']
    	milk_type = request.form['milk_type']
    	quantity = request.form['quantity']
    	rate=request.form['rate']
    	amount=request.form['amount']

    	cursor = mysql.connection.cursor()
    	query='UPDATE dairy_project.retail_milksell SET  day=%s ,daytime=%s,milk_type=%s,quantity=%s,rate=%s,amount=%s where name=%s'
    	cursor.execute(query,(day,daytime,milk_type,quantity,rate,amount,name))
    	flash('Seller Updated Successfully')
    	mysql.connection.commit()
    	return redirect(url_for('retailmilkdata'))

@app.route('/delete_retailsell/<name>', methods = ['POST','GET'])
def delete_retailsell(name):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM dairy_project.retail_milksell WHERE name LIKE %s', [name])
    # n={0}
    # print(n)
    # query='DELETE FROM dairy_project.retail_milksell WHERE name = %s'
    mysql.connection.commit()
    flash('User Removed Successfully')
    return redirect(url_for('retailmilkdata'))


#Fetching data From MySQL to Flask

@app.route('/retail.html', methods=["POST","GET"])
def retail():
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * FROM dairy_project.retailsell")
	data=cursor.fetchall()
	cursor.execute("SELECT day,round(sum(quantity),2),round(sum(amount),2) FROM dairy_project.retailsell where milk_type='cow' group by day order by day")
	cowdata1=cursor.fetchall()
	cursor.execute("SELECT day,round(sum(quantity),2),round(sum(amount),2) FROM dairy_project.retailsell where milk_type='buffallo' group by day order by day")
	buffallodata1=cursor.fetchall()
	bquan=buffallodata1[0][1]
	bamount=buffallodata1[0][2]
	cursor.execute("SELECT round(sum(quantity),2),round(sum(amount),2) FROM dairy_project.retailsell  group by day order by day")
	totaldata1=cursor.fetchall()
	tquan=totaldata1[0][0]
	tamount=totaldata1[0][1]
	cursor.close()
	return render_template('milkselling.html',data=data,cowdata1=cowdata1,bquan=bquan,bamount=bamount,tquan=tquan,tamount=tamount)

@app.route('/dairy.html', methods=['POST','GET'])
def dairy():
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * FROM dairy_project.sanghreciept")
	data=cursor.fetchall()
	
	cursor.close()
	return render_template('dairy.html',data=data)


@app.route('/customerdetails.html', methods=['POST','GET'])
def customerdetails():
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * FROM dairy_project.register")
	data=cursor.fetchall()
	cursor.close()
	return render_template('customerdetails.html',data=data)


@app.route('/advancedetails.html', methods=['POST','GET'])
def advancedetails():
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * FROM dairy_project.advance")
	data=cursor.fetchall()
	cursor.execute("SELECT * FROM dairy_project.advance_entry")
	data1=cursor.fetchall()
	cursor.close()
	return render_template('advancedetails.html',data=data,data1=data1)

@app.route('/cattledetails.html', methods=['POST','GET'])
def cattledetails():
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * FROM dairy_project.cattlefeed")
	data=cursor.fetchall()
	cursor.execute("SELECT * FROM dairy_project.cattlefeedsell")
	data1=cursor.fetchall()
	cursor.close()
	return render_template('cattledetails.html',data=data,data1=data1)

@app.route('/profit.html', methods=['POST','GET'])
def profit():
	cursor=mysql.connection.cursor()
	cursor.execute("SELECT * FROM dairy_project.collection")
	data=cursor.fetchall()
	cursor.execute("SELECT * FROM dairy_project.selling")
	data1=cursor.fetchall()
	cursor.execute("SELECT * FROM dairy_project.sanghreciept")
	data2=cursor.fetchall()
	cursor.close()
	return render_template('cattledetails.html',data=data,data1=data1)


#---------------------------------------------------------------------- Reports Section Start -----------------------------------------------------------------

@app.route('/')
def upload_form():
	return render_template('reports.html')


@app.route('/download/report/pdf')
def download_report1():
	now=datetime.today()
	now2=now.strftime('%Y-%m-%d')
	cursor = mysql.connection.cursor()
	
	cursor.execute("SELECT * FROM dairy_project.register")
	result = cursor.fetchall()
	cursor.execute("SELECT count('sell') from dairy_project.register where cust_type='sell'")
	data=cursor.fetchall()
	cursor.execute("SELECT count('buy') from dairy_project.register where cust_type='buy'")
	data1=cursor.fetchall()
		
		
	pdf = FPDF()
	pdf.add_page()
		
	page_width = pdf.w - 2 * pdf.l_margin
		
	pdf.set_font('Times','B',21.0) 
	pdf.set_font('Times','U',21.0) 
	pdf.image('static/img/Logo7.png', x = 55, y = 10, w =90, h =40, type = '', link = '')
	# pdf.cell(page_width, 0.0, "GOVARDHAN DUDH DAIRY", align='C')
	pdf.set_font('Times','B',16.0)
	pdf.ln(43)
	pdf.set_font('Times','B',18.0) 
	pdf.cell(page_width, 0.0, "Details Of Customer and Supplier", align='C')
	pdf.ln(10)
	pdf.set_font('Times','B',12.0) 
	pdf.cell(page_width, 0.0, 'Date :- '+str(now2), align='L')
	pdf.ln(5)
	pdf.set_font('Times','',10.0) 
	pdf.cell(page_width, 0.0, 'Total Suppliers :- '+str(data[0][0]), align='L')
	pdf.ln(5)
	pdf.cell(page_width, 0.0, 'Total Customers :- '+str(data1[0][0]), align='L')

	

	pdf.ln(10)


	pdf.set_font('Times', 'B', 12)
		
	col_width = page_width/5
		
	th = 4
	i=1
	pdf.cell(col_width,5,"Sr.No",border=1,align='C')
	pdf.cell(70,5,"Name",border=1,align='C')
	# pdf.cell(80,th,"address",border=1)
	# pdf.cell(col_width,th,"Pincode",border=1)
	pdf.cell(col_width,5,"Phone",border=1,align='C')
	pdf.cell(col_width,5,"Customer Type",border=1,align='C')
	pdf.ln(5)
	pdf.set_font('Times', '', 10)
	for col in result:
		pdf.cell(col_width, th, str(i), border=1,align='C')
		pdf.cell(70, th, (col[1]), border=1)
		# pdf.cell(80, th, (col[2]), border=1)
		# pdf.cell(col_width, th, str(col[3]), border=1)
		pdf.cell(col_width, th, str(col[4]), border=1,align='C')
		pdf.cell(col_width, th, (col[5]), border=1,align='C')
		i=i+1
		pdf.ln(th)
		
	pdf.ln(5)
         
	pdf.set_font('Times','',10.0) 
	pdf.cell(page_width, 0.0, '- end of report -', align='C')
	cursor.close()
			
	return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=AllCustomerAndSupplier.pdf'})
    


@app.route('/sellcust/report/pdf',methods=['POST','GET'])
def sellcust():
	now=datetime.today()
	now2=now.strftime('%Y-%m-%d')
	if request.method=="POST":
		cust_type=request.form['cust_type']
		print(cust_type)
		if cust_type=='sell':
			n='Supplier'
		else:
			n='Customer'
		cursor = mysql.connection.cursor()
		
		cursor.execute("SELECT * FROM dairy_project.register where cust_type=%s ",(cust_type,))
		result = cursor.fetchall()
		
		
	pdf = FPDF()
	pdf.add_page()
		
	page_width = pdf.w - 2 * pdf.l_margin
		
	pdf.set_font('Times','B',21.0) 
	pdf.set_font('Times','U',21.0) 
	pdf.image('static/img/Logo7.png', x = 55, y = 10, w =90, h =40, type = '', link = '')
	# pdf.cell(page_width, 0.0, "GOVARDHAN DUDH DAIRY", align='C')
	pdf.set_font('Times','B',16.0)
	pdf.ln(43)
	pdf.set_font('Times','B',18.0) 
	pdf.cell(page_width, 0.0, "Details Of "+str(n), align='C')
	pdf.ln(10)
	pdf.set_font('Times','B',12.0) 
	pdf.cell(page_width, 0.0, 'Date :- '+str(now2), align='L')
	

	pdf.ln(13)


	pdf.set_font('Times', 'B', 13)
		
	col_width = page_width/5
		
	th = 5
	i=1
	pdf.cell(15,5,"Sr.No",border=1,align='C')
	pdf.cell(50,5,"Name",border=1,align='C')
	pdf.cell(80,5,"Address",border=1,align='C')
	# pdf.cell(col_width,th,"Pincode",border=1)
	pdf.cell(col_width,5,"Phone",border=1,align='C')
	# pdf.cell(col_width,5,"Customer Type",border=1,align='C')
	pdf.ln(5)
	pdf.set_font('Times', '', 11)
	for col in result:
		pdf.cell(15, th, str(i), border=1,align='C')
		pdf.cell(50, th, (col[1]), border=1)
		pdf.cell(80, th, (col[2]), border=1)
		# pdf.cell(col_width, th, str(col[3]), border=1)
		pdf.cell(col_width, th, str(col[4]), border=1,align='C')
		# pdf.cell(col_width, th, (col[5]), border=1,align='C')
		i=i+1
		pdf.ln(th)
		
	pdf.ln(5)
         
	pdf.set_font('Times','',10.0) 
	pdf.cell(page_width, 0.0, '- end of report -', align='C')
	cursor.close()
			
	return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=AllSupplier.pdf'})
    


@app.route('/collectionReport/report/pdf',methods=['POST','GET'])
def collectionReport1():
	result=''
	now=datetime.today()
	now2=now.strftime('%Y-%m-%d')

	if request.method == "POST":
		fdate=request.form["fdate"]
		tdate=request.form["tdate"]
		userid=request.form['userid']


		
		print(type(fdate),tdate)
		print(type(fdate),tdate)

		cursor = mysql.connection.cursor()
		cursor.execute("SELECT * FROM dairy_project.collection where userid=%s and (str_to_date(day,'%%Y-%%m-%%d')>=%s and str_to_date(day,'%%Y-%%m-%%d')<=%s)" ,(userid,fdate,tdate,))
		result = cursor.fetchall()
		cursor.execute("SELECT name FROM dairy_project.register where userid=%s" ,(userid,))
		name=cursor.fetchall()
		cursor.execute("SELECT round(SUM(quantity),2),round(SUM(amount),2) FROM dairy_project.collection where userid=%s and (str_to_date(day,'%%Y-%%m-%%d')>=%s and str_to_date(day,'%%Y-%%m-%%d')<=%s)" ,(userid,fdate,tdate,))
		data = cursor.fetchall()
		print(name)
		name=name[0][0]
		
		print(result)
		
	pdf = FPDF()
	pdf.add_page()
		
	page_width = pdf.w - 2 * pdf.l_margin
		
	pdf.set_font('Times','B',16.0) 
	pdf.image('static/img/Logo7.png', x = 55, y = 10, w =90, h =40, type = '', link = '')
	# pdf.cell(page_width, 0.0, "GOVARDHAN DUDH DAIRY", align='C')
	pdf.set_font('Times','B',16.0)
	pdf.ln(46)
	pdf.set_font('Times','B',19.0) 
	pdf.cell(page_width, 0.0, "Date wise Milk Collection Report", align='C')
	pdf.ln(10)
	pdf.set_font('Times','',14.0) 
	pdf.cell(page_width, 0.0, 'From :- '+str(fdate)+'  '+'To:-'+str(tdate),align='L')	
	pdf.ln(5)
	pdf.cell(page_width, 0.0, 'Name :- '+str(name), align='L')
	pdf.ln(5)
	pdf.cell(page_width, 0.0, 'Milk Type :- '+str(result[0][3]), align='L')

	

	pdf.ln(10)


	pdf.set_font('Times', '', 12)
		
	col_width = page_width/8
		
	pdf.ln(1)
	pdf.set_font('Times','B',12.0) 
	th = 5
	i=1
	pdf.cell(15,th,"Sr.No",border=1,align='C')
	pdf.cell(30,th,"Day",border=1,align='C')
	pdf.cell(col_width,th,"Time",border=1,align='C')
	pdf.cell(28,th,"Quantity(ltr)",border=1,align='C')
	pdf.cell(20,th,"Fat",border=1,align='C')
	pdf.cell(20,th,"SNF",border=1,align='C')
	pdf.cell(21,th,"Rate(Rs)",border=1,align='C')
	pdf.cell(25,th,"Amount(Rs)",border=1,align='C')

	pdf.ln(th)
	pdf.set_font('Times','',12.0) 

	for col in result:
		pdf.cell(15, th, str(i), border=1,align='C')
		pdf.cell(30, th, str(col[0]), border=1,align='C')
		pdf.cell(col_width, th, (col[2]), border=1,align='C')
		pdf.cell(28, th, str(col[4]), border=1,align='C')
		pdf.cell(20, th, str(col[5]), border=1,align='C')
		pdf.cell(20,th,str(col[6]),border=1,align='C')

		pdf.cell(21, th, str(col[8]), border=1,align='C')
		pdf.cell(25, th, str(round((col[9]),2)), border=1,align='C')
		i=i+1
		pdf.ln(th)
		
	pdf.ln(10)
	pdf.set_font('Times','B',12.0) 
	pdf.cell(page_width, 0.0, 'Total Quantity :- '+str(data[0][0])+' ltr', align='L')
	pdf.ln(8)
	pdf.cell(page_width, 0.0, 'Total Amount :- '+str(data[0][1])+' Rs', align='L')
	pdf.ln(10)   
	pdf.set_font('Times','',10.0) 
	pdf.cell(page_width, 0.0, '- end of report -', align='C')

			
	return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=milkCollection_report.pdf'})
    

@app.route('/sellingreport/report/pdf',methods=['GET','POST'])
def sellingreport1():
	result=''
	now=datetime.today()
	now2=now.strftime('%Y-%m-%d')
	if request.method == "POST":
		fdate=request.form["fdate"]
		tdate=request.form["tdate"]
		userid=request.form['userid']
		
		print(type(fdate),fdate)
		# fdate = datetime.strptime(fdate, '%Y-%m-%d')
		# tdate = datetime.strptime(tdate, '%Y-%m-%d')
		# print(type(fdate),tdate)

		now=datetime.today()
		cursor = mysql.connection.cursor()
		cursor.execute("SELECT * FROM dairy_project.selling where str_to_date(day,'%%Y-%%m-%%d')>=%s and str_to_date(day,'%%Y-%%m-%%d')<=%s and userid=%s",(fdate,tdate,userid))
		result = cursor.fetchall()
		# print(result)

		cursor = mysql.connection.cursor()
		cursor.execute("SELECT name,userid FROM dairy_project.register where userid=%s",(userid))
		name = cursor.fetchone()
		cursor.execute("SELECT round(SUM(quantity),2),round(SUM(amount),2) FROM dairy_project.selling where userid=%s and (str_to_date(day,'%%Y-%%m-%%d')>=%s and str_to_date(day,'%%Y-%%m-%%d')<=%s)" ,(userid,fdate,tdate,))
		data = cursor.fetchall()
		# print(name)


	pdf = FPDF()
	pdf.add_page()
		
	page_width = pdf.w - 2 * pdf.l_margin
	pdf.set_font('Times','B',16.0) 
	pdf.image('static/img/Logo7.png', x = 55, y = 10, w =90, h =40, type = '', link = '')	# pdf.cell(page_width, 0.0, "GOVARDHAN DUDH DAIRY", align='C')
	pdf.set_font('Times','B',16.0)
	pdf.ln(46)
	pdf.set_font('Times','B',18.0) 
	pdf.cell(page_width, 0.0, "Date wise Milk Selling Report", align='C')
	pdf.ln(10)
	pdf.set_font('Times','',12.0) 
	pdf.cell(page_width, 0.0, 'From :- '+str(fdate)+'  '+'To:- '+str(tdate),align='L')	
	pdf.ln(5)
	pdf.cell(page_width, 0.0, 'Name :- '+str(name[0]),align='L')	
	pdf.ln(5)
	pdf.cell(page_width, 0.0, 'Milk Type :- '+(result[0][3]),align='L')	
	pdf.ln(5)
	pdf.cell(page_width, 0.0, 'Rate :- '+str(result[0][5]),align='L')	
	pdf.ln(5)

		
	pdf.set_font('Times', 'B', 14)
			
	col_width = page_width/5
			
	pdf.ln(1)
			
	th = 5
	i=1
	pdf.cell(col_width,th,"Sr.No",border=1,align='C')
	pdf.cell(col_width,th,"Date",border=1,align='C')
	# pdf.cell(col_width,th,"userid",border=1)
	pdf.cell(col_width,th,"Time",border=1,align='C')
	# pdf.cell(col_width,th,"Milk Type",border=1)
	pdf.cell(col_width,th,"Quantity(Ltr)",border=1,align='C')
	# pdf.cell(col_width,th,"Rate",border=1)
	pdf.cell(col_width,th,"Amount(Rs)",border=1,align='C')
	pdf.set_font('Times', '', 12)

	pdf.ln(th)
	for col in result:

		pdf.cell(col_width, th, str(i), border=1,align='C')
		pdf.cell(col_width, th, str(col[0]), border=1,align='C')
		# pdf.cell(col_width, th, str(col[1]), border=1)
		pdf.cell(col_width, th, str(col[2]), border=1,align='C')
		# pdf.cell(col_width, th, str(col[3]), border=1)
		pdf.cell(col_width, th, str(col[4]), border=1,align='C')
		# pdf.cell(col_width, th, str(col[5]), border=1)
		pdf.cell(col_width, th, str(col[6]), border=1,align='C')
	
		i=i+1
		pdf.ln(th)
		
	pdf.ln(10)
	pdf.set_font('Times','B',12.0) 
	pdf.cell(page_width, 0.0, 'Total Quantity :- '+str(data[0][0])+' ltr', align='L')
	pdf.ln(8)
	pdf.cell(page_width, 0.0, 'Total Amount :- '+str(data[0][1])+' Rs', align='L')
	pdf.ln(10)
         
	pdf.set_font('Times','',10.0) 
	pdf.cell(page_width, 0.0, '- end of report -', align='C')
	cursor.close()
				
	return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=milkselling_report.pdf'})


@app.route('/retail/report/pdf', methods=["POST",'GET'])
def retailReport():
	now=datetime.today()
	now2=now.strftime('%Y-%m-%d')
	if request.method == "POST":
		fdate=request.form["fdate"]
		tdate=request.form["tdate"]
		cursor = mysql.connection.cursor()
		
		cursor.execute("SELECT * FROM dairy_project.retailsell where str_to_date(day,'%%Y-%%m-%%d')>=%s and str_to_date(day,'%%Y-%%m-%%d')<=%s",(fdate,tdate))
		result = cursor.fetchall()
		print(result)
		cursor.execute("SELECT count(name) FROM dairy_project.retailsell where str_to_date(day,'%%Y-%%m-%%d')>=%s and str_to_date(day,'%%Y-%%m-%%d')<=%s",(fdate,tdate))
		data=cursor.fetchall()
		cursor.execute("SELECT round(SUM(quantity),2),round(SUM(amount),2) FROM dairy_project.retailsell where  (str_to_date(day,'%%Y-%%m-%%d')>=%s and str_to_date(day,'%%Y-%%m-%%d')<=%s)" ,(fdate,tdate,))
		data1 = cursor.fetchall()
		cursor.execute("SELECT round(SUM(quantity),2),round(SUM(amount),2) FROM dairy_project.retailsell where  (str_to_date(day,'%%Y-%%m-%%d')>=%s and str_to_date(day,'%%Y-%%m-%%d')<=%s) and milk_type='cow'" ,(fdate,tdate,))
		data2 = cursor.fetchall()
		cursor.execute("SELECT round(SUM(quantity),2),round(SUM(amount),2) FROM dairy_project.retailsell where  (str_to_date(day,'%%Y-%%m-%%d')>=%s and str_to_date(day,'%%Y-%%m-%%d')<=%s) and milk_type='buffallo' ",(fdate,tdate,))
		data3 = cursor.fetchall()
		
	pdf = FPDF()
	pdf.add_page()
		
	page_width = pdf.w - 2 * pdf.l_margin
		
	pdf.set_font('Times','B',21.0) 
	pdf.set_font('Times','U',21.0) 
	pdf.image('static/img/Logo7.png', x = 55, y = 10, w =90, h =40, type = '', link = '')
	# pdf.cell(page_width, 0.0, "GOVARDHAN DUDH DAIRY", align='C')
	pdf.set_font('Times','B',16.0)
	pdf.ln(46)
	pdf.set_font('Times','B',18.0) 
	pdf.cell(page_width, 0.0, "Date wise Details Of Retail Sales", align='C')
	pdf.ln(15)
	pdf.set_font('Times','B',12.0) 
	pdf.cell(page_width, 0.0, 'From :- '+str(fdate)+'  '+'To:- '+str(tdate),align='L')	
	pdf.ln(10)
	pdf.set_font('Times','',12.0) 
	pdf.cell(page_width, 0.0, 'Total Retail Customer :- '+str(data[0][0]), align='L')
	pdf.ln(10)


	pdf.set_font('Times', 'B', 12)
		
	col_width = page_width/9
		
	th = 5
	i=1
	pdf.cell(12,th,"Sr.No",border=1,align='C')
	pdf.cell(25,th,"Date",border=1,align='C')
	pdf.cell(52,th,"Name",border=1,align='C')
	pdf.cell(20,th,"Time",border=1,align='C')
	pdf.cell(col_width,th,"Milk Type",border=1,align='C')
	pdf.cell(27,th,"Quantity(Ltr)",border=1,align='C')
	pdf.cell(15,th,"Rate",border=1,align='C')
	pdf.cell(24,th,"Amount(Rs)",border=1,align='C')
	pdf.set_font('Times', '', 12)

	pdf.ln(th)
	for col in result:

		pdf.cell(12, th, str(i), border=1,align='C')
		pdf.cell(25, th, str(col[0]), border=1,align='C')
		pdf.cell(52, th, (col[1]), border=1)
		pdf.cell(20, th, str(col[2]), border=1,align='C')
		pdf.cell(col_width, th, str(col[3]), border=1,align='C')
		pdf.cell(27, th, str(col[4]), border=1,align='C')
		pdf.cell(15, th, str(col[5]), border=1,align='C')
		pdf.cell(24, th, str(col[6]), border=1,align='C')
	
		i=i+1
		pdf.ln(th)
		
	pdf.ln(10)
	pdf.set_font('Times','',12.0) 

	pdf.cell(page_width, 0.0, 'Quantity of cow:- '+str(data2[0][0])+' ltr		               '+'Amount of cow:- '+str(data2[0][1])+' Rs', align='L')
	pdf.ln(8) 
	pdf.cell(page_width, 0.0, 'Quantity of buffallo:- '+str(data3[0][0])+' ltr		        '+'Amount of buffallo:- '+str(data3[0][1])+' Rs', align='L')
	pdf.ln(8)
	pdf.cell(page_width, 0.0, 'Total Quantity:- '+str(data1[0][0])+' ltr		                '+'Total Amount :- '+str(data1[0][1])+' Rs', align='L')
	pdf.ln(10)	
         
    
	pdf.set_font('Times','',10.0) 
	pdf.cell(page_width, 0.0, '- end of report -', align='C')
	cursor.close()
			
	return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=retailsell.pdf'})
    

@app.route('/advancereport/report/pdf',methods=['POST','GET'])
def advancereport1():
	now=datetime.today()
	now2=now.strftime('%Y-%m-%d')
	
	cursor = mysql.connection.cursor()
	
	# cursor.execute("SELECT register.name,advance_entry.day,advance_entry.advance FROM register LEFT JOIN advance_entry ON register.userid=advance_entry.userid where cust_type='sell' order by day")
	cursor.execute("SELECT dairy_project.register.name,dairy_project.advance_entry.advance,dairy_project.advance_entry.day,dairy_project.advance.reduction,dairy_project.advance.balance_amount from dairy_project.register,dairy_project.advance_entry,dairy_project.advance where dairy_project.register.userid=dairy_project.advance_entry.userid and dairy_project.register.userid=dairy_project.advance.userid and dairy_project.advance_entry.userid=dairy_project.advance.userid order by day")
	result = cursor.fetchall()
	cursor.execute("SELECT round(SUM(advance),2) FROM dairy_project.advance_entry")
	data3 = cursor.fetchall()
	cursor.execute("SELECT round(SUM(balance_amount),2) FROM dairy_project.advance")
	data2 = cursor.fetchall()
		
		
	pdf = FPDF()
	pdf.add_page()
		
	page_width = pdf.w - 2 * pdf.l_margin
		
	pdf.set_font('Times','B',21.0) 
	pdf.set_font('Times','U',21.0) 
	pdf.image('static/img/Logo7.png', x = 55, y = 10, w =90, h =40, type = '', link = '')
	# pdf.cell(page_width, 0.0, "GOVARDHAN DUDH DAIRY", align='C')
	pdf.set_font('Times','B',16.0)
	pdf.ln(46)
	pdf.set_font('Times','B',14.0) 
	pdf.cell(page_width, 0.0, "Details Of Advance", align='C')
	pdf.ln(10)
	pdf.set_font('Times','B',12.0) 
	pdf.cell(page_width, 0.0, 'Date:- '+str(now2),align='L')	
	pdf.ln(10)
	


	pdf.set_font('Times', 'B', 14)
		
	col_width = page_width/7
		
	pdf.ln(1)
		
	th =5
	i=1
	pdf.cell(10,th,"no",border=1,align='C')
	pdf.cell(60,th,"name",border=1,align='C')
	pdf.cell(32,th,"day",border=1,align='C')
	pdf.cell(col_width,th,"advance",border=1,align='C')
	pdf.cell(col_width,th,"reduction",border=1,align='C')
	pdf.cell(36,th,"balance amount",border=1,align='C')
	pdf.ln(th)
	print(result)
	pdf.set_font('Times', '', 12)
	for col in result:
			pdf.cell(10, th, str(i), border=1,align='C')
			pdf.cell(60, th, (col[0]), border=1)
			pdf.cell(32, th, str(col[2]), border=1,align='C')
			pdf.cell(col_width, th, str(col[1]), border=1,align='C')
			pdf.cell(col_width, th, str(col[3]), border=1,align='C')
			pdf.cell(36, th, str(col[4]), border=1,align='C')

			i=i+1
			pdf.ln(th)
		
	pdf.ln(10)
	pdf.cell(page_width, 0.0, 'Total Advance Taken:- '+str(data3[0][0])+' Rs', align='L')
	pdf.ln(8) 
	pdf.cell(page_width, 0.0, 'Total Balance Amount :- '+str(data2[0][0])+' Rs', align='L')
	pdf.ln(10)   
	pdf.set_font('Times','',10.0) 
	pdf.cell(page_width, 0.0, '- end of report -', align='C')
	cursor.close()
		
	return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=advance_report.pdf'})


@app.route('/cattlefeedreport/report/pdf')
def cattlefeedreport1():
	now=datetime.today()
	now2=now.strftime('%Y-%m-%d')

	cursor = mysql.connection.cursor()
	
	# cursor.execute("SELECT register.name,advance_entry.day,advance_entry.advance FROM register LEFT JOIN advance_entry ON register.userid=advance_entry.userid where cust_type='sell' order by day")
	cursor.execute("SELECT dairy_project.cattlefeedsell.day,dairy_project.cattlefeedsell.name,dairy_project.cattlefeedsell.feed_name,dairy_project.cattlefeedsell.sacks,dairy_project.cattlefeedsell.rate,dairy_project.cattlefeedsell.amount,dairy_project.cattlefeed.reduction,dairy_project.cattlefeed.bal from dairy_project.cattlefeed,dairy_project.cattlefeedsell where dairy_project.cattlefeedsell.userid=dairy_project.cattlefeed.userid and dairy_project.cattlefeedsell.day between '2023-04-01' and '2023-04-15' order by  day")
	result = cursor.fetchall()
	cursor.execute("SELECT sack_price, sack_no, feed_name from cattlefeedentry  group by feed_name")
	data3 = cursor.fetchall()
	print(data3)	
	cursor.execute("SELECT feed_name,sum(sacks) from dairy_project.cattlefeedentry2 group by feed_name")
	data4=cursor.fetchall()
	cursor.execute("SELECT feed_name,sum(sacks) from dairy_project.cattlefeedsell group by feed_name")
	data2=cursor.fetchall()
	print(data2)
	print(data4[0][1])
	print(data4[1][1])
	print(data4[2][1])
		
	pdf = FPDF()
	pdf.add_page()
		
	page_width = pdf.w - 2 * pdf.l_margin
		
	pdf.set_font('Times','B',21.0) 
	pdf.set_font('Times','U',21.0) 
	pdf.image('static/img/Logo7.png', x = 55, y = 10, w =90, h =40, type = '', link = '')
	# pdf.cell(page_width, 0.0, "GOVARDHAN DUDH DAIRY", align='C')
	pdf.set_font('Times','B',16.0)
	pdf.ln(46)
	pdf.set_font('Times','B',20.0) 
	pdf.cell(page_width, 0.0, "Details Of Cattlefeed", align='C')
	pdf.ln(10)
	pdf.set_font('Times','B',12.0) 
	pdf.cell(page_width, 0.0, 'From :- '+str('2023-04-01')+'  '+'To:- '+str('2023-04-15'),align='L')	
	pdf.ln(10)

	

	pdf.set_font('Times','B',14.0) 
	pdf.cell(page_width, 0.0, "Customer Wise Sell :-", align='L')
	pdf.ln(10)

	pdf.set_font('Times', 'B', 12)
		
	col_width = page_width/12
		
	pdf.ln(1)
		
	th = pdf.font_size
	i=1
	pdf.cell(10,th,"No",border=1)
	pdf.cell(30,th,"Day",border=1)
	pdf.cell(60,th,"Name",border=1)
	pdf.cell(45,th,"Feed",border=1)
	pdf.cell(col_width,th,"Sacks",border=1)
	# pdf.cell(col_width,th,"Rate",border=1)
	pdf.cell(col_width,th,"Amount",border=1)
	# pdf.cell(col_width,th,"reduction",border=1)
	# pdf.cell(col_width,th,"balance",border=1)



	pdf.ln(th)
	pdf.set_font('Times', '', 12)

	for col in result:
			pdf.cell(10, th, str(i), border=1)
			pdf.cell(30, th, str(col[0]), border=1)
			pdf.cell(60, th, (col[1]), border=1)
			pdf.cell(45, th, (col[2]), border=1)
			pdf.cell(col_width, th, str(col[3]), border=1)
			# pdf.cell(col_width, th, str(col[4]), border=1)
			pdf.cell(col_width, th, str(col[5]), border=1)
			# pdf.cell(col_width, th, str(col[6]), border=1)
			# pdf.cell(col_width, th, str(col[7]), border=1)			
			i=i+1
			pdf.ln(th)



		
	pdf.ln(20)

	pdf.set_font('Times','B',14.0) 
	pdf.cell(page_width, 0.0, "Overall Sell :-", align='L')
	pdf.ln(10)
		
	th = pdf.font_size
	i=1
	pdf.cell(10,th,"No",border=1,align="C")
	pdf.cell(40,th,"Feed Name",border=1,align="C")
	pdf.cell(col_width,th,"Rate",border=1,align="C")
	pdf.cell(35,th,"Selled Sacks",border=1,align="C")
	# pdf.cell(30,th,"Total Sackes",border=1,align="C")
	pdf.cell(45,th,"Remaining sacks",border=1,align="C")
	# pdf.cell(col_width,th,"amount",border=1)
	# pdf.cell(col_width,th,"reduction",border=1)
	# pdf.cell(col_width,th,"balance",border=1)



	pdf.ln(th)
	print(result)
	pdf.set_font('Times', '', 12)

	
	pdf.cell(10, th, str(1), border=1,align="C")
	pdf.cell(40, th, str(data3[0][2]), border=1,align="C")
	pdf.cell(col_width, th, str(data3[0][0]), border=1,align="C")
	pdf.cell(35, th, str(data2[0][1]), border=1,align="C")
	# pdf.cell(30, th, str(data4[0][1]), border=1,align="C")

	pdf.cell(45, th, str(data3[0][1]), border=1,align="C")
	# pdf.cell(col_width, th, str(col[5]), border=1)
	# pdf.cell(col_width, th, str(col[6]), border=1)
	# pdf.cell(col_width, th, str(col[7]), border=1)			
	i=i+1
	pdf.ln(th)
	pdf.cell(10, th, str(2), border=1,align="C")
	pdf.cell(40, th, str(data3[1][2]), border=1,align="C")
	pdf.cell(col_width, th, str(data3[1][0]), border=1,align="C")
	pdf.cell(35, th, str(data2[1][1]), border=1,align="C")
	# pdf.cell(30, th, str(data4[1][1]), border=1,align="C")

	pdf.cell(45, th, str(data3[1][1]), border=1,align="C")
	# pdf.cell(col_width, th, str(col[5]), border=1)
	# pdf.cell(col_width, th, str(col[6]), border=1)
	# pdf.cell(col_width, th, str(col[7]), border=1)			
	i=i+1
	pdf.ln(th)
	pdf.cell(10, th, str(3), border=1,align="C")
	pdf.cell(40, th, str(data3[2][2]), border=1,align="C")
	pdf.cell(col_width, th, str(data3[2][0]), border=1,align="C")
	pdf.cell(35, th, str(data2[2][1]), border=1,align="C")
	# pdf.cell(30, th, str(data4[2][1]), border=1,align="C")
	pdf.cell(45, th, str(data3[2][1]), border=1,align="C")
	# pdf.cell(col_width, th, str(col[5]), border=1)
	# pdf.cell(col_width, th, str(col[6]), border=1)
	# pdf.cell(col_width, th, str(col[7]), border=1)			
	i=i+1
	pdf.ln(th)
	

	pdf.ln(10)
         
	pdf.set_font('Times','',10.0) 
	pdf.cell(page_width, 0.0, '- end of report -', align='C')
	cursor.close()
			
	return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=cattlefeedsell.pdf'})

@app.route('/cattlefeed/report/pdf', methods=["POST",'GET'])
def cattlefeed():
	now=datetime.today()
	now2=now.strftime('%Y-%m-%d')
	if request.method == "POST":
		fdate=request.form["fdate"]
		tdate=request.form["tdate"]
		cursor = mysql.connection.cursor()
		
		cursor.execute("SELECT * FROM dairy_project.cattlefeedentry2 where str_to_date(day,'%%Y-%%m-%%d')>=%s and str_to_date(day,'%%Y-%%m-%%d')<=%s order by day",(fdate,tdate))
		result = cursor.fetchall()
		# print(result)
		cursor.execute("SELECT sum(sacks) FROM dairy_project.cattlefeedentry2 where str_to_date(day,'%%Y-%%m-%%d')>=%s and str_to_date(day,'%%Y-%%m-%%d')<=%s group by feed_name ",(fdate,tdate))
		data=cursor.fetchall()
		print(data)
		
	pdf = FPDF()
	pdf.add_page()
	pdf.l_margin=30
	page_width = pdf.w - 2 * pdf.l_margin
		
	pdf.set_font('Times','B',21.0) 
	pdf.set_font('Times','U',21.0) 
	pdf.image('static/img/Logo7.png', x = 55, y = 10, w =90, h =40, type = '', link = '')
	# pdf.cell(page_width, 0.0, "GOVARDHAN DUDH DAIRY", align='C')
	pdf.set_font('Times','B',16.0)
	pdf.ln(46)
	pdf.set_font('Times','B',18.0) 
	pdf.cell(page_width, 0.0, "Date wise Cattlefeed Entry Details", align='C')
	pdf.ln(15)
	pdf.set_font('Times','B',12.0) 
	pdf.cell(page_width, 0.0, 'From :- '+str(fdate)+'  '+'To:- '+str(tdate),align='L')	
	pdf.ln(10)
	


	pdf.set_font('Times', 'B', 12)
		
	col_width = page_width/9
		
	th = 5
	i=1
	pdf.cell(12,th,"Sr.No",border=1,align='C')
	pdf.cell(25,th,"Date",border=1,align='C')
	pdf.cell(52,th,"Feed Name",border=1,align='C')
	pdf.cell(20,th,"No. Sacks",border=1,align='C')
	pdf.cell(col_width,th,"Rate",border=1,align='C')
	pdf.set_font('Times', '', 12)

	pdf.ln(th)
	for col in result:
		pdf.cell(12, th, str(i), border=1,align='C')
		pdf.cell(25, th, str(col[2]), border=1,align='C')
		pdf.cell(52, th, (col[1]), border=1)
		pdf.cell(20, th, str(col[3]), border=1,align='C')
		pdf.cell(col_width, th, str(col[4]), border=1,align='C')
		i=i+1
		pdf.ln(th)
		
	pdf.ln(10)
	pdf.set_font('Times','',12.0) 

	pdf.cell(page_width, 0.0, 'No of Cotten Seed Cake Sacks:-  '+str(data[0][0]), align='L')
	pdf.ln(8) 
	pdf.cell(page_width, 0.0, 'No of Chaff Sacks:- 			   '+str(data[1][0]), align='L')
	pdf.ln(8)
	pdf.cell(page_width, 0.0, 'No of Cotten Seed Goli Sacks:-  '+str(data[2][0]), align='L')
	pdf.ln(10)	
         
    
	pdf.set_font('Times','',10.0) 
	pdf.cell(page_width, 0.0, '- end of report -', align='C')
	cursor.close()
			
	return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=cattlefeedentry.pdf'})


@app.route('/totalsell/report/pdf', methods=["POST",'GET'])
def totalsell():
	now=datetime.today()
	now2=now.strftime('%Y-%m-%d')
	if request.method == "POST":
		fdate=request.form["fdate"]
		tdate=request.form["tdate"]
		milk_type=request.form['milk_type']
		cursor = mysql.connection.cursor()

		if milk_type=="buffallo":
		
			cursor.execute("SELECT * FROM db.selling where str_to_date(day,'%%Y-%%m-%%d')>=%s and str_to_date(day,'%%Y-%%m-%%d')<=%s and milk_type='buffallo' order by day",(fdate,tdate,))
			result = cursor.fetchall()
			# print(result)
			cursor.execute("SELECT round(SUM(quantity),2),round(SUM(amount),2) FROM db.selling where  (str_to_date(day,'%%Y-%%m-%%d')>=%s and str_to_date(day,'%%Y-%%m-%%d')<=%s) and milk_type='buffallo' group by daytime" ,(fdate,tdate,))
			data1 = cursor.fetchall()
			print(data1)
			
		else:
			cursor.execute("SELECT * FROM db.selling where str_to_date(day,'%%Y-%%m-%%d')>=%s and str_to_date(day,'%%Y-%%m-%%d')<=%s and milk_type='cow' order by day",(fdate,tdate))
			result = cursor.fetchall()
			# print(result)

			cursor.execute("SELECT round(SUM(quantity),2),round(SUM(amount),2) FROM db.selling where  (str_to_date(day,'%%Y-%%m-%%d')>=%s and str_to_date(day,'%%Y-%%m-%%d')<=%s) and milk_type='cow' group by daytime" ,(fdate,tdate,))
			data1 = cursor.fetchall()
			

		
	pdf = FPDF()
	pdf.add_page()
	pdf.l_margin=40
		
	page_width = pdf.w - 2 * pdf.l_margin
		
	pdf.set_font('Times','B',21.0) 
	pdf.set_font('Times','U',21.0) 
	pdf.image('static/img/Logo7.png', x = 55, y = 10, w =90, h =40, type = '', link = '')
	# pdf.cell(page_width, 0.0, "GOVARDHAN DUDH DAIRY", align='C')
	pdf.set_font('Times','B',16.0)
	pdf.ln(46)
	pdf.set_font('Times','B',18.0) 
	pdf.cell(page_width, 0.0, "Total Milk Selling", align='C')
	pdf.ln(15)
	pdf.set_font('Times','B',14.0) 
	pdf.cell(page_width, 0.0, 'From :- '+str(fdate)+'  '+'To:- '+str(tdate),align='L')	
	pdf.ln(10)
	pdf.set_font('Times','U',14.0) 
	pdf.cell(page_width, 0.0, 'Milk Type :- '+str(milk_type), align='L')
	pdf.ln(10)
	pdf.cell(page_width, 0.0, 'Rate :- '+str(60)+" Rs per litr", align='L')
	pdf.ln(10)

	pdf.set_font('Times', 'B', 12)
		
	col_width = page_width/9
		
	th = 5
	i=1
	pdf.cell(15,th,"Sr.No",border=1,align='C')
	pdf.cell(30,th,"Date",border=1,align='C')
	# pdf.cell(52,th,"Name",border=1,align='C')
	pdf.cell(30,th,"Time",border=1,align='C')
	# pdf.cell(col_width,th,"Milk Type",border=1,align='C')
	pdf.cell(30,th,"Quantity(Ltr)",border=1,align='C')
	pdf.cell(30,th,"Amount(Rs)",border=1,align='C')
	# pdf.cell(15,th,"Rate",border=1,align='C')
	pdf.set_font('Times', '', 12)

	pdf.ln(th)
	for col in result:

		pdf.cell(15, th, str(i), border=1,align='C')
		pdf.cell(30, th, str(col[0]), border=1,align='C')
		# pdf.cell(52, th, (col[1]), border=1)
		pdf.cell(30, th, str(col[1]), border=1,align='C')
		pdf.cell(30, th, str(col[3]), border=1,align='C')
		# pdf.cell(30, th, str(col[2]), border=1,align='C')
		pdf.cell(30, th, str(col[4]), border=1,align='C')
		# pdf.cell(15, th, str(col[5]), border=1,align='C')
	
		i=i+1
		pdf.ln(th)
		
	pdf.ln(10)
	pdf.set_font('Times','',12.0) 

	pdf.cell(page_width, 0.0, 'Morning Quantity:- '+str(data1[0][0])+' ltr		                '+'Morning Amount :- '+str(data1[0][1])+' Rs', align='L')
	pdf.ln(8) 
	pdf.cell(page_width, 0.0, 'Evening Quantity:- '+str(data1[1][0])+' ltr		        		      '+'Evening Amount:- '+str(data1[1][1])+' Rs', align='L')
	pdf.ln(8)
	pdf.cell(page_width, 0.0, 'Total Quantity:- '+str(data1[0][0]+data1[1][0])+' ltr		                    '+'Total Amount :- '+str(data1[0][1]+data1[1][1])+' Rs', align='L')
	pdf.ln(10)	
         
    
	pdf.set_font('Times','',10.0) 
	pdf.cell(page_width, 0.0, '- end of report -', align='C')
	cursor.close()
			
	return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=retailsell.pdf'})
    
@app.route('/dailysell/report/pdf', methods=["POST",'GET'])
def dailysell():
	now=datetime.today()
	now2=now.strftime('%Y-%m-%d')
	if request.method == "POST":
		fdate=request.form["fdate"]
		# tdate=request.form["tdate"]
		milk_type=request.form['milk_type']
		cursor = mysql.connection.cursor()

		if milk_type=="buffallo":
		
			cursor.execute("SELECT selling.daytime,selling.quantity,selling.rate,selling.amount,register.name FROM dairy_project.selling,dairy_project.register where selling.day=%s and selling.milk_type='buffallo' and selling.userid=register.userid ",(fdate,))
			result = cursor.fetchall()
			print(result)
			cursor.execute("SELECT round(SUM(quantity),2),round(SUM(amount),2) FROM dairy_project.selling where  selling.day=%s and milk_type='buffallo' group by daytime" ,(fdate,))
			data1 = cursor.fetchall()
			print(data1)
			
		else:
			cursor.execute("SELECT selling.daytime,selling.quantity,selling.rate,selling.amount,register.name FROM dairy_project.selling,dairy_project.register where selling.day=%s and selling.milk_type='cow' and selling.userid=register.userid ",(fdate,))
			result = cursor.fetchall()
			print(result)

			cursor.execute("SELECT round(SUM(quantity),2),round(SUM(amount),2) FROM dairy_project.selling where  selling.day=%s and milk_type='cow' group by daytime" ,(fdate,))
			data1 = cursor.fetchall()
			

		
	pdf = FPDF()
	pdf.add_page()
	pdf.l_margin=40
		
	page_width = pdf.w - 2 * pdf.l_margin
		
	pdf.set_font('Times','B',21.0) 
	pdf.set_font('Times','U',21.0) 
	pdf.image('static/img/Logo7.png', x = 55, y = 10, w =90, h =40, type = '', link = '')
	# pdf.cell(page_width, 0.0, "GOVARDHAN DUDH DAIRY", align='C')
	pdf.set_font('Times','B',16.0)
	pdf.ln(46)
	pdf.set_font('Times','B',18.0) 
	pdf.cell(page_width, 0.0, "Daily Milk Selling", align='C')
	pdf.ln(15)
	pdf.set_font('Times','B',14.0) 
	pdf.cell(page_width, 0.0, 'Date :- '+str(fdate),align='L')	
	pdf.ln(10)
	pdf.set_font('Times','U',14.0) 
	pdf.cell(page_width, 0.0, 'Milk Type :- '+str(milk_type), align='L')
	pdf.ln(10)
	pdf.cell(page_width, 0.0, 'Rate :- '+str(result[0][2]), align='L')
	pdf.ln(10)

	pdf.set_font('Times', 'B', 12)
		
	col_width = page_width/9
		
	th = 5
	i=1
	pdf.cell(15,th,"Sr.No",border=1,align='C')
	# pdf.cell(30,th,"Date",border=1,align='C')
	pdf.cell(52,th,"Name",border=1,align='C')
	pdf.cell(30,th,"Time",border=1,align='C')
	# pdf.cell(col_width,th,"Milk Type",border=1,align='C')
	pdf.cell(30,th,"Quantity(Ltr)",border=1,align='C')
	pdf.cell(30,th,"Amount(Rs)",border=1,align='C')
	# pdf.cell(15,th,"Rate",border=1,align='C')
	pdf.set_font('Times', '', 12)

	pdf.ln(th)
	for col in result:

		pdf.cell(15, th, str(i), border=1,align='C')
		# pdf.cell(30, th, str(col[0]), border=1,align='C')
		pdf.cell(52, th, (col[4]), border=1)
		pdf.cell(30, th, str(col[0]), border=1,align='C')
		pdf.cell(30, th, str(col[1]), border=1,align='C')
		# pdf.cell(30, th, str(col[2]), border=1,align='C')
		pdf.cell(30, th, str(col[3]), border=1,align='C')
		# pdf.cell(15, th, str(col[5]), border=1,align='C')
	
		i=i+1
		pdf.ln(th)
		
	pdf.ln(10)
	pdf.set_font('Times','',12.0) 

	pdf.cell(page_width, 0.0, 'Morning Quantity:- '+str(data1[0][0])+' ltr		                '+'Morning Amount :- '+str(data1[0][1])+' Rs', align='L')
	pdf.ln(8) 
	pdf.cell(page_width, 0.0, 'Evening Quantity:- '+str(data1[1][0])+' ltr		        		      '+'Evening Amount:- '+str(data1[1][1])+' Rs', align='L')
	pdf.ln(8)
	pdf.cell(page_width, 0.0, 'Total Quantity:- '+str(data1[0][0]+data1[1][0])+' ltr		                    '+'Total Amount :- '+str(data1[0][1]+data1[1][1])+' Rs', align='L')
	pdf.ln(10)	
         
    
	pdf.set_font('Times','',10.0) 
	pdf.cell(page_width, 0.0, '- end of report -', align='C')
	cursor.close()
			
	return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=Daily_sell.pdf'})
    
@app.route('/dailycollect/report/pdf', methods=["POST",'GET'])
def dailycollect():
	now=datetime.today()
	now2=now.strftime('%Y-%m-%d')
	if request.method == "POST":
		fdate=request.form["fdate"]
		# tdate=request.form["tdate"]
		milk_type=request.form['milk_type']
		cursor = mysql.connection.cursor()

		if milk_type=="buffallo":
		
			cursor.execute("SELECT collection.daytime,collection.quantity,collection.fat,collection.snf,collection.rate,collection.amount,register.name FROM dairy_project.collection,dairy_project.register where collection.day=%s and collection.milk_type='buffallo' and collection.userid=register.userid order by daytime desc",(fdate,))
			result = cursor.fetchall()
			# print(result)
			cursor.execute("SELECT round(SUM(quantity),2),round(SUM(amount),2) FROM dairy_project.collection where  collection.day=%s and milk_type='buffallo' group by daytime" ,(fdate,))
			data1 = cursor.fetchall()
			print(data1)
			
		else:
			cursor.execute("SELECT collection.daytime,collection.quantity,collection.fat,collection.snf,collection.rate,collection.amount,register.name FROM dairy_project.collection,dairy_project.register where collection.day=%s and collection.milk_type='cow' and collection.userid=register.userid order by daytime desc",(fdate,))
			result = cursor.fetchall()
			# print(result)

			cursor.execute("SELECT round(SUM(quantity),2),round(SUM(amount),2) FROM dairy_project.collection where  collection.day=%s and milk_type='cow' group by daytime" ,(fdate,))
			data1 = cursor.fetchall()
			

		
	pdf = FPDF()
	pdf.add_page()
	# pdf.l_margin=40
		
	page_width = pdf.w - 2 * pdf.l_margin
		
	pdf.set_font('Times','B',21.0) 
	pdf.set_font('Times','U',21.0) 
	pdf.image('static/img/Logo7.png', x = 55, y = 10, w =90, h =40, type = '', link = '')
	# pdf.cell(page_width, 0.0, "GOVARDHAN DUDH DAIRY", align='C')
	pdf.set_font('Times','B',16.0)
	pdf.ln(46)
	pdf.set_font('Times','B',18.0) 
	pdf.cell(page_width, 0.0, "Daily Milk collection", align='C')
	pdf.ln(15)
	pdf.set_font('Times','B',14.0) 
	pdf.cell(page_width, 0.0, 'Date :- '+str(fdate),align='L')	
	pdf.ln(10)
	pdf.set_font('Times','U',14.0) 
	pdf.cell(page_width, 0.0, 'Milk Type :- '+str(milk_type), align='L')
	pdf.ln(10)

	pdf.set_font('Times', 'B', 12)
		
	col_width = page_width/9
		
	th = 5
	i=1
	pdf.cell(13,th,"Sr.No",border=1,align='C')
	# pdf.cell(30,th,"Date",border=1,align='C')
	pdf.cell(52,th,"Name",border=1,align='C')
	pdf.cell(23,th,"Time",border=1,align='C')
	# pdf.cell(col_width,th,"Milk Type",border=1,align='C')
	pdf.cell(28,th,"Quantity(Ltr)",border=1,align='C')
	pdf.cell(13,th,"Fat",border=1,align='C')
	pdf.cell(13,th,"SNF",border=1,align='C')
	pdf.cell(22,th,"Rate(Rs/lit)",border=1,align='C')
	pdf.cell(28,th,"Amount(Rs)",border=1,align='C')
	pdf.set_font('Times', '', 12)

	pdf.ln(th)
	for col in result:

		pdf.cell(13, th, str(i), border=1,align='C')
		# pdf.cell(30, th, str(col[0]), border=1,align='C')
		pdf.cell(52, th, (col[6]), border=1)
		pdf.cell(23, th, str(col[0]), border=1,align='C')
		pdf.cell(28, th, str(col[1]), border=1,align='C')
		pdf.cell(13, th, str(col[2]), border=1,align='C')
		pdf.cell(13, th, str(col[3]), border=1,align='C')
		pdf.cell(22, th, str(col[4]), border=1,align='C')
		pdf.cell(28, th, str(col[5]), border=1,align='C')
	
		i=i+1
		pdf.ln(th)
		
	pdf.ln(10)
	pdf.set_font('Times','',12.0) 

	pdf.cell(page_width, 0.0, 'Morning Quantity:- '+str(data1[0][0])+' ltr		                '+'Morning Amount :- '+str(data1[0][1])+' Rs', align='L')
	pdf.ln(8) 
	pdf.cell(page_width, 0.0, 'Evening Quantity:- '+str(data1[1][0])+' ltr		        		      '+'Evening Amount:- '+str(data1[1][1])+' Rs', align='L')
	pdf.ln(8)
	pdf.cell(page_width, 0.0, 'Total Quantity:- '+str(data1[0][0]+data1[1][0])+' ltr		                    '+'Total Amount :- '+str(data1[0][1]+data1[1][1])+' Rs', align='L')
	pdf.ln(10)	
         
    
	pdf.set_font('Times','',14.0) 
	pdf.cell(page_width, 0.0, '- end of report -', align='C')
	cursor.close()
			
	return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=Daily_collection.pdf'})