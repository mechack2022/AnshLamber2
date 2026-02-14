# from langchain_openai import ChatOpenAI
# from langchain.agents import create_react_agent, AgentExecutor
# from langchain.tools import tool
# from langchain.prompts import PromptTemplate


from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent  # ✅ CORRECT IMPORT
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool

# Define LAMISPlus tools
@tool
def search_patient(name: str) -> str:
    """Search for patient by name, returns patient ID"""
    patients = {"John Doe": "LAM12345", "Jane Smith": "LAM67890"}
    return patients.get(name, "Not found")

@tool
def get_patient_labs(patient_id: str) -> dict:
    """Get latest lab results for patient"""
    labs = {
        "LAM12345": {"cd4": 450, "viral_load": 50, "date": "2026-01-15"},
        "LAM67890": {"cd4": 180, "viral_load": 75000, "date": "2026-01-20"}
    }
    return labs.get(patient_id, {})

@tool
def get_current_regimen(patient_id: str) -> str:
    """Get patient's current ARV regimen"""
    regimens = {
        "LAM12345": "TDF/3TC/DTG",
        "LAM67890": "TDF/3TC/EFV"
    }
    return regimens.get(patient_id, "Unknown")

@tool
def check_adherence(patient_id: str) -> str:
    """Check patient's medication adherence level"""
    adherence = {
        "LAM12345": "Good - 95% adherence",
        "LAM67890": "Good - 92% adherence"
    }
    return adherence.get(patient_id, "Unknown")

# Create agent
tools = [search_patient, get_patient_labs, get_current_regimen, check_adherence]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

react_prompt = PromptTemplate.from_template("""
You are a medical AI assistant for LAMISPlus HIV treatment system.

You have access to these tools:
{tools}

Use this format:
Question: {input}
Thought: [what should I do?]
Action: [tool name]
Action Input: [input to tool]
Observation: [result]
... (repeat as needed)
Thought: I now have enough information
Final Answer: [comprehensive response]

Question: {input}{agent_scratchpad}
""")

agent = create_react_agent(llm, tools, react_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Test it
result = agent_executor.invoke({
    "input": "Assess John Doe's current HIV treatment status and recommend if regimen change is needed"
})

print(result['output'])