import sys
import json
import os

def extract_text(path):
    if path.endswith('.pdf'):
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            return ''.join([page.extract_text() or '' for page in pdf.pages])
    elif path.endswith('.docx'):
        from docx import Document
        doc = Document(path)
        return '\n'.join([para.text for para in doc.paragraphs])
    else:
        return ""

def analyze_resume(text, job_role):
    keywords = {
        "Software Engineer": ['python', 'developer', 'coding', 'git'],
        "Data Scientist": ['data', 'python', 'statistics', 'machine learning'],
        "Product Manager": ['product', 'management', 'strategy', 'agile']
    }

    score = 0
    matched_keywords = []

    for word in keywords.get(job_role, []):
        if word.lower() in text.lower():
            score += 10
            matched_keywords.append(word)

    return score, matched_keywords

def main():
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Invalid arguments"}))
        return

    path = sys.argv[1]
    job = sys.argv[2]

    text = extract_text(path)

    if not text:
        print(json.dumps({"error": "Failed to extract resume text"}))
        return

    match_score, matched_keywords = analyze_resume(text, job)
    suggestions = "Add more relevant keywords for a higher match"

    print(json.dumps({
        "matchScore": match_score,
        "matchedKeywords": matched_keywords,
        "suggestions": suggestions
    }))

if __name__ == "__main__":
    main()
