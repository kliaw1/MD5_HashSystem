'''
Created on Feb 6, 2020

@author: Karen
'''
import hashlib
import random

#PROBLEM 1: VERIFYING COMPUTED MD5 HASH VALUE
uID = "001"
password = "0599"

salt = "054"
givenHash = "4a1d6f102cd95fac33853e4d72fe1dc5"

def computeMD5(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()
def computeConcat(password, salt):
    concatenatedSalt = password + salt
    computedHash = computeMD5(concatenatedSalt)
    return computedHash
def verifier(password, salt, givenHash):
    concatenatedSalt = password + salt
    #print (concatenatedSalt)
    computedHash = computeMD5(concatenatedSalt)
    

    if computedHash == givenHash:
        print("Hash was verified to be the same as given hash")
        print("computed hash is " + computedHash)
        print("given hash is " + givenHash)
        return True
    #else: 
        #print("hash failed to match")
    return False
print(" Problem 1 ")
computedHash = verifier(password, salt, givenHash)
print()
print(" Problem 2 ")
#PROBLEM 2: DETERMINE THAT UID SAL AND PASSWORD VALUES CORRESPOND TO HASH

def generateRandomPass(): #generates a random password number
    testPass = str(random.randrange(0,1001))
    if len(testPass)!=4:
        x = 4-len(testPass)
        for addZero in range(x):
            testPass = "0"+testPass
    return testPass
def generateRandomSalt(): #generates a random salt
    testSalt = str(random.randrange(0,101))
    if len(testSalt)!=3:
        x = 3-len(testSalt)
        for addZero in range(x):
            testSalt = "0"+testSalt  
    return testSalt  
def makeList(): #generates random hashes to compare with the given hash list to find the password and salt
    f = open("sampleHashList.txt", "a") #append to the brute force test list
    for x in range(50):
        testPass = generateRandomPass()
        testSalt = generateRandomSalt()
        compCon = computeConcat(testPass, testSalt)
        finalHash= computeMD5(compCon)
        f.write(finalHash)
        f.write('\n')
        f.write(testPass + " " + testSalt)
        f.write('\n')
    f.close()

def getLines():
    f = open("sampleHashList.txt", "r")
    i = 0
    for lines in f:
        i = i + 1
    return i #get the number of lines in the sample hash file
def bruteforceCheck(idNum, hashLine):
    found = False #found is initially set to false until found
    #print ("current hash to crack is " + hashLine)
    f = open("sampleHashList.txt", "r")
    num = getLines() #get number of lines in the sample file used for the brute force test
    for i in range(0, num):
        line = f.readline()
        line = line.replace('\n', '')
        if(line == hashLine):
            foundPassSalt = f.readline(i+1) #if a match is found, read the next line, which has the password and salt for that hash that matched
            foundPassSalt = foundPassSalt.replace('\n', '')  #remove the new line character
            foundPass = foundPassSalt[:4] #get the first four characters of the string which is the password
            foundSalt = foundPassSalt[5:] #get the last three characters of the string which is the salt
            print("'" + idNum +"',    " + "'" + hashLine + "',        " + "'" + foundPass + "',            " + "'" + foundSalt + "'") #print in the format as directed
            found = True #set the found variable to true so it doesn't run the 'not found' condition
            break #break from the for loop since there's no reason to continue scanning the lines in the file
    if found == False: 
        print(hashLine + " had something wrong!")  
        print("Something went wrong!")
     
idFile = open("UID.txt", "r")
hashFile = open("Hash.txt", "r")

print("[UID                HASHED PASSWORD                 PASSWORD            SALT]")
for num in range(0,100): #run through both id and hash lists
    idNum = idFile.readline() 
    idNum = idNum.replace('\n', '') #remove the \n character at the end (otherwise the comparison returns false since they don't match otherwise
    x = hashFile.readline()
    x = x.replace('\n', '')
    bruteforceCheck(idNum, x)

#PROBLEM 3: TAKE USER INPUT FOR USER ID AND PASSWORD AND DETERMINE IF THE RESULTING HASH MATCHES OR NOT
print()
print(" Problem 3 ")
def checkPassword(user, givenPass):
    found = False #initialize found to false (finding the user id)
    check = False #initialize check to false (finding the matching hash)
    file = open("uIDwithPass.txt", "r"); #premade the user id with password and salt and resulting hash into one text file
    for i in range(0, 102): #run through every user
        line = file.readline() #read line
        use = line[:3] #trim and get substring containing user id
        if(use == user): #check if the inputted 'user' variable matches any users in the user list
            found = True #set found to true
            clip = line[9::] #clip line to get salt
            salted = clip[:3] #trim to get just salt, no hash
            hash = clip[4:] #trim to get hash
            hash = hash.replace('\n', '') #remove new line character to ensure no mismatch based on length
            calHash = computeConcat(str(givenPass), salted) #compute concatenation with givenPass and the corresponding user salt
            if(hash == calHash): #compare stored hash and computed hash
                check = True #set check to true
                print("The input password and salt matches the hash value in the database")
                break #break from for loop (no need to keep searching through files if user and password are found)
    if check == False: #if there were no matching hash, print
        print("The input password and salt does not match the hash value in the database")
    if found == False: #if there was no matching user id, print
        print("User does not exist")
user = input("Please enter Username: ") #request user input
givenPass = input("Please enter Password: ") #request password input
print(user + " " + password) 
checkPassword(user, givenPass)
