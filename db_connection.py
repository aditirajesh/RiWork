from pymongo import MongoClient
import os 
from dotenv import load_dotenv
client = MongoClient()
client = MongoClient('localhost', 27017)
import pandas as pd 
import random 

mydatabase = client['Riwork']   #mongodb database that will be storing all information for this application 

def company_info_logging(company_id,company_name,total_branches): 
    '''This function is used to gain inputs from user about their company details and accordingly updating them on the mongodb server'''
    company_collection = mydatabase['Company']   #collection which will be storing the company information 
    branches_list = branch_info_logging(total_branches)

    document ={
        'CompanyName':company_name, #name of the company 
        'CID':company_id,     #company id 
        'Branches':branches_list
    }  #this is the document that will be inserted into the company collection 

    record = company_collection.insert_one(document)
    print(record.inserted_id)

#company_info_logging('RadioStudio',1221,312021,500,2)

def employee_info_logging(cmpid,empid,empname,email,latitude,longitude,teamno,teamname,password):
    employee_collection = mydatabase['Employees']
    
    document = {
        'CMPID':cmpid,
        'EMPID':empid,
        'ENAME':empname,
        'EMAIL':email,
        'LATITUDE':latitude,
        'LONGITUDE':longitude,
        'TEAM': {teamno:teamname},
        'PASSWORD':password}
    
    record = employee_collection.insert_one(document)
    return record.inserted_id

#employee_info_logging('1221','1001','Aditi Rajesh',9884713174,'guindy','aditir2607@gmail.com','CEO','Finance','abcde')

def branch_info_logging(total_branches):
     branches = []
     for _ in total_branches:
          branch_id = int(input('Enter branch id: '))
          branch_name = input('Enter branch name: ')
          branch_latitude = float(input('Enter latitude: '))
          branch_longitude = float(input("Enter longitude: "))
          branch_seats = int(input('Enter number of seats in branch: '))
          branch_address = input('Enter the address: ')
          branch_details = {"OfficeID":branch_id,"OfficeName":branch_name,
                            "Latitude":branch_latitude,"Longitude":branch_longitude,
                            "Capacity":branch_seats,"Address":branch_address}
          branches.append(branch_details)
     return branches
     

def mass_entry(csv_file):
    '''This function allows mass entry of employee details - through a csv file'''
    employee_mass_collection = mydatabase['Employees']
    file = pd.read_csv(csv_file,encoding = "utf-8").dropna()
    file_records = file.values.tolist()

    for record in file_records:
        document = {
        'EMPID':record[0],
        'ENAME':record[1],
        'EMAIL':record[2],
        'PASSWORD':record[3],
        'LATITUDE':record[4],
        'LONGITUDE':record[5],
        'TEAM':{record[6]:record[7]}
        }

        record = employee_mass_collection.insert_one(document)
        print(record.inserted_id)

    print('All records have been successfully logged into the database!')

def get_users():
    '''this function is used to obtain all the users that have an account in the '''
    company_collection = mydatabase["Company"]
    employee_collection = mydatabase['Employees']
    users = []
    for employee in employee_collection.find({},{"ENAME":1,"EMAIL":1,"PASSWORD":1}):
           users.append(employee)#gives a list of all the registered mails and their password 
           #print(employee)

    return list(users)
    
#print(get_users())
#//MASS LOGGING IN EMPLOYEES 
def mass_info_logging():
    for i in range(0,156):
         #//CREATING 156 EMPLOYEE RECORDS 
        employee_collection = mydatabase["Employees"]
        cmpid = 12251
        empid = i
        ename = "test"+str(i)
        email = "test"+str(i)+"@gmail.com"
        password = "test"+str(i)+"pass"
        if i <= 4:
             team = {"0":"Scrum Team"}

        elif 4 < i <= 13:
             team = {"1":"IT Operations Team"}

        elif 13 < i <= 23:
             team = {"2":"DevOps Team"}

        elif 23 < i <= 35:
             team = {"3":"Development Team"}

        elif 35 < i <= 48:
             team = {"4": "Product Marketing Team"}

        elif 48 < i <= 67:
             team = {"5": "Quality Assurance Team"}

        elif 67 < i <= 76:
             team = {"6": "Documentation Team"}

        elif 76 < i <= 81:
             team = {"7": "Localisation Team"}

        elif 81 < i <= 83:
             team = {"8":"Product Support Team"}
             
        elif 83 < i <= 104:
             team = {"9":"Product Management Team"}
             
        elif 104 < i <= 155:
             team = {"10":"UI design Team"}
        latitude = random.uniform(12.9637,13.2172)
        longitude = random.uniform(80.1209,80.3170)

        document = {"CMPID":cmpid,
                    "EMPID": empid,
                    "ENAME": ename,
                    "EMAIL": email,
                    "PASSWORD":password,
                    "LATITUDE":latitude,
                    "LONGITUDE":longitude,
                    "TEAM":team}
        
        record = employee_collection.insert_one(document)

    return 'insertion complete'

#mass_info_logging()
             
def teamdata_retrieval(cmpid):
    '''gives information about the number of employees in the team'''
    teams = []
    teams_dict = {}
    client = MongoClient('localhost', 27017)
    mydatabase = client['Riwork'] 
    employee_collection = mydatabase['Employees']

    for employee in employee_collection.find():
        team = employee["TEAM"]
        team_id = list(team.keys())[0]
        if team_id in teams_dict:
            teams_dict[team_id] = teams_dict[team_id] + 1

        else:
            teams_dict[team_id] = 1 

    for id in teams_dict:
        teams.append(teams_dict[id])

    return teams


def officedata_retrieval(cmpid):
    '''obtaining office data from the database - specifically retrieving branch data'''
    office_locations = []
    client = MongoClient('localhost', 27017)
    mydatabase = client['Riwork'] 
    company_collection = mydatabase['Company']  #accessing the company collection 
    item = company_collection.find_one({'CMPID':cmpid})
    if item != None:
        item_dict = dict(item)
        cid = item_dict['CMPID']
        cname = item_dict['CompanyName']
        for branch in item_dict['Branches']:
            location_id = branch["OfficeID"]
            latitude = branch["Latitude"]
            longitude = branch["Longitude"]
            capacity = branch["Capacity"]
            address = branch["Address"]
            office = [cid,cname,location_id,capacity,latitude,longitude,address]
            office_locations.append(office)

    return office_locations 
#print(officedata_retrieval(12251))

def employee_dataretrieval(cmpid,teamid):
    employee_collection = mydatabase["Employees"]
    team_employees = []
    for employee in employee_collection.find({},{"CMPID":cmpid}):
        team = employee["TEAM"]
        team_id = list(team.keys())[0]
        team_name = team[team_id]
        if team_id == teamid:
            employee_details = [employee["EMPID"],employee["ENAME"],employee["LATITUDE"],employee["LONGITUDE"],employee["TEAM"]]
            team_employees.append(employee_details)

    return team_employees

    


        




