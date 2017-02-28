from app import db, models
from queries import *
import random
import string

#Lists for random generation.
firstNames = ['Donny', 'Miles', 'Renaldo', 'Mitchel', 'Jamar', 'Kevin',
              'Zackary', 'Roy', 'Cedrick', 'Dorsey', 'Jamal', 'Ed', 'Jerrell',
              'Antony', 'Duncan', 'Harrison', 'Freddie', 'Demarcus', 'Ronny',
              'Edward', 'Arica', 'Virginia', 'Martha', 'Amiee', 'Kayleen',
              'Lawanna', 'Sharonda', 'Tiffaney', 'Enda', 'Meghan', 'Serafina',
              'Sebrina', 'Mathilde', 'Cierra', 'Rosalyn', 'Karen', 'Jennell',
              'Margy', 'Kali', 'Tatyana']


lastNames = ['Thurber', 'Sase', 'Seoh', 'Mcneill', 'Foley', 'Flemming',
             'Ghildyal', 'Bashevis', 'Lyons', 'Lowenstein', 'Hansen', 'Ettner',
             'Bodrock', 'Tam', 'Judd', 'Revlin', 'Grusby', 'Inniss', 'Conklin',
             'Esslemont', 'Malova', 'Barrant', 'Dottin', 'Campos', 'Magruder',
             'Serfling', 'Touborg', 'Casacchia', 'Merrill', 'Larsen', 'Hyatt',
             'Burner', 'Ebbitt', 'Randolph', 'Munoz-porras', 'Jaccarino',
             'Butters', 'Sommariva']

locations = ['Here', 'There', 'Not There', 'Everywhere', 'Overhere', 'Where']

roomType = ['Seminar Room', 'Lecture Theater', 'Computer Suite',
            'Conference Suite']

roomAccess = ['W', 'A', 'L']

courseTitle = ['Business', 'Geography', 'Witchcraft', 'Drama', 'Mandarin',
               'Art of Manliness', 'Mathematics', 'Physics', 'Biology',
               'English', 'Computer Science']

#Specified to decide how many database entries will be added.
adminCount = 25
trainerCount = 25
roomCount = 15
classCount = 30
delCount = 40

#This will generate a random 8 digit password made up of capital letters and
#numbers.
def createPassword():
    characters = string.ascii_uppercase + string.digits
    password = ''
    x = 0
    while x < 8:
        password = password + random.choice(characters)
        x = x + 1
    return password

#This will create a random phone number.
def createPhoneNum():
    characters = string.digits
    phoneNum = '447'
    x = 0
    while x < 9:
        phoneNum = phoneNum + random.choice(characters)
        x = x + 1
    return int(phoneNum)

#This will concatenate a random first and last name.
def createName():
    name = random.choice(firstNames) + ' ' + random.choice(lastNames)
    return name

#This will create a user name based on the name handed to the function.
def createUsername(name):
    name = name + str(random.randint(0,999))
    return name

#This will create a name and email address to together.
def createNameandEmail():
    firstName = random.choice(firstNames)
    lastName = random.choice(lastNames)
    name = firstName + ' ' + lastName
    email = firstName[0] + lastName + '@email@com'
    return name, email

#This is where the adding to the database begins.
#First Admins.
print("Creating admins.")
x = 0
while x < adminCount:
    print('.', end='', flush=True)
    name = createName()
    username = createUsername(name)
    password = createPassword()
    addNewAdmin(name, username, password)
    x = x + 1
print('')

#Then Trainers.
print("Creating trainers.")
x = 0
while x < trainerCount:
    print('.', end='', flush=True)
    name, email = createNameandEmail()
    address = random.choice(locations)
    phone = createPhoneNum()
    username = createUsername(name)
    password = createPassword()
    addNewTrainer(name, address, phone, email, username, password)
    x = x + 1
print('')

#Next Rooms.
print("Creating rooms.")
x = 0
while x < roomCount:
    print('.', end='', flush=True)
    capacity = random.randint(0,200)
    roomType = random.choice(roomType)
    location = random.choice(locations)
    accessRating = random.choice(roomAccess)
    addNewRoom(capacity, roomType, accessRating, location)
    x = x + 1
print('')

#Forthly Courses.
print("Creating courses.")
for items in courseTitle:
    print('.', end='', flush=True)
    addNewCourse(items, "The description seriously does not matter.")
print('')

#Queries currently made databases for dependencies.
rooms = rooms()
trainers = trainers()
delegates = delegates()
courses = courses()

#Penultimately Classes.
print("Creating classes.")
x = 0
while x < classCount:
    print('.', end='', flush=True)
    courseNum = random.randint(0,10)
    capacity = random.randint(0,200)
    roomNum = random.randint(0,roomCount)
    trainerNum = random.randint(0,trainerCount)
    waitingList = []
    addNewClass(courses[courseNum].courseID, "Class Title",
                "Some description for a class.", capacity,rooms[roomNum].roomID,
                trainers[trainerNum].trainerID, waitingList)
    x = x + 1
print('')

#Queries classes for dependency on delegates.
classes = classes()

#Finally Delegates.
print("Creating delegates.")
x = 0
while x < delCount:
    print('.', end='', flush=True)
    name = createName()
    username = createUsername(name)
    password = createPassword()
    classList = random.sample(classes, 5)
    addNewDel(name, username, password, classList)
    x = x + 1
print('')

print('DONE')
