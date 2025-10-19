"""
Модуль для чтения и анализа файлов резюме
Поддерживает PDF, DOCX, TXT форматы
"""

import os
import re
import logging
from typing import Dict, List, Optional, Any
from django.core.files.uploadedfile import UploadedFile

logger = logging.getLogger(__name__)

class ResumeParser:
    """Парсер резюме для извлечения структурированной информации"""
    
    def __init__(self):
        self.skill_keywords = [
            # Программирование
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
            'PHP', 'Ruby', 'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB',
            
            # Фреймворки и библиотеки
            'Django', 'Flask', 'FastAPI', 'React', 'Vue', 'Angular', 'Node.js',
            'Spring', 'Laravel', 'Symfony', 'Express', 'Next.js', 'Nuxt.js',
            
            # Базы данных
            'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch', 'SQLite',
            'Oracle', 'SQL Server', 'Cassandra', 'Neo4j',
            
            # DevOps и инфраструктура
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Linux', 'Git',
            'Jenkins', 'GitLab CI', 'GitHub Actions', 'Terraform', 'Ansible',
            
            # Data Science и ML
            'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch',
            'Keras', 'OpenCV', 'NLTK', 'spaCy', 'Jupyter', 'Apache Spark',
            
            # Другие технологии
            'HTML', 'CSS', 'SASS', 'LESS', 'Webpack', 'Babel', 'ESLint',
            'Figma', 'Adobe Photoshop', 'Sketch', 'InVision'
        ]
        
        self.experience_patterns = [
            r'(\d+)\s*(?:год|года|лет|year|years)\s*(?:опыта|работы|experience)',
            r'(?:опыт|experience).*?(\d+)\s*(?:год|года|лет|year|years)',
            r'(\d+)\+?\s*(?:год|года|лет|year|years)',
        ]
        
        self.education_patterns = [
            r'(?:высшее|высшее образование|university|college)',
            r'(?:бакалавр|bachelor)',
            r'(?:магистр|master)',
            r'(?:кандидат|phd|doctor)',
            r'(?:доктор|doctorate)',
        ]
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Основной метод для парсинга файла резюме"""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.pdf':
                text = self._extract_from_pdf(file_path)
            elif file_extension == '.docx':
                text = self._extract_from_docx(file_path)
            elif file_extension == '.txt':
                text = self._extract_from_txt(file_path)
            else:
                raise ValueError(f"Неподдерживаемый формат файла: {file_extension}")
            
            return self._parse_text(text)
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге файла {file_path}: {e}")
            return {}
    
    def parse_uploaded_file(self, uploaded_file: UploadedFile) -> Dict[str, Any]:
        """Парсинг загруженного файла"""
        try:
            # Сохраняем временный файл
            temp_path = f"/tmp/{uploaded_file.name}"
            with open(temp_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            
            result = self.parse_file(temp_path)
            
            # Удаляем временный файл
            os.remove(temp_path)
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге загруженного файла: {e}")
            return {}
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Извлечение текста из PDF"""
        try:
            from PyPDF2 import PdfReader
            text = ""
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except ImportError:
            logger.error("PyPDF2 не установлен. Установите: pip install PyPDF2")
            return ""
        except Exception as e:
            logger.error(f"Ошибка при чтении PDF: {e}")
            return ""
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Извлечение текста из DOCX"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except ImportError:
            logger.error("python-docx не установлен. Установите: pip install python-docx")
            return ""
        except Exception as e:
            logger.error(f"Ошибка при чтении DOCX: {e}")
            return ""
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Извлечение текста из TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Ошибка при чтении TXT: {e}")
            return ""
    
    def _parse_text(self, text: str) -> Dict[str, Any]:
        """Парсинг текста резюме"""
        if not text:
            return {}
        
        # Очищаем текст
        text = re.sub(r'\s+', ' ', text)
        text_lower = text.lower()
        
        return {
            'full_name': self._extract_name(text),
            'email': self._extract_email(text),
            'phone': self._extract_phone(text),
            'skills': self._extract_skills(text_lower),
            'experience_years': self._extract_experience(text_lower),
            'education_level': self._extract_education(text_lower),
            'languages': self._extract_languages(text_lower),
            'summary': self._extract_summary(text),
            'work_experience': self._extract_work_experience(text),
            'education': self._extract_education_details(text),
        }
    
    def _extract_name(self, text: str) -> Optional[str]:
        """Извлечение ФИО"""
        # Паттерны для поиска ФИО
        patterns = [
            r'\b[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+(?: [А-ЯЁ][а-яё]+)?\b',
            r'[A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        return None
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Извлечение email"""
        email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Извлечение телефона"""
        # Паттерны для российских номеров
        phone_patterns = [
            r'\+7\s?\(?\d{3}\)?\s?\d{3}-?\d{2}-?\d{2}',
            r'8\s?\(?\d{3}\)?\s?\d{3}-?\d{2}-?\d{2}',
            r'\d{3}-?\d{3}-?\d{2}-?\d{2}',
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        return None
    
    def _extract_skills(self, text_lower: str) -> List[str]:
        """Извлечение навыков"""
        found_skills = []
        for skill in self.skill_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        return found_skills
    
    def _extract_experience(self, text_lower: str) -> Optional[int]:
        """Извлечение опыта работы в годах"""
        for pattern in self.experience_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                try:
                    return int(matches[0])
                except ValueError:
                    continue
        return None
    
    def _extract_education(self, text_lower: str) -> str:
        """Определение уровня образования"""
        if any(pattern in text_lower for pattern in ['доктор', 'doctorate', 'phd']):
            return 'doctor'
        elif any(pattern in text_lower for pattern in ['кандидат', 'phd']):
            return 'phd'
        elif any(pattern in text_lower for pattern in ['магистр', 'master']):
            return 'master'
        elif any(pattern in text_lower for pattern in ['бакалавр', 'bachelor']):
            return 'bachelor'
        elif any(pattern in text_lower for pattern in ['высшее', 'university', 'college']):
            return 'bachelor'
        else:
            return 'secondary'
    
    def _extract_languages(self, text_lower: str) -> List[str]:
        """Извлечение языков"""
        language_keywords = [
            'английский', 'english', 'немецкий', 'german', 'французский', 'french',
            'испанский', 'spanish', 'итальянский', 'italian', 'китайский', 'chinese',
            'японский', 'japanese', 'корейский', 'korean'
        ]
        
        found_languages = []
        for lang in language_keywords:
            if lang in text_lower:
                found_languages.append(lang)
        return found_languages
    
    def _extract_summary(self, text: str) -> str:
        """Извлечение краткого описания (о себе)"""
        # Ищем секции типа "О себе", "Summary", "About"
        summary_patterns = [
            r'(?:о себе|about|summary)[:\s]*(.*?)(?:\n\n|\n[A-ZА-Я]|$)',
            r'(?:краткое описание|description)[:\s]*(.*?)(?:\n\n|\n[A-ZА-Я]|$)',
        ]
        
        for pattern in summary_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            if matches:
                return matches[0].strip()[:500]  # Ограничиваем длину
        
        # Если не найдено, берем первые несколько предложений
        sentences = text.split('.')[:3]
        return '. '.join(sentences).strip()[:500]
    
    def _extract_work_experience(self, text: str) -> List[Dict[str, str]]:
        """Извлечение опыта работы"""
        # Упрощенная версия - ищем упоминания компаний и должностей
        companies = re.findall(r'(?:ООО|ЗАО|ИП|LLC|Inc\.|Corp\.)\s*[А-Яа-яA-Za-z\s]+', text)
        positions = re.findall(r'(?:разработчик|developer|менеджер|manager|аналитик|analyst)', text, re.IGNORECASE)
        
        experience = []
        for i, company in enumerate(companies[:3]):  # Ограничиваем 3 записями
            experience.append({
                'company': company.strip(),
                'position': positions[i] if i < len(positions) else 'Специалист',
                'description': 'Опыт работы в компании'
            })
        
        return experience
    
    def _extract_education_details(self, text: str) -> List[Dict[str, str]]:
        """Извлечение деталей образования"""
        # Ищем университеты и специальности
        universities = re.findall(r'(?:МГУ|МФТИ|ВШЭ|МИФИ|СПбГУ|ИТМО|МГТУ|МАИ)', text)
        specialties = re.findall(r'(?:факультет|специальность|направление)[:\s]*([А-Яа-я\s]+)', text, re.IGNORECASE)
        
        education = []
        for i, university in enumerate(universities[:2]):  # Ограничиваем 2 записями
            education.append({
                'institution': university,
                'degree': specialties[i] if i < len(specialties) else 'Высшее образование',
                'description': 'Образование'
            })
        
        return education


class ResumeAnalyzer:
    """Анализатор резюме для системы рекомендаций"""
    
    def __init__(self):
        self.parser = ResumeParser()
    
    def analyze_resume_file(self, file_path: str) -> Dict[str, Any]:
        """Полный анализ файла резюме"""
        parsed_data = self.parser.parse_file(file_path)
        
        if not parsed_data:
            return {}
        
        # Дополнительный анализ
        analysis = {
            'parsed_data': parsed_data,
            'skill_score': self._calculate_skill_score(parsed_data.get('skills', [])),
            'experience_level': self._determine_experience_level(parsed_data.get('experience_years', 0)),
            'education_score': self._calculate_education_score(parsed_data.get('education_level', '')),
            'completeness_score': self._calculate_completeness_score(parsed_data),
        }
        
        return analysis
    
    def _calculate_skill_score(self, skills: List[str]) -> float:
        """Оценка навыков (0-10)"""
        if not skills:
            return 0.0
        
        # Базовый счетчик навыков
        base_score = min(len(skills) * 0.5, 5.0)
        
        # Бонусы за популярные навыки
        popular_skills = ['Python', 'JavaScript', 'Java', 'SQL', 'Git']
        bonus = sum(1.0 for skill in skills if skill in popular_skills)
        
        return min(base_score + bonus, 10.0)
    
    def _determine_experience_level(self, years: int) -> str:
        """Определение уровня опыта"""
        if years == 0:
            return 'no_experience'
        elif years <= 2:
            return 'junior'
        elif years <= 5:
            return 'middle'
        elif years <= 8:
            return 'senior'
        else:
            return 'lead'
    
    def _calculate_education_score(self, education_level: str) -> float:
        """Оценка образования (0-10)"""
        scores = {
            'secondary': 2.0,
            'bachelor': 6.0,
            'master': 8.0,
            'phd': 9.0,
            'doctor': 10.0,
        }
        return scores.get(education_level, 3.0)
    
    def _calculate_completeness_score(self, data: Dict[str, Any]) -> float:
        """Оценка полноты резюме (0-10)"""
        required_fields = ['full_name', 'email', 'phone', 'skills', 'experience_years']
        filled_fields = sum(1 for field in required_fields if data.get(field))
        
        return (filled_fields / len(required_fields)) * 10.0


# Пример использования
if __name__ == "__main__":
    parser = ResumeParser()
    analyzer = ResumeAnalyzer()
    
    # Тестирование на примере файла
    test_file = "resume_example.pdf"
    if os.path.exists(test_file):
        result = analyzer.analyze_resume_file(test_file)
        print("Результат анализа резюме:")
        for key, value in result.items():
            print(f"{key}: {value}")
