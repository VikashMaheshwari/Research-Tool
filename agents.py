import json
import re
from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url 
from dotenv import load_dotenv

## model load
load_dotenv()
llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)

class CustomSearchAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {t.name: t for t in tools}

    def invoke(self, state: dict) -> dict:
        user_message = state["messages"][-1][1]
        
        system_prompt = (
            "You are a search assistant. You have access to a tool named `web_search` which takes a `query` string.\n"
            "If you need to search the web to answer the user query, respond ONLY with a JSON object in this format:\n"
            "{\n"
            '  "action": "web_search",\n'
            '  "query": "search query here"\n'
            "}\n"
            "Do not include any other text, explanation, or markdown formatting. Just the raw JSON object.\n"
            "If you do not need to search the web, answer the user query directly in plain text."
        )
        
        response = self.llm.invoke([
            ("system", system_prompt),
            ("user", user_message)
        ])
        
        content = response.content.strip()
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            try:
                tool_call = json.loads(match.group(0))
                if tool_call.get("action") == "web_search":
                    query = tool_call.get("query")
                    tool_output = self.tools["web_search"].invoke(query)
                    return {"messages": [AIMessage(content=tool_output)]}
            except Exception as e:
                pass
                
        return {"messages": [AIMessage(content=content)]}

class CustomReaderAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {t.name: t for t in tools}

    def invoke(self, state: dict) -> dict:
        user_message = state["messages"][-1][1]
        
        system_prompt = (
            "You are a reading assistant. You have access to a tool named `scrape_url` which takes a `url` string.\n"
            "Based on the search results provided by the user, find the most relevant URL and call the tool by responding ONLY with a JSON object in this format:\n"
            "{\n"
            '  "action": "scrape_url",\n'
            '  "url": "http://example.com/url-to-scrape"\n'
            "}\n"
            "Do not include any other text, explanation, or markdown formatting. Just the raw JSON object."
        )
        
        response = self.llm.invoke([
            ("system", system_prompt),
            ("user", user_message)
        ])
        
        content = response.content.strip()
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            try:
                tool_call = json.loads(match.group(0))
                if tool_call.get("action") == "scrape_url":
                    url = tool_call.get("url")
                    tool_output = self.tools["scrape_url"].invoke(url)
                    return {"messages": [AIMessage(content=tool_output)]}
            except Exception as e:
                pass
                
        return {"messages": [AIMessage(content="Error: Could not scrape content.")]}

##1st agent    
def build_search_agent():
    return CustomSearchAgent(llm, [web_search])

## 2nd agent
def build_reader_agent():
    return CustomReaderAgent(llm, [scrape_url])

### writer chain lcel pipeline, runnable

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."), ## system prompt
    ("human", """Write a detailed research report on the topic below.   

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""), ## user prompt
])

## binding output parser to the writer prompt we will create a chain and we will invoke that 
writer_chain = writer_prompt | llm | StrOutputParser()


### critic will review the writer


critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])  ### format


critic_chain = critic_prompt | llm | StrOutputParser()