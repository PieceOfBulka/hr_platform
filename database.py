from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, Table, Enum, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.dialects.postgresql import UUID as PostgresUUID  # Не нужен для SQLite
from datetime import datetime
import os
import enum

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hr_platform.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enums
class UserRole(str, enum.Enum):
    HR = "hr"
    UNIVERSITY_REP = "university_rep"
    ADMIN = "admin"
    APPLICANT = "applicant"

class VacancyStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING_MODERATION = "pending_moderation"
    PUBLISHED = "published"
    CLOSED = "closed"
    EXPIRED = "expired"

class ApplicationStatus(str, enum.Enum):
    NEW = "new"
    VIEWED = "viewed"
    INVITED = "invited"
    REJECTED = "rejected"

class InternshipStatus(str, enum.Enum):
    PENDING_MODERATION = "pending_moderation"
    PUBLISHED = "published"
    REJECTED = "rejected"

class ModerationStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class ItemType(str, enum.Enum):
    VACANCY = "vacancy"
    INTERNSHIP_REQUEST = "internship_request"

class SkillCategory(str, enum.Enum):
    TECHNICAL = "technical"
    SOFT = "soft"
    LANGUAGE = "language"
    DOMAIN = "domain"

# Связующая таблица для навыки вакансий
vacancy_skills = Table(
    'vacancy_skills',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('vacancy_id', Integer, ForeignKey('vacancies.id')),
    Column('skill_id', Integer, ForeignKey('list_of_skills.id')),
    Column('is_required', Boolean, default=False),
    Column('priority', Integer, default=1)
)

# Связующая таблица для навыки резюме
resume_skills = Table(
    'resume_skills',
    Base.metadata,
    Column('resume_id', Integer, ForeignKey('resumes.id')),
    Column('skill_id', Integer, ForeignKey('list_of_skills.id'))
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    name_of_place = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_verified = Column(Boolean, default=False)

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    contact_person = Column(String(255))
    contact_email = Column(String(255))
    contact_phone = Column(String(50))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Связи
    user = relationship("User")
    vacancies = relationship("Vacancy", back_populates="company")

class Vacancy(Base):
    __tablename__ = "vacancies"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    requirements = Column(Text)
    contact_info = Column(Text)
    status = Column(String(50), default="draft")
    publish_until = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    published_at = Column(DateTime)
    
    # Связи
    company = relationship("Company", back_populates="vacancies")
    skills = relationship("ListOfSkills", secondary=vacancy_skills, backref="vacancies")
    applications = relationship("Application", back_populates="vacancy")

class ListOfSkills(Base):
    __tablename__ = "list_of_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    category = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class InternshipRequest(Base):
    __tablename__ = "internship_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    university_name = Column(String(255), nullable=False)
    specialty = Column(String(255))
    student_count = Column(Integer)
    period_start = Column(Date)
    period_end = Column(Date)
    status = Column(String(50), default="pending_moderation")
    created_at = Column(DateTime, default=datetime.utcnow)
    published_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Связи
    user = relationship("User")

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    resume_file_url = Column(String(500))
    summary = Column(Text)
    specialty = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Связи
    user = relationship("User")
    skills = relationship("ListOfSkills", secondary=resume_skills, backref="resumes")
    applications = relationship("Application", back_populates="resume")

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    vacancy_id = Column(Integer, ForeignKey("vacancies.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    status = Column(String(50), default="new")
    applied_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    vacancy = relationship("Vacancy", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")

class ModerationQueue(Base):
    __tablename__ = "moderation_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    item_type = Column(String(50), nullable=False)
    item_id = Column(Integer, nullable=False)
    moderator_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(50), default="pending")
    comment = Column(Text)
    reviewed_at = Column(DateTime)
    
    # Связи
    moderator = relationship("User")

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    vacancy_id = Column(Integer, ForeignKey("vacancies.id"))
    score = Column(Float, nullable=False)  # Оценка совместимости от 0 до 1
    reason = Column(Text)  # Объяснение рекомендации
    created_at = Column(DateTime, default=datetime.utcnow)
    is_viewed = Column(Boolean, default=False)
    
    # Связи
    resume = relationship("Resume")
    vacancy = relationship("Vacancy")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)