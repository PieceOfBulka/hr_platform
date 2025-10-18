# Руководство по корпоративному стилю ОЭЗ "Технополис Москва"

## Корпоративная цветовая палитра

### Основные цвета
- **Основной синий**: `#0066cc` - Основной корпоративный цвет
- **Темно-синий**: `#004499` - Для заголовков и акцентов
- **Светло-синий**: `#3399ff` - Для hover-эффектов и градиентов
- **Корпоративный красный**: `#cc0000` - Для важных действий и предупреждений
- **Корпоративный зеленый**: `#00cc66` - Для успешных операций
- **Корпоративный оранжевый**: `#ff6600` - Для предупреждений

### Нейтральные цвета
- **Очень темный**: `#1a1a1a` - Основной текст
- **Темно-серый**: `#333333` - Вторичный текст
- **Средне-серый**: `#666666` - Приглушенный текст
- **Светло-серый**: `#999999` - Неактивные элементы
- **Бледно-серый**: `#cccccc` - Границы
- **Белый**: `#ffffff` - Фон карточек
- **Фоновый**: `#f8f9fa` - Основной фон

## Корпоративные компоненты

### Логотип и брендинг
```html
<!-- Основной логотип -->
<div class="technopolis-brand">
    <div class="technopolis-logo">
        <span class="text-primary">ОЭЗ</span> Технополис Москва
    </div>
</div>

<!-- Корпоративный бейдж -->
<span class="technopolis-badge">Официальная платформа</span>
```

### Корпоративные кнопки
```html
<!-- Основная корпоративная кнопка -->
<button class="btn-corporate">Действие</button>

<!-- Контурная корпоративная кнопка -->
<button class="btn-corporate-outline">Действие</button>

<!-- Стандартные кнопки с корпоративными цветами -->
<button class="btn btn-primary">Основная</button>
<button class="btn btn-danger">Опасная</button>
<button class="btn btn-success">Успех</button>
```

### Корпоративные карточки
```html
<!-- Стандартная корпоративная карточка -->
<div class="corporate-card">
    <h3>Заголовок карточки</h3>
    <p>Содержимое карточки</p>
</div>

<!-- Карточка с иконкой -->
<div class="corporate-card">
    <div class="corporate-icon">
        <i class="fas fa-users"></i>
    </div>
    <h3>Заголовок</h3>
    <p>Описание</p>
</div>
```

### Корпоративная статистика
```html
<div class="corporate-stats">
    <div class="corporate-stats-number">150</div>
    <div class="corporate-stats-label">Активных вакансий</div>
</div>
```

### Корпоративные бейджи
```html
<span class="corporate-badge">Основной</span>
<span class="corporate-badge corporate-badge-success">Успех</span>
<span class="corporate-badge corporate-badge-warning">Предупреждение</span>
<span class="corporate-badge corporate-badge-danger">Ошибка</span>
```

### Корпоративные формы
```html
<div class="corporate-form">
    <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" class="form-control" id="email">
    </div>
    <button class="btn-corporate">Отправить</button>
</div>
```

### Корпоративные таблицы
```html
<div class="corporate-table">
    <table class="table">
        <thead>
            <tr>
                <th>Заголовок 1</th>
                <th>Заголовок 2</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Данные 1</td>
                <td>Данные 2</td>
            </tr>
        </tbody>
    </table>
</div>
```

### Корпоративные уведомления
```html
<div class="corporate-alert corporate-alert-primary">
    Информационное сообщение
</div>

<div class="corporate-alert corporate-alert-success">
    Успешное выполнение
</div>

<div class="corporate-alert corporate-alert-warning">
    Предупреждение
</div>

<div class="corporate-alert corporate-alert-danger">
    Ошибка
</div>
```

## Корпоративные секции

### Секция с корпоративным заголовком
```html
<section class="corporate-section corporate-section-light">
    <div class="container">
        <div class="corporate-header">
            <h1>Заголовок секции</h1>
            <p>Описание секции</p>
        </div>
    </div>
</section>
```

### Темная корпоративная секция
```html
<section class="corporate-section corporate-section-dark">
    <div class="container">
        <h2>Заголовок</h2>
        <p>Содержимое секции</p>
    </div>
</section>
```

## Корпоративные утилиты

### Цвета текста
```html
<span class="text-corporate-primary">Основной синий</span>
<span class="text-corporate-secondary">Темно-синий</span>
<span class="text-corporate-accent">Светло-синий</span>
<span class="text-corporate-red">Красный</span>
<span class="text-corporate-green">Зеленый</span>
<span class="text-corporate-orange">Оранжевый</span>
```

### Фоны
```html
<div class="bg-corporate-primary">Синий фон</div>
<div class="bg-corporate-secondary">Темно-синий фон</div>
<div class="bg-corporate-accent">Светло-синий фон</div>
```

### Границы
```html
<div class="border border-corporate-primary">Синяя граница</div>
<div class="border border-corporate-secondary">Темно-синяя граница</div>
<div class="border border-corporate-accent">Светло-синяя граница</div>
```

### Градиенты
```html
<div class="gradient-corporate-primary">Основной градиент</div>
<div class="gradient-corporate-accent">Акцентный градиент</div>
<div class="gradient-corporate-hero">Герой градиент</div>
```

### Тени
```html
<div class="shadow-corporate">Корпоративная тень</div>
<div class="shadow-corporate-lg">Большая корпоративная тень</div>
```

## Корпоративные анимации

### Анимация пульсации
```html
<div class="corporate-pulse">Пульсирующий элемент</div>
```

### Анимация появления
```html
<div class="corporate-slide-in">Появляющийся элемент</div>
```

## Примеры использования

### Главная страница с корпоративным дизайном
```html
<section class="hero-section-modern corporate-gradient">
    <div class="container">
        <div class="row align-items-center min-vh-50">
            <div class="col-lg-8 mx-auto text-center text-white">
                <div class="hero-badge mb-4">
                    <div class="technopolis-logo mb-3">
                        <h2 class="text-white fw-bold mb-0">ОЭЗ "ТЕХНОПОЛИС МОСКВА"</h2>
                        <div class="logo-subtitle text-white-50">Официальная HR платформа</div>
                    </div>
                    <span class="technopolis-badge">
                        <i class="fas fa-star me-2"></i>Платформа для карьеры в IT
                    </span>
                </div>
            </div>
        </div>
    </div>
</section>
```

### Секция функций
```html
<section class="corporate-section corporate-section-light">
    <div class="container">
        <div class="row g-4">
            <div class="col-lg-4">
                <div class="corporate-card">
                    <div class="corporate-icon">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <h3>Проверенные компании</h3>
                    <p>Все вакансии проходят модерацию администрации ОЭЗ</p>
                </div>
            </div>
        </div>
    </div>
</section>
```

### Статистика
```html
<section class="corporate-section">
    <div class="container">
        <div class="row g-4">
            <div class="col-lg-3">
                <div class="corporate-stats">
                    <div class="corporate-stats-number">50+</div>
                    <div class="corporate-stats-label">Компаний-резидентов</div>
                </div>
            </div>
        </div>
    </div>
</section>
```

## Принципы использования

1. **Консистентность**: Используйте корпоративные цвета везде, где это возможно
2. **Иерархия**: Основной синий для важных элементов, красный для критических действий
3. **Доступность**: Обеспечивайте достаточный контраст для читаемости
4. **Брендинг**: Всегда указывайте принадлежность к ОЭЗ "Технополис Москва"
5. **Профессионализм**: Используйте современные градиенты и тени для премиального вида

Этот корпоративный стиль обеспечивает единообразный и профессиональный внешний вид всей HR платформы, соответствующий стандартам ОЭЗ "Технополис Москва".
