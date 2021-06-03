# Store images in Sqlite3 DB with Python
# Helps user to store and retrive images
# Very useful if user wants a backup for his images
# Supports both single file adding and batch images adding
# Your image should be beside your python script
# For adding all images place the script where images are located  
# Script created by Ayan: ayanU881@gmail.com

import os
import sqlite3

DATABASE='db/image.db'

conn=sqlite3.connect(DATABASE)
batch=[]#to check how many files have been added at once

#creating table
def createTable():	
	command="""CREATE TABLE objectfiles(photoname TEXT NOT NULL, image BLOB);"""

	try:
		conn.execute(command)
		print("Table has been created")
	except:
		print("You already have a safe")


#converting image file to binary object
def convertToBinary(filename):
	with open(filename,'rb') as f:
		blobData=f.read()

	return blobData

#inserting binary into DB
def insertFile():
	filename=input("Enter name of photo:")
	params=(filename,convertToBinary(filename))
	conn.execute("INSERT INTO objectfiles VALUES(?,?);",params)
	print("inserted !")
	conn.commit()

#show listed files in db
def showfiles():
	command="SELECT rowid,photoname FROM objectfiles;"

	cursor=conn.execute(command)

	for row in cursor:
		print('ID:',row[0])
		print('PHOTO:',row[1])
		print()
#write the image
def writeFile(blobdata,filename):
	with open(filename,'wb') as f:
		f.write(blobdata)

	print("Success!")

#retriving image data from database
def retriveImage():
	photo_name=input("Enter photo name:")
	id=int(input("Enter id number:"))
	cursor=conn.execute(f"SELECT image FROM objectfiles WHERE rowid={id};")
	for row in cursor:
		writeFile(row[0],photo_name)

def batchFileInsert():
	filelist=os.listdir()

	for file in filelist:
		ext=file.split('.')[-1]
		if ext=='jpg' or ext=='png' or ext=='jpeg':		
			conn.execute("INSERT INTO objectfiles VALUES(?,?);",(file,convertToBinary(file)))
			batch.append(file)

	print(f"{len(batch)} files added to database")
	batch.clear()

#creates table if database doesn't have any table
createTable()

option=''
while option!='q':
	print("what would you like to do now?")
	print('Press i to store single image.')
	print('Press s to show image list.')
	print('Press r to retrive Image.')
	print('Press b to add all images.')
	print('Press q to quit')

	option=input('>')

	if option.lower()=='i':
		insertFile()

	if option.lower()=='s':
		showfiles()

	if option.lower()=='r':
		retriveImage()

	if option.lower()=='b':
		batchFileInsert()

	if option.lower()=='q':
		break