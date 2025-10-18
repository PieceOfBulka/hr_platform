# Руководство по использованию стилистики Technopolis

## Цветовая палитра

### Основные акцентные цвета (RAL)
- `--accent-1: #d63344` - Основной красный (RAL 3026)
- `--accent-2: #8f453d` - Коричневый (RAL 3000) 
- `--accent-3: #c68487` - Розовый (RAL 3014)
- `--accent-4: #8a4b4b` - Темно-красный (RAL 3027)
- `--accent-5: #4b2624` - Очень темный коричневый (RAL 3032)
- `--accent-6: #2a1c1b` - Черно-коричневый (RAL 3007)

### Нейтральные цвета
- `--neutral-1: #9fa1a3` - Серый (RAL 7004)
- `--neutral-2: #3f3f3f` - Темно-серый (RAL 7022)
- `--neutral-3: #3a3f44` - Очень темно-серый (RAL 7024)
- `--neutral-4: #b9b9b6` - Светло-серый (RAL 9018)
- `--neutral-5: #e6e5dd` - Кремовый (RAL 9002)
- `--neutral-6: #fbfdf4` - Белый (RAL 9010)

## Основные компоненты

### Кнопки
```html
<!-- Основная кнопка -->
<button class="btn btn-primary">Основная кнопка</button>

<!-- Контурная кнопка -->
<button class="btn btn-outline">Контурная кнопка</button>

<!-- Опасная кнопка -->
<button class="btn btn-danger">Опасная кнопка</button>
```

### Карточки
```html
<!-- Базовая карточка -->
<div class="card">
  <div class="card-body">
    <h5 class="card-title">Заголовок</h5>
    <p class="card-text">Содержимое карточки</p>
  </div>
</div>

<!-- Карточка вакансии -->
<div class="vacancy-card">
  <div class="vacancy-header">
    <div class="vacancy-icon">
      <i class="fas fa-briefcase"></i>
    </div>
    <div class="vacancy-info">
      <h5 class="vacancy-title">Название вакансии</h5>
      <div class="vacancy-company">Название компании</div>
    </div>
  </div>
  <div class="vacancy-badges">
    <span class="badge bg-primary">Полная занятость</span>
  </div>
  <p class="vacancy-description">Описание вакансии</p>
  <button class="btn btn-primary vacancy-apply-btn">Откликнуться</button>
</div>
```

### Теги и бейджи
```html
<!-- Тег -->
<span class="tag">Тег</span>

<!-- Бейдж -->
<span class="badge bg-primary">Бейдж</span>
```

### Формы
```html
<div class="form-group">
  <label for="input">Метка</label>
  <input type="text" class="form-control" id="input" placeholder="Плейсхолдер">
</div>
```

### Статистика
```html
<div class="stats-card">
  <div class="stats-icon bg-gradient-primary">
    <i class="fas fa-users"></i>
  </div>
  <div class="stats-content">
    <div class="stats-number">100</div>
    <div class="stats-label">Пользователей</div>
  </div>
</div>
```

### Навигация
```html
<nav class="navbar navbar-expand-lg navbar-light bg-white">
  <div class="container">
    <a class="navbar-brand fw-bold" href="/">
      <span class="text-danger">HR</span> Платформа
    </a>
    <div class="navbar-nav">
      <a class="nav-link" href="/vacancies">Вакансии</a>
      <a class="nav-link" href="/internships">Стажировки</a>
    </div>
  </div>
</nav>
```

## Специальные компоненты

### Дашборд
```html
<div class="dashboard-card">
  <h4>Заголовок секции</h4>
  <p>Содержимое дашборда</p>
</div>
```

### Модерация
```html
<div class="moderation-card pending">
  <h5>Элемент на модерации</h5>
  <p>Описание</p>
  <div class="moderation-actions">
    <button class="btn btn-primary">Одобрить</button>
    <button class="btn btn-danger">Отклонить</button>
  </div>
</div>
```

### Резюме
```html
<div class="resume-card">
  <div class="resume-header">
    <div class="resume-avatar">ИИ</div>
    <div class="resume-info">
      <h5>Иван Иванов</h5>
      <p>Frontend разработчик</p>
    </div>
  </div>
  <div class="resume-skills">
    <span class="skill-tag">JavaScript</span>
    <span class="skill-tag">React</span>
  </div>
</div>
```

## Адаптивность

Стили автоматически адаптируются под разные размеры экранов:

- **Desktop** (>768px): Полная функциональность
- **Tablet** (768px): Адаптированная сетка
- **Mobile** (<576px): Компактный дизайн

## Анимации

### Появление
```html
<div class="fade-in">Элемент с анимацией появления</div>
<div class="slide-in-up">Элемент с анимацией снизу вверх</div>
```

### Плавающие элементы
```html
<div class="floating-icon" style="top: 20%; left: 10%;">
  <i class="fas fa-code"></i>
</div>
```

## Утилиты

### Цвета
```html
<span class="text-accent-1">Текст основного цвета</span>
<div class="bg-accent-1">Фон основного цвета</div>
<div class="border-accent-1">Рамка основного цвета</div>
```

### Загрузка
```html
<div class="loading-spinner"></div>
```

### Прогресс
```html
<div class="progress-modern">
  <div class="progress-bar" style="width: 50%"></div>
</div>
```

## Темная тема

Система автоматически поддерживает темную тему через `prefers-color-scheme: dark`.

## Примеры использования

### Главная страница
```html
<section class="hero-section-modern">
  <div class="hero-background">
    <div class="hero-grid"></div>
  </div>
  <div class="container">
    <div class="row align-items-center min-vh-50">
      <div class="col-lg-8 mx-auto text-center text-white">
        <h1 class="display-3 fw-bold mb-4">
          Заголовок
          <span class="hero-gradient-text">с градиентом</span>
        </h1>
      </div>
    </div>
  </div>
</section>
```

### Секция функций
```html
<section class="features-section py-5">
  <div class="container">
    <div class="row g-4">
      <div class="col-lg-4">
        <div class="feature-card">
          <div class="feature-icon">
            <i class="fas fa-shield-alt"></i>
          </div>
          <h4 class="feature-title">Заголовок функции</h4>
          <p class="feature-description">Описание функции</p>
        </div>
      </div>
    </div>
  </div>
</section>
```

Эта стилистика обеспечивает единообразный и профессиональный внешний вид всей HR платформы в стиле Technopolis.
