import re
import phonenumbers
from PyPDF2 import PdfReader
import os

folder_path = "../parsing_resume/"


def extract_text_from_pdf(file_path):
    """Извлекает текст из PDF через PyPDF2"""
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def parse_resume(file_path):
    text = extract_text_from_pdf(file_path)

    # --- ФИО ---
    fio_pattern = re.findall(r"\b[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+(?: [А-ЯЁ][а-яё]+)?\b", text)
    fio = fio_pattern[0] if fio_pattern else None

    # --- Email ---
    email_pattern = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    email = email_pattern[0] if email_pattern else None

    # --- Телефон ---
    phones = [str(match.number) for match in phonenumbers.PhoneNumberMatcher(text, "RU")]

    # --- Навыки ---
    skill_keywords = [
        "Python", "C++", "C#", "Java", "JavaScript", "TypeScript", "React",
        "Vue", "Django", "Flask", "SQL", "PostgreSQL", "MySQL", "MongoDB",
        "Docker", "Kubernetes", "Linux", "Git", "Excel", "Power BI",
        "ML", "AI", "Data Science", "Pandas", "NumPy", "TensorFlow", "PyTorch"
    ]
    skills = [s for s in skill_keywords if s.lower() in text.lower()]

    # --- Образование ---
    education = re.findall(
        r"(бакалавр|магистр|высшее образование|университет|институт|академия)",
        text, re.IGNORECASE
    )

    # --- Опыт работы ---
    experience = re.findall(
        r"(\d+)\s+(?:год|года|лет)\s+(?:опыта|работы)",
        text.lower()
    )

    return {
        "ФИО": fio,
        "Email": email,
        "Телефоны": phones,
        "Навыки": skills,
        "Образование": education,
        "Опыт (лет)": experience[0] if experience else None
    }


if __name__ == "__main__":
    for filename in os.listdir(folder_path):
        if not filename.endswith('pdf'):
            continue
        data = parse_resume(filename)
        for key, value in data.items():
            print(f"{key}: {value}")
        print()
