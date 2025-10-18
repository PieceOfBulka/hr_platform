CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- включание расширение для uuid

-- Таблица пользователей платформы
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255),
    role VARCHAR(20) NOT NULL
        CHECK (role IN ('hr', 'university_rep', 'admin', 'applicant')),
    name_of_place TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    is_verified BOOLEAN DEFAULT FALSE
);


-- наполнение данными в таблицу users

INSERT INTO users (id, email, password_hash, role, name_of_place, created_at, is_verified)
VALUES
-- Администратор ОЭЗ
(uuid_generate_v4(), 'admin@technopolis.moscow', '$2a$10$examplehash123456789', 'admin', 'ОЭЗ Технополис Москва', NOW() - INTERVAL '10 days', true),

-- HR-представители компаний-резидентов
(uuid_generate_v4(), 'hr@robovision.ru', '$2a$10$examplehash123456789', 'hr', 'РобоВижн Технолоджис', NOW() - INTERVAL '5 days', true),
(uuid_generate_v4(), 'recruitment@quantum-dev.ru', '$2a$10$examplehash123456789', 'hr', 'Квантовые Решения', NOW() - INTERVAL '3 days', true),
(uuid_generate_v4(), 'jobs@neurotech.moscow', '$2a$10$examplehash123456789', 'hr', 'НейроТех Москва', NOW() - INTERVAL '2 days', true),

-- Представители вузов
(uuid_generate_v4(), 'internships@bmstu.ru', '$2a$10$examplehash123456789', 'university_rep', 'МГТУ им. Н.Э. Баумана', NOW() - INTERVAL '4 days', true),
(uuid_generate_v4(), 'career@mipt.ru', '$2a$10$examplehash123456789', 'university_rep', 'МФТИ (ГУ)', NOW() - INTERVAL '6 days', true),
(uuid_generate_v4(), 'practice@itmo.ru', '$2a$10$examplehash123456789', 'university_rep', 'Университет ИТМО', NOW() - INTERVAL '1 day', true)
ON CONFLICT (email) DO NOTHING;