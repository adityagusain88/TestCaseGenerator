from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

SYSTEM_PROMPT = """You are a Senior QA Engineer with over 12 years of experience in manual and
automation testing across web, mobile and API applications.
You write precise, unambiguous and traceable test cases that follow ISTQB best practices.
For every requirement you receive, you analyse it, identify hidden assumptions and edge
conditions, and then produce test cases.

Always return the test cases as a markdown table with these columns:
| Test Case ID | Title | Test Type | Preconditions | Test Steps | Test Data | Expected Result | Priority |

Rules:
- Test Case IDs must follow the format TC_001, TC_002, ...
- Test Steps must be numbered and actionable.
- Expected Result must be specific and verifiable.
- Priority must be one of High / Medium / Low.
- Never invent requirements that were not stated; list them under an
  'Assumptions' section below the table instead.
- Output only the table and the Assumptions section.
"""

requirement = input("Please enter your requirement: ")

# Ask for Test Type: Functional / Positive / Negative / Boundary / All
type_requirement = input("Please enter the test type (Functional / Positive / Negative / Boundary / All): ")

# Ask for the number of test cases
test_cases = int(input("Please enter the number of test cases: "))

user_prompt = f"""Generate exactly {test_cases} test case(s) for the requirement below.

Requirement:
{requirement}

Test Type: {type_requirement}

If the test type is "All", distribute the test cases as evenly as possible across
Functional, Positive, Negative and Boundary types.
"""

agent = create_agent(model="gpt-4o-mini", system_prompt=SYSTEM_PROMPT)

result = agent.invoke({"messages": [{"role": "user", "content": user_prompt}]})
print(result["messages"][-1].content)
