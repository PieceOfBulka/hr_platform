ALTER TABLE companies DROP FOREIGN KEY FK_companies_users;
-- (имя ограничения может отличаться — смотрите через SHOW CREATE TABLE companies)

ALTER TABLE users
MODIFY id CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT (UUID());



CREATE TABLE internship_requests (
    id CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin PRIMARY KEY DEFAULT (UUID()),
    university_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
    specialty VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
    student_count INT NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    status ENUM('pending_moderation', 'published', 'rejected') NOT NULL DEFAULT 'pending_moderation',
    created_at DATETIME NOT NULL DEFAULT NOW(),
    published_at DATETIME NULL,
    user_id CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


ALTER TABLE companies
MODIFY user_id CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;


ALTER TABLE companies
ADD CONSTRAINT FK_companies_users
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE SET NULL  -- или CASCADE / RESTRICT
ON UPDATE CASCADE;


-- Заявка от МГТУ им. Н.Э. Баумана
INSERT INTO internship_requests (
    id,
    university_name,
    specialty,
    student_count,
    period_start,
    period_end,
    status,
    created_at,
    published_at,
    user_id
)
SELECT
    UUID(),
    'МГТУ им. Н.Э. Баумана',
    'Информатика и вычислительная техника',
    15,
    '2025-06-01',
    '2025-08-15',
    'pending_moderation',
    NOW(),
    NULL,
    u.id
FROM users u
WHERE u.email = 'internships@bmstu.ru'
LIMIT 1;

