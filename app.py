import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import  initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
import os
from dotenv import load_dotenv
arxiv_wrapper = ArxivAPIWrapper(top_k_results = 1, doc_content_chars_max= 200)
arxiv = ArxivQueryRun(api_wrapper= arxiv_wrapper)

wiki_wrapper = WikipediaAPIWrapper(top_k_results= 1, doc_content_chars_max= 200)
wiki = WikipediaQueryRun(api_wrapper= wiki_wrapper)

search = DuckDuckGoSearchRun(name= "Search")

st.sidebar.title("🔎 Langchain - Chat with Search")
api_key = st.sidebar.text_input("Enter Groq API Key:", type= "password")

if 'messages' not in st.session_state:
    st.session_state["messages"] = [
        {'role': 'assistant', 'content':'Hi, I am a chatbot who can search the web. How can I help you today?'}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

if prompt:= st.chat_input(placeholder='what is machinlearning?'):
    st.session_state.messages.append({'role':'user', 'content': prompt})
    st.chat_message('user').write(prompt)

    llm = ChatGroq(api_key= api_key)
    tools = [search, arxiv, wiki]
    search_agent = initialize_agent(tools, llm, agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION, handling_parse_errors = True)
    
