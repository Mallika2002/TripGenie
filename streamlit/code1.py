import os
from pymongo import MongoClient
import streamlit as st
from usellm import UseLLM, Message, Options
from utils1 import TOUR_GUIDE_SYSTEM, TRIP_PLANNER_SYSTEM
from utils1 import format_trip_planner_message 

service = UseLLM(service_url="https://usellm.org/api/llm")

st.set_page_config(layout="wide")

page_bg_img = """
<style>

 [data-testid="stApp"]{
 background-image:url('https://raw.githubusercontent.com/Mallika2002/TripGenie/main/sky.jpg');
 background-size:cover;
 }

 [data-testid="stToolbar"]{
 right:2rem;
 }

</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['tripdb']


# Custom CSS for styling input box
custom_css = """
    <style>
        .stTextInput{
            width:1200px !important;
        }
        .stTextInput input {
            color: black !important;
            background-color: lightyellow !important;
            border:1px solid black !important;
        }
        
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

def tour_guide_section():
    st.title(r"$\textsf{\Large Tour Guide Assistant}$")
    user_input = st.text_input(r"$\textsf{\normalsize Enter the Place You Want to Visit}$", key="input1")
    if st.button(r"$\textsf{\normalsize Send}$", key="button1"):
        if user_input:
            system_message = TOUR_GUIDE_SYSTEM
            output = get_response(system_message, user_input)
            st.markdown(output.content)
        else:
            st.markdown("Please Enter Some Text")

def update_sidebar_user(user_input):
    if user_input:
        st.sidebar.markdown(f'<div class="place-block">{user_input}</div>', unsafe_allow_html=True)
    else:
        user_data_path = os.path.join(os.path.dirname(__file__), '..', 'user_data.txt')
    
        with open(user_data_path, 'r') as user_data_file:
            username = user_data_file.read().strip()

        if username:
            user_data = db.users.find_one({"username": username})
            if user_data:
                trips = user_data.get("trips", [])
                if "trips" in user_data:
                        trips = user_data["trips"]
                        st.sidebar.header("Your trips:")
                        for trip in trips:
                            st.sidebar.markdown(f'<div class="place-block">{trip}</div>', unsafe_allow_html=True)
                else:
                    st.sidebar.header("Your trips:")
            else:
                st.sidebar.header("Your trips:")


    custom_css = """
        <style>


        .place-list {
            display: flex;
            flex-wrap: wrap;
        }

            .place-block {
            background-color: #eaf9e2; /* Subtle green color */
            padding: 5px;
            margin: 5px;
            display:inline-block;
            border-radius: 5px;
            width: 100px; /* Set a fixed width for each block */
            color:black;
            }
        </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)



def trip_planner_section():
    st.title(r"$\textsf{\Large Personal Trip Planner}$")
    
    user_data_path = os.path.join(os.path.dirname(__file__), '..', 'user_data.txt')
    
    with open(user_data_path, 'r') as user_data_file:
        username = user_data_file.read().strip()
    
    user_input = st.text_input(r"$\textsf{\normalsize Enter the Place You Want to Visit}$", key="input2")
    days = st.text_input(r"$\textsf{\normalsize Enter the Number of Days}$", key="input3")
    budget = st.text_input(r"$\textsf{\normalsize Enter the Budget per person}$", key="input4")
    
    if st.button(r"$\textsf{\normalsize Send}$", key="button2"):
        
        if user_input:
            if len(username)>0:
                user_data = db.users.find_one({"username": username})
                if user_data:
                    user_location = user_data["location"].get("address", "Unknown Address")
                    system_message = TRIP_PLANNER_SYSTEM.format(days=days, budget=budget, user_location=user_location, user_input=user_input)
                    output = get_response(system_message, user_input)
                    st.markdown(output.content)

                    trips = user_data.get("trips", [])
                    if user_input not in trips:
                        trips.append(user_input)
                        db.users.update_one({"username": username}, {"$set": {"trips": trips}})
                        update_sidebar_user(user_input)  # Update the sidebar in case there are changes
        
            else:
                user_location = "Visakhapatnam, India"
                system_message = TRIP_PLANNER_SYSTEM.format(days=days, budget=budget, user_location=user_location, user_input=user_input)
                output = get_response(system_message, user_input)
                st.markdown(output.content)


def get_response(system_message, user_input, *args):
    messages = [
        Message(role="system", content=system_message),
        Message(role="user", content=user_input)
    ]
    options = Options(messages=messages)
    output = service.chat(options)
    return output


def show(output):
    if output:
        st.markdown(output.content)
    elif output == "NULL":
        st.markdown("Please Enter Some Text")

def main():
    user_data_path = os.path.join(os.path.dirname(__file__), '..', 'user_data.txt')

    if os.stat(user_data_path).st_size == 0:

        tab1, tab2 = st.tabs([r"$\textsf{\Large Tour Guide}$", r"$\textsf{\Large Trip Planner}$"])
        with tab1:
            output = tour_guide_section()
            show(output)

        with tab2:
            output = trip_planner_section()
            show(output)

    else:
    
        with open(user_data_path, 'r') as user_data_file:
            username = user_data_file.read().strip()
            
        if username:
            update_sidebar_user("")

        tab1, tab2 = st.tabs([r"$\textsf{\Large Tour Guide}$", r"$\textsf{\Large Trip Planner}$"])
        with tab1:
            output = tour_guide_section()
            show(output)

        with tab2:
            output = trip_planner_section()
            show(output)


if __name__ == "__main__":
    main()
