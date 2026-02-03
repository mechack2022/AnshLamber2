from pydantic import BaseModel

class PatientData(BaseModel):
    patient_id: str

class LabResults(BaseModel):
    cd4: int
    viral_load: int

class Recommendation(BaseModel):
    recommendation: str
