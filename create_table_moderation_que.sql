CREATE TABLE moderation_queue (
    id CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin PRIMARY KEY DEFAULT (UUID()),
    item_type ENUM('vacancy', 'internship_request') NOT NULL,
    item_id CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    moderator_id CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
    status ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
    comment TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
    reviewed_at DATETIME NULL,

    -- Внешний ключ на модератора (пользователь с ролью 'admin')
    CONSTRAINT fk_moderation_moderator FOREIGN KEY (moderator_id) REFERENCES users(id) ON DELETE SET NULL,

    -- Индексы для производительности
    INDEX idx_item (item_type, item_id),
    INDEX idx_status (status),
    INDEX idx_moderator (moderator_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- 1. Заявка на стажировку от МГТУ — одобрена
INSERT INTO moderation_queue (item_type, item_id, moderator_id, status, comment, reviewed_at)
SELECT
    'internship_request',
    ir.id,
    u.id,
    'approved',
    'Все данные корректны, вуз подтверждён.',
    NOW() - INTERVAL 1 DAY
FROM internship_requests ir
CROSS JOIN users u
WHERE ir.university_name = 'МГТУ им. Н.Э. Баумана'
  AND u.email = 'admin@technopolis.moscow'
LIMIT 1;

-- 2. Заявка от МФТИ — отклонена
INSERT INTO moderation_queue (item_type, item_id, moderator_id, status, comment, reviewed_at)
SELECT
    'internship_request',
    ir.id,
    u.id,
    'rejected',
    'Указано нереалистичное количество студентов (1000). Уточните данные.',
    NOW() - INTERVAL 2 DAY
FROM internship_requests ir
CROSS JOIN users u
WHERE ir.university_name = 'МФТИ (ГУ)'
  AND u.email = 'admin@technopolis.moscow'
LIMIT 1;

-- 3. Заявка от ИТМО — на модерации
INSERT INTO moderation_queue (item_type, item_id, moderator_id, status, comment, reviewed_at)
SELECT
    'internship_request',
    ir.id,
    NULL,
    'pending',
    NULL,
    NULL
FROM internship_requests ir
WHERE ir.university_name = 'Университет ИТМО'
LIMIT 1;

-- 4. Вакансия "Backend-разработчик (Python)" — одобрена
INSERT INTO moderation_queue (item_type, item_id, moderator_id, status, comment, reviewed_at)
SELECT
    'vacancy',
    v.id,
    u.id,
    'approved',
    'Вакансия соответствует требованиям ОЭЗ.',
    NOW() - INTERVAL 3 HOUR
FROM vacancies v
CROSS JOIN users u
WHERE v.title = 'Backend-разработчик (Python)'
  AND u.email = 'admin@technopolis.moscow'
LIMIT 1;

-- 5. Вакансия "ML инженер (нейроинтерфейсы)" — одобрена
INSERT INTO moderation_queue (item_type, item_id, moderator_id, status, comment, reviewed_at)
SELECT
    'vacancy',
    v.id,
    u.id,
    'approved',
    'Инновационная позиция, одобрена к публикации.',
    NOW() - INTERVAL 5 HOUR
FROM vacancies v
CROSS JOIN users u
WHERE v.title = 'ML инженер (нейроинтерфейсы)'
  AND u.email = 'admin@technopolis.moscow'
LIMIT 1;

-- 6. Вакансия "DevOps инженер" — на модерации
INSERT INTO moderation_queue (item_type, item_id, moderator_id, status, comment, reviewed_at)
SELECT
    'vacancy',
    v.id,
    NULL,
    'pending',
    NULL,
    NULL
FROM vacancies v
WHERE v.title = 'DevOps инженер'
LIMIT 1;

-- 7. Вакансия "Frontend разработчик (Vue.js)" — отклонена
INSERT INTO moderation_queue (item_type, item_id, moderator_id, status, comment, reviewed_at)
SELECT
    'vacancy',
    v.id,
    u.id,
    'rejected',
    'Не указаны требования к кандидату. Верните на доработку.',
    NOW() - INTERVAL 1 HOUR
FROM vacancies v
CROSS JOIN users u
WHERE v.title = 'Frontend разработчик (Vue.js)'
  AND u.email = 'admin@technopolis.moscow'
LIMIT 1;

-- 8. Вакансия "QA инженер" — одобрена
INSERT INTO moderation_queue (item_type, item_id, moderator_id, status, comment, reviewed_at)
SELECT
    'vacancy',
    v.id,
    u.id,
    'approved',
    'Стандартная позиция, всё в порядке.',
    NOW() - INTERVAL 4 HOUR
FROM vacancies v
CROSS JOIN users u
WHERE v.title = 'QA инженер'
  AND u.email = 'admin@technopolis.moscow'
LIMIT 1;

-- 9. Заявка на стажировку (допустим, есть ещё одна) — на модерации
-- Используем любую другую заявку, например, по specialty
INSERT INTO moderation_queue (item_type, item_id, moderator_id, status, comment, reviewed_at)
SELECT
    'internship_request',
    ir.id,
    NULL,
    'pending',
    NULL,
    NULL
FROM internship_requests ir
WHERE ir.specialty = 'Прикладная математика и физика'
LIMIT 1;

-- 10. Вакансия "Data scientist (медицинская аналитика)" — одобрена
INSERT INTO moderation_queue (item_type, item_id, moderator_id, status, comment, reviewed_at)
SELECT
    'vacancy',
    v.id,
    u.id,
    'approved',
    'Соответствует профилю резидентов ОЭЗ.',
    NOW()
FROM vacancies v
CROSS JOIN users u
WHERE v.title = 'Data scientist (медицинская аналитика)'
  AND u.email = 'admin@technopolis.moscow'
LIMIT 1;