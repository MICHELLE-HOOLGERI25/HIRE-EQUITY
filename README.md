# HireEquity
### Hybrid AI + ML Powered Job Description Generator & Bias Auditor

## 🌐 Live Demo

**[Click Here to Open App](https://hireequity.streamlit.app/)**

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/AI-Groq%20Llama%203.x-orange?style=for-the-badge)](https://console.groq.com)
[![Transformers](https://img.shields.io/badge/ML-Zero--Shot%20Transformer-blue?style=for-the-badge)](https://huggingface.co/facebook/bart-large-mnli)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)](https://python.org)

---

# What is HireEquity?

HireEquity is a Hybrid AI + Machine Learning platform that helps HR teams create, analyze and improve job descriptions.

Instead of relying only on an LLM, HireEquity combines:

- AI-powered Job Description Generation
- Rule-based Bias Detection
- ML-based Semantic Bias Detection
- AI Job Description Rewriting
- PDF Audit Reporting
- Analytics Dashboard

The system automatically identifies biased language, assigns an inclusivity score, rewrites biased content, and generates a professional audit report.

---

# Problem Statement

Many organizations unknowingly publish job descriptions containing biased language that discourages qualified candidates and reduces workforce diversity.

Examples include:

| Biased Phrase | Category |
|---------------|----------|
| Rockstar, Ninja | Gender Bias |
| Young & Energetic | Age Bias |
| He should... | Gender Bias |
| IIT/NIT Only | Elitism |
| Physically Fit | Ableism |
| 10+ Years Mandatory | Restrictive Hiring |

HireEquity automates the complete auditing process using a Hybrid AI + ML pipeline.

---

# Hybrid Workflow

```text
Step 1 → User enters Role / Level / Domain
          OR Pastes Existing Job Description

↓

Step 2 → Groq Llama 3.x generates Job Description

↓

Step 3 → Hybrid Bias Detection

        • Gaucher Bias Wordlist
        • Zero-Shot Transformer
          (facebook/bart-large-mnli)

↓

Step 4 → Bias Score
          Severity
          Confidence
          Category Analysis

↓

Step 5 → Groq AI rewrites biased Job Description

↓

Step 6 → Before vs After Comparison

↓

Step 7 → PDF Report + Analytics Dashboard
```

---

# Features

- AI Job Description Generator
- Hybrid Bias Detection Engine
- Zero-Shot Semantic Classification
- Gaucher Bias Wordlist Scanner
- Inclusivity Score (0–100)
- Severity Classification
- Confidence Score
- AI Job Description Rewriter
- Before vs After Comparison
- Interactive Analytics Dashboard
- PDF Audit Report
- Candidate Persona Insights

---

# System Architecture

```
User Input
      │
      ▼
Groq Llama 3.x
Job Description Generator
      │
      ▼
Hybrid Bias Detection Engine

 ├── Gaucher Bias Wordlist
 └── Zero-Shot Transformer
     (facebook/bart-large-mnli)

      │
      ▼
Bias Scoring Engine

      │
      ▼
Groq AI Rewrite Engine

      │
      ▼
Analytics Dashboard
+
PDF Report
+
Inclusive Job Description
```

---

# Tech Stack

| Component | Technology |
|------------|------------|
| Frontend | Streamlit |
| AI Generation | Groq Llama 3.x |
| AI Rewriting | Groq Llama 3.x |
| Semantic Detection | facebook/bart-large-mnli |
| ML Framework | Hugging Face Transformers |
| Lexicon Detection | Gaucher Bias Wordlist |
| NLP | NLTK |
| Charts | Plotly |
| PDF Export | ReportLab |
| Backend | Python |
| Deployment | Streamlit Community Cloud |

---

# Hybrid Bias Detection

## Rule-Based Detection

Uses the Gaucher et al. (2011) bias lexicon.

Detects:

- Gender Bias
- Age Bias
- Ableism
- Elitism
- Restrictive Hiring
- Nationality Bias

using exact and partial word matching.

---

## ML-Based Semantic Detection

Model Used

```
facebook/bart-large-mnli
```

Uses Zero-Shot Classification to identify contextual bias that keyword matching cannot detect.

Outputs:

- Bias Category
- Confidence Score
- Severity Level

---

# Dataset / Knowledge Base

HireEquity does not require supervised model training.

Instead it combines:

### Academic Bias Lexicon

**Gaucher et al. (2011)**

Includes:

- Masculine-coded words
- Feminine-coded words
- Age Bias
- Ableism
- Elitism
- Restrictive Hiring

### Pre-trained Transformer

```
facebook/bart-large-mnli
```

Used for Zero-Shot semantic bias classification.

---

# Project Structure

```
HireEquity/

app.py
bias_detector.py
jd_generator.py
rewriter.py
pdf_export.py
wordlists.py

architecture.png
pipeline.png

screenshots/

requirements.txt
README.md
.env.example
.gitignore
```

---

# How to Run

```bash
git clone https://github.com/MICHELLE-HOOLGERI25/HIRE-EQUITY.git

cd HIRE-EQUITY

pip install -r requirements.txt

streamlit run app.py
```

---

# Screenshots

Add screenshots of:

- Dashboard
- AI JD Studio
- Bias Audit
- AI Rewrite
- Analytics

---

# Built For

**PS-HR3 – AI Powered Job Description Generator & Bias Auditor Hackathon**
