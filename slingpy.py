#!/usr/bin/env python3

from datetime import datetime
from datetime import date
from dateutil import parser
import pytz
import requests
import fileinput
import os
import sys
# https://www.tutorialspoint.com/How-to-open-a-file-in-the-same-directory-as-a-Python-script


#pip3 install python-dateutil
#pip3 install pytz


# slingPy
# Goal: create a schedule notifier without the use of Sling Premimum

# API
# https://api.sling.is/#/

# curl -X GET "https://api.sling.is/v1/shifts/current" 
#-H "accept: application/json" 
#-H "Authorization: bf4ee23cb6b248b9b1ae6a8aa9ba4aad "

# Start of Loop
# apikeys must be obtained for each user :(
# login to sling, right click Inspect, go to network tab
# refresh page, click on item with "session?XXYYXX"
# under "Request Headers" you can find authorization token

# Create file "apikeys.txt" with each API key on it's own line
apikeys = [line.rstrip('\n') for line in open(os.path.join(sys.path[0],"apikeys.txt"))]


# File to insert in to php code
webFile = "working.php"

# clear webFile fresh
f = open(os.path.join(sys.path[0], webFile), "w")
f.write("<?php" + "\n" + "echo \"<br>\"" + ";" + "\n" + "echo \"<br>\"" + ";" + "\n" + "echo \"Currently Working:\"" + ";" + "\n" + "echo \"<br>\"" + ";" + "\n")
f.close()

for key in apikeys:
    API = key
    # Get name pertaining to API key
    header = "accept: application/json"
    url = "https://api.sling.is/v1/account/sessions"
    headers = {'accept': 'application/json', 'Authorization' : API}
    r = requests.get(url, headers=headers)
    #print(r.status_code)
    if r.status_code == 405:
        # bad response
        print("Bad response code:", r.status_code )
        exit
    # list -> dict
    jsonOutput = r.json()
    # try to convert json output to dict
    try:
      jsonDict = jsonOutput[0]
    except IndexError:
        print("User has no future shift. User must have a shift scheduled in the next 6 weeks.")
        print("Program will continue, however.")
    else:

    # got the names here
    # nested dict
      fname = jsonDict['user']['name']
      lname = jsonDict['user']['lastname']

      

    # Now get next/current shift
    # Current shifts are shifts that have been clocked into but haven’t been clocked out of yet;
    # shifts that start within the next 6 hours; and at least one (first) shift in the next 4 weeks.
      url = "https://api.sling.is/v1/shifts/current"
      r = requests.get(url, headers=headers)
      jsonOutput = r.json()
    try:
      jsonDict = jsonOutput[0]
    except IndexError:
        print("User has no future shift. User must have a shift scheduled in the next 6 weeks.")
        print("Program will continue, however.")
    else:
    # get shift start and shift end
      shiftStart = jsonDict['dtstart']
      shiftEnd = jsonDict['dtend']  

      position = jsonDict['position']['name']
      # get first letter of each word in string
      # https://stackoverflow.com/questions/41191424/extract-first-character-of-each-word-from-the-sentence-string/41191867
      position = (''.join([x[0] for x in position.split()]))

    # thank stallman I don't have to deal with the full date
      shiftStart = parser.parse(shiftStart)
      shiftEnd = parser.parse(shiftEnd)

    # okay this is related to date.. pytz = py timezone?
      today = datetime.now(pytz.utc)
    # if right now is after shift start but between shift end
    # if user is currently working
      if ( shiftStart < today < shiftEnd ):
          # convert datetime to str to int
          shiftStartHR = int(shiftStart.strftime("%H"))
          shiftEndHR = int(shiftEnd.strftime("%H"))

          shiftStartMIN = str(shiftStart.strftime("%M"))
          shiftEndMIN = str(shiftEnd.strftime("%M"))

          # convert away from military time
          if shiftStartHR > 12:
            shiftStartHR = shiftStartHR - 12

          if shiftEndHR > 12:
            shiftEndHR = shiftEndHR - 12

          # convert back to str for concat
          shiftStartHR = str(shiftStartHR)
          shiftEndHR = str(shiftEndHR)

          f = open(os.path.join(sys.path[0], webFile), "a")
          f.write("\n" + "echo " + "\"" + fname + " " + lname
          + " [" + position + "]" +
          " (" + shiftStartHR + ":" + shiftStartMIN + 
          " - " 
          + shiftEndHR + ":" + shiftEndMIN + ")" +  "\""
          + ";" + "\n" + "echo \"<br>\";")
          f.close()

# Append end of php
f = open(os.path.join(sys.path[0], webFile), "a")
f.write( "\n" + "?>")
f.close()



