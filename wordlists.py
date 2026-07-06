# Gaucher et al. and Additional Bias Word Lists
# Categorized with severity levels and suggested replacements

MASCULINE_HIGH = [
    "rockstar", "ninja", "dominant", "aggressive", "competitive", 
    "dominate", "fearless", "warrior", "crusade", "headstrong", 
    "he", "his", "him", "assertive", "driven", "ambitious", 
    "outspoken", "stubborn", "arrogant", "challenging"
]

MASCULINE_MEDIUM = [
    "confident", "independent", "analytical", "decisive", "strong", 
    "objective", "self-reliant", "lead", "boast", "individual"
]

FEMININE = [
    "collaborative", "warm", "supportive", "nurturing", "interpersonal", 
    "sensitive", "compassionate", "honest", "trust", "committed", 
    "interdependent", "yield", "shrill", "enthusiastic", "together"
]

AGE_HIGH = [
    "young", "energetic", "fresh graduate", "digital native", 
    "recent grad", "youthful", "junior only", "new grad"
]

ELITISM = [
    "ivy league", "tier-1", "top university", "premier institute", 
    "only IIT", "only NIT", "top college"
]

ABLEISM = [
    "able-bodied", "walk-in", "stand for long hours", "physically fit", 
    "no disability"
]

OVERLY_RESTRICTIVE = [
    "10 years experience", "15 years experience", "must have PhD", 
    "mandatory MBA"
]

# Mapping word/phrase to category, severity, and suggested alternative
BIAS_DICTIONARY = {}

# Customize specific suggestions for best UX
SUGGESTIONS = {
    # Masculine High (Gender Bias, Critical)
    "rockstar": "expert, specialist, talented professional",
    "ninja": "skilled professional, key contributor, specialist",
    "dominant": "leading, established, premier",
    "aggressive": "motivated, determined, proactive",
    "competitive": "forward-thinking, ambitious, dynamic",
    "dominate": "excel in, lead in, capture",
    "fearless": "confident, bold, proactive",
    "warrior": "dedicated professional, team champion",
    "crusade": "initiative, mission, drive",
    "headstrong": "determined, independent",
    "he": "they, the candidate, the successful applicant",
    "his": "their, the candidate's",
    "him": "them, the candidate",
    "assertive": "confident, clear-minded, articulate",
    "driven": "motivated, goal-oriented, passionate",
    "ambitious": "motivated, growth-minded",
    "outspoken": "expressive, articulate communicator",
    "stubborn": "persistent, dedicated",
    "arrogant": "confident, self-assured",
    "challenging": "stimulating, reward-driven, engaging",

    # Masculine Medium (Gender Bias, Moderate)
    "confident": "capable, assured, skilled",
    "independent": "self-motivated, autonomous",
    "analytical": "detail-oriented, logical, structured",
    "decisive": "focused, clear-minded",
    "strong": "effective, solid, proven",
    "objective": "unbiased, fair, impartial",
    "self-reliant": "autonomous, self-managing",
    "lead": "guide, facilitate, coordinate",
    "boast": "possess, demonstrate, feature",
    "individual": "team member, colleague, contributor",

    # Feminine (Gender Bias, Minor)
    "collaborative": "cooperative, team-oriented",
    "warm": "welcoming, friendly",
    "supportive": "helpful, encouraging",
    "nurturing": "supportive, development-oriented",
    "interpersonal": "communication-oriented, relational",
    "sensitive": "responsive, empathetic",
    "compassionate": "empathetic, supportive",
    "honest": "transparent, authentic",
    "trust": "reliability, integrity",
    "committed": "dedicated, focused",
    "interdependent": "collaborative, team-integrated",
    "yield": "produce, generate, support",
    "shrill": "focused, direct",
    "enthusiastic": "motivated, engaged",
    "together": "collaboratively, as a team",

    # Age Bias (Age Bias, Critical)
    "young": "dynamic, forward-thinking, modern",
    "energetic": "enthusiastic, motivated, dynamic",
    "fresh graduate": "entry-level applicant, early-career candidate",
    "digital native": "tech-savvy, digitally literate",
    "recent grad": "entry-level candidate",
    "youthful": "vibrant, modern",
    "junior only": "entry-level, introductory-level",
    "new grad": "entry-level candidate",

    # Elitism (Elitism, Moderate)
    "ivy league": "accredited university degree, equivalent experience",
    "tier-1": "reputable academic institutions, equivalent work history",
    "top university": "accredited higher education, relevant academic background",
    "premier institute": "relevant degree or certificate program",
    "only iit": "engineering degree or equivalent practical expertise",
    "only nit": "engineering degree or equivalent practical expertise",
    "top college": "accredited institution",

    # Ableism (Ableism, Critical)
    "able-bodied": "capable of performing core duties with or without reasonable accommodation",
    "walk-in": "scheduled visit, virtual check-in, scheduled interview",
    "stand for long hours": "perform essential physical aspects of the role (clarify if strictly required)",
    "physically fit": "capable of completing required physical tasks",
    "no disability": "remove entirely (non-inclusive and legally sensitive)",

    # Overly Restrictive (Overly Restrictive, Moderate)
    "10 years experience": "demonstrated experience in a similar role, substantial experience",
    "15 years experience": "proven track record in leadership, extensive experience",
    "must have phd": "PhD or equivalent practical experience preferred",
    "mandatory mba": "MBA or equivalent professional experience preferred"
}

# Populate standard lists into the unified dictionary
for w in MASCULINE_HIGH:
    BIAS_DICTIONARY[w.lower()] = {
        "category": "Gender Bias (Masculine)",
        "severity": "critical",
        "suggestion": f"Use '{SUGGESTIONS.get(w.lower(), 'inclusive language')}' instead."
    }

for w in MASCULINE_MEDIUM:
    BIAS_DICTIONARY[w.lower()] = {
        "category": "Gender Bias (Masculine)",
        "severity": "moderate",
        "suggestion": f"Use '{SUGGESTIONS.get(w.lower(), 'inclusive language')}' instead."
    }

for w in FEMININE:
    BIAS_DICTIONARY[w.lower()] = {
        "category": "Gender Bias (Feminine)",
        "severity": "minor",
        "suggestion": f"Use '{SUGGESTIONS.get(w.lower(), 'inclusive language')}' to balance or generalize gender appeal."
    }

for w in AGE_HIGH:
    BIAS_DICTIONARY[w.lower()] = {
        "category": "Age Bias",
        "severity": "critical",
        "suggestion": f"Use '{SUGGESTIONS.get(w.lower(), 'inclusive language')}' instead."
    }

for w in ELITISM:
    BIAS_DICTIONARY[w.lower()] = {
        "category": "Elitism",
        "severity": "moderate",
        "suggestion": f"Use '{SUGGESTIONS.get(w.lower(), 'inclusive language')}' instead."
    }

for w in ABLEISM:
    BIAS_DICTIONARY[w.lower()] = {
        "category": "Ableism",
        "severity": "critical",
        "suggestion": f"Use '{SUGGESTIONS.get(w.lower(), 'inclusive language')}' instead."
    }

for w in OVERLY_RESTRICTIVE:
    BIAS_DICTIONARY[w.lower()] = {
        "category": "Overly Restrictive",
        "severity": "moderate",
        "suggestion": f"Use '{SUGGESTIONS.get(w.lower(), 'inclusive language')}' instead."
    }
