from tools import get_cd4_count, get_viral_load, recommend_regimen
from models import PatientData, LabResults

def medical_agent(patient_id: str) -> str:
    """Orchestrates the tools to produce a recommendation."""
    # Wrap patient input
    patient = PatientData(patient_id=patient_id)

    # Call tools
    cd4 = get_cd4_count.invoke(patient)
    vl = get_viral_load.invoke(patient)

    # Wrap lab results
    labs = LabResults(cd4=cd4, viral_load=vl)

    # Get recommendation
    recommendation = recommend_regimen.invoke({"labs": labs})

    # Return formatted string
    return (
        f"Patient ID: {patient.patient_id}\n"
        f"CD4 count: {cd4}\n"
        f"Viral load: {vl}\n"
        f"Recommendation: {recommendation.recommendation}"
    )
