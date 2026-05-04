# 🏛️ EU Information Systems Governance Prototype

This project is a prototype designed to analyze the impact of legal documents on information system components within the context of EU governance.

It uses Natural Language Processing (NLP) techniques to process PDF documents and identify how they affect different system components such as digital services, data fields, stakeholders, and information pages.

---

## 🚀 Features

- 📄 Upload and analyze legal PDF documents
- 🧠 NLP pipeline using spaCy and Sentence Transformers
- 🔍 Hybrid scoring system:
  - Keyword matching
  - Semantic similarity
  - Entity recognition
- 📊 Impact classification (HIGH / MEDIUM / LOW)
- 🧾 Traceability through relevant text fragments
- 💻 Interactive UI built with Streamlit

---

## 🏗️ Project Structure

project/
│
├── backend/
│   ├── app.py              # FastAPI server
│   ├── analyzer.py        # Scoring logic
│   ├── nlp_pipeline.py    # NLP processing
│   └── db.py              # Database access
│
├── frontend/
│   └── app_streamlit.py   # Streamlit UI
│
├── data/
│   ├── knowledge.db       # SQLite database
│   └── schema.sql         # Database schema
│
└── README.md

---

## ⚙️ Installation

1. Clone the repository:

git clone <your-repo>  
cd project

2. Create and activate virtual environment:

python -m venv venv  
venv\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt

4. Download spaCy model:

python -m spacy download en_core_web_sm

---

## ▶️ Running the Application

### Start backend:

uvicorn backend.app:app --reload

### Start frontend:

streamlit run frontend/app_streamlit.py

Then open:  
http://localhost:8501

---

## 🧪 How It Works

1. Upload a PDF document  
2. The system extracts and processes the text  
3. NLP pipeline generates embeddings and entities  
4. Components are scored based on relevance  
5. Results are displayed with explanations and fragments  

---

## ⚠️ Limitations

- Optimized for English documents  
- Depends on keyword quality in database  
- Not a replacement for legal analysis  

---

## 🔮 Future Improvements

- Multilingual support  
- Integration with EUR-Lex  
- Legal-specific NLP models  
- Graph-based visualization  

---

## 📄 License

This project is for academic purposes.