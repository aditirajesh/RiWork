import streamlit as st
import streamlit.components.v1 as components
from PIL import Image



def page_design():
    #BACKGROUND IMAGE 
    page_bg =  """
        <style>
        [data-testid="stAppViewContainer"] > .main {
        background-image: url("https://images.unsplash.com/photo-1509641498745-13c26fd1ed89?q=80&w=2787&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-position: top left;
        background-size: 180%;
        background-repeat: no-repeat;
        background-attachment:local;
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
    st.markdown(page_bg,unsafe_allow_html=True)

    st.title(':red[Welcome to Riwork!] :sunny:')
    st.write('----')

    col3,col4 = st.columns(2)

    with col3:
        title = '<p style="color:black; font-size:30px; font-weight:bold;">Welcome to riwork - where innovation meets workplace harmony! Our cutting-edge application is revolutionizing office space allocation, ensuring that every employee enjoys a dynamic and personalized workspace!</p>'
        st.markdown(title, unsafe_allow_html=True)


    with col4:
        bottom_image = "/Users/aditirajesh/Desktop/program_files/RiWork/office_meeting.jpg"
        st.image(bottom_image)

    st.write("  ")
    st.write("  ")


    st.title(':red[The Future of The Office has Arrived]')
    col5,col6 = st.columns(2)
    with col5:
        st.subheader(":red[In the USA]")
        subtext = '<p style="color:black; font-size:20px; font-weight:bold;">Researchers from Gallup established the remote work trends below to monitor the work locations, future plans and preferences of “remote-capable employees.”</p>'
        st.markdown(subtext,unsafe_allow_html=True)
        st.write(" ")
        subtext2 = '<p style="color:black; font-size:20px; font-weight:bold;"> "Hybrid"is the most common style of work for remote-capable employees.In 2019, 60% of remote-capable employees spent their week working fully on-site, whereas that figure has fallen to just 20% in 2023. In contrast, only 8% worked exclusively remotely in 2019, compared with the 29% of remote-capable employees who are fully remote today. At the same time, hybrid work has increased significantly, en route to becoming the most prevalent work arrangement in most offices.</p>'
        st.markdown(subtext2,unsafe_allow_html=True)

        st.write("   ")
        st.write("    ")
        st.subheader(":red[In India]")
        subtext3 = '<p style="color:black; font-size:20px; font-weight:bold;">As urban centres become more congested and commuting times increase, employees are seeking alternatives to long journeys to work. Managed workspaces strategically located in prime business districts provide a convenient solution. Employees can choose to work from a workspace close to their homes, reducing their daily commute and saving valuable time.The hybrid work model is a significant driving force behind the increasing demand for managed workspaces in India. By providing the necessary infrastructure, flexibility, and convenience to support both remote work and in-office collaboration, managed workspaces are catering to the evolving needs of businesses and employees.  </p>'
        st.markdown(subtext3,unsafe_allow_html=True)



    with col6:
        graph_image = "/Users/aditirajesh/Desktop/program_files/RiWork/graph_analysis.jpeg"
        image = Image.open(graph_image)
        new_image = image.resize((600, 400))
        #//FOR SPACING PURPOSES
        for _ in range(4):
            st.title(" ")
        st.image(new_image)

        #//USED FOR SPACING PURPOSES 
        for i in range(7):
            st.title("  ")

        subtext4 = '<p style="color:black; font-size:30px; font-weight:bold;">A recent study by Indeed unveiled that a majority (71%) of Indian jobseekers now prefer job flexibility, including the ability to work from home and set their own hours, over high salary packages. </p>'
        st.markdown(subtext4,unsafe_allow_html=True)
    st.title(':red[ Our Mission]')
    subtext5 = '<p style="color:black; font-size:20px; font-weight:bold;"> With riwork, we prioritize employee convenience, adapting to individual preferences to enhance productivity and job satisfaction. Beyond optimizing the work environment, our platform is a game-changer for the planet. By intelligently allocating office spaces, we contribute to reducing carbon footprints and fostering a sustainable, eco-friendly workplace.</p>'
    st.markdown(subtext5,unsafe_allow_html=True)

    st.title(" ")
    st.title(":red[Join Us Today!]")
    subtext5 = '<p style="color:black; font-size:20px; font-weight:bold;"> Join riwork today and be part of a movement that not only prioritizes employee well-being but also champions environmental preservation, all while optimizing company resources. Embrace the future of work with riwork- where smart office allocation meets corporate sustainability!"</p>'
    st.markdown(subtext5,unsafe_allow_html=True)

    subtext5 = '<p style="color:black; font-size:20px; font-weight:bold;"> This is a paid service starting at Rs.199 a month.</p>'
    st.markdown(subtext5,unsafe_allow_html=True)

    st.subheader(":red[Contact us Through: ]")
    subtext6 = '<p style="color:black; font-size:20px; font-weight:bold;"> Phone: 9876543219</p>'
    st.markdown(subtext6,unsafe_allow_html=True)

    subtext7 = '<p style="color:black; font-size:20px; font-weight:bold;"> Email: riwork755@gmail.com</p>'
    st.markdown(subtext7,unsafe_allow_html=True)








