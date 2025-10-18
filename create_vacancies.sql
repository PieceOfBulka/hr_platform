CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- включание расширение для uuid

-- Таблица вакансий
CREATE TABLE vacancies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    requirements TEXT,
    contact_info TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'draft'
        CHECK (status IN ('draft', 'pending_moderation', 'published', 'closed', 'expired')),
    publish_until TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    published_at TIMESTAMPTZ,

    -- Внешний ключ на таблицу компаний (предполагается, что она существует)
    CONSTRAINT fk_company
        FOREIGN KEY (company_id)
        REFERENCES companies(id)
        ON DELETE CASCADE
);

WITH inserted_vacancies AS (
    INSERT INTO vacancies (company_id, title, description, requirements, contact_info)
    SELECT
        c.id,
        v.title,
        v.description,
        v.requirements,
        v.contact_info
    FROM companies c
    INNER JOIN (
        VALUES
        -- 1. Нанотехнологический центр композитов
        ('Нанотехнологический центр композитов', 'Инженер-материаловед', 'Разработка композитов для аэрокосмической отрасли.', 'Опыт с полимерами, знание ГОСТ, CAD.', 'hr@nanocomposite.ru'),
        ('Нанотехнологический центр композитов', 'Технолог производства', 'Оптимизация процессов изготовления композитов.', 'Опыт на производстве, AutoCAD.', 'hr@nanocomposite.ru'),
        -- 2. Медплант
        ('Медплант', 'Инженер по медицинским изделиям', 'Разработка имплантов.', 'Знание ISO 13485, опыт в медтехнике.', 'hr@medplant.ru'),
        ('Медплант', 'Биоматериаловед', 'Исследование биосовместимости.', 'Высшее образование в биоматериалах.', 'hr@medplant.ru'),
        -- 3. Сенсор
        ('Сенсор', 'Инженер по разработке сенсоров', 'Проектирование MEMS-сенсоров.', 'SolidWorks, Embedded Systems, C++.', 'hr@sensor-tech.ru'),
        ('Сенсор', 'Программист встраиваемых систем', 'ПО для микроконтроллеров.', 'C, RTOS, датчики.', 'hr@sensor-tech.ru'),
        -- 4. ИНКОРО
        ('ИНКОРО', 'Инженер-схемотехник', 'Разработка аналоговых схем.', 'Altium Designer, VHDL.', 'hr@inkoro.ru'),
        ('ИНКОРО', 'FPGA-разработчик', 'Логика на ПЛИС.', 'Verilog, Xilinx.', 'hr@inkoro.ru'),
        -- 5. Тест-Контакт
        ('Тест-Контакт', 'Инженер-диагност', 'Разработка диагностических систем.', 'LabVIEW, медицинское оборудование.', 'hr@test-contact.ru'),
        ('Тест-Контакт', 'Тестировщик ПО', 'Тестирование ПО для лабораторий.', 'Manual Testing, знание стандартов.', 'hr@test-contact.ru'),
        -- 6. ПК Экопласт
        ('ПК Экопласт', 'Технолог-полимерщик', 'Разработка рецептур полимеров.', 'Химическое образование, опыт с полимерами.', 'hr@ecoplast.ru'),
        ('ПК Экопласт', 'Инженер по переработке', 'Оптимизация переработки вторсырья.', 'Знание оборудования, опыт на производстве.', 'hr@ecoplast.ru'),
        -- 7. Акрус БиоМед
        ('Акрус БиоМед', 'Биоинформатик', 'Анализ геномных данных.', 'Python, NGS, Pandas.', 'hr@akrusbiomed.ru'),
        ('Акрус БиоМед', 'Клинический исследователь', 'Организация клинических испытаний.', 'GCP, опыт в фарме.', 'hr@akrusbiomed.ru'),
        -- 8. Концерн Гудвин
        ('Концерн Гудвин (Гудвин Европа)', 'Инженер-робототехник', 'Разработка промышленных роботов.', 'ROS, C++, Python, Robotics.', 'hr@goodwin-europe.ru'),
        ('Концерн Гудвин (Гудвин Европа)', 'Программист PLC', 'Логика управления автоматизированными линиями.', 'Siemens TIA Portal, PLC Programming.', 'hr@goodwin-europe.ru'),
        -- 9. Научные развлечения
        ('Научные развлечения', 'Методист STEM', 'Разработка образовательных программ.', 'Опыт преподавания, STEM Education.', 'hr@sci-entertain.ru'),
        ('Научные развлечения', 'Frontend-разработчик', 'Интерактивные обучающие модули.', 'React, TypeScript.', 'hr@sci-entertain.ru'),
        -- 10. Русская технологическая компания
        ('Русская технологическая компания', 'Системный интегратор', 'Интеграция промышленных решений.', 'Промышленное ПО, сети.', 'hr@rustech.ru'),
        ('Русская технологическая компания', 'DevOps-инженер', 'Поддержка инфраструктуры.', 'Docker, Kubernetes, CI/CD.', 'hr@rustech.ru'),
        -- 11. ГемаТех
        ('ГемаТех', 'Аналитик лабораторных данных', 'Обработка биоаналитических данных.', 'Python, Data Analysis, Biostatistics.', 'hr@gematech.ru'),
        ('ГемаТех', 'Лаборант-исследователь', 'Проведение лабораторных анализов.', 'Биологическое/химическое образование.', 'hr@gematech.ru'),
        -- 12. ЦПОСН Ортомода
        ('ЦПОСН Ортомода', 'Инженер 3D-печати', 'Печать ортопедических изделий.', '3D Printing, анатомия, SolidWorks.', 'hr@orthomoda.ru'),
        ('ЦПОСН Ортомода', 'CAD-модельер', 'Создание 3D-моделей имплантов.', 'SolidWorks, медицинское моделирование.', 'hr@orthomoda.ru'),
        -- 13. Амедарт
        ('Амедарт', 'Инженер по стерилизации', 'Обеспечение стерильности изделий.', 'Знание стандартов стерилизации.', 'hr@amedart.ru'),
        ('Амедарт', 'QA-инженер', 'Контроль качества продукции.', 'ISO 13485, QA.', 'hr@amedart.ru'),
        -- 14. Бифорком Тек
        ('Бифорком Тек', 'Data Scientist (геномика)', 'ML-модели для анализа ДНК.', 'PyTorch, Python, Genomics.', 'hr@biforcom.tech'),
        ('Бифорком Тек', 'Биоинформатик-стажёр', 'Поддержка анализа NGS-данных.', 'Базовый Python, биоинформатика.', 'hr@biforcom.tech'),
        -- 15. Микробор
        ('Микробор', 'Инженер микроэлектроники', 'Разработка микросхем.', 'Cadence, Microelectronics.', 'hr@microbor.ru'),
        ('Микробор', 'Технолог чипов', 'Контроль процессов изготовления.', 'Техническое образование, опыт на производстве.', 'hr@microbor.ru'),
        -- 16. Диагностика-М
        ('Диагностика-М', 'Инженер по диагностическому оборудованию', 'Техподдержка и разработка.', 'Электроника, микроконтроллеры.', 'hr@diagnostica-m.ru'),
        ('Диагностика-М', 'Продуктовый аналитик', 'Анализ рынка диагностических решений.', 'Аналитическое мышление, здравоохранение.', 'hr@diagnostica-m.ru'),
        -- 17. ИВА Технолоджис
        ('ИВА Технолоджис', 'Программист промышленного ПО', 'Разработка SCADA и АСУ ТП.', 'C#, .NET, Industrial Automation.', 'hr@iva-tech.ru'),
        ('ИВА Технолоджис', 'Инженер АСУ ТП', 'Проектирование систем управления.', 'Siemens, Allen Bradley.', 'hr@iva-tech.ru'),
        -- Дополнительные вакансии для достижения 50
        ('Сенсор', 'Data Scientist (IoT)', 'Анализ данных с промышленных сенсоров.', 'Python, Spark, Machine Learning.', 'hr@sensor-tech.ru'),
        ('ИНКОРО', 'Инженер по кибербезопасности', 'Защита встроенных систем.', 'Cybersecurity, Embedded Systems.', 'hr@inkoro.ru'),
        ('Концерн Гудвин (Гудвин Европа)', 'Инженер по компьютерному зрению', 'Алгоритмы для промышленной робототехники.', 'OpenCV, Computer Vision, C++.', 'hr@goodwin-europe.ru'),
        ('Акрус БиоМед', 'DevOps для биоинформатики', 'Инфраструктура для геномных вычислений.', 'Kubernetes, AWS, Docker.', 'hr@akrusbiomed.ru'),
        ('Русская технологическая компания', 'Инженер по цифровым двойникам', 'Разработка Digital Twin для промышленности.', 'Digital Twin, IoT, Python.', 'hr@rustech.ru'),
        ('Научные развлечения', 'UX/UI-дизайнер (edtech)', 'Дизайн интерфейсов для STEM-платформ.', 'Figma, UX Research, UI Design.', 'hr@sci-entertain.ru'),
        ('ГемаТех', 'Инженер по автоматизации лабораторий', 'Роботизация лабораторных процессов.', 'Robotics, PLC Programming.', 'hr@gematech.ru'),
        ('ЦПОСН Ортомода', 'Инженер по биомеханике', 'Моделирование нагрузок на импланты.', 'Mechanical Design, MATLAB Simulink.', 'hr@orthomoda.ru'),
        ('Бифорком Тек', 'ML Engineer (NLP)', 'Обработка медицинских текстов.', 'NLP, PyTorch, Python.', 'hr@biforcom.tech'),
        ('Микробор', 'Инженер по радиочастотным системам', 'Разработка RF-компонентов.', 'RF Engineering, Signal Processing.', 'hr@microbor.ru'),
        ('ИВА Технолоджис', 'Архитектор промышленных решений', 'Проектирование комплексных систем.', 'Domain-Driven Design, Microservices.', 'hr@iva-tech.ru'),
        ('Нанотехнологический центр композитов', 'Инженер по неразрушающему контролю', 'Тестирование композитов.', 'Signal Processing, опыт с датчиками.', 'hr@nanocomposite.ru'),
        ('Медплант', 'Регуляторный специалист', 'Подготовка документов для регистрации изделий.', 'Знание регуляторных требований.', 'hr@medplant.ru'),
        ('ПК Экопласт', 'Эколог производства', 'Контроль экологической безопасности.', 'Экологическое образование.', 'hr@ecoplast.ru'),
        ('Тест-Контакт', 'Инженер по биосенсорам', 'Разработка сенсоров для диагностики.', 'Biosensors, Electronics.', 'hr@test-contact.ru')
    ) AS v(company_name, title, description, requirements, contact_info)
    ON c.name = v.company_name
    RETURNING id, title
),

-- Привязка навыков
skill_assignments AS (
    SELECT
        iv.id AS vacancy_id,
        s.id AS skill_id,
        CASE
            WHEN s.name IN (
                'Python', 'C++', 'SQL', 'Embedded Systems', 'PLC Programming', 'FPGA', 'CAD',
                'SolidWorks', 'ROS', 'OpenCV', 'PyTorch', 'Machine Learning', 'DevOps',
                'Kubernetes', 'Docker', 'Cybersecurity', 'RF Engineering', 'MATLAB Simulink'
            ) THEN true
            ELSE false
        END AS is_required,
        CASE
            WHEN s.name IN (
                'Python', 'C++', 'PLC Programming', 'FPGA', 'CAD', 'SolidWorks', 'ROS',
                'OpenCV', 'PyTorch', 'Kubernetes', 'RF Engineering'
            ) THEN 5
            WHEN s.name IN ('Git', 'Linux', 'English (B2)', 'Agile', 'Scrum') THEN 3
            ELSE 2
        END AS priority
    FROM inserted_vacancies iv
    JOIN skills s ON (
        -- Технические навыки по ключевым словам
        (iv.title ILIKE '%материаловед%' AND s.name IN ('CAD', 'AutoCAD', 'Composite Materials', 'Polymer Chemistry'))
        OR (iv.title ILIKE '%медицинским изделиям%' AND s.name IN ('Medical Devices', 'ISO 13485', 'QA'))
        OR (iv.title ILIKE '%сенсоров%' AND s.name IN ('Sensors', 'Embedded Systems', 'C++', 'SolidWorks'))
        OR (iv.title ILIKE '%схемотехник%' AND s.name IN ('Electronics', 'VHDL', 'FPGA', 'Altium Designer'))
        OR (iv.title ILIKE '%диагност%' AND s.name IN ('LabVIEW', 'Medical Devices', 'Data Analysis'))
        OR (iv.title ILIKE '%полимерщик%' AND s.name IN ('Polymer Chemistry', 'Chemistry'))
        OR (iv.title ILIKE '%биоинформатик%' AND s.name IN ('Python', 'Genomics', 'Biostatistics', 'Pandas'))
        OR (iv.title ILIKE '%робототехник%' AND s.name IN ('Robotics', 'ROS', 'C++', 'Python', 'Computer Vision'))
        OR (iv.title ILIKE '%STEM%' AND s.name IN ('STEM Education', 'Коммуникабельность', 'Работа в команде'))
        OR (iv.title ILIKE '%DevOps%' AND s.name IN ('Docker', 'Kubernetes', 'CI/CD', 'AWS'))
        OR (iv.title ILIKE '%3D-печати%' AND s.name IN ('3D Printing', 'SolidWorks'))
        OR (iv.title ILIKE '%геномика%' AND s.name IN ('Genomics', 'PyTorch', 'Python', 'NLP'))
        OR (iv.title ILIKE '%микроэлектроники%' AND s.name IN ('Microelectronics', 'FPGA', 'VHDL', 'Verilog'))
        OR (iv.title ILIKE '%АСУ ТП%' AND s.name IN ('PLC Programming', 'Industrial Automation', 'Siemens'))
        OR (iv.title ILIKE '%Data Scientist%' AND s.name IN ('Python', 'Machine Learning', 'PyTorch', 'Spark'))
        OR (iv.title ILIKE '%кибербезопасности%' AND s.name IN ('Cybersecurity', 'Embedded Systems', 'Secure Coding'))
        OR (iv.title ILIKE '%компьютерному зрению%' AND s.name IN ('Computer Vision', 'OpenCV', 'C++'))
        OR (iv.title ILIKE '%цифровым двойникам%' AND s.name IN ('Digital Twin', 'IoT', 'Python'))
        OR (iv.title ILIKE '%UX/UI%' AND s.name IN ('Figma', 'UI Design', 'UX Research'))
        OR (iv.title ILIKE '%автоматизации лабораторий%' AND s.name IN ('Robotics', 'PLC Programming'))
        OR (iv.title ILIKE '%биомеханике%' AND s.name IN ('Mechanical Design', 'MATLAB Simulink'))
        OR (iv.title ILIKE '%NLP%' AND s.name IN ('NLP', 'PyTorch', 'Python'))
        OR (iv.title ILIKE '%радиочастотным%' AND s.name IN ('RF Engineering', 'Signal Processing'))
        OR (iv.title ILIKE '%архитектор%' AND s.name IN ('Domain-Driven Design', 'Microservices', 'Clean Architecture'))
        OR (iv.title ILIKE '%неразрушающему контролю%' AND s.name IN ('Signal Processing', 'Sensors'))
        OR (iv.title ILIKE '%регуляторный%' AND s.name IN ('Compliance (ISO 27001)', 'Risk Assessment'))
        OR (iv.title ILIKE '%эколог%' AND s.name IN ('Environmental Safety', 'Sustainability'))
        OR (iv.title ILIKE '%биосенсорам%' AND s.name IN ('Biosensors', 'Electronics', 'Embedded Systems'))
        -- Общие soft skills и английский
        OR (s.category = 'soft' AND s.name IN ('Коммуникабельность', 'Работа в команде', 'Решение проблем', 'Английский язык (B2)'))
    )
)

INSERT INTO vacancy_skills (vacancy_id, skill_id, is_required, priority)
SELECT vacancy_id, skill_id, is_required, priority
FROM skill_assignments;