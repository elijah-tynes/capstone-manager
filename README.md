# CapstoneManager
CapstoneManager is a project management tool designed using AI inferencing to parse student resumes and assign them to project teams in a logical, balanced manner. 

## Key Features
Project managers are able to use this tool to:
 - Develop project teams containing members with complementary skills
 - Meet team size constraints while maximizing team synergy
 - Produce teams to address business needs with minimal human involvement

## Prerequisites
  - [Install Python](https://www.python.org/downloads)
  - [Create an Azure OpenAI Key](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/quickstart?pivots=rest-api)

## Getting Started
1) Install necessary Python packages:
```bash
pip install streamlit
pip install python-dotenv
pip install pypdf
pip install azure-ai-inference
```

2) Configure your `.env` file with the required environment variable: 
```env
OPENAI_API_KEY=[Replace with your Azure OpenAI token]
```

3) Clone the repository and run the application to start Streamlit:
```bash
git clone https://github.com/elijah-tynes/capstone-manager.git
cd capstone-manager
python -m streamlit run capstonemanager.py
```

4) Upload a project description document containing `project names`, `project descriptions`, and `number of students` needed for each project clearly stated (PDF format)

5) Upload each student resume as a separate file (PDF format)

6) Click "Assign students to projects" to generate project-team assignments
