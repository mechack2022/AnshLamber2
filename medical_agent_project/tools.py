from langchain.tools import tool
from models import PatientData, LabResults, Recommendation

@tool
def get_cd4_count(patient: PatientData) -> int:
    """Get the CD4 count for a patient."""
    database = {"LAM12345": 450, "LAM67890": 280}
    return database.get(patient.patient_id, 0)

@tool
def get_viral_load(patient: PatientData) -> int:
    """Get the viral load for a patient."""
    database = {"LAM12345": 50, "LAM67890": 75000}
    return database.get(patient.patient_id, 0)

@tool
def recommend_regimen(labs: LabResults) -> Recommendation:
    """Recommend HIV treatment regimen based on CD4 and viral load."""
    if labs.viral_load < 1000 and labs.cd4 > 350:
        rec = "Continue current regimen - patient is stable"
    elif labs.viral_load > 1000:
        rec = "Consider switching to second-line regimen"
    else:
        rec = "Intensify adherence counseling"
    return Recommendation(recommendation=rec)
