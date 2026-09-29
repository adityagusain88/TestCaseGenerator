import os

from langchain.agents import create_agent
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

# On Streamlit Cloud the key comes from st.secrets instead of a local .env file.
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    os.environ["LANGSMITH_TRACING"] = st.secrets["LANGSMITH_TRACING"]
    os.environ["LANGSMITH_API_KEY"] = st.secrets["LANGSMITH_API_KEY"]
    os.environ["LANGSMITH_PROJECT"] = st.secrets["LANGSMITH_PROJECT"]
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]

if not os.environ.get("OPENAI_API_KEY"):
    st.error(
        "OPENAI_API_KEY is not configured. On Streamlit Cloud add it under "
        "Manage app -> Settings -> Secrets, locally add it to your .env file."
    )
    st.stop()

SYSTEM_PROMPT = """You are a Senior QA Engineer with over 12 years of experience in manual and
automation testing across web, mobile and API applications.
You write precise, unambiguous and traceable test cases that follow ISTQB best practices.
For every requirement you receive, you analyse it, identify hidden assumptions and edge
conditions, and then produce test cases.

Always return the test cases as a markdown table with these columns:
| Test Case ID | Title | Test Type | Preconditions | Test Steps | Test Data | Expected Result | Priority |

Rules:
- Test Case IDs must follow the format TC_001, TC_002, ...
- Test Steps must be numbered and actionable. Separate steps inside a cell with <br>
  so the markdown table stays intact (never use real line breaks inside a cell).
- Escape any literal | inside a cell as \\|.
- Expected Result must be specific and verifiable.
- Priority must be one of High / Medium / Low.
- Never invent requirements that were not stated; list them under an
  'Assumptions' section below the table instead.
- Output only the table and the Assumptions section.
"""
st.title("Test Case Generator")
requirement = st.text_input("Please enter your requirement:")

# Ask for Test Type: Functional / Positive / Negative / Boundary / All
type_requirement = st.selectbox("Please enter the test type", ["Functional", "Positive", "Negative", "Boundary", "All"])

# Ask for the number of test cases
test_cases = st.number_input("Please enter the number of test cases:", min_value=1, max_value=50, value=5, step=1)

user_prompt = f"""Generate exactly {test_cases} test case(s) for the requirement below.

Requirement:
{requirement}

Test Type: {type_requirement}

If the test type is "All", distribute the test cases as evenly as possible across
Functional, Positive, Negative and Boundary types.
"""

agent = create_agent(model="gpt-4o-mini", system_prompt=SYSTEM_PROMPT)

if st.button("Ask") and requirement:
    with st.spinner("Thinking..."):
        result = agent.invoke({"messages": [{"role": "user", "content": user_prompt}]})
        message = result["messages"][-1].content
        st.markdown(message, unsafe_allow_html=True)
        with st.expander("Raw markdown"):
            st.code(message, language="markdown")
        st.download_button("Download test cases", message, file_name="test_cases.md")