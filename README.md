# HireEquity 
### AI-Powered Job Description Generator & Bias Auditor

## 🌐 Live Demo
 **[Click Here to Open App](https://hireequity.streamlit.app/)**

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203.1-orange?style=for-the-badge)](https://console.groq.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://python.org)



---

##  What is HireEquity?

HireEquity is a professional, AI-powered web application that helps HR teams, recruiters, and hiring managers write **fairer, more inclusive job descriptions**. It automatically detects biased language, scores the JD out of 100, fixes it using AI, and generates a professional PDF audit report — all in seconds.

---

## Problem Statement

Many companies unknowingly write job descriptions with biased words that discourage qualified candidates from applying and reduce workforce diversity.

| Biased Word | Type | Impact |
|---|---|---|
| "rockstar", "ninja" | Gender Bias | Women feel unwelcome |
| "He should" | Gender Assumption | Excludes non-male candidates |
| "Young and energetic" | Age Bias | Discriminates older candidates |
| "IIT/NIT only" | Elitism | Narrows talent pool unfairly |
| "Physically fit" | Ableism | Excludes differently abled |
| "10+ years experience" | Overly Restrictive | Blocks qualified candidates |

Research by **Gaucher et al. (2011)** proves that masculine-coded words like *rockstar, dominant, competitive* significantly lower appeal for female applicants. Manually reviewing and rephrasing these documents is time-consuming and requires specialized DEI expertise. **HireEquity automates this entire process.**

---

## What It Does — 4 Step Workflow

```
Step 1 → Paste existing JD  OR  type role name to generate new JD
Step 2 → Dual engine scan (Gaucher wordlist + Llama 3.1 semantic check)
Step 3 → AI auto rewrites biased JD, shows before vs after comparison
Step 4 → View insights dashboard + download PDF audit report
```

---

## Features

-  **AI JD Generator** — Generate full professional JD from just a role name, level and domain
-  **Dual Engine Bias Scanner** — Gaucher wordlist matching + Llama 3.1 semantic analysis
-  **Color Heatmap** — Red = Critical, Yellow = Moderate, Blue = Minor bias words
-  **Inclusivity Score** — Bias score out of 100 shown as Plotly gauge chart
-  **One Click Auto Fix** — AI rewrites entire JD removing all bias instantly
-  **Before vs After Comparison** — Side by side view with strikethroughs on bad words
-  **Candidate Persona Predictor** — Predicts gender ratio of applicants before and after fix
-  **PDF Audit Report** — 3 page professional report with full audit details
- **Insights Dashboard** — Charts, score delta, category breakdown analytics

---

##  Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| AI Model | Llama 3.1 via Groq API |
| Bias Detection | Gaucher et al. Wordlist |
| Charts | Plotly Express and Plotly Graph Objects |
| PDF Export | ReportLab |
| Styling | Custom CSS with glassmorphic dark theme |
| Environment | Python Dotenv |

---

##  Dataset Used

**Gaucher et al. (2011)** — Peer reviewed academic research proving that certain words in job ads attract or repel specific demographics. No model training required. Pure word matching combined with LLM semantic understanding.

Wordlist covers:
-  Masculine coded words (aggressive, dominant, rockstar, ninja)
-  Feminine coded words (collaborative, nurturing, warm, compassionate)
-  Age bias words (young, digital native, fresh graduate, below 30)
- Elitism bias (ivy league, tier-1, only IIT, premier institute)
-  Ableism (able-bodied, physically fit, stand for long hours)
-  Overly restrictive (10+ years experience, mandatory PhD)

---

##  How to Run Locally

### Prerequisites
- Python 3.8 or higher
- Free Groq API Key from [console.groq.com](https://console.groq.com)

### Step 1 — Clone the Repository
```bash
git clone https://github.com/ayeshamaniyar26/HireEquity.git
cd HireEquity
```

### Step 2 — Set Up Virtual Environment (Recommended)
```bash
python -m venv .venv

# On Windows
.venv\Scripts\Activate.ps1

# On macOS/Linux
source .venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Configure Environment Variables
Create a `.env` file in the root folder:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### Step 5 — Run the App
```bash
streamlit run app.py
```

Open browser at `http://localhost:8501` 

---

##  Project Structure

```
HireEquity/
│
├── app.py              → Main Streamlit app and all pages
├── bias_detector.py    → Gaucher wordlist + Llama 3.1 semantic scanner
├── jd_generator.py     → AI JD generation via Groq API
├── rewriter.py         → AI auto rewriter for biased JD
├── pdf_export.py       → PDF audit report generator
├── wordlists.py        → Full Gaucher bias wordlist dictionary
│
├── screenshots/        → App screenshots
│   ├── page1.png
│   ├── page2.png
│   ├── page3.png
│   └── page4.png
│
├── requirements.txt    → Python dependencies
├── .env.example        → API key template
├── .gitignore          → Excludes .env and cache files
└── README.md           → Documentation
```

---

##  Screenshots

| Page 1: JD Input | Page 2: Bias Audit |
|---|---|
| ![Page 1](screenshots/page1.png) | ![Page 2](screenshots/page2.png) |

| Page 3: Auto Fix & Compare | Page 4: Insights Dashboard |
|---|---|
| ![Page 3](screenshots/page3.png) | ![Page 4](screenshots/page4.png) |

---

##  Built For

**PS-HR3** — AI Powered Job Description Generator and Bias Auditor Hackathon Challenge

---
