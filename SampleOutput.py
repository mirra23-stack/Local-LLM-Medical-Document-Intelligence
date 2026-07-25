import json
import random
import re

# Patient names from A (binary 0 / 0000) to M (binary 12 / 1100) using custom patterns
patient_names = [
    "AAAAAAAA0000",  # Patient A (0)
    "BBBBBBBB0001",  # Patient B (1)
    "CCCCCCCC0010",  # Patient C (2)
    "DDDDDDDD0011",  # Patient D (3)
    "EEEEEEEE0100",  # Patient E (4)
    "FFFFFFFF0101",  # Patient F (5)
    "GGGGGGGG0110",  # Patient G (6)
    "HHHHHHHH0111",  # Patient H (7)
    "IIIIIIII1000",  # Patient I (8)
    "JJJJJJJJ1001",  # Patient J (9)
    "KKKKKKKK1010",  # Patient K (10)
    "LLLLLLLL1011",  # Patient L (11)
    "MMMMMMMM1100"   # Patient M (12)
]

conditions = ["Hypertension", "Type 2 Diabetes Mellitus", "Acute Bronchitis", "Hyperlipidemia", "Mild Asthma"]
medications = [
    {"name": "Lisinopril", "dosage": "10mg daily"},
    {"name": "Metformin", "dosage": "500mg twice daily"},
    {"name": "Atorvastatin", "dosage": "20mg nightly"},
    {"name": "Albuterol inhaler", "dosage": "2 puffs PRN"}
]
lab_tests = [
    {"test": "Blood Glucose", "range": "70-99 mg/dL"},
    {"test": "Cholesterol Total", "range": "< 200 mg/dL"},
    {"test": "Hemoglobin A1c", "range": "< 5.7%"}
]

def generate_random_date():
    year = 2025
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"

# 1. Generate the dataset mapping each custom binary-indexed name
dataset = []
for i, name in enumerate(patient_names, start=1):
    doc_id = f"MED-{i}"
    date = generate_random_date()
    
    lines = [
        f"DOCUMENT ID: #{doc_id}",
        f"DATE OF ENCOUNTER: {date}",
        "ATTENDING PHYSICIAN: Dr. XXXXX, MD",
        f"PATIENT NAME: {name}",
        "--- START OF CLINICAL NOTES ---",
        "Patient presents for routine follow-up evaluation.",
        "Chief Complaint: Patient reports occasional fatigue and mild discomfort.",
        f"Vital Signs - BP: {random.randint(110, 140)}/{random.randint(70, 90)}, HR: {random.randint(60, 100)} bpm.",
        f"Primary Assessment / Diagnosis: {random.choice(conditions)}.",
        "Relevant Lab Results:",
        f" - {lab_tests[0]['test']}: {random.randint(80, 180)} mg/dL (Normal: {lab_tests[0]['range']})",
        f" - {lab_tests[1]['test']}: {random.randint(150, 240)} mg/dL (Normal: {lab_tests[1]['range']})",
        "Prescription & Treatment Plan:",
    ]
    
    chosen_meds = random.sample(medications, k=random.randint(1, 2))
    for med in chosen_meds:
        lines.append(f" * Rx: {med['name']} - {med['dosage']}")
        
    lines.extend([
        "Patient advised to maintain diet and schedule follow-up lab work in 3 months.",
        "--- END OF CLINICAL NOTES ---"
    ])
    
    dataset.append({
        "document_id": doc_id,
        "patient": name,
        "parsed_lines": lines
    })

# 2. Function to look up and extract key points for a specific patient input
def get_patient_summary(target_patient_name):
    matched_doc = None
    for doc in dataset:
        if doc["patient"].lower() == target_patient_name.strip().lower():
            matched_doc = doc
            break
            
    if not matched_doc:
        return f"No records found for '{target_patient_name}'."
        
    extracted_data = {
        "document_id": matched_doc["document_id"],
        "patient": matched_doc["patient"],
        "key_points": {}
    }
    
    for line in matched_doc["parsed_lines"]:
        if "BP:" in line:
            bp_match = re.search(r"BP:\s*([\d/]+)", line)
            if bp_match:
                extracted_data["key_points"]["blood_pressure"] = bp_match.group(1)
                
        if "Blood Glucose" in line:
            glucose_match = re.search(r"Blood Glucose:\s*([\d]+\s*mg/dL)", line)
            if glucose_match:
                extracted_data["key_points"]["sugar_level"] = glucose_match.group(1)
                
        if "Primary Assessment / Diagnosis:" in line:
            diag_match = re.search(r"Diagnosis:\s*(.+)", line)
            if diag_match:
                extracted_data["key_points"]["diagnosis"] = diag_match.group(1).strip()
                
        if "* Rx:" in line:
            if "medications" not in extracted_data["key_points"]:
                extracted_data["key_points"]["medications"] = []
            rx_match = re.search(r"\* Rx:\s*(.+)", line)
            if rx_match:
                extracted_data["key_points"]["medications"].append(rx_match.group(1).strip())
                
    return extracted_data

# 3. Interactive prompt loop using custom binary tags
print("--- Medical Document Information Extraction System ---")
print("Available records: AAAAAAAA0000 up to MMMMMMMM1100")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("Enter patient name (e.g., AAAAAAAA0000): ")
    if user_input.lower() == 'exit':
        break
        
    result = get_patient_summary(user_input)
    print(json.dumps(result, indent=4))
    print("-" * 40)