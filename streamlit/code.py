import os
from pymongo import MongoClient
import streamlit as st
from usellm import UseLLM, Message, Options
from utils1 import TRIP_PLANNER_SYSTEM
from utils1 import format_trip_planner_message 

from streamlit_geolocation import streamlit_geolocation

service = UseLLM(service_url="https://usellm.org/api/llm")

st.set_page_config(layout="wide")

video_html = """
		<style>

		#myVideo {
		  position: fixed;
		  right: 0;
		  bottom: 0;
		  min-width: 100%; 
		  min-height: 100%;
		}
        

		.content {
		  position: fixed;
		  bottom: 0;
		  background: rgba(0, 0, 0, 0.5);
		  color: #f1f1f1;
		  width: 100%;
		  padding: 20px;
          
		}

		</style>
		<video autoplay muted loop id="myVideo">
		  <source src="https://static.streamlit.io/examples/star.mp4")>
		  Your browser does not support HTML5 video.
		</video>
        """

st.markdown(video_html, unsafe_allow_html=True)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['tripdb']


# Custom CSS for styling input box
custom_css = """
    <style>
        .stTextInput input[type="text"] {
            background-color: transparent !important;
            border: 1px solid transparent !important; /* Set initial border color to transparent */
            font-size: 25px !important;
            font-weight: bold !important;
            color: white !important;
            position: absolute !important;
            z-index: 1 !important; /* Ensure the text input field appears over the video */
            transition: border-color 0.3s ease; /* Add smooth transition for border color change */
        }

        .stTextInput input[type="text"]:focus {
            border-color: white !important; /* Change border color to white when the input is focused */
        }
        .st-c0{
        width:500px !important;
        }
        .st-b0{
        width:500px !important;
        }
        .st-dh{
        width:500px !important;
        }
        .st-cr st-cs st-ct st-d8 st-d9 .st{
    transform: translate3d(79px, 762px, 0px);
}
        .stTextInput {
            width: 400px !important;
            height: 90px !important;
        }
        div[data-testid="element-container"] p{
            font-size:20px;
        }
        div[data-testid="element-container"] li{
            font-size:20px;
        }
        .stApp-container{
            margin-left:35px;
        }
        
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# def tour_guide_section():
#     st.title(r"$\textsf{\Large Tour Guide Assistant}$")
#     user_input = st.text_input(r"$\textsf{\normalsize Enter the Place You Want to Visit}$", key="input1")
#     if st.button(r"$\textsf{\normalsize Send}$", key="button1"):
#         if user_input:
#             system_message = TOUR_GUIDE_SYSTEM
#             output = get_response(system_message, user_input)
#             st.markdown(output.content)
#         else:
#             st.markdown("Please Enter Some Text")



def update_sidebar_user(user_input):
    if user_input:
        st.sidebar.markdown(f'<div class="place-block" style="text-align: center;">{user_input}</div>', unsafe_allow_html=True)
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
                        st.sidebar.markdown('<div style="margin-left:5px;margin-bottom:10px;color: pink;font-weight: bold;font-size:43px;">TripGenie</div>', unsafe_allow_html=True)
                        st.sidebar.markdown('<div style="margin-left:13px;margin-top:30px;margin-bottom:10px;color: white;font-size:23px;">Your Trips:</div>', unsafe_allow_html=True)


                        for trip in trips:
                            st.sidebar.markdown(f'<div class="place-block" style="text-align: center;">{trip}</div>', unsafe_allow_html=True)
                else:
                    st.sidebar.markdown('<div style="margin-left:5px;margin-bottom:10px;color: pink;font-weight: bold;font-size:43px;">TripGenie</div>', unsafe_allow_html=True)
                    st.sidebar.header("Your trips:")
            else:
                # st.sidebar.markdown('<div style="margin-left:5px;margin-bottom:10px;color: pink;font-weight: bold;font-size:43px;">TripGenie</div>', unsafe_allow_html=True)
                st.sidebar.header("Your trips:")


    custom_css = """
        <style>

        
        .place-list {
            display: flex;
            flex-wrap: wrap;

        }
        [data-testid="stSidebar"]{
        padding-left:30px;
        width:300px !important;
        background-image:url('https://images.unsplash.com/photo-1583161443085-2e2947a6664c?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzB8fHRyYXZlbGxpbmd8ZW58MHx8MHx8fDA%3D');
        background-size:cover;
        width:350px !important;
        
        }
        .st-emotion-cache-16txtl3 {
        padding: 4rem 1rem;
        }

        .place-block {
        margin-bottom:10px;
        background-color: #eaf9e2; /* Subtle green color */
        padding: 5px;
        font-size:20px;
        margin: 5px;
        display:inline-block;
        border-radius: 8px;
        width:130px; /* Set a fixed width for each block */
        color:black;
        }
        </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)



def trip_planner_section():
    st.title(r"$\textsf{\Large Personal Trip Planner}$")
    
    user_data_path = os.path.join(os.path.dirname(__file__), '..', 'user_data.txt')
    no_user_data_path = os.path.join(os.path.dirname(__file__), '..', 'no_user_data.txt')
    
    with open(user_data_path, 'r') as user_data_file:
        username = user_data_file.read().strip()

    if len(username)==0:
        st.header("Share your Location")
        user_location = streamlit_geolocation()
        st.markdown(
        f"""
        <style>
            .element-container iframe {{
                width: 30px;  /* Set your desired width */
                height: 30px;  /* Set your desired height */
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    
     
    user_input = st.text_input(r"$\textsf{\normalsize Enter the Place You Want to Visit}$", key="input2")
    days = st.text_input(r"$\textsf{\normalsize Enter the Number of Days}$", key="input3")
    budget = st.text_input(r"$\textsf{\normalsize Enter the Budget per person}$", key="input4")
    
    conditions = st.selectbox(r"$\textsf{\normalsize Select Conditions}$", ["Couple", "Friends", "Family"], key="conditions")


    if st.button(r"$\textsf{\normalsize Generate Itinerary}$", key="button2"):
        
        if user_input:
            if len(username)>0:
                user_data = db.users.find_one({"username": username})
                if user_data:
                    user_location = user_data["location"].get("address", "Unknown Address")
                    system_message = TRIP_PLANNER_SYSTEM.format(days=days, budget=budget, user_location=user_location, user_input=user_input,conditions=conditions)
                    output = get_response(system_message, user_input)
                    st.markdown(output.content)

                    trips = user_data.get("trips", [])
                    if user_input not in trips:
                        trips.append(user_input)
                        db.users.update_one({"username": username}, {"$set": {"trips": trips}})
                        update_sidebar_user(user_input)  # Update the sidebar in case there are changes
        
            else:

                # user_location = "Visakhapatnam, India"
                system_message = TRIP_PLANNER_SYSTEM.format(days=days, budget=budget, user_location=user_location, user_input=user_input,conditions=conditions)
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
        output=trip_planner_section()
        show(output)

    else:
    
        with open(user_data_path, 'r') as user_data_file:
            username = user_data_file.read().strip()
            
        if username:
            update_sidebar_user("")
            output=trip_planner_section()
            show(output)


if __name__ == "__main__":
    main()
