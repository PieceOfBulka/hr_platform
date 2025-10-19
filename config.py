"""
Конфигурационный файл для системы рекомендаций
Содержит токены и настройки для внешних сервисов
"""

import os
from decouple import config

# Hugging Face API токен для доступа к Gemma модели
HUGGINGFACE_API_TOKEN = config('HUGGINGFACE_API_TOKEN', default='your-huggingface-token-here')

# Настройки базы данных
DATABASE_CONFIG = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': config('DB_NAME', default='hr_platform'),
    'USER': config('DB_USER', default='postgres'),
    'PASSWORD': config('DB_PASSWORD', default='your-db-password'),
    'HOST': config('DB_HOST', default='localhost'),
    'PORT': config('DB_PORT', default='5432'),
}

# Настройки для локальной Gemma модели
GEMMA_CONFIG = {
    'MODEL_NAME': 'google/gemma-2-2b-it',
    'MAX_TOKENS': 256,
    'TEMPERATURE': 0.7,
    'DEVICE': 'auto',  # auto, cuda, cpu
    'TORCH_DTYPE': 'bfloat16',
}

# Настройки рекомендаций
RECOMMENDATION_CONFIG = {
    'MIN_SCORE_THRESHOLD': 0.3,
    'MAX_RECOMMENDATIONS': 10,
    'CACHE_DURATION_HOURS': 24,
    'ENABLE_LLM_ANALYSIS': True,
}
