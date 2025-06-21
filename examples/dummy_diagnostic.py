"""Simple diagnostic example.
This script demonstrates a toy diagnostic reasoning process.
"""

SYMPTOMS_DB = {
    ("fever", "cough"): "Influenza",
    ("headache", "stiff neck"): "Meningitis",
    ("chest pain", "shortness of breath"): "Possible heart condition"
}

def diagnose(symptoms):
    """Return a dummy diagnosis based on symptoms list."""
    for key, diagnosis in SYMPTOMS_DB.items():
        if all(symptom in symptoms for symptom in key):
            return diagnosis
    return "Unknown - consult a professional"

if __name__ == "__main__":
    user_input = input("Enter symptoms separated by comma: ")
    symptoms = [s.strip().lower() for s in user_input.split(',')]
    result = diagnose(symptoms)
    print(f"Possible diagnosis: {result}")
