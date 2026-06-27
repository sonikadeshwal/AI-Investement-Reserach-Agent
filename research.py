import langchain
import langgraph
from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import tool_node , tools_condition
from typing import TypedDict
from pydantic import BaseModel
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
from langchain_core.messages import HumanMessage , AIMessage , SystemMessage
from IPython.display import display , Image
from datetime import datetime

llm = ChatGroq(model="llama-3.1-8b-instant")

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun

tavily = TavilySearchResults(max_results=5)

Duck = DuckDuckGoSearchRun()

tool = [tavily,Duck]

llm_with_tool = llm.bind_tools(tool)

class Portfolio(TypedDict):
    query : str
    facts:str
    score:str
    final_response:str

def user_query(state:Portfolio)->Portfolio:
    message = [
        SystemMessage(content=f"""
    You are an intelligent Financial investment AI Assistant.
"""),
HumanMessage(content=f"Find the 5 Bullets point about the Organization why to Invest in the organization {state["query"]}")
    ]

    response = llm_with_tool.invoke(message)
    return {"facts":response.content}


def score(state:Portfolio)->Portfolio:
    message = [SystemMessage(content=f"""You are an Intelligent Financial AI Assistant""")
        ,HumanMessage(content=f"""
    Find the confidence score out of 10 based on the Facts: {state["facts"]} for the investment.
    Calculate confidence score individually for every kind of Investments.
""")]
    
    response = llm.invoke(message)
    return {"score":response.content}

def final_report(state:Portfolio)->Portfolio:
    message = [SystemMessage(content=f"""
You are an Intelligent Final summary Report Creator and use Date of the day when report is generated in the report 
Current Date is {datetime.now()}
"""),
        HumanMessage(content=f"""
                Create a final report by considering facts {state["facts"]} and the Confidence score {state["score"]} and tell the final decision
                should i invest in this organization {state["query"]} or not with all the facts.
""")]
    
    response = llm.invoke(message)
    return {"final_response":response.content}

builder = StateGraph(Portfolio)

builder.add_node("user_query",user_query)
builder.add_node("score",score)
builder.add_node("final_report",final_report)

builder.add_edge(START,"user_query")
builder.add_edge("user_query","score")
builder.add_edge("score","final_report")
builder.add_edge("final_report",END)

graph = builder.compile()

#display(Image(graph.get_graph().draw_mermaid_png()))