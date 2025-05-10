import os
import json
import pandas as pd
from bs4 import BeautifulSoup
from docx import Document
from unstructured.partition.pdf import partition_pdf

def parse_pdf(filepath):
    elements = partition_pdf(filename=filepath)
    return [el.text for el in elements if el.text and len(el.text) > 30]

def parse_csv(filepath):
    df = pd.read_csv(filepath)
    return df.to_dict(orient="records")

def parse_docx(filepath):
    doc = Document(filepath)
    return [para.text for para in doc.paragraphs if para.text.strip()]

def parse_html(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    return [p.get_text() for p in soup.find_all("p")]

def analyse_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        return parse_pdf(filepath)
    elif ext == ".csv":
        return parse_csv(filepath)
    elif ext == ".docx":
        return parse_docx(filepath)
    elif ext == ".html":
        return parse_html(filepath)
    else:
        return ["Format non supporté"]

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1]
    output = analyse_file(input_file)
    print(json.dumps(output, indent=2, ensure_ascii=False))