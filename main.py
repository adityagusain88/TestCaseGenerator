from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


@tool
def spiritual_coach(message: str) -> str:
    """Provide spiritual guidance based on the user's message."""
    return model.invoke(message).content


@tool
def life_advice(message: str) -> str:
    """Provide practical life advice based on the user's message."""
    return model.invoke(message).content


agent = create_agent(
    model=model,
    tools=[spiritual_coach, life_advice],
    system_prompt=(
        "You are a helpful assistant. "
        "Use spiritual_coach for spiritual questions "
        "and life_advice for practical life questions."
    ),
)

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What is Playwright?"
        }
    ]
})

print(response["messages"][-1].content)