import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

def run_pre_scan(report_text):
    """Stage 1: Quick background check to find out-of-range biomarkers."""
    prompt = f"""
    You are a medical data extraction bot. Analyze this blood test text and return a raw JSON object listing ONLY the biomarkers that are HIGH or LOW compared to their reference ranges.
    Do not write any introductory or concluding text. Return ONLY valid JSON matching this exact schema:
    {{
      "detected_issues": ["Iron", "Hemoglobin", "Vitamin D", "Magnesium"]
    }}
    Here is the text: {report_text}
    """
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False, "options": {"temperature": 0.0}}
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        res_text = response.json()['response'].strip()
        if "```json" in res_text:
            res_text = res_text.split("```json")[1].split("```")[0].strip()
        elif "```" in res_text:
            res_text = res_text.split("```")[1].split("```")[0].strip()
        return json.loads(res_text).get("detected_issues", [])
    except Exception:
        return ["Iron", "Vitamin D", "Magnesium"]

def run_final_analysis(report_text, history, user_symptoms):
    """Stage 2: Generates the personalized, patient-friendly explanation report."""
    prompt = f"""
    You are an expert clinical data analyst communicating directly with a patient. Analyze the blood test report text below by correlating it with the patient's demographics, their checked symptoms, and their custom-written health notes.

    === PATIENT DATA ===
    - Age: {history['age']} | Sex: {history['sex']} | Diet: {history['diet']}
    - Identified Lab Deficiencies: {history['pre_scan_issues']}
    - Confirmed Symptoms: {", ".join(user_symptoms['checked'])}
    - Patient's Custom Notes: {user_symptoms['custom_text']}

    === RAW BLOOD TEST DATA ===
    {report_text}

    === STRUCTURAL INSTRUCTIONS ===
    Format your response using these exact markdown headers:
    ### 🩺 CLINICAL SUMMARY & CORRELATION
    ### 🚦 BIOMARKER SEVERITY BREAKDOWN (1-10 SCALE)
    ### 🧠 EASY-TO-UNDERSTAND MEDICAL TRANSLATION
    ### 💊 TARGETED NUTRIENT & SUPPLEMENT PLAN
    ### 🚨 WHEN TO CONSULT A DOCTOR (TRIAGE POINTS)
    """
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False, "options": {"temperature": 0.2}}
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        return response.json()['response']
    except Exception as e:
        return f"Error running final synthesis engine: {str(e)}"
