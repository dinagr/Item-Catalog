from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from puppies import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()


#Add Shelters
shelter1 = Shelter(name = "Oakland Animal Services", address = "1101 29th Ave", city = "Oakland", state = "California", zipCode = "94601", website = "oaklandanimalservices.org")
session.add(shelter1)

shelter2 = Shelter(name = "San Francisco SPCA Mission Adoption Center", address="250 Florida St", city="San Francisco", state="California", zipCode = "94103", website = "sfspca.org")
session.add(shelter2)

shelter3 = Shelter(name = "Wonder Dog Rescue", address= "2926 16th Street", city = "San Francisco", state = "California" , zipCode = "94103", website = "http://wonderdogrescue.org")
session.add(shelter3)

shelter4 = Shelter(name = "Humane Society of Alameda", address = "PO Box 1571" ,city = "Alameda" ,state = "California", zipCode = "94501", website = "hsalameda.org")
session.add(shelter4)

shelter5 = Shelter(name = "Palo Alto Humane Society" ,address = "1149 Chestnut St." ,city = "Menlo Park", state = "California" ,zipCode = "94025", website = "paloaltohumane.org")
session.add(shelter5)


#Add Puppies

male_names = ["Bailey", "Max", "Charlie", "Buddy","Rocky","Jake", "Jack", "Toby", "Cody", "Buster", "Duke", "Cooper", "Riley", "Harley", "Bear", "Tucker", "Murphy", "Lucky", "Oliver", "Sam", "Oscar", "Teddy", "Winston", "Sammy", "Rusty", "Shadow", "Gizmo", "Bentley", "Zeus", "Jackson", "Baxter", "Bandit", "Gus", "Samson", "Milo", "Rudy", "Louie", "Hunter", "Casey", "Rocco", "Sparky", "Joey", "Bruno", "Beau", "Dakota", "Maximus", "Romeo", "Boomer", "Luke", "Henry"]

female_names = ['Bella', 'Lucy', 'Molly', 'Daisy', 'Maggie', 'Sophie', 'Sadie', 'Chloe', 'Bailey', 'Lola', 'Zoe', 'Abby', 'Ginger', 'Roxy', 'Gracie', 'Coco', 'Sasha', 'Lily', 'Angel', 'Princess','Emma', 'Annie', 'Rosie', 'Ruby', 'Lady', 'Missy', 'Lilly', 'Mia', 'Katie', 'Zoey', 'Madison', 'Stella', 'Penny', 'Belle', 'Casey', 'Samantha', 'Holly', 'Lexi', 'Lulu', 'Brandy', 'Jasmine', 'Shelby', 'Sandy', 'Roxie', 'Pepper', 'Heidi', 'Luna', 'Dixie', 'Honey', 'Dakota']

puppy_images = ["https://www.google.co.il/imgres?imgurl=http://i.imgur.com/nZlaeSH.jpg&imgrefurl=https://www.reddit.com/r/aww/comments/1oxs8p/extremely_photogenic_puppy/&h=3456&w=5184&tbnid=d6J7dbQyjLQ1UM:&docid=lnW3iWYnLnlooM&ei=2620Vq7zNMO-OozzqfAP&tbm=isch&ved=0ahUKEwjuzICP5-DKAhVDnw4KHYx5Cv4QMwgyKAIwAg",
                "https://www.google.co.il/imgres?imgurl=https://c1.staticflickr.com/5/4112/5170590074_714d36db83_b.jpg&imgrefurl=https://www.flickr.com/photos/27587002@N07/5170590074&h=812&w=1024&tbnid=IK61rTGRUXP04M:&docid=c0KI6K67s0XnVM&ei=2620Vq7zNMO-OozzqfAP&tbm=isch&ved=0ahUKEwjuzICP5-DKAhVDnw4KHYx5Cv4QMwgzKAMwAw",
                "https://www.google.co.il/imgres?imgurl=http://upload.wikimedia.org/wikipedia/commons/6/64/The_Puppy.jpg&imgrefurl=https://www.thedodo.com/top-puppy-names-of-2014-858523582.html&h=683&w=1024&tbnid=YftG_KOtbpnrMM:&docid=BcAP4neSEhZupM&ei=2620Vq7zNMO-OozzqfAP&tbm=isch&ved=0ahUKEwjuzICP5-DKAhVDnw4KHYx5Cv4QMwhXKB0wHQ",
                "https://www.google.co.il/imgres?imgurl=http://hellogiggles.com/wp-content/uploads/2013/12/09/a-cutest-puppies-11.jpg%253F123&imgrefurl=http://hellogiggles.com/puppies-are-girls-best-friend/&h=375&w=500&tbnid=iCIg3U5XvoBZKM:&docid=CSa0d1UZbTOEeM&ei=2620Vq7zNMO-OozzqfAP&tbm=isch&ved=0ahUKEwjuzICP5-DKAhVDnw4KHYx5Cv4QMwhRKBcwFw",
                "https://www.google.co.il/imgres?imgurl=http://www.rchangout.com/wp-content/uploads/2015/09/puppy-2.jpg&imgrefurl=http://www.rchangout.com/puppy-training-pads-make-potty-training-easier/&h=545&w=580&tbnid=kqiMInHGDQJjTM:&docid=rUQFpJVfgAO8vM&ei=2620Vq7zNMO-OozzqfAP&tbm=isch&ved=0ahUKEwjuzICP5-DKAhVDnw4KHYx5Cv4QMwh7KEEwQQ",
                "https://www.google.co.il/imgres?imgurl=http://indiabright.com/wp-content/uploads/2015/10/31-cute-puppies-that-you-want-to-hug-31.jpg&imgrefurl=http://indiabright.com/puppy-pictures-cute-puppy-pics-cute-puppies/&h=1200&w=1600&tbnid=mnqi3GgkVAkFiM:&docid=EYPoNZ7UHHx6HM&ei=2620Vq7zNMO-OozzqfAP&tbm=isch&ved=0ahUKEwjuzICP5-DKAhVDnw4KHYx5Cv4QMwhYKB4wHg",
                "https://www.google.co.il/imgres?imgurl=http://www.pitt.edu/~egs21/infocute.jpg&imgrefurl=http://www.pitt.edu/~egs21/info.html&h=390&w=600&tbnid=GFX-T5uSQio-oM:&docid=l33jdHPYEDQW5M&ei=2620Vq7zNMO-OozzqfAP&tbm=isch&ved=0ahUKEwjuzICP5-DKAhVDnw4KHYx5Cv4QMwhCKBIwEg",
                "https://www.google.co.il/imgres?imgurl=http://www.imgion.com/images/01/White-Cute-Puppy-.jpg&imgrefurl=https://www.tes.com/lessons/OmgyQBwqXthIgA/puppy-care&h=800&w=1280&tbnid=rsfCZBVKmqLiSM:&docid=CfJCnv0eIL6XzM&ei=2620Vq7zNMO-OozzqfAP&tbm=isch&ved=0ahUKEwjuzICP5-DKAhVDnw4KHYx5Cv4QMwg6KAowCg",
                "https://www.google.co.il/imgres?imgurl=http://www.pawderosa.com/images/puppies.jpg&imgrefurl=http://www.pawderosa.com/puppies!.html&h=333&w=500&tbnid=YoV6I4BmMqqraM:&docid=etcGLLZMe4iwPM&ei=2620Vq7zNMO-OozzqfAP&tbm=isch&ved=0ahUKEwjuzICP5-DKAhVDnw4KHYx5Cv4QMwg4KAgwCA",
                "https://www.google.co.il/imgres?imgurl=http://assets.nydailynews.com/polopoly_fs/1.1245686!/img/httpImage/image.jpg_gen/derivatives/article_970/afp-cute-puppy.jpg&imgrefurl=https://www.udacity.com/course/viewer%23!/c-ud088/l-4325204629/m-4291466849&h=970&w=970&tbnid=A1ZxIJ9TzuYiwM:&docid=E805k0xvXVM6YM&ei=2620Vq7zNMO-OozzqfAP&tbm=isch&ved=0ahUKEwjuzICP5-DKAhVDnw4KHYx5Cv4QMwg0KAQwBA"]

#This method will make a random age for each puppy between 0-18 months(approx.) old from the day the algorithm was run.
def CreateRandomAge():
	today = datetime.date.today()
	days_old = randint(0,540)
	birthday = today - datetime.timedelta(days = days_old)
	return birthday

#This method will create a random weight between 1.0-40.0 pounds (or whatever unit of measure you prefer)
def CreateRandomWeight():
	return random.uniform(1.0, 40.0)

for i,x in enumerate(male_names):
	new_puppy = Puppy(name = x, gender = "male", dateOfBirth = CreateRandomAge(),picture=random.choice(puppy_images) ,shelter_id=randint(1,5), weight= CreateRandomWeight())
	session.add(new_puppy)
	session.commit()

for i,x in enumerate(female_names):
	new_puppy = Puppy(name = x, gender = "female", dateOfBirth = CreateRandomAge(),picture=random.choice(puppy_images),shelter_id=randint(1,5), weight= CreateRandomWeight())
	session.add(new_puppy)
	session.commit()
