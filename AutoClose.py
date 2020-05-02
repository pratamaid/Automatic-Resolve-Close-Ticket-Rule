#This Python script is used to update the status of the Request through Custom Schedules for Custom Scripts.

#Below are the list of Packages used in this Script.We have used a Python Library called 'Requests' which is not bundled by default with Python installation.
#More information on this Package and the instructions on installing it on the Application Server are available in the following link.
# http://docs.python-requests.org/en/latest/user/install/#install
import requests
import sys
import json
import datetime
from pprint import pprint


#----------------------------------------------------Inputs Required---------------------------------------------------#
#Update the application url and portnumber here
url = "http://localhost:8080"

#Update the Technician's API key here.
TechnicianKey=''

#This is the name of the Operation that is performed in this API call.
OperationName=''

#Value for the status field.
status_name = 'Closed'

#Value for the resolution.
# resolution_value = 'Ticket Closed'

#----------------------------------------------------Inputs Required---------------------------------------------------#



#Create a Session Object that will be used to pass different parameters across the HTTP requests.
#All the parameters like the ServerName , protocol , portnumber and Technician API key that are used in the Script are Input here.Please update this based on your Environment.
with requests.Session() as s:
    url = url

#Reading the argument passed to the script.The Report Output is stored as array of JSON Objects(one JSON object for each row) in a file and its path is provided to the Script as input.
reportJson = str(sys.argv[1])

#Reading the Request JSON array from the json file.
json_data=open(reportJson).read()
data = json.loads(json_data.encode("utf-8"))

#Each JSON object has column names as the keys and corresponding data as the values.Please find a sample json below for reference.
'''[
    {
        "Request ID":"47",
        "Technician":"Heather Graham"
    },
    {
        "Request ID":"128",
        "Technician":"Shawn Adams"
    }
]'''

#This block is used to iterate through the JSON array read the value of Request ID in each row.
for request_Obj in data:
	RequestID = request_Obj['Request ID']
	#Timeclose = request_Obj['Closeticket']
	
	#Creating the json object for the Request Create operation and storing it in the variable 'jsonData'
	operationJson={}
	operationJson["operation"]={}
	detailsJson={}
	detailsJson["details"]={}
	jsonObj={}
	jsonObj["status"]=status_name
	# jsonObj["resolution"]=resolution_value
	jsonObj["COMPLETEDTIME"]=detailsJson["Timeclose"]
	jsonObj["RESOLVEDTIME"]=detailsJson["Timeclose"]

	detailsJson["details"]=jsonObj
	operationJson["operation"]=detailsJson
	jsonData=json.dumps(operationJson)
	
	#Constructing the url for the API call and submitting that to the ServiceDesk Plus server
	apprUrl = url + "/sdpapi/request/" + RequestID
	data = {'OPERATION_NAME' : 'EDIT_REQUEST','INPUT_DATA' : jsonData ,'TECHNICIAN_KEY': TechnicianKey,'format':'json'}
	r = s.post(apprUrl,data)
	print(r.text)
	
	if(r.status_code == 200):#Checking if the API Request was Submitted successfully.The Status Code 200 is returned if the POST operation had succeeded 
		
		#Reading the Json Response got by submitting the API request to the ServiceDesk application
		
		responseobj=r.json()
		status=responseobj["operation"]["result"]["status"]
		message=responseobj["operation"]["result"]["message"]
		
		#This message will be printed to Result column in the Custom Schedules list view , if the request update operation was successful.
		print("Request " + RequestID +" - "+ status +" - "+ message)
									
			
	else: 
		
		#This message will be printed to Result column in the Custom Schedules list view , if the request update operation was a fai;ure.
		print("Problem updating requests")
			
