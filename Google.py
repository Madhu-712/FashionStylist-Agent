from phi.agent import Agent
from phi.tools.googlesearch import GoogleSearch
import streamlit as st
import os

# Define system prompt and instructions

SYSTEM_PROMPTS="""You are a google search agent that helps users search the information from the web and give response in markdown format.""",
    

agent = Agent(
    tools=[GoogleSearch()],
    description="You are a news agent that helps users find the latest news.",
    instructions=[
        "Given a topic by the user, respond with 4 latest news items about that topic.",
        "Search for 10 news items and select the top 4 unique items.",
        "Search in English and in French.",
    ],
    show_tool_calls=True,
    debug_mode=True,
)
agent.print_response("Mistral AI", markdown=True)
