from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

agent=create_agent(model="gpt-4o-mini",system_prompt=(
        "You are a helpful assistant. "
        "Keep answer as precise as possible"
        "do not give lengthy response"
    ))
result=agent.invoke({"messages":[{"role":"user","content":"what is playwright?"}]})

print(result["messages"][-1].content)
