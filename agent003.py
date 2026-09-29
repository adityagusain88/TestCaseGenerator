from unittest import result

from langchain.agents import create_agent
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

agent=create_agent(model="gpt-4o-mini",system_prompt=(
        "You are a helpful assistant. "
        "Keep answer as precise as possible"
        "do not give lengthy response"
    ))
st.title("Hello AI Assistant👋")
st.markdown(
    """ 
    You are an AI assistant.
    Ask any question and I will provide a concise answer.
    I will keep my answers short and to the point.
    """
)
st.write("Ask a question and click 'Ask' to get a concise answer.")
question=st.text_input("Your question:", placeholder="Type your question here...")
if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        result=agent.invoke({"messages":[{"role":"user","content":question}]})
        message=result["messages"][-1].content
        st.write(message)
