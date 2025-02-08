# Hiring Assistant Chatbot Documentation

## Project Overview
The **TalentScout Hiring Assistant Chatbot** is designed to assist in the candidate screening process for technology positions. It collects essential candidate details, asks relevant technical questions based on the provided tech stack, and evaluates responses with friendly feedback. The chatbot aims to streamline the initial phases of the hiring process by leveraging a language model to provide an interactive and engaging experience for candidates.

### Capabilities
- **Candidate Information Gathering**: Collects details such as full name, email, phone number, years of experience, desired position, current location, and tech stack.
- **Technical Question Generation**: Dynamically generates 5 technical questions based on the candidate's declared tech stack and position.
- **Interactive Interview Flow**: Maintains a seamless interaction flow by presenting questions one at a time, accepting answers, and providing feedback.
- **Data Storage**: Saves candidate information along with their questions and responses in a JSON file for further analysis.
- **Validation**: Ensures input fields like email and phone number meet formatting requirements.

---

## Installation Instructions
### Prerequisites
- Python 3.8 or higher
- Internet connection (to access the Google Gemini API)
- Installed Python libraries: `streamlit`, `requests`

### Steps to Set Up Locally
1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd talentscout_chatbot
   ```
2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application**
   ```bash
   streamlit run app.py
   ```
5. **Access the Application**
   - Open your browser and navigate to `http://localhost:8501`.

---

## Usage Guide
### How to Use the Chatbot
1. **Enter Candidate Details**
   - Fill out the form with your full name, email address, phone number, years of experience, desired position, current location, and tech stack.
   - Click **Submit** to begin the interview.

2. **Answer Questions**
   - The chatbot will ask technical questions one at a time.
   - Type your response and click **Submit Answer**.
   - After providing feedback, the chatbot will automatically present the next question.

3. **Save Candidate Data**
   - Once the interview is complete, click **Save Candidate Information** to store the candidate details and responses in a JSON file.

---

## Technical Details
### Libraries Used
- **Streamlit**: For building the interactive UI.
- **Requests**: For making API calls to the Google Gemini API.
- **JSON**: For data handling and storage.
- **Re**: For input validation (email and phone number).

### Model Details
- **Google Gemini API**:
  - Used for generating interview questions and providing feedback.
  - API Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent`
  - Requires a valid API key for access.

### Architectural Decisions
- **State Management**: Utilized Streamlit’s `session_state` to maintain chat history, candidate details, and interview flow.
- **Dynamic Question Handling**: The chatbot fetches questions dynamically based on the tech stack provided.
- **Validation**: Implemented custom functions to validate email and phone number formats before starting the interview.
- **Data Storage**: Saved responses in a JSON file for simplicity and future reference.

---

## Prompt Design
### Information Gathering
The chatbot uses clear and concise prompts to collect essential details from candidates. Example:
```
"Generate 5 basic questions about definitions and terms for a candidate skilled in {tech_stack} applying for {position}."
```
### Question Generation
Prompts ensure the questions are relevant to the declared tech stack and focus on fundamental concepts.

### Feedback
For each candidate’s response, the chatbot generates friendly and constructive feedback. Example:
```
"Provide friendly feedback on this answer: '{candidate_answer}'"
```
---

## Challenges & Solutions
### Challenges
1. **API Errors**:
   - Encountered issues with the Google Gemini API, such as 404 and 400 errors.
   - **Solution**: Implemented robust error handling to display meaningful error messages and debug API payloads.

2. **Input Validation**:
   - Ensuring candidate details (e.g., email and phone) were entered correctly.
   - **Solution**: Added regex-based validation for email and digit-length checks for phone numbers.

3. **UI Styling**:
   - Initial chat styling had visibility issues (e.g., white-on-white text).
   - **Solution**: Applied custom CSS to differentiate user and assistant messages visually.

4. **Dynamic Question Flow**:
   - Managing the flow of questions without manual intervention.
   - **Solution**: Used session state variables to track the current question and display the next one automatically after feedback.

---

