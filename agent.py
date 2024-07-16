from crewai import Agent, Crew, Task
from langchain_groq import ChatGroq
from tools.git import github_operations

repo_name = input("Enter the repository name: ")
description = input("Enter the repository description (optional): ")
issue_title = input("Enter the issue title: ")
issue_body = input("Enter the issue description: ")
branch_name = input("Enter the branch name: ")

my_llm = ChatGroq(
    api_key="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",
    model="llama3-8b-8192",
)

ScrumMaster = Agent(
    role="Scrum Master",
    goal=f"Create a new repository on GitHub named {repo_name} with the provided description, manage the repository, create an issue titled '{issue_title}', and create a branch '{branch_name}'.",
    backstory="The Scrum Master ensures the creation and management of repositories on GitHub, facilitates the development team's workflow, and handles issue and branch management.",
    llm=my_llm,
    tools=[github_operations],  
    verbose=True,
    allow_delegation=False,
)

scrum_master_task = Task(
    description=f"Create a new repository on GitHub named {repo_name} with the description '{description}', create a new issue titled '{issue_title}' with description '{issue_body}', and create a branch '{branch_name}'.",
    expected_output=f"A new repository on GitHub with the name '{repo_name}' and description '{description}', a new issue created with title '{issue_title}' and description '{issue_body}', and a branch '{branch_name}' created.",
    agent=ScrumMaster,
    output_file="scrum_master_output.md",
)

crew = Crew(agents=[ScrumMaster], tasks=[scrum_master_task], verbose=2)
result = crew.kickoff()
print(result)
