# Streamlit UI service imports
import streamlit as st

# OS imports
import os
from dotenv import load_dotenv

# AI imports
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Pdf reading imports
from pypdf import PdfReader

# Load env file
load_dotenv()

# Model info
endpoint = 'https://models.inference.ai.azure.com'
model_name = "gpt-4.1"
key = os.getenv("OPENAI_API_KEY") # Specify environment variable in .env file

# Control variable for response generation
generate = False

st.title("CapstoneManager")
st.text("This tool can be used to assign students to projects based on the skills outlined on their resumes")

# Divider element
st.divider()

# Project description document to be parsed
project_descriptions = st.file_uploader("Upload a document with **project names**, **project descriptions**, and **number of students per project** clearly stated", type="pdf", accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
project_string = ""

if project_descriptions is not None:
    # Create reader for project description pdf
    reader = PdfReader(project_descriptions)

    # Extract file strings
    for page in reader.pages:
        project_string += page.extract_text()
    
    # st.write(project_string) DEBUGGING

# Divider element
st.divider()

# Student resumes to be parsed
student_resumes = st.file_uploader("Upload **student resumes**", type="pdf", accept_multiple_files=True, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
resume_list = []

if student_resumes is not None:
    for resume in student_resumes:
        # Create reader for resume pdf
        reader = PdfReader(resume)
        resume_str = ""

        # Extract file strings
        for page in reader.pages:
            resume_str += page.extract_text()

        # st.write(resume_str) # DEBUGGING
        resume_list.append(resume_str)

# Number of students to be assigned to teams
num_students = len(resume_list)

# Concatenated string of all student resumes
all_student_resumes = "\n\n".join(f"Student {i+1}:\n{resume}" for i, resume in enumerate(resume_list))

# Ensure all fields have been completed before running the agent
if project_descriptions is not None and len(student_resumes) > 0:
    generate = st.button("Assign students to projects", type="primary")

# Create the client
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# Runs the agent when button has been clicked
if generate:
    try:
        # Call the Azure AI Inference API
        response = client.complete(
            messages=[
                SystemMessage(f"You are tasked with determining the best projects for students based on their skillsets given their resumes. Each student should be assigned to at most one project, and the teams should be balanced based on front-end and back-end experience fairly evenly. In the case that a student does not display any of these skills, you can randomly assign them. The number of students you need to distribute is {num_students}"),
                SystemMessage("If any of the following information is not provided for EVERY project, you should return an error message and disregard the request: Project title, project description, number of students (size of team)."),
                SystemMessage("Your response to this request should ONLY include a table containing Project, Assigned Student, Project Skill Requirements, Key Skills Matched, and justification. Ensure that the table is ordered by project such that each student belonging to each project are parallel."),
                UserMessage(f"Here is the project description: {project_string}"),
                UserMessage(f"Here are the student resumes: {all_student_resumes}")
            ],
            temperature=0.3,  # Lower temperature for more focused and consistent summaries
            max_tokens=1000,  # Limiting the response length
            model=model_name
        )
        
        # Extract and return the summary
        st.write(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Error generating review summary: {str(e)}")