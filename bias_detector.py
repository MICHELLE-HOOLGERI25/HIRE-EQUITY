import re
import os
import json
import logging
from groq import Groq
from dotenv import load_dotenv
from wordlists import BIAS_DICTIONARY
from transformers import pipeline
import torch
from functools import lru_cache

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# -------------------------------
# ML MODELS
# -------------------------------



DEVICE = 0 if torch.cuda.is_available() else -1

@lru_cache(maxsize=1)
def get_zero_shot_classifier():
    return pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        device=DEVICE
    )

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)

def scan_wordlist_bias(jd_text):
    """
    Scans the job description using the Gaucher et al. and other hardcoded word lists.
    Returns a list of dictionaries containing:
    - phrase: matching text in the JD
    - category: bias category (e.g. Gender, Age)
    - severity: critical/moderate/minor
    - suggestion: suggested alternative
    - start: start index in text
    - end: end index in text
    """
    if not jd_text or not jd_text.strip():
        return []

    flagged_items = []
    
    # We want to search for terms case-insensitively.
    # To handle plural forms, adverbs, and adjectives, we allow suffix letters
    # unless it's a short word where suffixes could cause false positives (e.g., 'he' -> 'hello').
    short_words_exact = {"he", "his", "him", "iit", "nit"}
    
    # Sort terms by length descending to match longer phrases (e.g., '10 years experience') 
    # before individual words (e.g., 'experience')
    sorted_terms = sorted(BIAS_DICTIONARY.keys(), key=len, reverse=True)
    
    # Track matched character spans to avoid overlapping matches
    matched_spans = []

    for term in sorted_terms:
        # Build regex based on whether it is a short word requiring exact match or can have suffixes
        if term in short_words_exact:
            pattern = rf"\b{re.escape(term)}\b"
        else:
            # Allow common suffixes like s, es, ed, ing, ly, er, est, etc.
            pattern = rf"\b{re.escape(term)}[a-zA-Z]*\b"

        for match in re.finditer(pattern, jd_text, re.IGNORECASE):
            start, end = match.span()
            matched_phrase = match.group()
            
            # Check if this span overlaps with any previously matched span
            overlap = False
            for m_start, m_end in matched_spans:
                if not (end <= m_start or start >= m_end):
                    overlap = True
                    break
            
            if not overlap:
                info = BIAS_DICTIONARY[term]
                flagged_items.append({
                    "phrase": matched_phrase,
                    "category": info["category"],
                    "severity": info["severity"],
                    "suggestion": info["suggestion"],
                    "start": start,
                    "end": end,
                    "source": "Gaucher Lexicon"
                })
                matched_spans.append((start, end))
                
    # Sort by starting position
    flagged_items.sort(key=lambda x: x["start"])
    return flagged_items

def classify_sentence_bias(sentence):
    """
    Classify a sentence into one of the predefined
    hiring bias categories.
    """

    labels = [
        "Gender Bias",
        "Age Bias",
        "Ableism",
        "Elitism",
        "Restrictive Hiring",
        "Nationality Bias",
        "Neutral"
    ]

    classifier = get_zero_shot_classifier()
    result = classifier(
        sentence,
        candidate_labels=labels,
        multi_label=False,
        hypothesis_template="This sentence contains {}."
    )

    return {
        "category": result["labels"][0],
        "confidence": float(result["scores"][0])
    }


import nltk
nltk.download("punkt", quiet=True)

from nltk.tokenize import sent_tokenize


def check_semantic_bias(jd_text):
    """
    ML-based semantic bias detection using Zero-shot Classification.
    No LLM is used for detection.
    """

    sentences = sent_tokenize(jd_text)

    # Better category-specific suggestions
    SUGGESTIONS = {
        "Gender Bias": "Use gender-neutral wording.",
        "Age Bias": "Avoid references to age.",
        "Ableism": "Use inclusive accessibility language.",
        "Elitism": "Avoid unnecessary educational restrictions.",
        "Restrictive Hiring": "Relax unnecessary qualification requirements.",
        "Nationality Bias": "Avoid nationality-specific requirements."
    }

    semantic_flags = []

    for sentence in sentences:

        # Remove extra spaces
        sentence = sentence.strip()

        # Skip empty or very short sentences
        if len(sentence) < 10:
              continue

        result = classify_sentence_bias(sentence)

        category = result["category"]
        confidence = result["confidence"]

        # Ignore neutral predictions
        if category == "Neutral":
            continue

        # Ignore low-confidence predictions
        if confidence < 0.75:
            continue

        # Assign severity based on confidence
        if confidence >= 0.90:
            severity = "critical"
        elif confidence >= 0.80:
            severity = "moderate"
        else:
            severity = "minor"

        semantic_flags.append({
            "phrase": sentence,
            "category": category,
            "severity": severity,
            "confidence": round(confidence, 3),
            "suggestion": SUGGESTIONS.get(
                category,
                "Rewrite using more inclusive language."
            ),
            "source": "Zero-Shot Transformer"
        })

    return semantic_flags

def check_semantic_bias_groq(jd_text):
    """
    Calls Groq API to run a semantic bias audit.
    Tries multiple fallback models in case of rate limits or service outages.
    """
    client = get_groq_client()
    if not client:
        logger.info("Groq semantic detector kept as fallback. Using Zero-Shot Transformer as primary detector.")
        return []

    prompt = f"""Analyze this job description for subtle bias that wordlists may miss.
Return JSON only, no extra text:
{{
  "biased_phrases": [
    {{
      "phrase": "string",
      "category": "string",
      "severity": "critical/moderate/minor",
      "suggestion": "string"
    }}
  ]
}}
JD: {jd_text}"""

    # List of models to try in sequence
    models_to_try = [
        "llama-3.1-8b-instant",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
        "llama-3.3-70b-versatile"
    ]

    last_error = None
    for model in models_to_try:
        try:
            logger.info(f"Attempting semantic bias check with Groq model: {model}")
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful HR assistant specialized in diversity, equity, and inclusion (DEI)."},
                    {"role": "user", "content": prompt}
                ],
                model=model,
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            logger.info(f"Groq Semantic Response using model {model}: {content}")
            data = json.loads(content)
            biased_phrases = data.get("biased_phrases", [])
            
            # Clean and standardise results
            cleaned_items = []
            for item in biased_phrases:
                phrase = item.get("phrase", "")
                if not phrase:
                    continue
                    
                # Standardize severity
                severity = item.get("severity", "moderate").lower()
                if severity not in ["critical", "moderate", "minor"]:
                    severity = "moderate"
                    
                cleaned_items.append({
                    "phrase": phrase,
                    "category": item.get("category", "General Bias"),
                    "severity": severity,
                    "suggestion": item.get("suggestion", "Rephrase using more inclusive terminology."),
                    "source": "semantic"
                })
            return cleaned_items
        except Exception as e:
            logger.warning(f"Failed semantic bias check using model {model}: {e}")
            last_error = e

    logger.error(f"All Groq models failed for Semantic Bias Check. Last error: {last_error}")
    # Return empty list so the app doesn't crash
    return []

def calculate_score(flagged_items):

    score = 100

    for item in flagged_items:

        severity = item["severity"].lower()

        confidence = item.get("confidence",1.0)

        if severity=="critical":
            penalty = 15

        elif severity=="moderate":
            penalty = 8

        else:
            penalty = 3

        score -= penalty*confidence

    return max(0,round(score))

def combine_and_align_flags(jd_text, wordlist_flags, semantic_flags):
    """
    Combines static wordlist flags with semantic flags.
    Finds starting and ending character positions for semantic flags
    so they can be highlighted, avoiding duplicates or overlaps.
    """
    if not jd_text:
        return []

    combined_flags = []
    # Add wordlist flags first (these have positions already)
    for flag in wordlist_flags:
        combined_flags.append(dict(flag))

    # Track matched spans to avoid highlighting twice
    matched_spans = [(f["start"], f["end"]) for f in combined_flags]

    # For each semantic flag, find where it appears in the text
    for flag in semantic_flags:
        phrase = flag["phrase"]
        # Find matches case-insensitively
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        
        found = False
        for match in pattern.finditer(jd_text):
            start, end = match.span()
            # Check overlap
            overlap = False
            for m_start, m_end in matched_spans:
                if not (end <= m_start or start >= m_end):
                    overlap = True
                    break
            
            if not overlap:
                # Add flag with positions
                new_flag = dict(flag)
                new_flag["start"] = start
                new_flag["end"] = end
                combined_flags.append(new_flag)
                matched_spans.append((start, end))
                found = True
                break # Just find first occurrence that doesn't overlap
                
        if not found:
            # If not found in text as exact phrase, we still keep it but set indices to -1
            # it won't be highlighted, but it will be in the table.
            new_flag = dict(flag)
            new_flag["start"] = -1
            new_flag["end"] = -1
            combined_flags.append(new_flag)

    # Sort by start index, pushing any non-positioned items (-1) to the end
    combined_flags.sort(key=lambda x: (x["start"] < 0, x["start"]))
    return combined_flags

def generate_highlighted_html(jd_text, flagged_items):
    """
    Generates HTML string with highlighted bias words based on severity.
    🔴 RED = Critical bias word
    🟡 YELLOW = Moderate bias word
    🟢 GREEN = Clean text (can represent safe replacements or we can style normal text nicely)
    """
    if not jd_text:
        return ""
        
    # Get only flags that have a valid position in the text
    positioned_flags = [f for f in flagged_items if f["start"] >= 0]
    # Sort them by start index ascending
    positioned_flags.sort(key=lambda x: x["start"])
    
    # We will build the HTML by stitching pieces together
    html_parts = []
    last_idx = 0
    
    for flag in positioned_flags:
        start = flag["start"]
        end = flag["end"]
        
        # Guard against index out of bounds or overlapping bugs
        if start < last_idx:
            continue
            
        # Append clean text before the flag
        html_parts.append(html_escape(jd_text[last_idx:start]))
        
        # Color based on severity
        severity = flag["severity"].lower()
        if severity == "critical":
            # Red Highlight
            badge_html = f'<span class="bias-highlight critical-highlight" title="Category: {flag["category"]} | Severity: Critical">{html_escape(jd_text[start:end])}</span>'
        elif severity == "moderate":
            # Yellow Highlight
            badge_html = f'<span class="bias-highlight moderate-highlight" title="Category: {flag["category"]} | Severity: Moderate">{html_escape(jd_text[start:end])}</span>'
        else:
            # Minor Highlight - let's make it a lighter orange or soft blue, or soft yellow
            badge_html = f'<span class="bias-highlight minor-highlight" title="Category: {flag["category"]} | Severity: Minor">{html_escape(jd_text[start:end])}</span>'
            
        html_parts.append(badge_html)
        last_idx = end
        
    # Append the rest of the text
    html_parts.append(html_escape(jd_text[last_idx:]))
    
    # Replace newlines with <br> to preserve formatting in HTML
    full_html = "".join(html_parts).replace("\n", "<br>")
    return full_html

def html_escape(text):
    """Simple HTML escaping to avoid rendering bugs"""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
