#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ai_recommendation_engine import AIRecommendationEngine
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка базы данных
DATABASE_URL = "sqlite:///./hr_platform_from_sql.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(title="AI-Enhanced HR Platform", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic модели
class AIRecommendationResponse(BaseModel):
    vacancy_id: int
    vacancy_title: str
    company_name: str
    score: float
    ai_analysis: dict
    personalized_reason: str
    skill_match: float
    experience_match: float
    text_similarity: float
    freshness_score: float

class ResumeCreate(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    summary: Optional[str] = None
    specialty: Optional[str] = None
    skill_ids: List[int] = []

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Получаем токен Hugging Face
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "ваш токен")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Главная страница с AI-улучшенным интерфейсом"""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI HR Platform - Smart Recommendations</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 40px; 
                text-align: center;
            }
            .header h1 { 
                margin: 0; 
                font-size: 2.5em; 
                font-weight: 300;
            }
            .header p { 
                margin: 10px 0 0 0; 
                font-size: 1.2em; 
                opacity: 0.9;
            }
            .ai-badge {
                display: inline-block;
                background: rgba(255,255,255,0.2);
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 0.9em;
                margin-top: 15px;
            }
            .search-form { 
                padding: 40px; 
                background: #f8f9fa;
            }
            .form-group { 
                margin-bottom: 25px; 
            }
            label { 
                display: block; 
                margin-bottom: 8px; 
                font-weight: 600; 
                color: #333;
            }
            input, select, textarea { 
                width: 100%; 
                padding: 15px; 
                border: 2px solid #e1e5e9; 
                border-radius: 10px; 
                font-size: 16px;
                transition: border-color 0.3s;
            }
            input:focus, select:focus, textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            button { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 10px; 
                cursor: pointer; 
                font-size: 16px; 
                font-weight: 600;
                transition: transform 0.2s;
            }
            button:hover { 
                transform: translateY(-2px);
            }
            .recommendations { 
                display: grid; 
                gap: 25px; 
                padding: 40px;
            }
            .recommendation-card { 
                background: white; 
                padding: 30px; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                border-left: 5px solid #667eea;
                transition: transform 0.2s;
            }
            .recommendation-card:hover {
                transform: translateY(-5px);
            }
            .score { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 8px 16px; 
                border-radius: 20px; 
                font-size: 14px; 
                display: inline-block; 
                margin-bottom: 15px; 
                font-weight: 600;
            }
            .company { 
                color: #666; 
                font-size: 14px; 
                margin-bottom: 15px; 
                font-weight: 500;
            }
            .ai-analysis {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin: 15px 0;
            }
            .ai-analysis h4 {
                margin: 0 0 10px 0;
                color: #667eea;
            }
            .strengths, .concerns {
                margin: 10px 0;
            }
            .strengths ul, .concerns ul {
                margin: 5px 0;
                padding-left: 20px;
            }
            .strengths li {
                color: #28a745;
            }
            .concerns li {
                color: #dc3545;
            }
            .reason { 
                color: #555; 
                font-style: italic; 
                margin-top: 15px; 
                line-height: 1.6;
            }
            .loading { 
                text-align: center; 
                padding: 60px; 
                color: #666; 
                font-size: 18px;
            }
            .error { 
                background: #ffebee; 
                color: #c62828; 
                padding: 20px; 
                border-radius: 10px; 
                margin: 20px 0; 
                border-left: 4px solid #c62828;
            }
            .ai-powered {
                background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
                color: white;
                padding: 5px 12px;
                border-radius: 15px;
                font-size: 12px;
                font-weight: 600;
                margin-left: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>AI HR Platform</h1>
                <p>Smart job recommendations using AI</p>
                <div class="ai-badge">
                    Powered by Gemma 3 AI Model
                </div>
            </div>
            
            <div class="search-form">
                <h2>Get AI Recommendations</h2>
                <form id="recommendationForm">
                    <div class="form-group">
                        <label for="resumeId">ID резюме:</label>
                        <input type="number" id="resumeId" name="resumeId" placeholder="Введите ID вашего резюме" required>
                    </div>
                    <button type="submit">
                        Get AI Recommendations
                    </button>
                </form>
            </div>
            
            <div id="results"></div>
        </div>
        
        <script>
            document.getElementById('recommendationForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const resumeId = document.getElementById('resumeId').value;
                const resultsDiv = document.getElementById('results');
                
                resultsDiv.innerHTML = '<div class="loading">AI is analyzing your data...<br><small>This may take a few seconds</small></div>';
                
                try {
                    const response = await fetch(`/api/ai-recommendations/resume/${resumeId}`);
                    const data = await response.json();
                    
                    if (data.length === 0) {
                        resultsDiv.innerHTML = '<div class="error">AI found no suitable recommendations. Try a different resume ID.</div>';
                        return;
                    }
                    
                    let html = '<div class="recommendations">';
                    data.forEach(rec => {
                        const aiAnalysis = rec.ai_analysis || {};
                        const strengths = aiAnalysis.strengths || [];
                        const concerns = aiAnalysis.concerns || [];
                        
                        html += `
                            <div class="recommendation-card">
                                <div class="score">
                                    AI Совместимость: ${Math.round(rec.score * 100)}%
                                    <span class="ai-powered">AI</span>
                                </div>
                                <h3>${rec.vacancy_title}</h3>
                                <div class="company">Company: ${rec.company_name}</div>
                                
                                <div class="ai-analysis">
                                    <h4>AI Analysis</h4>
                                    <div class="strengths">
                                        <strong>Strengths:</strong>
                                        <ul>
                                            ${strengths.map(s => `<li>${s}</li>`).join('')}
                                        </ul>
                                    </div>
                                    ${concerns.length > 0 ? `
                                    <div class="concerns">
                                        <strong>Areas for Development:</strong>
                                        <ul>
                                            ${concerns.map(c => `<li>${c}</li>`).join('')}
                                        </ul>
                                    </div>
                                    ` : ''}
                                </div>
                                
                                <div class="reason">
                                    <strong>Personalized Recommendation:</strong><br>
                                    ${rec.personalized_reason}
                                </div>
                            </div>
                        `;
                    });
                    html += '</div>';
                    resultsDiv.innerHTML = html;
                } catch (error) {
                    resultsDiv.innerHTML = '<div class="error">Error loading AI recommendations</div>';
                }
            });
        </script>
    </body>
    </html>
    """

@app.get("/api/ai-recommendations/resume/{resume_id}", response_model=List[AIRecommendationResponse])
async def get_ai_recommendations_for_resume(resume_id: int, db: Session = Depends(get_db)):
    """Получить AI-улучшенные рекомендации для резюме"""
    try:
        engine = AIRecommendationEngine(db, HF_TOKEN)
        recommendations = engine.get_ai_recommendations_for_resume(resume_id)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Проверка работоспособности системы"""
    return {
        "status": "healthy",
        "ai_model": "google/gemma-3-1b-it",
        "database": "sqlite",
        "version": "2.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting AI-enhanced HR platform...")
    print(f"AI Model: google/gemma-3-1b-it")
    print(f"HF Token: {'Configured' if HF_TOKEN else 'Not configured'}")
    print("Server: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
