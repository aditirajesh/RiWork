import random
import math
import db_connection 
from pymongo import MongoClient
import pandas as pd 
from datetime import datetime, timedelta
from pathlib import Path 
import streamlit as st 
from streamlit_extras.stylable_container import stylable_container
class Location:
    def __init__(self, latitude, longitude,):
        self.latitude = latitude
        self.longitude = longitude

class OfficeLocation(Location):
    def __init__(self, location_id, capacity, latitude, longitude,address):
        super().__init__(latitude, longitude)
        self.location_id = location_id
        self.capacity = capacity
        self.address = address
    
    def __str__(self):
        return f"{self.location_id}:{self.capacity}"
    
class Employee(Location):
    def __init__(self, emp_id, employee_name, lat, lon,teamID,teamName):
        super().__init__(lat, lon)
        self.employee_name = employee_name
        self.employee_id = emp_id
        self.teamID = teamID 
        self.teamName = teamName 

class Team:
    def __init__(self, nam, l):
        self.team_name = nam
        self.employees = l
        self.capacity = len(l)


def generate_initial_population(psize, no_teams):
    t = []
    for i in range(psize):
        po = []
        for j in range(no_teams):
            population = []
            while len(population) < 3:
                n = random.randint(0, 4)
                if n not in population:
                    population.append(n)
            po.append(sorted(population))
        t.append(po)
    return t

def allocate(offi, team, week, week_tots):
    office_allocations = [[] for _ in range(5)]

    for i in range(len(week_tots)):
        remaining_capacity = week_tots[i]
        sorted_offices = sorted(offi, key=lambda o: o.capacity,reverse=True)

        for j in range(len(sorted_offices)):
            if remaining_capacity <= 0:
                break

            if sorted_offices[j].capacity >= remaining_capacity:
                for l in range(1,len(sorted_offices)-j-1):
                    if remaining_capacity > sorted_offices[j+l].capacity:
                        j = j+l-1
                        break
                if remaining_capacity<sorted_offices[-1].capacity:
                    j = -1
                office_allocations[i].append(sorted_offices[j])
                remaining_capacity = 0
            else:
                office_allocations[i].append(sorted_offices[j])
                remaining_capacity -= sorted_offices[j].capacity

    return office_allocations



def calculate_average_distance(team, office):
    total_distance = 0
    num_employees = len(team.employees)

    for employee in team.employees:
        employee_distance = calculate_distance(employee.latitude, employee.longitude, office.latitude, office.longitude)
        total_distance += employee_distance

    if num_employees > 0:
        average_distance = total_distance / num_employees
        return average_distance
    else:
        return 0  # Avoid division by zero if the team has no employees

def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate distance between two points on the earth given their latitude and longitude
    R = 6371  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance



def calculate_fitness(s, offices, teams):
    week = [[] for _ in range(5)]
    week_total = []
    fitness = 0
    for i in range(len(s)):
        for j in s[i]:
            week[j].append(i)
    for j in week:
        dayt = 0
        for k in j:
            dayt += teams[k].capacity
            
        week_total.append(dayt)
    l = []
    teams_c = [i.capacity for i in teams]
    allo = allocate(offices, teams_c, week, week_total)
    
    for i in range(5):
        tots = 0
        for j in allo[i]:
            tots += j.capacity
        fitness += (tots - week_total[i])
    
    return fitness

def calculate_fitness(s, offices, teams):
    week = [[] for _ in range(5)]
    week_total = 0
    total_distance = 0
    fitness = 0

    for i in range(len(s)):
        for j in s[i]:
            week[j].append(i)
    
    for j in week:
        dayt = 0
        for k in j:
            dayt += teams[k].capacity
            # Calculate the average distance for each team from the first office
            total_distance += calculate_average_distance(teams[k], offices[0])

        week_total += dayt
    
    l = []
    allo = allocate(offices, teams, week, [week_total] * 5)
    
    for i in range(5):
        tots = sum(office.capacity for office in allo[i])
        fitness += max(0, tots - week_total)
    
    # Introduce a distance factor, you can adjust the weight as needed
    fitness += total_distance * 0.1  # Adjust the weight factor as needed
    
    return fitness


def get_office(s, offices, teams):
    week = [[] for _ in range(5)]
    week_total = []
    fitness = 0
    for i in range(len(s)):
        for j in s[i]:
            week[j].append(i)
    for j in week:
        dayt = 0
        for k in j:
            dayt += teams[k]
        week_total.append(dayt)
    l = []
    allo = allocate(offices, teams, week, week_total)
    return allo

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(solution, mutation_rate=0.1):
    mutated_solution = solution.copy()
    for i in range(len(mutated_solution)):
        if random.random() < mutation_rate:
            mutated_solution[i] = random.sample(range(len(solution[i])), len(solution[i]))
    return mutated_solution

def find_closest_sum_with_indices(numbers, target):
    closest_set = []
    closest_indices = []

    def find_combination(index, current_set, current_indices, current_sum):
        nonlocal closest_set, closest_indices

        if current_sum <= target:
            if current_sum > sum(closest_set):
                closest_set = current_set.copy()
                closest_indices = current_indices.copy()

        if index == len(numbers):
            return

        # Include the current number in the set
        find_combination(index + 1, current_set + [numbers[index]],
                          current_indices + [index], current_sum + numbers[index])

        # Exclude the current number from the set
        find_combination(index + 1, current_set, current_indices, current_sum)

    find_combination(0, [], [], 0)
    return closest_set, closest_indices

def genetic_algo(gensize, offices, te):
    population_size = 100
    no_teams = len(te)
    mutation_rate = 0.1
    teams = []
    for i in te:
        teams.append(len(i.employees))

    population = generate_initial_population(population_size, no_teams)

    for generation in range(gensize):
        # Evaluate fitness
        population = sorted(population, key=lambda s: calculate_fitness(s, offices, te))

        # Select the top 50% of the population as parents
        parents = population[:population_size // 2]

        # Create the next generation using crossover and mutation
        children = []
        while len(children) < population_size - len(parents):
            parent1, parent2 = random.sample(parents, 2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            children.extend([child1, child2])

        # Replace the old population with the new generation
        population = parents + children

    # Print the final result
    best_solution = population[0]
    office = get_office(best_solution, offices, teams)
    d={}
    for i in range(5):
        teams_list = []
        emps = 0
        for j in range(len(best_solution)):
            if i in best_solution[j]:
                teams_list.append(j)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        if not office[i]:
            tot = 0
            for il in teams_list:
                tot += teams[il]
            emp = tot
            for spaces in range(len(offices)):
                if tot > offices[spaces].capacity:
                    office[i].append(spaces - 1)
        for it in teams_list:
            emps += teams[it]

        dic = {}
        for it in teams_list:
            if len(office[i])==1:
                dic[it] = office[i]
        if len(office[i])>1:
            n_t = teams_list[::]
            while office[i]:
                o = office[i].pop()
                teams_cap = [teams[i] for i in teams_list]
                a,b=find_closest_sum_with_indices(teams_cap,o.capacity)
                for lli in b:
                    dic[teams_list[lli]]=[o]

                break
            for ti in teams_list:
                if ti not in dic:
                    dic[ti]=office[i]



                
        d[days[i]] = dic
    return d


def obtain_officeloc(locations_l):
    offices = []
    for location in locations_l:
        office = OfficeLocation(location[2],location[3],location[4],location[5],location[6])
        offices.append(office)

    return offices 
        

def employee_dataretrieval(cmpid):
    client = MongoClient('localhost', 27017)
    mydatabase = client['Riwork'] 
    employee_collection = mydatabase["Employees"]
    employees_objs = []
    for employee in employee_collection.find({},{"CMPID":cmpid,"ENAME":1,"EMPID":1,"LATITUDE":1,"LONGITUDE":1,"TEAM":1}):
        team = employee["TEAM"]
        team_id = list(team.keys())[0]
        team_name = team[team_id]
        employee_details = Employee(employee["EMPID"],employee["ENAME"],employee["LATITUDE"],employee["LONGITUDE"],team_id,team_name)
        employees_objs.append(employee_details)
    return employees_objs

locations_l = db_connection.officedata_retrieval(12251)
office_locations = obtain_officeloc(locations_l)  
OFFICES = sorted(office_locations, key=lambda office: office.capacity, reverse=True)
TEAMS = db_connection.teamdata_retrieval(12251)
NUMBER_OF_GENS = 10 #// after 10, it is a point of diminishing returns 



def teamobjs_definition(employee_objs):
    team_objs = []
    for i in range(0,len(TEAMS)):
        '''iterating through all the teams to assign all the employees to the teams'''
        team_employees = []
        for employee in employee_objs:
            if employee.teamID == str(i):
                team_employees.append(employee)

        team_obj = Team(team_employees[0].teamName,team_employees)
        team_objs.append(team_obj) 

    return team_objs

employee_objs = employee_dataretrieval(12251)
team_objs = teamobjs_definition(employee_objs)

r = genetic_algo(NUMBER_OF_GENS,OFFICES,team_objs)  #//KEYS - DAYS VALUES: A DICTIONARY MAPPING THE TEAMS ALONG WITH THE OFFICE AT WHICH THEY ARE WORKING 
#print(r)

def days_teamworking(r):
    '''computing for each day what team will be working offline'''
    days_dict = {}
    
    for i in r:
        value = r[i]   #team along with the office - it is a dictionary team:officeloc
        team_id = list(value.keys())
        all_days = []
        for ids in team_id:
            office_details = value[ids][0]
            all_days.append([ids,office_details])
        days_dict[i] = all_days

    return days_dict

def team_daysworking(days_dict): #days_dict format day:list(team,office_location) 
    '''computing which team will be working on what days'''
    teams_dict = {}
    for days,work_details in days_dict.items():
        team_ids = [work_details[i][0] for i in range(len(work_details))]
        office_details = [work_details[i][1] for i in range(len(work_details))]
        for id in team_ids:
            office = office_details[team_ids.index(id)]
            if id not in teams_dict:
                teams_dict[id] = {days:office}

            else:
                teams_dict[id].update({days:office})

    return teams_dict 

def get_officedetails(office_obj):
    officeid = office_obj.location_id
    office_lat = office_obj.latitude
    office_long = office_obj.longitude 
    office_cap = office_obj.capacity
    office_address = office_obj.address 
    return [officeid,office_cap,office_lat,office_long,office_address]
    

def day_date():
    days = []
    dates = []
    # Get the current date
    current_date = datetime.now()

    # Calculate the start of the week (Monday)
    start_of_week = current_date - timedelta(days=current_date.weekday())

    # Calculate the end of the week (Sunday)
    end_of_week = start_of_week + timedelta(days=6)

    # Generate all the dates in the current week
    current_week_dates = [start_of_week + timedelta(days=x) for x in range(7)]

    for date in current_week_dates:
        days.append(date.strftime("%A"))
        dates.append(date.strftime("%d %B %Y"))

    return days,dates

days_dict = days_teamworking(r)
teams_dict = team_daysworking(days_dict) 
def table_format(teams_dict,team_number):
    if team_number in teams_dict:
        working_days = list(teams_dict[team_number].keys())
        days,dates = day_date()

        officeids = []
        officecap = []
        officelat = []
        officelong = []
        officeadd = []
        officedates = []
        for day in working_days:
            if day in days:
                index = days.index(day)
                officedates.append(dates[index])
            office = teams_dict[team_number][day]
            office_details = get_officedetails(office)
            officeids.append(office_details[0])
            officecap.append(office_details[1])
            officelat.append(office_details[2])
            officelong.append(office_details[3])
            officeadd.append(office_details[4])

        df = pd.DataFrame(list(zip(working_days,officedates,officeids,officecap,officelat,officelong,officeadd)), columns=['Days Working',"Dates",
                                                                                                       'Office ID',
                                                                                                       'Office Branch',
                                                                                                       'Latitude',
                                                                                                       'Longitude',
                                                                                                       'Office Address'])
        file_path = Path(__file__).parent / "workingdays_df.csv"
        with file_path.open("w") as file:
            df.to_csv(file)

        return df



    