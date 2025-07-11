#!/usr/bin/python3
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

def connect_llm(query):
    load_dotenv()

    llm = ChatGroq(
        temperature=0.3,  # Lower temperature for more factual responses
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile"
    )

    result=llm.invoke(query)
    result=result.content

    return result
