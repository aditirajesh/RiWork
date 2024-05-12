import streamlit as st 
st.set_page_config(page_title="RiWork",page_icon=":tada:",layout="wide")
from pathlib import Path
import streamlit_authenticator as stauth
import db_connection 
import pickle 
from streamlit_extras.stylable_container import stylable_container
import About_page 
from streamlit_option_menu import option_menu 
from PIL import Image 
import pandas as pd 
import mods 
from pymongo import MongoClient
from datetime import datetime, timedelta
with st.sidebar:
    selected_option = option_menu("Menu",["About","Login"],
                                  icons=['sparkles','bust_in_silhouette'],menu_icon="cast",
                                  default_index=1)


if selected_option == "Login":
    
    col1,col2 = st.columns(2)
    with col1:
        #//background image of the login page 
        page_bg_img = """
        <style>
        [data-testid="stAppViewContainer"] {
        background-image: url(https://images.unsplash.com/photo-1475694867812-f82b8696d610?q=80&w=2832&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D);
        image-rendering: -webkit-optimize-contrast;
        background-size: cover;
        opacity: 0.8;
        }
        [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
        }
        [data-testid="stToolbar"]{
        right:2rem;
        }

        [data-testid="stSidebarContent"] {
        background-image: url("https://images.unsplash.com/photo-1585834377618-3d85069b884e?q=80&w=2835&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        }
        </style>"""
        st.markdown(page_bg_img,unsafe_allow_html= True)


        #//READING FROM DATABASE TO GET LOGIN AND PASSWORD//
        users = db_connection.get_users()
        names = [str(user["ENAME"]) for user in users]
        usernames = [str(user["EMAIL"]) for user in users]
        passwords = [str(user["PASSWORD"]) for user in users]

        file_path = Path(__file__).parent / "hashed_pw.pkl"
        with file_path.open("rb") as file:
            hashed_passwords = pickle.load(file)

        authenticator = stauth.Authenticate(names,usernames,hashed_passwords,"office_dashboard","abcdef")


        #//login form styling
        with stylable_container(
            key = "markdown_container",
            css_styles= """
            {
                border-radius: 2em;
                border-width: 5px 5px;
                border-style: solid;
                padding: 0.5em
                height: 500px;
                width: 100%;
                right: 500px
                margin-left:auto;
                margin-right:auto;
                background-image:linear-gradient(##2c3e50,#3498db);

            }
            """
        ):
            #//setting up the login form and the login status
            name, authentication_status, username = authenticator.login("Login","main")
        if authentication_status == False:  
            st.error("Username/password is incorrect",icon="⚠️")

        if authentication_status == None:
            st.warning("Please enter both your username and password",icon="⚠️")


    if authentication_status:
        #//STATUS SUCCESSFUL - REDIRECT TO THE LOGGED IN WEBSITE 

        #//BACKGROUND DESIGN 
        page_bg_img2 = """
        <style>
        [data-testid="stAppViewContainer"] > .main {
        background-image: url("https://images.unsplash.com/photo-1503891617560-5b8c2e28cbf6?q=80&w=2787&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-position: top left;
        background-size: 180%;
        background-repeat: no-repeat;
        background-attachment:local;
        opacity: 0.8;
        }

        [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
        }
        [data-testid="stToolbar"]{
        right:2rem;
        }
        
        """
        st.markdown(page_bg_img2,unsafe_allow_html= True)   
        with stylable_container(
            key = "welcome_title",
            css_styles= """
            {
                top:-120px;

            }
            """
        ):
            st.title(f':red[Welcome {name}!]')
            st.title(' ')
            st.success('Logged in successfully!')
            st.title('----------------------------------------------------------------')
            subtext5 = '<p style="color:black; font-size:25px; font-weight:bold;"> Welcome back! Check out your working schedule for the week and drop below any complaints you may have, and your issue will be taken up as soon as possible. Happy Working!"</p>'
            st.markdown(subtext5,unsafe_allow_html=True)

            def collect_companydata(cmpid=12251):
                client = MongoClient()
                client = MongoClient('localhost', 27017)
                mydatabase = client['Riwork']
                company_collection = mydatabase["Company"]
                company = company_collection.find_one({"CMPID":cmpid})
                cname = company["CompanyName"]
                company_branches = company["Branches"]
                officeids = []
                officenames = []
                latitudes = []
                longitudes = []
                capacities = []
                addresses = []
                for d in company_branches:
                    officeids.append(d["OfficeID"])
                    officenames.append(d["OfficeName"])
                    latitudes.append(d["Latitude"])
                    longitudes.append(d["Longitude"])
                    capacities.append(d["Capacity"])
                    addresses.append(d["Address"])

                df = pd.DataFrame(list(zip(officeids,officenames,latitudes,longitudes,capacities,addresses)),columns=["Office ID","Office Name","Latitudes","Longitudes","Capacity","Address"])

                return [cmpid,cname,df]


            def collect_userdata(name,username):
                client = MongoClient()
                client = MongoClient('localhost', 27017)
                mydatabase = client['Riwork']
                employee_collection = mydatabase['Employees']

                employee = employee_collection.find_one({"ENAME":name,"EMAIL":username})
                if employee is not None:
                    empid = employee["EMPID"]
                    latitude = employee["LATITUDE"]
                    longitude = employee["LONGITUDE"]
                    team = employee["TEAM"]
                    teamID = list(team.keys())[0]
                    teamName = team[teamID]

                return [teamID,teamName,latitude,longitude,empid]
            
            teamID,teamName,latitude,longitude,empid = collect_userdata(name,username)
            st.subheader(f':red[Work Schedule for {name} as well as all members part of the {teamName}]')

            locations_l = db_connection.officedata_retrieval(12251)
            office_locations = mods.obtain_officeloc(locations_l)  
            OFFICES = sorted(office_locations, key=lambda office: office.capacity, reverse=True)
            TEAMS = db_connection.teamdata_retrieval(12251)
            NUMBER_OF_GENS = 10 #// after 10, it is a point of diminishing returns 

            employees_objs = mods.employee_dataretrieval(12251) 
            team_objs = mods.teamobjs_definition(employees_objs) 

            r = mods.genetic_algo(NUMBER_OF_GENS,OFFICES,team_objs)
            days_dict = mods.days_teamworking(r)
            teams_dict = mods.team_daysworking(days_dict) 
            df = mods.table_format(teams_dict,int(teamID))

            st.dataframe(df,use_container_width=False)

            def mail_contact():
                st.title(" ")
                st.title(" ")
                st.subheader(":red[for any queries, submit them below]")

                st.subheader("Contact through mail :mailbox:")
                contact_form = '''
                <form action="https://formsubmit.co/riwork755@gmail.com" method="POST">
                    <input type="text" name="name" placeholder = "Your name" required>
                    <textarea name="message" placeholder="What issue are you facing?"></textarea>
                    <button type="submit">Send</button>
                    <input type="hidden" name="_captcha" value="false">
                </form>
                '''

                st.markdown(contact_form,unsafe_allow_html = True)
            mail_contact()

            def local_css(file_name):
                with open(file_name) as f:
                    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

            local_css("/Users/aditirajesh/Desktop/program_files/RiWork/style/style.css")

            st.subheader(':red[Employee and Company Details: ]')
            col7,col8 = st.columns(2)

            with col7:
                cmpid,cname,office_df = collect_companydata()
                st.write(f':red[Company ID: ]{cmpid}')
                st.write(f':red[Company Name: ]{cname}')
                st.dataframe(office_df,use_container_width=False)

            with col8:
                st.write(f':red[Employee ID: ]{empid}')
                st.write(f':red[Name: ]{name}')
                st.write(f':red[Email: ]{username}')
                st.write(f':red[Team: ]{teamName}')
                st.write(f':red[Latitude: ]{latitude}')
                st.write(f':red[Longitude: ]{longitude}')

            def phone_contact():
                st.caption("  \n\n\n\n\n\n")
                st.subheader(":red[Contact through phone :phone:]")
                col1,col2 = st.columns(2)
                with col1:
                    st.write("Contact number  1: 7010821856")
                    st.write("Contact number  2: 9092093093")
                    st.write("Contact number 3: 9840236063")

                with col2:
                    st.write("Name: Aditi Rajesh")
                    st.write("Name: Adharsh Gurudev")
                    st.write("Name: Ahamed Jumail")

                st.caption("Thank you for using RiWork!")

            phone_contact()
                        







        authenticator.logout("Logout","sidebar")

else:
    #//MAIN PAGE IS SELECTED AND ITS CONTENTS ARE DISPLAYED
    About_page.page_design()





