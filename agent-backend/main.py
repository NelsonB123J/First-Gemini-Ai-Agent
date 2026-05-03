import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

app = FastAPI()

# IMPORTANT: Enable CORS so your Vercel frontend can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Vercel URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini 3 Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash", 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Setup Search Tool
search = TavilySearchResults(k=3)
tools = [search]

# Create the LangGraph Agent
agent_executor = create_react_agent(llm, tools)

@app.get("/")
def home():
    return {"status": "Agent is online"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_msg = data.get("message")
    file_content = data.get("fileContent", "")
    
    # Combine file context and user question
    prompt = f"Context from file: {file_content}\n\nUser: {user_msg}" if file_content else user_msg
    
    inputs = {"messages": [HumanMessage(content=prompt)]}
    result = agent_executor.invoke(inputs)
    
    return {"response": result["messages"][-1].content}