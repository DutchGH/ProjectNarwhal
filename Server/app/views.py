from flask import render_template,session,redirect, flash
from app import app, db, models
import datetime as dt
import sys
import logging

##Default logging posts
logging.basicConfig(filename='wonderLand.log',level=logging.DEBUG)
logging.info('Application launched on '+dt.datetime.today().strftime("%m/%d/%Y"))

##The route used to pass a user accID to the view page
@app.route('/<string:accID>')
def userProfile(accID):
	session["view"] = accID
	logging.info("Application moved to /userProfile route with an accID = "+session["view"]+".")
	return redirect("http://localhost:5000/view")

##The redirect to the login page, clearing the "user" session and
##logging the user out
@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session["user"] = "NONE"
	logging.info("User logged out through /logout route.")
	return redirect("http://localhost:5000/")

##The login page route
@app.route('/', methods=['GET', 'POST'])
def login():
	logging.info("User landed on login page with / route.")
	form = log()
	session["search"] = "NONE"
	session["user"] = "NONE"
	session["view"] = "NONE"
	message = ""
	if form.validate_on_submit():
		account = models.Accounts.query.filter_by(login=form.logName.data).all()
		if(len(account)==0):
			message = "This account does not exist."
		else:
			account = account[0]
			##Check if the passwords match
			if(account.password == form.password.data):
				session["user"] = account.accID
				return redirect("http://localhost:5000/home")
				logging.info(account.login+" logged in successfully.")
			else:
				message ="Incorrect password."
				logging.warning("Incorrect password entered when user attempted to access account "+account.login)
		db.session.commit()
	return render_template('login.html',
						   message=message,
						   form=form,
						   link="http://localhost:5000/create",
						   title='Wonderland')

##The profile creation route
@app.route('/create', methods=['GET', 'POST'])
def makeUser():
	#Declare the needed variables
	form = newUser()
	logging.info("User creating a profile.")
	message = ""
	if form.validate_on_submit():
		check = models.Accounts.query.filter_by(login=form.login.data).all()
		if(len(check) != 0):
			message = "This username already exists."
			logging.warning("The username "+form.login.data+" already exists.")
		else:
			##Check if the passwords match
			if(form.checkpass.data != form.password.data):
				message = "The passwords do not match."
				logging.warning("The provided passwords do not match.")
			else:
				accounts = models.Accounts.query.all()
				newID = len(accounts)
				account = models.Accounts(accID=newID,name=form.name.data,login=form.login.data,desc=form.bio.data,pic=form.pic.data,password=form.password.data,rank=0.0,ratings=0)
				db.session.add(account)
				db.session.commit()
				account = models.Accounts.query.filter_by(accID=account.accID).all()
				account = account[0]
				session["user"] = account.accID
				logging.info("New account created with login "+account.login)
				return redirect("http://localhost:5000/home")
	return render_template('create.html',
						   form=form,
						   message = message,
						   title='Wonderland')

##The home page route
@app.route('/home', methods=['GET', 'POST'])
def home():
	logging.info("The user landed on the home screen with the /home path.")
	if(session["user"]=="NONE"):
		logging.warning("User is not logged in and has been redirected to / route.")
		return redirect("http://localhost:5000/")
	account = models.Accounts.query.filter_by(accID=session["user"]).all()
	account = account[0]
	form = search()
	if form.validate_on_submit():
		logging.info("The user searched for users with the word(s) '"+form.searchWord.data+"'")
		session["search"] = "NONE"
		##Check the database for non friends
		names = models.Accounts.query.filter_by(login=form.searchWord.data).all()
		if(len(names) !=0):
			names = names[0]
			##make a list of friends
			if(len(models.Relationships.query.filter_by(userOne=names).filter_by(userTwo=account).all()) == 0):
				if(len(models.Relationships.query.filter_by(userTwo=names).filter_by(userOne=account).all()) == 0):
					logging.info("The user found results.")
					session["search"] = names.accID
		return redirect("http://localhost:5000/search")
	postForm = ratePost()
	message = ""
	if postForm.validate_on_submit():
		##get the post
		logging.info("The user rated the post "+postForm.postID.data)
		post = models.Posts.query.filter_by(postID=int(postForm.postID.data)).all()
		post = post[0]
		value = float(postForm.rating.data)
		curAdv = post.rank*post.ratings
		curAdv = curAdv+value
		curAdv = curAdv/(post.ratings+1)
		post.rank = round(curAdv,2)
		post.ratings += 1
		db.session.commit()
	postList = models.Posts.query.filter_by(target=account).all()
	allList = models.Posts.query.filter_by(secure=False).order_by(models.Posts.rank.desc()).all()
	return render_template('home.html',
						   form=form,
						   postForm = postForm,
						   posts=postList,
						   allList=allList,
						   logged = account,
						   title='Wonderland')

##The redirect to home route, clears the "search" session
@app.route('/return', methods=['GET', 'POST'])
def back():
	session["search"] = "NONE"
	return redirect("http://localhost:5000/home")

##The search result route
@app.route('/search', methods=['GET', 'POST'])
def result():
	logging.info("The user landed on the search screen at route /search.")
	if(session["user"]=="NONE"):
		logging.warning("User has not searched and is being redirected to home screen via route /home.")
		return redirect("http://localhost:5000/home")
	account = models.Accounts.query.filter_by(accID=session["user"]).all()
	account = account[0]
	form = search()
	if form.validate_on_submit():
		logging.info("The user searched for users with the word(s) '"+form.searchWord.data+"'")
		session["search"] = "NONE"
		##Check the database for non friends
		names = models.Accounts.query.filter_by(login=form.searchWord.data).all()
		if(len(names) !=0):
			names = names[0]
			##make a list of friends
			if(len(models.Relationships.query.filter_by(userOne=names).filter_by(userTwo=account).all()) == 0):
				if(len(models.Relationships.query.filter_by(userTwo=names).filter_by(userOne=account).all()) == 0):
					logging.info("The user found results.")
					session["search"] = names.accID
		return redirect("http://localhost:5000/search")
	userForm = addUser()
	if userForm.validate_on_submit():
		logging.info("User accID:"+str(account.accID)+" made a relationship with accID:"+userForm.userID.data+".")
		session["search"] = "NONE"
		friend = models.Accounts.query.filter_by(accID=userForm.userID.data).all()
		friend = friend[0]
		relationships = models.Relationships.query.all()
		newRelID = len(relationships)
		newRel = models.Relationships(relID = newRelID, userOne=account, userTwo = friend)
		db.session.add(newRel)
		db.session.commit()
		return redirect("http://localhost:5000/home")
	if(session["search"]=="NONE"):
		bannerText = "Sorry, there are no users with this login..."
		results = []
	else:
		bannerText = "Would you like to add this user?"
		results = models.Accounts.query.filter_by(accID=session["search"]).all()
	allList = models.Posts.query.filter_by(secure=False).order_by(models.Posts.rank.desc()).all()
	return render_template('results.html',
						   form=form,
						   userForm=userForm,
						   results = results,
						   bannerText = bannerText,
						   allList=allList,
						   logged = account,
						   title='Wonderland')

##The friend page route
@app.route('/view', methods=['GET', 'POST'])
def view():
	if(session["user"]=="NONE"):
		logging.warning("User is not logged in and has been redirected to / route.")
		return redirect("http://localhost:5000/")
	if(session["view"]=="NONE"):
		logging.warning("User is not logged in and has been redirected to / route.")
		return redirect("http://localhost:5000/")
	account = models.Accounts.query.filter_by(accID=session["user"]).all()
	account = account[0]
	messageForm = addMessage()
	if messageForm.validate_on_submit():
		##get the post
		target = models.Accounts.query.filter_by(accID=int(messageForm.targetID.data)).all()
		target = target[0]
		postContent = messageForm.message.data
		posts = models.Posts.query.all()
		postID = len(posts)
		f = models.Posts(postID=postID,content=postContent,date=dt.datetime.today().strftime("%m/%d/%Y"),poster=account,target=target,secure=False,rank=0.0,ratings=0)
		db.session.add(f)
		db.session.commit()
		logging.info("User posted postID:"+str(f.postID)+" to user accID:"+str(target.accID))
		return redirect("http://localhost:5000/"+str(target.accID))
	postForm = ratePost()
	if postForm.validate_on_submit():
		##get the post
		logging.info("The user rated the user userID:"+postForm.postID.data+".")
		victim = models.Accounts.query.filter_by(accID=int(postForm.postID.data)).all()
		victim = victim[0]
		value = float(postForm.rating.data)
		curAdv = victim.rank*victim.ratings
		curAdv = curAdv+value
		curAdv = curAdv/(victim.ratings+1)
		victim.rank = round(curAdv,2)
		victim.ratings += 1
		db.session.commit()
		return redirect("http://localhost:5000/"+str(victim.accID))
	form = search()
	if form.validate_on_submit():
		logging.info("The user searched for users with the word(s) '"+form.searchWord.data+"'")
		session["search"] = "NONE"
		##Check the database for non friends
		names = models.Accounts.query.filter_by(login=form.searchWord.data).all()
		if(len(names) !=0):
			names = names[0]
			##make a list of friends
			if(len(models.Relationships.query.filter_by(userOne=names).filter_by(userTwo=account).all()) == 0):
				if(len(models.Relationships.query.filter_by(userTwo=names).filter_by(userOne=account).all()) == 0):
					logging.info("The user found results.")
					session["search"] = names.accID
		return redirect("http://localhost:5000/search")
	userProfile = models.Accounts.query.filter_by(accID=session["view"]).all()
	userProfile = userProfile[0]
	logging.info("User landed on profile accID:+"+str(userProfile.accID)+".")
	allList = models.Posts.query.filter_by(secure=False).order_by(models.Posts.rank.desc()).all()
	return render_template('view.html',
						   form=form,
						   messageForm=messageForm,
						   userProfile=userProfile,
						   postForm=postForm,
						   allList=allList,
						   logged = account,
						   title='Wonderland')

##The profile editing page route
@app.route('/edit', methods=['GET', 'POST'])
def edit():
	message=""
	if(session["user"]=="NONE"):
		logging.warning("User is not logged in and has been redirected to / route.")
		return redirect("http://localhost:5000/")
	account = models.Accounts.query.filter_by(accID=session["user"]).all()
	account = account[0]
	logging.info("User accID:"+str(account.accID)+" has moved to the route /edit.")
	form = search()
	if form.validate_on_submit():
		logging.info("The user searched for users with the word(s) '"+form.searchWord.data+"'")
		session["search"] = "NONE"
		##Check the database for non friends
		names = models.Accounts.query.filter_by(login=form.searchWord.data).all()
		if(len(names) !=0):
			names = names[0]
			##make a list of friends
			if(len(models.Relationships.query.filter_by(userOne=names).filter_by(userTwo=account).all()) == 0):
				if(len(models.Relationships.query.filter_by(userTwo=names).filter_by(userOne=account).all()) == 0):
					logging.info("The user found results.")
					session["search"] = names.accID
		return redirect("http://localhost:5000/search")
	updateForm = update()
	if updateForm.validate_on_submit():
		if(updateForm.oldPass.data != account.password):
			message="Current password incorrect!"
			logging.warning("The password provided is not correct.")
		else:
			##Check if the passwords match
			if(updateForm.checkpass.data != updateForm.password.data):
				message = "The passwords do not match."
				logging.warning("The new passwords provided do not match.")
			else:
				account.name = updateForm.name.data
				account.desc = updateForm.bio.data
				account.pic = updateForm.pic.data
				account.password = updateForm.password.data
				db.session.commit()
				logging.info("The user has successfully updated their account.")
				return redirect("http://localhost:5000/home")
	allList = models.Posts.query.filter_by(secure=False).order_by(models.Posts.rank.desc()).all()
	return render_template('edit.html',
						   form=form,
						   message=message,
						   allList=allList,
						   updateForm = updateForm,
						   logged = account,
						   title='Wonderland')

##The friend page route
@app.route('/friends', methods=['GET', 'POST'])
def friends():
	logging.info("The user has viewed their friend list on route /friends.")
	if(session["user"]=="NONE"):
		logging.warning("User is not logged in and has been redirected to / route.")
		return redirect("http://localhost:5000/home")
	account = models.Accounts.query.filter_by(accID=session["user"]).all()
	account = account[0]
	form = search()
	if form.validate_on_submit():
		logging.info("The user searched for users with the word(s) '"+form.searchWord.data+"'")
		session["search"] = "NONE"
		##Check the database for non friends
		names = models.Accounts.query.filter_by(login=form.searchWord.data).all()
		if(len(names) !=0):
			names = names[0]
			##make a list of friends
			if(len(models.Relationships.query.filter_by(userOne=names).filter_by(userTwo=account).all()) == 0):
				if(len(models.Relationships.query.filter_by(userTwo=names).filter_by(userOne=account).all()) == 0):
					logging.info("The user found results.")
					session["search"] = names.accID
		return redirect("http://localhost:5000/search")
	myRels = models.Relationships.query.filter_by(userOne=account).all()
	friends = []
	theirRels = models.Relationships.query.filter_by(userTwo=account).all()
	for x in myRels:
		friends.append(x.userTwo)
	for y in theirRels:
		friends.append(y.userOne)
	if(len(friends) == 0):
		bannerText = "Sorry, you haven't made any friends yet..."
		results = []
	else:
		bannerText = "Here they are:"
		results = friends
	allList = models.Posts.query.filter_by(secure=False).order_by(models.Posts.rank.desc()).all()
	return render_template('friends.html',
						   form=form,
						   results = results,
						   bannerText = bannerText,
						   allList=allList,
						   logged = account,
						   title='Wonderland')
