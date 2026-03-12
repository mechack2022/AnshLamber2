from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain.prompts import PromptTemplate

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