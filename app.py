import streamlit as st
import requests
import json
import re

# Google Gemini API details
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
API_KEY = "AIzaSyChpvT-miHvwDxWxxkjgHJCGk4OL8Dcv5w"  

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "candidate_details" not in st.session_state:
    st.session_state["candidate_details"] = {}
if "interview_started" not in st.session_state:
    st.session_state["interview_started"] = False
if "questions" not in st.session_state:
    st.session_state["questions"] = []
if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0
if "responses" not in st.session_state:
    st.session_state["responses"] = {}

# Function to validate email
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# Function to validate phone number (10 digits)
def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

# Function to send request to Google Gemini API
def query_gemini_api(prompt):
    headers = {"Content-Type": "application/json"}
    params = {"key": API_KEY}
    data = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}]
    }

    response = requests.post(API_URL, headers=headers, params=params, json=data)

    if response.status_code != 200:
        st.error(f"Error {response.status_code}: {response.text}")
        return f"Error {response.status_code}: {response.text}"

    try:
        json_response = response.json()
        if "candidates" in json_response and len(json_response["candidates"]) > 0:
            return json_response["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Sorry, I didn't get a valid response from the model."
    except json.JSONDecodeError:
        return "Sorry, the API returned an unexpected response."

# Function to save candidate data
def save_candidate_data():
    candidate_data = {
        "Candidate Details": st.session_state["candidate_details"],
        "Interview Questions & Answers": st.session_state["responses"],
    }
    with open("candidate_info.json", "w") as f:
        json.dump(candidate_data, f, indent=4)
    st.success("✅ Candidate information & responses saved successfully!")

# Streamlit UI Customization
st.markdown("""
    <style>
    .assistant {
        background-color: #f1f1f1;
        color: black;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        text-align: left;
        width: 70%;
    }
    .user {
        background-color: #cce5ff;
        color: black;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        text-align: right;
        width: 70%;
        float: right;
    }
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("TalentScout Hiring Assistant 🤖")
st.write("This chatbot will help screen candidates for technology positions.")

# Candidate information form
with st.form("candidate_form"):
    st.subheader("📋 Please enter your details")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
    position = st.text_input("Desired Position(s)")
    location = st.text_input("Current Location")
    tech_stack = st.text_input("Tech Stack (e.g., Python, TensorFlow, SQL)")
    submit = st.form_submit_button("Submit")

# Validate form input
if submit:
    if not full_name or not email or not phone or not position or not tech_stack:
        st.error("❌ All fields are required!")
    elif not is_valid_email(email):
        st.error("❌ Invalid email format!")
    elif not is_valid_phone(phone):
        st.error("❌ Phone number must be exactly 10 digits!")
    else:
        # Store details and start interview
        st.session_state["candidate_details"] = {
            "Full Name": full_name,
            "Email": email,
            "Phone": phone,
            "Experience": experience,
            "Position": position,
            "Location": location,
            "Tech Stack": tech_stack,
        }
        st.session_state["interview_started"] = True
        st.session_state["chat_history"].append({"role": "assistant", "content": f"Hello {full_name}, let's start your interview! 🎯"})

        # Generate basic questions
        prompt = f"Generate 5 basic questions about definitions and terms for a candidate skilled in {tech_stack} applying for {position}."
        questions = query_gemini_api(prompt)
        st.session_state["questions"] = questions.split("\n")
        st.session_state["current_question"] = 0

# Display chat history
st.subheader("💬 Chat with the Assistant")
chat_container = st.container()
with chat_container:
    for message in st.session_state["chat_history"]:
        if message["role"] == "user":
            st.markdown(f"<div class='user'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistant'>{message['content']}</div>", unsafe_allow_html=True)

# Ask questions one by one
if st.session_state["interview_started"] and st.session_state["current_question"] < len(st.session_state["questions"]):
    current_question = st.session_state["questions"][st.session_state["current_question"]]
    if "current_question_displayed" not in st.session_state or not st.session_state["current_question_displayed"]:
        st.session_state["chat_history"].append({"role": "assistant", "content": current_question})
        st.session_state["current_question_displayed"] = True

# User input box
user_input = st.text_input("Type your answer here:", key="answer_input", value="")
if st.button("Submit Answer"):
    if user_input.strip():
        # Store user answer
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        st.session_state["responses"][current_question] = user_input

        # Generate feedback for the answer
        feedback_prompt = f"Provide friendly feedback on this answer: '{user_input}'"
        feedback_response = query_gemini_api(feedback_prompt)

        # Append feedback and move to the next question automatically
        st.session_state["chat_history"].append({"role": "assistant", "content": feedback_response})
        st.session_state["current_question"] += 1
        st.session_state["current_question_displayed"] = False

# Button to save candidate data
if st.button("💾 Save Candidate Information"):
    save_candidate_data()
