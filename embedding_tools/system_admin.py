import os
import re
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import pandas as pd
import requests
from markdownify import markdownify
from requests.exceptions import RequestException
from smolagents import (CodeAgent, DuckDuckGoSearchTool, OpenAIServerModel,
                        ToolCallingAgent, tool)
from smol_tool_library import create_directory, delete_directory, delete_file, list_directory_contents, get_current_directory, replace_code_block, read_file, write_file 


# Web browsing tool
@tool
def visit_webpage(url: str) -> str:
    """Visits a webpage at the given URL and returns its content as a markdown string.

    Args:
        url: The URL of the webpage to visit.

    Returns:
        The content of the webpage converted to Markdown, or an error message if the request fails.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Convert the HTML content to Markdown
        markdown_content = markdownify(response.text).strip()

        # Remove multiple line breaks
        markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

        return markdown_content

    except RequestException as e:
        return f"Error fetching the webpage: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Initialize the OpenAI models
web_model = OpenAIServerModel(
    model_id="gpt-4o-mini-2024-07-18",
    api_base="https://api.openai.com/v1",
    api_key=os.environ["OPENAI_API_KEY"],
)

reasoning_model = OpenAIServerModel(
    model_id="o3-mini-2025-01-31",
    api_base="https://api.openai.com/v1",
    api_key=os.environ["OPENAI_API_KEY"],
)

# Create specialized agents
# 1. Web Search Agent - for retrieving current best practices
web_agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool(), visit_webpage],
    model=web_model,
    max_steps=8,
    name="web_search_agent",
    description="Searches the web for recent best practices for what we are building.",
)

# 2. Analysis Agent - for processing information
analysis_agent = ToolCallingAgent(
    tools=[create_directory, delete_directory, delete_file, list_directory_contents, get_current_directory],
    model=reasoning_model,
    max_steps=5,
    name="analysis_agent",
    description="Analyzes market data to extract sentiment and key metrics",
)

# 3. Manager Agent - orchestrates the entire process
lead_developer_agent = CodeAgent(
    model=reasoning_model,
    tools=[],
    managed_agents=[web_agent, sys_admin_agent, coder_agent, test_runner_agent],
    additional_authorized_imports=["pandas", "matplotlib.pyplot"],
    name="market_research_manager",
    description="Manages the market research workflow and compiles the final report",
    planning_interval=2,
    max_steps=12,
    verbosity_level=2
)

# Display the agent hierarchy
def visualize_agent_system():
    lead_developer_agent.visualize()

# Example usage function
def build_module( module_name: str, module_description: str ):
    """
    Create a python module.
    
    Args:
        module_name: The name of the module to create
        module_description: The description of the module to create
        
    Returns:
        Status of the module creation
    """
    prompt = f"""
    You are a lead developer. Your task is to create module { module_name }.
    The description of the module is { module_description }. 
    
    Follow these steps:
       1. Do a web search to get ideas on best practices to create the { module_name } module.
       
       2. Create a directory called { module_name } so that we can put all of the files into it.
       
       3. Create the { module_name }.py file in the { module_name } directory.
       
       4. Create any other Interfaces, Enums, utility functions, helper files, etc... that you may need for the { module_name } module.
       
       5. Create the __init__.py file so that the module can be imported from outside
       
       6. Make sure that the necessary dependent software is installed in the system.  For example, if you are using the `openai` module in { module_name }.py, use the `uv` command to make sure that it is installed or use the `uv add` command to install it.  If `uv` is not installed, use your web search tool to find out how to install it and do so.
       
       7. Write a { module_name }_test.py file to test the module.
       
       8. Run the { module_name }_test.py file, if it fails, fix the problem
       
       9. Repeat running the test file and making modifications until the test passes.
       
       10. Create a mermaid class diagram for the module in the { module_name } directory to show how it should be used in a system.
       
       11. Create a mermaid sequence diagram for the module in the { module_name } directory to show how it should be used in a system.
       
       12. Write a readme.md file with the following information:
            - ideas that you have gotten from your web search when you thought about how to construct the module in step 1.
            - all of the files created ( Interfaces, helper functions, Enums, etc.. ) and a brief description of each
            - a list of all the modules that you have had to install and a brief description of why we need them in the { module_name } module.
            - the problems that you ran into and how you have corrected them
            - suggestions for using the module effectively
            - example code to use the module
       
    """
    
    result = lead_developer_agent.run(prompt)
    return result

# Usage example
if __name__ == "__main__":
    # Visualize the agent system
    visualize_agent_system()
    
    # Run a market research for the renewable energy industry
    result = lead_developer_agent("tennis_scoreboard_display", "Shows the games, sets, serve status and points of a current tennis game using ASCII art." )
    print( result )
    
    # You can easily run research for other industries
    # report = run_market_research("electric vehicles")
    # report = run_market_research("artificial intelligence")