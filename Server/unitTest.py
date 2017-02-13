import os
import unittest
from app import db, models


##Test an account query
def getAccount(ID):
    acc = models.Accounts.query.filter_by(accID=ID).all()
    acc = acc[0]
    return acc.name

##Test a post query
def getPost(ID):
    post = models.Posts.query.filter_by(postID=ID).all()
    post = post[0]
    return post.poster.name

##Test a relationship query
def getRel(ID):
    rel = models.Relationships.query.filter_by(relID=ID).all()
    rel = rel[0]
    return rel.userOne.name

##Test adding an account
def addAcc(tempName):
    acc = models.Accounts(accID= 997,name=tempName,login="test3_login",password="test3Pass",pic="test3pic",rank=0.0,ratings=0)
    db.session.add(acc)
    db.session.commit()
    result = len(models.Accounts.query.filter_by(name=tempName).all())
    return result

##Test removing an account
def delAcc(tempName):
    acc = models.Accounts.query.filter_by(name=tempName).all()
    acc = acc[0]
    db.session.delete(acc)
    db.session.commit()
    result = len(models.Accounts.query.filter_by(name=tempName).all())
    return result

##Test adding a post
def addPost(tempName):
    post = models.Posts(postID= 997,content=tempName,date="21/12/1990",secure=True,rank=0.0,ratings=0)
    db.session.add(post)
    db.session.commit()
    result = len(models.Posts.query.filter_by(content=tempName).all())
    return result

##Test removing a post
def delPost(tempName):
    post = models.Posts.query.filter_by(content=tempName).all()
    post = post[0]
    db.session.delete(post)
    db.session.commit()
    result = len(models.Posts.query.filter_by(content=tempName).all())
    return result

##Test adding a relationship
def addRel(tempNum):
    rel = models.Relationships(relID = tempNum)
    db.session.add(rel)
    db.session.commit()
    result = len(models.Relationships.query.filter_by(relID=tempNum).all())
    return result

##Test removing a relationship
def delRel(tempNum):
    rel = models.Relationships.query.filter_by(relID=tempNum).all()
    rel = rel[0]
    db.session.delete(rel)
    db.session.commit()
    result = len(models.Relationships.query.filter_by(relID=tempNum).all())
    return result

##Check an account password
def checkPass(ID,password):
    acc = models.Accounts.query.filter_by(accID=ID).all()
    acc = acc[0]
    if(acc.password == password):
        return True
    else:
        return False

##Check that two passwords match
def compPass(one,two):
    if(one==two):
        return True
    else:
        return False

##Get a list of friends
def getFriends(ID):
    acc = models.Accounts.query.filter_by(accID=ID).all()
    acc = acc[0]
    friends = []
    myRels = models.Relationships.query.filter_by(userOne=acc).all()
    theirRels = models.Relationships.query.filter_by(userTwo=acc).all()
    for x in myRels:
        friends.append(x.userTwo)
    for y in theirRels:
        friends.append(y.userOne)
    return len(friends)

##Get a list of posts relvant to an account
def getPosts(ID):
    acc = models.Accounts.query.filter_by(accID=ID).all()
    acc = acc[0]
    posts = models.Posts.query.filter_by(target=acc).all()
    return len(posts)

##Rate a user
def rateUser(ID,rank):
    acc = models.Accounts.query.filter_by(accID=ID).all()
    acc = acc[0]
    acc.rank = float(((acc.rank*acc.ratings)+rank)/(acc.ratings+1))
    db.session.commit()
    acc = models.Accounts.query.filter_by(accID=ID).all()
    acc = acc[0]
    return acc.rank

##Rate a post
def ratePost(ID,rank):
    post = models.Posts.query.filter_by(postID=ID).all()
    post = post[0]
    post.rank = float(((post.rank*post.ratings)+rank)/(post.ratings+1))
    db.session.commit()
    post = models.Posts.query.filter_by(postID=ID).all()
    post = post[0]
    return post.rank

class TestCase(unittest.TestCase):
    def setUp(self):
        ##Add a couple of each model for use in the tests
        ## use 998 and 999 to reduce chance of currently
        ##Existing elements blocking these.
        a1 = models.Accounts(accID= 998,name="test1_name",login="test1_login",password="test1Pass",pic="test1pic",rank=0.0,ratings=0)
        a2 = models.Accounts(accID= 999,name="test2_name",login="test2_login",password="test2Pass",pic="test2pic",rank=0.0,ratings=0)
        p1 = models.Posts(postID=998,content="This is a test.",date="21/12/1990",poster=a1,target=a2,secure=True,rank=0.0,ratings=0)
        r1 = models.Relationships(relID = 998, userOne=a1, userTwo = a2)
        ##Add these to the database
        db.session.add(a1)
        db.session.add(a2)
        db.session.add(p1)
        db.session.add(r1)
        db.session.commit()


    def tearDown(self):
        ##Get the accounts,posts and relationships declared in the setUp
        a1 = models.Accounts.query.filter_by(accID=998).all()
        a1 = a1[0]
        a2 = models.Accounts.query.filter_by(accID=999).all()
        a2 = a2[0]
        p1 = models.Posts.query.filter_by(postID=998).all()
        p1 = p1[0]
        r1 = models.Relationships.query.filter_by(relID=998).all()
        r1 = r1[0]
        ##Remove them from the database
        db.session.delete(a1)
        db.session.delete(a2)
        db.session.delete(p1)
        db.session.delete(r1)
        db.session.commit()


    ##Test an account query
    def testAccountQuery(self):
        assert getAccount(998) == "test1_name"

    ##Test a post query
    def testPostQuery(self):
        assert getPost(998) == "test1_name"

    ##Test a relationship query
    def testRelQuery(self):
        assert getRel(998) == "test1_name"

    ##Test adding an account
    def testaddAcc(self):
        assert addAcc("TEST") == 1

    ##Test removing an account
    def testdelAcc(self):
        assert delAcc("TEST") == 0

    ##Test adding a post
    def testaddPost(self):
        assert addPost("TEST") == 1

    ##Test removing a post
    def testdelPost(self):
        assert delPost("TEST") == 0

    ##Test adding a relationship
    def testaddRel(self):
        assert addRel(997) == 1

    ##Test removing a relationship
    def testdelRel(self):
        assert delRel(997) == 0

    ##Test a correct password will be validated
    def testCorrectPass(self):
        assert checkPass(998,"test1Pass") == True

    ##Test an incorrect password will be rejected
    def testCorrectPass(self):
        assert checkPass(998,"wrongPass") == False

    ##Test an correct password comparison will be accepted
    def testCorrectPassComp(self):
        assert compPass("rightPass","rightPass") == True

    ##Test an incorrect password comparison will be rejected
    def testIncorrectPassComp(self):
        assert compPass("rightPass","wrongPass") == False

    ##Test for a list of friends
    def testFriends(self):
        assert getFriends(998) == 1

    ##Test for a list of posts
    def testPosts(self):
        assert getPosts(999) == 1

    ##Test rating a user
    def testRateUser(self):
        assert rateUser(998,5.0) == 5.0

    ##Test rating a post
    def testRatePost(self):
        assert ratePost(998,5.0) == 5.0


if __name__ == '__main__':
    unittest.main()
