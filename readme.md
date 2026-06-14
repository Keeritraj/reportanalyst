# Hemo-Analyst Pro: AI-Powered Blood Report Explainer

Developed by Keertiraj Singh 

🩸 Project Overview
Hemo-Analyst Pro is a context-aware medical NLP application designed to translate complex, unstructured blood test PDFs into patient-friendly, educational explanations. 

By taking patient demographics, diet, and dynamic symptoms into account *before* running final analysis, the system ensures highly personalized health summaries alongside an absolute 1–10 severity scaling model.

 📁 System Architecture
The codebase is structured modularly to separate presentation logic from core AI processing:
- `app/main.py`: Streamlit frontend interface, state mechanics, and multi-stage user workflow.
- `backend/llm_client.py`: Inferences local Llama 3.2 via Ollama using targeted dual-stage system prompting.
- `utils/pdf_generator.py`: Manages raw string extraction from uploaded documents and compiles formatted download files.

 🚀 Local Installation & Execution
1. Ensure your local AI engine is running in your background terminal:
   ```bash
   ollama run llama3.2
