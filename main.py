from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, create_tables, User, Resume, Vacancy, Company, ListOfSkills, Recommendation
from recommendation_engine import RecommendationEngine
from ai_recommendation_engine import AIRecommendationEngine, create_ai_recommendation_engine
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Создаем таблицы
create_tables()

app = FastAPI(title="HR Platform Recommendation System", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Статические файлы и шаблоны (не нужны для простого HTML)
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# Pydantic модели для API
class RecommendationResponse(BaseModel):
    vacancy_id: int
    vacancy_title: str
    company_name: str
    score: float
    reason: str
    skill_score: float
    experience_score: float
    text_score: float
    specialty_score: float
    freshness_score: float

class ResumeCreate(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    summary: Optional[str] = None
    specialty: Optional[str] = None
    skill_ids: List[int] = []

class VacancyResponse(BaseModel):
    id: int
    title: str
    company_name: str
    description: str
    requirements: str
    status: str
    created_at: str

# API endpoints
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Главная страница с интерфейсом рекомендаций"""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HR Platform - Рекомендации</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; }
            .search-form { background: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            button { background: #667eea; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            button:hover { background: #5a6fd8; }
            .recommendations { display: grid; gap: 20px; }
            .recommendation-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-left: 4px solid #667eea; }
            .score { background: #667eea; color: white; padding: 5px 10px; border-radius: 15px; font-size: 14px; display: inline-block; margin-bottom: 10px; }
            .company { color: #666; font-size: 14px; margin-bottom: 10px; }
            .reason { color: #555; font-style: italic; margin-top: 10px; }
            .loading { text-align: center; padding: 40px; color: #666; }
            .error { background: #ffebee; color: #c62828; padding: 15px; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎯 HR Platform - Система рекомендаций</h1>
                <p>Найдите идеальную работу на основе ваших навыков и опыта</p>
            </div>
            
            <div class="search-form">
                <h2>Получить рекомендации</h2>
                <form id="recommendationForm">
                    <div class="form-group">
                        <label for="resumeId">ID резюме:</label>
                        <input type="number" id="resumeId" name="resumeId" placeholder="Введите ID вашего резюме" required>
                    </div>
                    <div class="form-group">
                        <label>
                            <input type="checkbox" id="useAI" checked> Использовать AI рекомендации (Hugging Face)
                        </label>
                    </div>
                    <button type="submit">Получить рекомендации</button>
                </form>
            </div>
            
            <div id="results"></div>
        </div>
        
        <script>
            document.getElementById('recommendationForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const resumeId = document.getElementById('resumeId').value;
                const useAI = document.getElementById('useAI').checked;
                const resultsDiv = document.getElementById('results');
                
                resultsDiv.innerHTML = '<div class="loading">Загрузка рекомендаций...</div>';
                
                try {
                    const endpoint = useAI ? `/api/ai/recommendations/resume/${resumeId}` : `/api/recommendations/resume/${resumeId}`;
                    const response = await fetch(endpoint);
                    const data = await response.json();
                    
                    if (data.length === 0) {
                        resultsDiv.innerHTML = '<div class="error">Рекомендации не найдены. Попробуйте другой ID резюме.</div>';
                        return;
                    }
                    
                    let html = '<div class="recommendations">';
                    if (useAI) {
                        html += '<div style="background: #e3f2fd; padding: 10px; border-radius: 5px; margin-bottom: 20px; color: #1976d2;">🤖 AI рекомендации с использованием Hugging Face</div>';
                    }
                    
                    data.forEach(rec => {
                        const scoreColor = rec.score > 0.7 ? '#4caf50' : rec.score > 0.5 ? '#ff9800' : '#f44336';
                        html += `
                            <div class="recommendation-card">
                                <div class="score" style="background: ${scoreColor}">Совместимость: ${Math.round(rec.score * 100)}%</div>
                                <h3>${rec.vacancy_title}</h3>
                                <div class="company">${rec.company_name}</div>
                                <div class="reason">${rec.reason}</div>
                                ${useAI ? `
                                    <div style="margin-top: 10px; font-size: 12px; color: #666;">
                                        <div>Навыки: ${Math.round(rec.skill_score * 100)}% | 
                                             Текст: ${Math.round(rec.text_score * 100)}% | 
                                             Специализация: ${Math.round(rec.specialty_score * 100)}% | 
                                             Свежесть: ${Math.round(rec.freshness_score * 100)}%</div>
                                    </div>
                                ` : ''}
                            </div>
                        `;
                    });
                    html += '</div>';
                    resultsDiv.innerHTML = html;
                } catch (error) {
                    resultsDiv.innerHTML = '<div class="error">Ошибка при загрузке рекомендаций: ' + error.message + '</div>';
                }
            });
        </script>
    </body>
    </html>
    """

@app.get("/api/recommendations/resume/{resume_id}", response_model=List[RecommendationResponse])
async def get_recommendations_for_resume(resume_id: int, db: Session = Depends(get_db)):
    """Получить рекомендации для конкретного резюме"""
    try:
        engine = RecommendationEngine(db)
        recommendations = engine.get_recommendations_for_resume(resume_id)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ai/recommendations/resume/{resume_id}", response_model=List[RecommendationResponse])
async def get_ai_recommendations_for_resume(resume_id: int, db: Session = Depends(get_db)):
    """Получить AI рекомендации для конкретного резюме"""
    try:
        # Получаем токен Hugging Face из переменных окружения
        huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
        
        engine = create_ai_recommendation_engine(db, huggingface_token)
        recommendations = engine.get_recommendations_for_resume(resume_id)
        
        # Конвертируем в формат API
        api_recommendations = []
        for rec in recommendations:
            api_recommendations.append(RecommendationResponse(
                vacancy_id=rec.vacancy_id,
                vacancy_title=rec.vacancy_title,
                company_name=rec.company_name,
                score=rec.score,
                reason=rec.reason,
                skill_score=rec.skill_score,
                experience_score=rec.experience_score,
                text_score=rec.text_score,
                specialty_score=rec.specialty_score,
                freshness_score=rec.freshness_score
            ))
        
        return api_recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recommendations/user/{user_id}", response_model=List[RecommendationResponse])
async def get_recommendations_for_user(user_id: int, db: Session = Depends(get_db)):
    """Получить рекомендации для пользователя"""
    try:
        engine = RecommendationEngine(db)
        recommendations = engine.get_recommendations_for_user(user_id)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ai/recommendations/user/{user_id}", response_model=List[RecommendationResponse])
async def get_ai_recommendations_for_user(user_id: int, db: Session = Depends(get_db)):
    """Получить AI рекомендации для пользователя"""
    try:
        huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
        
        engine = create_ai_recommendation_engine(db, huggingface_token)
        recommendations = engine.get_recommendations_for_user(user_id)
        
        # Конвертируем в формат API
        api_recommendations = []
        for rec in recommendations:
            api_recommendations.append(RecommendationResponse(
                vacancy_id=rec.vacancy_id,
                vacancy_title=rec.vacancy_title,
                company_name=rec.company_name,
                score=rec.score,
                reason=rec.reason,
                skill_score=rec.skill_score,
                experience_score=rec.experience_score,
                text_score=rec.text_score,
                specialty_score=rec.specialty_score,
                freshness_score=rec.freshness_score
            ))
        
        return api_recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vacancies", response_model=List[VacancyResponse])
async def get_vacancies(db: Session = Depends(get_db)):
    """Получить список всех активных вакансий"""
    vacancies = db.query(Vacancy).filter(Vacancy.status == "published").all()
    return [
        VacancyResponse(
            id=vacancy.id,
            title=vacancy.title,
            company_name=vacancy.company.name if vacancy.company else "Неизвестная компания",
            description=vacancy.description or "",
            requirements=vacancy.requirements or "",
            status=vacancy.status,
            created_at=vacancy.created_at.isoformat()
        )
        for vacancy in vacancies
    ]

@app.get("/api/skills")
async def get_skills(db: Session = Depends(get_db)):
    """Получить список всех навыков"""
    skills = db.query(ListOfSkills).all()
    return [{"id": skill.id, "name": skill.name, "category": skill.category} for skill in skills]

@app.post("/api/resumes")
async def create_resume(resume: ResumeCreate, db: Session = Depends(get_db)):
    """Создать новое резюме"""
    try:
        # Создаем пользователя-соискателя
        user = User(
            email=resume.email,
            password_hash="dummy_hash",  # В реальном приложении нужно хешировать пароль
            role="applicant",
            name_of_place=resume.full_name
        )
        db.add(user)
        db.flush()  # Получаем ID пользователя
        
        # Создаем резюме
        new_resume = Resume(
            full_name=resume.full_name,
            email=resume.email,
            phone=resume.phone,
            summary=resume.summary,
            specialty=resume.specialty,
            user_id=user.id
        )
        db.add(new_resume)
        db.flush()
        
        # Добавляем навыки
        if resume.skill_ids:
            skills = db.query(ListOfSkills).filter(ListOfSkills.id.in_(resume.skill_ids)).all()
            new_resume.skills = skills
        
        db.commit()
        
        return {"message": "Резюме создано", "resume_id": new_resume.id, "user_id": user.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recommendations/stats/{resume_id}")
async def get_recommendation_stats(resume_id: int, db: Session = Depends(get_db)):
    """Получить статистику рекомендаций для резюме"""
    recommendations = db.query(Recommendation).filter(Recommendation.resume_id == resume_id).all()
    
    if not recommendations:
        return {"message": "Рекомендации не найдены"}
    
    avg_score = sum(rec.score for rec in recommendations) / len(recommendations)
    max_score = max(rec.score for rec in recommendations)
    min_score = min(rec.score for rec in recommendations)
    
    return {
        "total_recommendations": len(recommendations),
        "average_score": round(avg_score, 3),
        "max_score": round(max_score, 3),
        "min_score": round(min_score, 3)
    }

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)
