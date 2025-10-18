-- соискатель


-- создание таблицы пользователей --

CREATE TABLE users (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255),
    role VARCHAR(20) NOT NULL CHECK (role IN ('hr', 'university_rep', 'admin', 'applicant')),
    name_of_place TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_verified TINYINT(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- заполнение данными пользователей --
INSERT INTO users (id, email, password_hash, role, name_of_place, created_at, is_verified)
VALUES
(UUID(), 'admin@technopolis.moscow', '$2a$10$examplehash123456789', 'admin', 'ОЭЗ Технополис Москва', DATE_SUB(NOW(), INTERVAL 10 DAY), 1), -- Администратор ОЭЗ (1 для тестов)

(UUID(), 'hr@robovision.ru', '$2a$10$examplehash123456789', 'hr', 'РобоВижн Технолоджис', DATE_SUB(NOW(), INTERVAL 5 DAY), 1), -- HR-представители компаний-резидентов
(UUID(), 'recruitment@quantum-dev.ru', '$2a$10$examplehash123456789', 'hr', 'Квантовые Решения', DATE_SUB(NOW(), INTERVAL 3 DAY), 1),
(UUID(), 'jobs@neurotech.moscow', '$2a$10$examplehash123456789', 'hr', 'НейроТех Москва', DATE_SUB(NOW(), INTERVAL 2 DAY), 1),


(UUID(), 'internships@bmstu.ru', '$2a$10$examplehash123456789', 'university_rep', 'МГТУ им. Н.Э. Баумана', DATE_SUB(NOW(), INTERVAL 4 DAY), 1), -- Представители вузов
(UUID(), 'career@mipt.ru', '$2a$10$examplehash123456789', 'university_rep', 'МФТИ (ГУ)', DATE_SUB(NOW(), INTERVAL 6 DAY), 1),
(UUID(), 'practice@itmo.ru', '$2a$10$examplehash123456789', 'university_rep', 'Университет ИТМО', DATE_SUB(NOW(), INTERVAL 1 DAY), 1);


-- создание списка компаний --

CREATE TABLE companies (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(500) NOT NULL,
    description VARCHAR(1000),
    contact_person VARCHAR(150),
    contact_email VARCHAR(200),
    contact_phone VARCHAR(20),
    user_id CHAR(36) NULL,
    CONSTRAINT FK_companies_users
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;




-- Вставка данных про компании резиденты (взяты с сайта ОЭЗ)
INSERT INTO companies (
    name,
    description,
    contact_person,
    contact_email,
    contact_phone
)
VALUES
('Нанотехнологический центр композитов', 'Разработка и производство композитных материалов нового поколения.', 'HR-менеджер', 'hr@nanocomposite.ru', '+7 (495) 123-45-67'),
('Медплант', 'Производство биосовместимых имплантов и медицинских решений.', 'HR-менеджер', 'hr@medplant.ru', '+7 (495) 123-45-68'),
('Сенсор', 'Разработка и производство высокоточных сенсоров для промышленности.', 'HR-менеджер', 'hr@sensor-tech.ru', '+7 (495) 123-45-69'),
('ИНКОРО', 'Инновационные решения в области микроэлектроники.', 'HR-менеджер', 'hr@inkoro.ru', '+7 (495) 123-45-70'),
('Тест-Контакт', 'Диагностическое оборудование и тест-системы.', 'HR-менеджер', 'hr@test-contact.ru', '+7 (495) 123-45-71'),
('ПК Экопласт', 'Производство экологичных полимерных материалов.', 'HR-менеджер', 'hr@ecoplast.ru', '+7 (495) 123-45-72'),
('Акрус БиоМед', 'Биотехнологии и разработка лекарственных препаратов.', 'HR-менеджер', 'hr@akrusbiomed.ru', '+7 (495) 123-45-73'),
('Концерн Гудвин (Гудвин Европа)', 'Промышленная автоматизация и робототехника.', 'HR-менеджер', 'hr@goodwin-europe.ru', '+7 (495) 123-45-74'),
('Научные развлечения', 'Интерактивные образовательные технологии и STEM-продукты.', 'HR-менеджер', 'hr@sci-entertain.ru', '+7 (495) 123-45-75'),
('Русская технологическая компания', 'Интеграция передовых технологий в промышленность.', 'HR-менеджер', 'hr@rustech.ru', '+7 (495) 123-45-76'),
('ГемаТех', 'Лабораторная диагностика и биоаналитика.', 'HR-менеджер', 'hr@gematech.ru', '+7 (495) 123-45-77'),
('ЦПОСН Ортомода', 'Цифровые решения в ортопедии и протезировании.', 'HR-менеджер', 'hr@orthomoda.ru', '+7 (495) 123-45-78'),
('Амедарт', 'Медицинские имплантаты и хирургические инструменты.', 'HR-менеджер', 'hr@amedart.ru', '+7 (495) 123-45-79'),
('Бифорком Тек', 'Биоинформатика и анализ геномных данных.', 'HR-менеджер', 'hr@biforcom.tech', '+7 (495) 123-45-80'),
('Микробор', 'Микроэлектронные компоненты для специального назначения.', 'HR-менеджер', 'hr@microbor.ru', '+7 (495) 123-45-81'),
('Диагностика-М', 'Медицинская диагностика и лабораторные системы.', 'HR-менеджер', 'hr@diagnostica-m.ru', '+7 (495) 123-45-82'),
('ИВА Технолоджис', 'Промышленное ПО и автоматизация.', 'HR-менеджер', 'hr@iva-tech.ru', '+7 (495) 123-45-83'),
('Фотоэксперт', 'Цифровая обработка изображений и фотоника.', 'HR-менеджер', 'hr@fotoexpert.ru', '+7 (495) 123-45-84'),
('Европейская электротехника', 'Электротехническое оборудование и компоненты.', 'HR-менеджер', 'hr@euroelectro.ru', '+7 (495) 123-45-85'),
('Пьезус', 'Пьезоэлектрические устройства и сенсоры.', 'HR-менеджер', 'hr@piezus.ru', '+7 (495) 123-45-86'),
('Аддитивный инжиниринг', '3D-печать и аддитивные технологии.', 'HR-менеджер', 'hr@additive-eng.ru', '+7 (495) 123-45-87'),
('Мастерская цифровых решений', 'Разработка цифровых продуктов и ИТ-решений.', 'HR-менеджер', 'hr@digital-solutions.ru', '+7 (495) 123-45-88'),
('Неорос', 'Нейротехнологии и интерфейсы мозг-компьютер.', 'HR-менеджер', 'hr@neoros.tech', '+7 (495) 123-45-89'),
('НПО Композит', 'Научно-производственное объединение в области композитов.', 'HR-менеджер', 'hr@npo-composite.ru', '+7 (495) 123-45-90'),
('ОнкоТаргет', 'Таргетная терапия и онкодиагностика.', 'HR-менеджер', 'hr@oncotarget.ru', '+7 (495) 123-45-91'),
('Хирана+', 'Медицинские устройства и цифровое здравоохранение.', 'HR-менеджер', 'hr@hirana-plus.ru', '+7 (495) 123-45-92'),
('ТЗМОИ', 'Технологии защиты и обработки информации.', 'HR-менеджер', 'hr@tzmoi.ru', '+7 (495) 123-45-93'),
('РАДА-ФАРМА', 'Фармацевтические разработки и производство.', 'HR-менеджер', 'hr@rada-pharma.ru', '+7 (495) 123-45-94'),
('Мезоформула', 'Космецевтика и биоактивные формулы.', 'HR-менеджер', 'hr@mesoformula.ru', '+7 (495) 123-45-95'),
('НТЦ ХайТэк', 'Научно-технический центр высоких технологий.', 'HR-менеджер', 'hr@ntc-hightech.ru', '+7 (495) 123-45-96'),
('ЛазерТек', 'Лазерные технологии и оборудование.', 'HR-менеджер', 'hr@lasertech.ru', '+7 (495) 123-45-97'),
('АСЭЗ', 'Автоматизированные системы энергосбережения.', 'HR-менеджер', 'hr@asez.ru', '+7 (495) 123-45-98'),
('Промис', 'Промышленные информационные системы.', 'HR-менеджер', 'hr@promis.ru', '+7 (495) 123-45-99'),
('СиГнал', 'Связь, телекоммуникации и IoT.', 'HR-менеджер', 'hr@signal-iot.ru', '+7 (495) 123-46-00'),
('Элтекс', 'Сетевое и телекоммуникационное оборудование.', 'HR-менеджер', 'hr@eltex.ru', '+7 (495) 123-46-01'),
('Элтекс Энерго', 'Энергетические решения на базе цифровых технологий.', 'HR-менеджер', 'hr@eltex-energo.ru', '+7 (495) 123-46-02'),
('Промсвязь', 'Индустриальные решения в области связи.', 'HR-менеджер', 'hr@promsvyaz.ru', '+7 (495) 123-46-03'),
('Интеллектуальные технологии', 'AI и интеллектуальные системы управления.', 'HR-менеджер', 'hr@intech-ai.ru', '+7 (495) 123-46-04'),
('Лаборатория Касперского', 'Кибербезопасность и защита данных.', 'HR-менеджер', 'hr@kaspersky.ru', '+7 (495) 123-46-05'),
('Резидент ПЛК Технолоджи', 'Программируемые логические контроллеры.', 'HR-менеджер', 'hr@plc-tech.ru', '+7 (495) 123-46-06'),
('Диаклон', 'Медицинские диагностические системы.', 'HR-менеджер', 'hr@diaclone.ru', '+7 (495) 123-46-07'),
('Висмо', 'Компьютерное зрение и видеоаналитика.', 'HR-менеджер', 'hr@vismo.ai', '+7 (495) 123-46-08'),
('Центр Диагностика', 'Комплексные диагностические решения.', 'HR-менеджер', 'hr@center-diagnostica.ru', '+7 (495) 123-46-09'),
('Биомед', 'Биомедицинские технологии и оборудование.', 'HR-менеджер', 'hr@biomed.ru', '+7 (495) 123-46-10'),
('Институт микроэлектроники', 'Научные исследования в микроэлектронике.', 'HR-менеджер', 'hr@ime.ru', '+7 (495) 123-46-11'),
('Интеграл', 'Полупроводниковые компоненты и микросхемы.', 'HR-менеджер', 'hr@integral.ru', '+7 (495) 123-46-12'),
('СВЧ Компоненты', 'Высокочастотная электроника и СВЧ-устройства.', 'HR-менеджер', 'hr@microwave-comp.ru', '+7 (495) 123-46-13'),
('Гравион', 'Квантовые сенсоры и гравиметрия.', 'HR-менеджер', 'hr@gravion.tech', '+7 (495) 123-46-14'),
('Оптэл', 'Оптоэлектронные системы и приборы.', 'HR-менеджер', 'hr@optel.ru', '+7 (495) 123-46-15'),
('МикроОптика', 'Микрооптические компоненты и системы.', 'HR-менеджер', 'hr@microoptica.ru', '+7 (495) 123-46-16'),
('Элтрон', 'Электронные компоненты и модули.', 'HR-менеджер', 'hr@eltron.ru', '+7 (495) 123-46-17'),
('Теслар', 'Энергетические и электротехнические решения.', 'HR-менеджер', 'hr@teslar.ru', '+7 (495) 123-46-18'),
('Электроника-М', 'Микроэлектроника и сборка.', 'HR-менеджер', 'hr@electronica-m.ru', '+7 (495) 123-46-19'),
('АйТиПро', 'ИТ-аутсорсинг и разработка ПО.', 'HR-менеджер', 'hr@itpro.ru', '+7 (495) 123-46-20'),
('Эстетика', 'Медицинская эстетика и косметология.', 'HR-менеджер', 'hr@estetica-med.ru', '+7 (495) 123-46-21'),
('ФармХим', 'Фармацевтическая химия и синтез.', 'HR-менеджер', 'hr@pharmchem.ru', '+7 (495) 123-46-22'),
('БиоПром', 'Биотехнологическое производство.', 'HR-менеджер', 'hr@bioprom.ru', '+7 (495) 123-46-23'),
('Микротех', 'Микромеханика и прецизионные устройства.', 'HR-менеджер', 'hr@microtech.ru', '+7 (495) 123-46-24'),
('ИнтегралСвет', 'Светодиодные и осветительные технологии.', 'HR-менеджер', 'hr@integralsvet.ru', '+7 (495) 123-46-25'),
('АйСиДжи', 'Инженерные и консалтинговые услуги.', 'HR-менеджер', 'hr@icg.ru', '+7 (495) 123-46-26'),
('Логос', 'Программное обеспечение для моделирования.', 'HR-менеджер', 'hr@logos.ru', '+7 (495) 123-46-27'),
('АСБЭЛ', 'Автоматизация и безопасность.', 'HR-менеджер', 'hr@asbel.ru', '+7 (495) 123-46-28'),
('ЭнергоИнновация', 'Энергоэффективные технологии.', 'HR-менеджер', 'hr@energoinnov.ru', '+7 (495) 123-46-29'),
('Инжиниринг МС', 'Машиностроительный инжиниринг.', 'HR-менеджер', 'hr@eng-ms.ru', '+7 (495) 123-46-30'),
('Нейрософт', 'Нейросетевые алгоритмы и ПО.', 'HR-менеджер', 'hr@neurosoft.ru', '+7 (495) 123-46-31'),
('Биосенсорика', 'Биосенсоры и лабораторная диагностика.', 'HR-менеджер', 'hr@biosensorica.ru', '+7 (495) 123-46-32'),
('РБК-Мед', 'Медицинские информационные системы.', 'HR-менеджер', 'hr@rbk-med.ru', '+7 (495) 123-46-33'),
('ХимИнжиниринг', 'Химическое машиностроение и процессы.', 'HR-менеджер', 'hr@chemeng.ru', '+7 (495) 123-46-34'),
('Квант', 'Квантовые технологии и вычисления.', 'HR-менеджер', 'hr@kvant.tech', '+7 (495) 123-46-35'),
('СТМ', 'Специальная техника и материалы.', 'HR-менеджер', 'hr@stm.ru', '+7 (495) 123-46-36'),
('Динамика', 'Системы управления и динамика.', 'HR-менеджер', 'hr@dinamika.ru', '+7 (495) 123-46-37'),
('Вектор', 'Биофармацевтика и вакцины.', 'HR-менеджер', 'hr@vector.ru', '+7 (495) 123-46-38'),
('Квантум', 'Квантовые сенсоры и коммуникации.', 'HR-менеджер', 'hr@quantum-tech.ru', '+7 (495) 123-46-39'),
('ИнноваМед', 'Инновационные медицинские технологии.', 'HR-менеджер', 'hr@innovamed.ru', '+7 (495) 123-46-40'),
('ПромБиоТех', 'Промышленная биотехнология.', 'HR-менеджер', 'hr@prombiotech.ru', '+7 (495) 123-46-41'),
('МетПром', 'Металлургические технологии.', 'HR-менеджер', 'hr@metprom.ru', '+7 (495) 123-46-42'),
('ХайТекМаш', 'Высокотехнологичное машиностроение.', 'HR-менеджер', 'hr@hightekmash.ru', '+7 (495) 123-46-43'),
('ЛинТех', 'Линейные технологии и приводы.', 'HR-менеджер', 'hr@lintech.ru', '+7 (495) 123-46-44'),
('СибЭлектро', 'Электротехническое оборудование.', 'HR-менеджер', 'hr@sibelectro.ru', '+7 (495) 123-46-45'),
('Микромаш', 'Микроэлектромеханические системы (MEMS).', 'HR-менеджер', 'hr@micromash.ru', '+7 (495) 123-46-46'),
('Фотоника', 'Фотонные технологии и оптика.', 'HR-менеджер', 'hr@photonica.ru', '+7 (495) 123-46-47'),
('КвантЛазер', 'Лазерные квантовые системы.', 'HR-менеджер', 'hr@kvantlaser.ru', '+7 (495) 123-46-48'),
('МикроХим', 'Микрохимические системы и анализ.', 'HR-менеджер', 'hr@microhim.ru', '+7 (495) 123-46-49'),
('ХимПроМед', 'Химические технологии в медицине.', 'HR-менеджер', 'hr@himpromed.ru', '+7 (495) 123-46-50'),
('ФармаТех', 'Фармацевтическое оборудование.', 'HR-менеджер', 'hr@pharmatech.ru', '+7 (495) 123-46-51'),
('ЛабМед', 'Лабораторная медицина и диагностика.', 'HR-менеджер', 'hr@labmed.ru', '+7 (495) 123-46-52'),
('НаноСенс', 'Наносенсоры и нанодиагностика.', 'HR-менеджер', 'hr@nanosens.ru', '+7 (495) 123-46-53'),
('НаноПро', 'Нанотехнологии и материалы.', 'HR-менеджер', 'hr@nanopro.ru', '+7 (495) 123-46-54'),
('Фотоникс', 'Оптоэлектронные компоненты.', 'HR-менеджер', 'hr@photonix.ru', '+7 (495) 123-46-55'),
('МикроТехПро', 'Микротехнологии и производство.', 'HR-менеджер', 'hr@microtechpro.ru', '+7 (495) 123-46-56'),
('МедЛаб', 'Медицинские лабораторные услуги.', 'HR-менеджер', 'hr@medlab.ru', '+7 (495) 123-46-57'),
('НаноТех', 'Нанотехнологические разработки.', 'HR-менеджер', 'hr@nanotech.ru', '+7 (495) 123-46-58'),
('БиоТех', 'Биотехнологии и биоинженерия.', 'HR-менеджер', 'hr@biotech.ru', '+7 (495) 123-46-59'),
('Резонанс', 'Радиочастотные и резонансные технологии.', 'HR-менеджер', 'hr@rezonans.ru', '+7 (495) 123-46-60'),
('Энергия', 'Энергетические решения и системы.', 'HR-менеджер', 'hr@energia-tech.ru', '+7 (495) 123-46-61'),
('НейроТек', 'Нейротехнологии и интерфейсы.', 'HR-менеджер', 'hr@neurotech.moscow', '+7 (495) 123-46-62'),
('МикроСвет', 'Микрооптика и освещение.', 'HR-менеджер', 'hr@microsvet.ru', '+7 (495) 123-46-63'),
('Оптима', 'Оптимизация производственных процессов.', 'HR-менеджер', 'hr@optima-industry.ru', '+7 (495) 123-46-64'),
('Эврика', 'Инновационные R&D-проекты.', 'HR-менеджер', 'hr@eureka-lab.ru', '+7 (495) 123-46-65'),
('Сигма', 'Инженерные и аналитические решения.', 'HR-менеджер', 'hr@sigma-engineering.ru', '+7 (495) 123-46-66'),
('Атом', 'Ядерные и радиационные технологии.', 'HR-менеджер', 'hr@atom-tech.ru', '+7 (495) 123-46-67'),
('ПрофиЛаб', 'Профессиональные лабораторные решения.', 'HR-менеджер', 'hr@profilab.ru', '+7 (495) 123-46-68'),
('Инновация', 'Управление инновационными проектами.', 'HR-менеджер', 'hr@innovatsiya.ru', '+7 (495) 123-46-69'),
('ВекторПлюс', 'Расширенные биомедицинские решения.', 'HR-менеджер', 'hr@vectorplus.ru', '+7 (495) 123-46-70'),
('КвантумЛаб', 'Лаборатория квантовых технологий.', 'HR-менеджер', 'hr@quantumlabs.ru', '+7 (495) 123-46-71');


-- Таблица справочника навыков (всевозможный перечень навыков для специальностей)
CREATE TABLE skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    category VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Вставка 200 технического навыков --
INSERT INTO skills (name, category) VALUES
('Python', 'technical'),
('JavaScript', 'technical'),
('TypeScript', 'technical'),
('Java', 'technical'),
('C++', 'technical'),
('C#', 'technical'),
('Go', 'technical'),
('Rust', 'technical'),
('PHP', 'technical'),
('Ruby', 'technical'),
('SQL', 'technical'),
('PostgreSQL', 'technical'),
('MySQL', 'technical'),
('MongoDB', 'technical'),
('Redis', 'technical'),
('Docker', 'technical'),
('Kubernetes', 'technical'),
('Git', 'technical'),
('Linux', 'technical'),
('Bash', 'technical'),
('CI/CD', 'technical'),
('REST API', 'technical'),
('GraphQL', 'technical'),
('React', 'technical'),
('Vue.js', 'technical'),
('Angular', 'technical'),
('Node.js', 'technical'),
('Django', 'technical'),
('Flask', 'technical'),
('Spring Boot', 'technical'),
('FastAPI', 'technical'),
('TensorFlow', 'technical'),
('PyTorch', 'technical'),
('Scikit-learn', 'technical'),
('Pandas', 'technical'),
('NumPy', 'technical'),
('OpenCV', 'technical'),
('Computer Vision', 'technical'),
('NLP', 'technical'),
('Machine Learning', 'technical'),
('Deep Learning', 'technical'),
('Data Analysis', 'technical'),
('Data Engineering', 'technical'),
('ETL', 'technical'),
('Apache Kafka', 'technical'),
('RabbitMQ', 'technical'),
('AWS', 'technical'),
('Azure', 'technical'),
('Google Cloud', 'technical'),
('Terraform', 'technical'),
('Ansible', 'technical'),
('Prometheus', 'technical'),
('Grafana', 'technical'),
('Jenkins', 'technical'),
('GitLab CI', 'technical'),
('GitHub Actions', 'technical'),
('Microservices', 'technical'),
('OAuth2', 'technical'),
('JWT', 'technical'),
('Blockchain', 'technical'),
('Solidity', 'technical'),
('Web3', 'technical'),
('Cybersecurity', 'technical'),
('Penetration Testing', 'technical'),
('Network Security', 'technical'),
('Cryptography', 'technical'),
('DevOps', 'technical'),
('MLOps', 'technical'),
('Agile', 'methodology'),
('Scrum', 'methodology'),
('Kanban', 'methodology'),
('Jira', 'tool'),
('Confluence', 'tool'),
('Notion', 'tool'),
('Figma', 'tool'),
('Postman', 'tool'),
('Swagger', 'tool'),
('Tableau', 'tool'),
('Power BI', 'tool'),
('Excel', 'tool'),
('Matlab', 'tool'),
('CAD', 'engineering'),
('SolidWorks', 'engineering'),
('AutoCAD', 'engineering'),
('MATLAB Simulink', 'engineering'),
('PLC Programming', 'engineering'),
('Embedded Systems', 'engineering'),
('RTOS', 'engineering'),
('FPGA', 'engineering'),
('Verilog', 'engineering'),
('VHDL', 'engineering'),
('Robotics', 'engineering'),
('IoT', 'engineering'),
('5G', 'engineering'),
('RF Engineering', 'engineering'),
('Signal Processing', 'engineering'),
('Control Systems', 'engineering'),
('Thermodynamics', 'engineering'),
('Fluid Dynamics', 'engineering'),
('Mechanical Design', 'engineering'),
('Electrical Engineering', 'engineering'),
('Power Electronics', 'engineering'),
('PCB Design', 'engineering'),
('Altium Designer', 'engineering'),
('OrCAD', 'engineering'),
('English (B1)', 'language'),
('English (B2)', 'language'),
('English (C1)', 'language'),
('German', 'language'),
('Chinese', 'language'),
('French', 'language'),
('Spanish', 'language'),
('Data Visualization', 'technical'),
('Big Data', 'technical'),
('Hadoop', 'technical'),
('Spark', 'technical'),
('Airflow', 'technical'),
('dbt', 'technical'),
('Looker', 'tool'),
('Metabase', 'tool'),
('Superset', 'tool'),
('ClickHouse', 'technical'),
('Elasticsearch', 'technical'),
('Kibana', 'tool'),
('Logstash', 'technical'),
('Fluentd', 'technical'),
('Nginx', 'technical'),
('Apache', 'technical'),
('Traefik', 'technical'),
('Istio', 'technical'),
('Service Mesh', 'technical'),
('OAuth', 'technical'),
('SAML', 'technical'),
('LDAP', 'technical'),
('Active Directory', 'technical'),
('Zero Trust', 'security'),
('SIEM', 'security'),
('IDS/IPS', 'security'),
('Vulnerability Scanning', 'security'),
('Compliance (GDPR)', 'security'),
('Compliance (ISO 27001)', 'security'),
('Risk Assessment', 'security'),
('Incident Response', 'security'),
('Digital Forensics', 'security'),
('Cloud Security', 'security'),
('Container Security', 'security'),
('API Security', 'security'),
('Secure Coding', 'security'),
('Threat Modeling', 'security'),
('QA', 'technical'),
('Manual Testing', 'technical'),
('Automated Testing', 'technical'),
('Selenium', 'technical'),
('Cypress', 'technical'),
('Playwright', 'technical'),
('JUnit', 'technical'),
('PyTest', 'technical'),
('Load Testing', 'technical'),
('JMeter', 'technical'),
('Locust', 'technical'),
('Accessibility (a11y)', 'technical'),
('SEO', 'technical'),
('UX Research', 'design'),
('UI Design', 'design'),
('User Testing', 'design'),
('Wireframing', 'design'),
('Prototyping', 'design'),
('Design Systems', 'design'),
('Responsive Design', 'design'),
('Cross-browser Compatibility', 'technical'),
('Web Performance', 'technical'),
('Lighthouse', 'tool'),
('Webpack', 'tool'),
('Vite', 'tool'),
('Rollup', 'tool'),
('Babel', 'tool'),
('ESLint', 'tool'),
('Prettier', 'tool'),
('Yarn', 'tool'),
('npm', 'tool'),
('pnpm', 'tool'),
('Rust (embedded)', 'technical'),
('Zig', 'technical'),
('Assembly', 'technical'),
('Quantum Computing', 'emerging'),
('AR/VR Development', 'emerging'),
('Unity', 'tool'),
('Unreal Engine', 'tool'),
('Game Development', 'technical'),
('Audio Programming', 'technical'),
('3D Modeling', 'design'),
('Blender', 'tool'),
('Maya', 'tool'),
('Digital Twin', 'emerging'),
('Edge Computing', 'technical'),
('Serverless', 'technical'),
('AWS Lambda', 'technical'),
('Azure Functions', 'technical'),
('Google Cloud Functions', 'technical'),
('Firebase', 'technical'),
('Supabase', 'technical'),
('Hasura', 'technical'),
('Prisma', 'tool'),
('TypeORM', 'tool'),
('Sequelize', 'tool'),
('SQLAlchemy', 'tool'),
('Alembic', 'tool'),
('Liquibase', 'tool'),
('Flyway', 'tool'),
('Database Migration', 'technical'),
('Indexing', 'technical'),
('Query Optimization', 'technical'),
('Replication', 'technical'),
('Sharding', 'technical'),
('Backup & Recovery', 'technical'),
('Disaster Recovery', 'technical'),
('High Availability', 'technical'),
('Load Balancing', 'technical'),
('CDN', 'technical'),
('WebSockets', 'technical'),
('gRPC', 'technical'),
('Protocol Buffers', 'technical'),
('Message Queues', 'technical'),
('Event-Driven Architecture', 'technical'),
('Domain-Driven Design', 'methodology'),
('Clean Architecture', 'methodology'),
('TDD', 'methodology');

-- софт навыки --


INSERT INTO skills (name, category) VALUES
('Коммуникабельность', 'soft'),
('Работа в команде', 'soft'),
('Решение проблем', 'soft'),
('Критическое мышление', 'soft'),
('Тайм-менеджмент', 'soft'),
('Лидерство', 'soft'),
('Гибкость', 'soft'),
('Креативность', 'soft'),
('Эмоциональный интеллект', 'soft'),
('Разрешение конфликтов', 'soft'),
('Навыки ведения переговоров', 'soft'),
('Публичные выступления', 'soft'),
('Активное слушание', 'soft'),
('Ориентация на клиента', 'soft'),
('Внимание к деталям', 'soft'),
('Самомотивация', 'soft'),
('Стрессоустойчивость', 'soft'),
('Управление проектами', 'soft'),
('Стратегическое мышление', 'soft'),
('Принятие решений', 'soft'),
('Наставничество', 'soft'),
('Коучинг', 'soft'),
('Навыки презентации', 'soft'),
('Письменная коммуникация', 'soft'),
('Аналитическое мышление', 'soft'),
('Исследовательские навыки', 'soft'),
('Организационные навыки', 'soft'),
('Инициативность', 'soft'),
('Ответственность', 'soft'),
('Эмпатия', 'soft'),
('Умение делегировать', 'soft'),
('Работа в условиях неопределённости', 'soft'),
('Многозадачность', 'soft'),
('Самоорганизация', 'soft'),
('Этичное поведение', 'soft'),
('Проактивность', 'soft'),
('Обратная связь (умение давать и принимать)', 'soft'),
('Культурная осведомлённость', 'soft'),
('Способность к обучению', 'soft'),
('Адаптивность к изменениям', 'soft'),
('Фокус на результате', 'soft'),
('Построение доверительных отношений', 'soft'),
('Умение работать с возражениями', 'soft'),
('Саморефлексия', 'soft'),
('Управление ожиданиями', 'soft'),
('Работа с обратной связью', 'soft'),
('Эффективное планирование', 'soft'),
('Навыки фасилитации', 'soft'),
('Медиация', 'soft');

-- Вставка навыков (с игнорированием дубликатов)
INSERT IGNORE INTO skills (name, category) VALUES
-- Системы и ПО
('AutoCAD', 'engineering'),
('SolidWorks', 'engineering'),
('CATIA', 'engineering'),
('Creo (Pro/ENGINEER)', 'engineering'),
('Siemens NX', 'engineering'),
('Autodesk Inventor', 'engineering'),
('PTC Windchill', 'engineering'),
('Teamcenter', 'engineering'),
('SAP ERP (модули PP, MM, QM)', 'erp'),
('1С:ERP', 'erp'),
('Oracle ERP', 'erp'),
('MES-системы (Manufacturing Execution Systems)', 'automation'),
('SCADA-системы', 'automation'),
('Siemens TIA Portal', 'automation'),
('Программирование ПЛК (Siemens S7)', 'automation'),
('Программирование ПЛК (Allen-Bradley / Rockwell)', 'automation'),
('Программирование ПЛК (Schneider Electric)', 'automation'),
('Программирование ПЛК (Omron)', 'automation'),
('WinCC', 'automation'),
('iFIX', 'automation'),
('Citect SCADA', 'automation'),
('RSLogix / Studio 5000', 'automation'),
('CODESYS', 'automation'),
('HMI-панели (настройка и программирование)', 'automation'),

-- Безопасность и качество
('Промышленная безопасность', 'safety'),
('Охрана труда (ОТ)', 'safety'),
('Пожарная безопасность', 'safety'),
('Экологическая безопасность', 'safety'),
('Системы менеджмента качества (ISO 9001)', 'quality'),
('Системы экологического менеджмента (ISO 14001)', 'quality'),
('Менеджмент промышленной безопасности (ISO 45001)', 'safety'),
('Внутренний аудит качества', 'quality'),
('Статистический контроль процессов (SPC)', 'quality'),
('Анализ причин дефектов (RCA)', 'quality'),
('5S', 'methodology'),
('Lean Manufacturing', 'methodology'),
('Kaizen', 'methodology'),
('TPM (Total Productive Maintenance)', 'methodology'),
('Six Sigma (Green Belt / Black Belt)', 'methodology'),
('Управление запасами (Just-in-Time)', 'logistics'),
('Контроль качества продукции', 'quality'),
('Неразрушающий контроль (НК): ультразвуковой, магнитопорошковый, капиллярный', 'technical'),

-- Энергетика и инфраструктура
('Эксплуатация электрических подстанций', 'energy'),
('Релейная защита и автоматика', 'energy'),
('Обслуживание дизель-генераторов', 'energy'),
('Работа с системами АСУ ТП', 'automation'),
('Техническое обслуживание КИПиА', 'technical'),
('Обслуживание систем вентиляции и кондиционирования', 'technical'),
('Обслуживание котельных установок', 'energy'),
('Работа с системами водоподготовки', 'technical'),
('Обслуживание компрессорных станций', 'technical'),
('Энергоаудит', 'energy'),
('Энергосбережение на производстве', 'energy'),

-- Логистика и склад
('Управление складскими запасами', 'logistics'),
('Работа с погрузочной техникой (погрузчики, штабелёры)', 'logistics'),
('Системы WMS (Warehouse Management System)', 'logistics'),
('Управление внутренними транспортными потоками', 'logistics'),
('Упаковка и маркировка продукции', 'logistics'),

-- Мягкие навыки для производства
('Работа в условиях многозадачности', 'soft'),
('Соблюдение регламентов и инструкций', 'soft'),
('Дисциплинированность', 'soft'),
('Ответственность за результат', 'soft'),
('Готовность к работе вахтовым методом', 'soft'),
('Готовность к работе в ночную смену', 'soft'),
('Командная работа на производстве', 'soft'),
('Обучение персонала на рабочем месте', 'soft'),

-- 🔧 ДОПОЛНИТЕЛЬНЫЕ ПРОИЗВОДСТВЕННЫЕ НАВЫКИ (новые!)
('Работа на токарно-винторезных станках', 'technical'),
('Фрезерные работы', 'technical'),
('Шлифовальные работы', 'technical'),
('Слесарная обработка', 'technical'),
('Сборка механических узлов', 'technical'),
('Гидравлические испытания', 'technical'),
('Пневматические испытания', 'technical'),
('Балансировка роторов', 'technical'),
('Вибродиагностика оборудования', 'technical'),
('Термография оборудования', 'technical'),
('Работа с мостовыми кранами', 'technical'),
('Строповка грузов', 'technical'),
('Сертификация сварщиков (НАКС)', 'certification'),
('Радиографический контроль', 'technical'),
('Визуальный и измерительный контроль (ВИК)', 'technical'),
('Тепловизионный контроль', 'technical'),
('Обслуживание систем пневмотранспорта', 'technical'),
('Работа с системами пылеулавливания', 'technical'),
('Обслуживание холодильных установок', 'technical'),
('Работа с системами очистки сточных вод', 'technical'),
('Метрологическое обеспечение производства', 'quality'),
('Калибровка измерительных приборов', 'technical'),
('Работа с тахометрами и виброметрами', 'technical'),
('Техническое диагностирование оборудования', 'technical'),
('Планирование ТОиР (технического обслуживания и ремонта)', 'technical');



-- создание таблицы с вакансиями --

CREATE TABLE vacancies (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    company_id CHAR(36) NOT NULL,
    title VARCHAR(300) NOT NULL,
    description TEXT,
    contact_info TEXT,
    status ENUM('draft', 'pending_moderation', 'published', 'closed', 'expired') DEFAULT 'draft',
    publish_until DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    published_at DATETIME NULL,

    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;




-- Связующая таблица "вакансия - навык"
CREATE TABLE vacancy_skills (
    vacancy_id CHAR(36) NOT NULL,
    skill_id INT NOT NULL,
    is_required BOOLEAN DEFAULT FALSE,        -- обязательно или желательно
    priority TINYINT UNSIGNED DEFAULT 1 CHECK (priority >= 1 AND priority <= 5),

    PRIMARY KEY (vacancy_id, skill_id),
    FOREIGN KEY (vacancy_id) REFERENCES vacancies(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Добавляем 10 соискателей (applicants)
INSERT INTO users (id, email, password_hash, role, name_of_place, created_at, is_verified)
VALUES
(UUID(), 'ivan.petrov@example.com', '$2a$10$examplehash123456789', 'applicant', NULL, NOW() - INTERVAL 5 DAY, 1),
(UUID(), 'maria.sokolova@example.com', '$2a$10$examplehash123456789', 'applicant', NULL, NOW() - INTERVAL 4 DAY, 1),
(UUID(), 'alexey.smirnov@example.com', '$2a$10$examplehash123456789', 'applicant', NULL, NOW() - INTERVAL 3 DAY, 1),
(UUID(), 'ekaterina.kuznetsova@example.com', '$2a$10$examplehash123456789', 'applicant', NULL, NOW() - INTERVAL 2 DAY, 1),
(UUID(), 'dmitry.popov@example.com', '$2a$10$examplehash123456789', 'applicant', NULL, NOW() - INTERVAL 1 DAY, 1),
(UUID(), 'anna.volkova@example.com', '$2a$10$examplehash123456789', 'applicant', NULL, NOW(), 1),
(UUID(), 'sergey.lebedev@example.com', '$2a$10$examplehash123456789', 'applicant', NULL, NOW(), 1),
(UUID(), 'olga.morozova@example.com', '$2a$10$examplehash123456789', 'applicant', NULL, NOW(), 1),
(UUID(), 'mikhail.novikov@example.com', '$2a$10$examplehash123456789', 'applicant', NULL, NOW(), 1),
(UUID(), 'natalia.orlova@example.com', '$2a$10$examplehash123456789', 'applicant', NULL, NOW(), 1);


CREATE TABLE resumes (
    id CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin PRIMARY KEY DEFAULT (UUID()),
    full_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
    email VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
    phone VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
    resume_file_url VARCHAR(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
    summary TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
    specialty VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
    created_at DATETIME NOT NULL DEFAULT NOW(),
    user_id CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
    CONSTRAINT fk_resumes_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



-- 1. Резюме от зарегистрированных соискателей (10 шт)
INSERT INTO resumes (full_name, email, phone, resume_file_url, summary, specialty, created_at, user_id)
SELECT
    'Иван Петров',
    'ivan.petrov@example.com',
    '+7 (901) 123-45-67',
    'https://storage.example.com/resumes/ivan_petrov.pdf',
    'Студент МГТУ им. Баумана, 4 курс. Опыт в Python, Django, SQL. Участвовал в хакатонах.',
    'Разработка ПО',
    NOW() - INTERVAL 5 DAY,
    id
FROM users WHERE email = 'ivan.petrov@example.com' LIMIT 1;

INSERT INTO resumes (full_name, email, phone, resume_file_url, summary, specialty, created_at, user_id)
SELECT
    'Мария Соколова',
    'maria.sokolova@example.com',
    '+7 (902) 234-56-78',
    NULL,
    'Выпускница ВШЭ, факультет бизнес-информатики. Знаю Python, pandas, Power BI. Ищу стажировку в аналитике.',
    'Аналитика данных',
    NOW() - INTERVAL 4 DAY,
    id
FROM users WHERE email = 'maria.sokolova@example.com' LIMIT 1;

INSERT INTO resumes (full_name, email, phone, resume_file_url, summary, specialty, created_at, user_id)
SELECT
    'Алексей Смирнов',
    'alexey.smirnov@example.com',
    '+7 (903) 345-67-89',
    'https://storage.example.com/resumes/alexey_s.pdf',
    'Студент МФТИ, 3 курс. Занимаюсь ML, TensorFlow, OpenCV. Есть публикации в студенческих конференциях.',
    'Машинное обучение',
    NOW() - INTERVAL 3 DAY,
    id
FROM users WHERE email = 'alexey.smirnov@example.com' LIMIT 1;

INSERT INTO resumes (full_name, email, phone, resume_file_url, summary, specialty, created_at, user_id)
SELECT
    'Екатерина Кузнецова',
    'ekaterina.kuznetsova@example.com',
    '+7 (904) 456-78-90',
    NULL,
    'Дизайнер интерфейсов. Опыт в Figma, Adobe XD. Делала проекты для стартапов.',
    'UI/UX-дизайн',
    NOW() - INTERVAL 2 DAY,
    id
FROM users WHERE email = 'ekaterina.kuznetsova@example.com' LIMIT 1;

INSERT INTO resumes (full_name, email, phone, resume_file_url, summary, specialty, created_at, user_id)
SELECT
    'Дмитрий Попов',
    'dmitry.popov@example.com',
    '+7 (905) 567-89-01',
    'https://storage.example.com/resumes/d_popov_cv.pdf',
    'Backend-разработчик (Java, Spring Boot). Участвовал в разработке корпоративного портала.',
    'Java-разработка',
    NOW() - INTERVAL 1 DAY,
    id
FROM users WHERE email = 'dmitry.popov@example.com' LIMIT 1;

INSERT INTO resumes (full_name, email, phone, resume_file_url, summary, specialty, created_at, user_id)
SELECT
    'Анна Волкова',
    'anna.volkova@example.com',
    '+7 (906) 678-90-12',
    NULL,
    'Лингвист, изучаю NLP. Знаю Python, spaCy, NLTK. Хочу работать в области обработки естественного языка.',
    'NLP / Обработка текстов',
    NOW(),
    id
FROM users WHERE email = 'anna.volkova@example.com' LIMIT 1;

INSERT INTO resumes (full_name, email, phone, resume_file_url, summary, specialty, created_at, user_id)
SELECT
    'Сергей Лебедев',
    'sergey.lebedev@example.com',
    '+7 (907) 789-01-23',
    'https://storage.example.com/resumes/s_lebedev.pdf',
    'DevOps-инженер. Опыт с Docker, Kubernetes, GitLab CI. Администрирование Linux-серверов.',
    'DevOps',
    NOW(),
    id
FROM users WHERE email = 'sergey.lebedev@example.com' LIMIT 1;

INSERT INTO resumes (full_name, email, phone, resume_file_url, summary, specialty, created_at, user_id)
SELECT
    'Ольга Морозова',
    'olga.morozova@example.com',
    '+7 (908) 890-12-34',
    NULL,
    'Финансовый аналитик. Работала с Excel, Power BI, SQL. Ищу возможность развиваться в FinTech.',
    'Финансовый анализ',
    NOW(),
    id
FROM users WHERE email = 'olga.morozova@example.com' LIMIT 1;

INSERT INTO resumes (full_name, email, phone, resume_file_url, summary, specialty, created_at, user_id)
SELECT
    'Михаил Новиков',
    'mikhail.novikov@example.com',
    '+7 (909) 901-23-45',
    'https://storage.example.com/resumes/m_novikov_resume.pdf',
    'Frontend-разработчик (React, TypeScript). Делал SPA для e-commerce проектов.',
    'Frontend-разработка',
    NOW(),
    id
FROM users WHERE email = 'mikhail.novikov@example.com' LIMIT 1;

INSERT INTO resumes (full_name, email, phone, resume_file_url, summary, specialty, created_at, user_id)
SELECT
    'Наталья Орлова',
    'natalia.orlova@example.com',
    '+7 (910) 012-34-56',
    NULL,
    'Менеджер проектов. Опыт в IT-стартапах. Знаю Agile, Jira, Confluence.',
    'Управление проектами',
    NOW(),
    id
FROM users WHERE email = 'natalia.orlova@example.com' LIMIT 1;



------------------------------------------------------------------------------------------------------


INSERT INTO resumes (full_name, email, phone, resume_file_url, summary, specialty, created_at, user_id)
SELECT * FROM (
    SELECT
        'Артём Васильев' AS full_name,
        'artem.vasiliev@mail.ru' AS email,
        '+7 (911) 111-22-33' AS phone,
        NULL AS resume_file_url,
        'Студент ИТМО, 2 курс. Интересуюсь кибербезопасностью.' AS summary,
        'Информационная безопасность' AS specialty,
        NOW() - INTERVAL 1 HOUR AS created_at,
        NULL AS user_id
    UNION ALL
    SELECT 'Полина Козлова', 'polina.kozlova@inbox.ru', '+7 (912) 222-33-44', 'https://example.com/resumes/pkozl.pdf', 'Заканчиваю РЭУ им. Плеханова. Ищу стажировку в маркетинге.', 'Маркетинг', NOW() - INTERVAL 2 HOUR, NULL
    UNION ALL
    SELECT 'Тимофей Зайцев', 'tim.zaytsev@gmail.com', '+7 (913) 333-44-55', NULL, 'Python-разработчик, 1 год опыта. Django, REST API.', 'Python-разработка', NOW() - INTERVAL 3 HOUR, NULL
    UNION ALL
    SELECT 'Вероника Семёнова', 'v.semenova@yandex.ru', '+7 (914) 444-55-66', NULL, 'Графический дизайнер. Работаю в Adobe Illustrator и Photoshop.', 'Графический дизайн', NOW() - INTERVAL 4 HOUR, NULL
    UNION ALL
    SELECT 'Глеб Медведев', 'gleb.medvedev@mail.ru', '+7 (915) 555-66-77', 'https://example.com/resumes/gmedved.pdf', 'Студент ВШЭ. Участвую в олимпиадах по экономике.', 'Экономика', NOW() - INTERVAL 5 HOUR, NULL
    UNION ALL
    SELECT 'Алиса Виноградова', 'alisa.vinogradova@gmail.com', '+7 (916) 666-77-88', NULL, 'Тестировщик ПО. Знаю Selenium, Postman, SQL.', 'QA / Тестирование', NOW() - INTERVAL 6 HOUR, NULL
    UNION ALL
    SELECT 'Роман Егоров', 'roman.egorov@inbox.ru', '+7 (917) 777-88-99', NULL, 'Системный администратор. Опыт с Windows Server и сетями.', 'Системное администрирование', NOW() - INTERVAL 7 HOUR, NULL
    UNION ALL
    SELECT 'Дарья Фролова', 'darya.frolova@mail.ru', '+7 (918) 888-99-00', 'https://example.com/resumes/dfrolova.pdf', 'PR-менеджер. Организовывала мероприятия для стартапов.', 'PR / Коммуникации', NOW() - INTERVAL 8 HOUR, NULL
    UNION ALL
    SELECT 'Степан Никитин', 'stepan.nikitin@gmail.com', '+7 (919) 999-00-11', NULL, 'Embedded-разработчик. C, C++, микроконтроллеры STM32.', 'Embedded-системы', NOW() - INTERVAL 9 HOUR, NULL
    UNION ALL
    SELECT 'Ксения Логинова', 'ksenia.loginova@yandex.ru', '+7 (920) 000-11-22', NULL, 'HR-ассистент. Провожу первичные собеседования.', 'HR', NOW() - INTERVAL 10 HOUR, NULL

    UNION ALL SELECT 'Максим Белов', 'max.belov@mail.ru', '+7 (921) 111-22-33', NULL, 'Студент МИСиС. Интересуюсь материаловедением и инженерией.', 'Материаловедение', NOW() - INTERVAL 11 HOUR, NULL
    UNION ALL SELECT 'Анастасия Жукова', 'nastya.zhukova@gmail.com', '+7 (922) 222-33-44', 'https://example.com/resumes/azhukova.pdf', 'Копирайтер. Пишу тексты для сайтов и соцсетей.', 'Контент / Копирайтинг', NOW() - INTERVAL 12 HOUR, NULL
    UNION ALL SELECT 'Илья Соколов', 'ilya.sokolov@inbox.ru', '+7 (923) 333-44-55', NULL, 'Data engineer. Работаю с Airflow, Spark, Kafka.', 'Data Engineering', NOW() - INTERVAL 13 HOUR, NULL
    UNION ALL SELECT 'Елизавета Морозова', 'liza.morozova@mail.ru', '+7 (924) 444-55-66', NULL, 'Юрист. Специализация — IT-право и интеллектуальная собственность.', 'Юриспруденция', NOW() - INTERVAL 14 HOUR, NULL
    UNION ALL SELECT 'Арсений Павлов', 'arseniy.pavlov@gmail.com', '+7 (925) 555-66-77', 'https://example.com/resumes/apavlov.pdf', '3D-художник. Blender, Maya, Unity.', '3D-моделирование', NOW() - INTERVAL 15 HOUR, NULL
    UNION ALL SELECT 'Виктория Степанова', 'vika.stepanova@yandex.ru', '+7 (926) 666-77-88', NULL, 'Биоинформатик. Анализ геномных данных на Python.', 'Биоинформатика', NOW() - INTERVAL 16 HOUR, NULL
    UNION ALL SELECT 'Даниил Козлов', 'dan.kozlov@mail.ru', '+7 (927) 777-88-99', NULL, 'Mobile-разработчик (Kotlin). Делал приложения для Android.', 'Android-разработка', NOW() - INTERVAL 17 HOUR, NULL
    UNION ALL SELECT 'Софья Васнецова', 'sofiya.vasnetsova@gmail.com', '+7 (928) 888-99-00', 'https://example.com/resumes/svasnet.pdf', 'Продуктовый аналитик. A/B-тестирование, метрики, funnel-анализ.', 'Продуктовая аналитика', NOW() - INTERVAL 18 HOUR, NULL
    UNION ALL SELECT 'Матвей Захаров', 'matvey.zakharov@inbox.ru', '+7 (929) 999-00-11', NULL, 'Сетевой инженер. Настройка Cisco, маршрутизация, VLAN.', 'Сетевые технологии', NOW() - INTERVAL 19 HOUR, NULL
    UNION ALL SELECT 'Ульяна Сорокина', 'ulyana.sorokina@mail.ru', '+7 (930) 000-11-22', NULL, 'Логист. Опыт работы с 1С и транспортными компаниями.', 'Логистика', NOW() - INTERVAL 20 HOUR, NULL

    UNION ALL SELECT 'Лев Орлов', 'lev.orlov@gmail.com', '+7 (931) 111-22-33', NULL, 'Искусственный интеллект. Исследую LLM и генеративные модели.', 'AI / Генеративные модели', NOW() - INTERVAL 21 HOUR, NULL
    UNION ALL SELECT 'Милана Федорова', 'milana.fedorova@yandex.ru', '+7 (932) 222-33-44', 'https://example.com/resumes/mfedorova.pdf', 'SMM-менеджер. Веду аккаунты в Instagram и Telegram.', 'SMM', NOW() - INTERVAL 22 HOUR, NULL
    UNION ALL SELECT 'Егор Селиверстов', 'egor.seliverstov@mail.ru', '+7 (933) 333-44-55', NULL, 'Go-разработчик. Микросервисы, gRPC, PostgreSQL.', 'Go-разработка', NOW() - INTERVAL 23 HOUR, NULL
    UNION ALL SELECT 'Арина Волкова', 'arina.volkova@gmail.com', '+7 (934) 444-55-66', NULL, 'Психолог. Провожу консультации онлайн.', 'Психология', NOW() - INTERVAL 24 HOUR, NULL
    UNION ALL SELECT 'Тимур Гусев', 'timur.gusev@inbox.ru', '+7 (935) 555-66-77', 'https://example.com/resumes/tgusev.pdf', 'Архитектор ПО. Проектирую масштабируемые системы.', 'Software Architecture', NOW() - INTERVAL 25 HOUR, NULL
    UNION ALL SELECT 'Варвара Романова', 'varya.romanova@mail.ru', '+7 (936) 666-77-88', NULL, 'Переводчик (EN/RU). Техническая и художественная литература.', 'Переводы', NOW() - INTERVAL 26 HOUR, NULL
    UNION ALL SELECT 'Никита Яковлев', 'nikita.yakovlev@gmail.com', '+7 (937) 777-88-99', NULL, 'Game developer (Unity, C#). Делал инди-игры.', 'Game Development', NOW() - INTERVAL 27 HOUR, NULL
    UNION ALL SELECT 'Алёна Сазонова', 'alena.sazonova@yandex.ru', '+7 (938) 888-99-00', 'https://example.com/resumes/asazonova.pdf', 'Бизнес-аналитик. Сбор требований, написание ТЗ.', 'Бизнес-анализ', NOW() - INTERVAL 28 HOUR, NULL
    UNION ALL SELECT 'Руслан Максимов', 'ruslan.maksimov@mail.ru', '+7 (939) 999-00-11', NULL, 'iOS-разработчик (Swift). Публиковал приложения в App Store.', 'iOS-разработка', NOW() - INTERVAL 29 HOUR, NULL
    UNION ALL SELECT 'Кира Ильина', 'kira.ilina@gmail.com', '+7 (940) 000-11-22', NULL, 'Эколог. Участвую в проектах по устойчивому развитию.', 'Экология', NOW() - INTERVAL 30 HOUR, NULL

    UNION ALL SELECT 'Савелий Борисов', 'saveliy.borisov@inbox.ru', '+7 (941) 111-22-33', NULL, 'Cybersecurity researcher. CTF-игрок, пентестинг.', 'Кибербезопасность', NOW() - INTERVAL 31 HOUR, NULL
    UNION ALL SELECT 'Маргарита Виноградова', 'margo.vinogradova@mail.ru', '+7 (942) 222-33-44', 'https://example.com/resumes/mvinograd.pdf', 'Event-менеджер. Организация IT-конференций.', 'Организация мероприятий', NOW() - INTERVAL 32 HOUR, NULL
    UNION ALL SELECT 'Артур Григорьев', 'artur.grigoryev@gmail.com', '+7 (943) 333-44-55', NULL, 'Rust-разработчик. Системное программирование.', 'Rust', NOW() - INTERVAL 33 HOUR, NULL
    UNION ALL SELECT 'Диана Крылова', 'diana.krylova@yandex.ru', '+7 (944) 444-55-66', NULL, 'UX-исследователь. Провожу интервью и usability-тесты.', 'UX-исследования', NOW() - INTERVAL 34 HOUR, NULL
    UNION ALL SELECT 'Мирон Зуев', 'miron.zuev@mail.ru', '+7 (945) 555-66-77', 'https://example.com/resumes/mzuev.pdf', 'Quant developer. Python, C++, финансовые модели.', 'Quantitative Finance', NOW() - INTERVAL 35 HOUR, NULL
    UNION ALL SELECT 'Людмила Соколова', 'lyuda.sokolova@gmail.com', '+7 (946) 666-77-88', NULL, 'Археолог. Участвую в раскопках и обработке данных.', 'Археология', NOW() - INTERVAL 36 HOUR, NULL
    UNION ALL SELECT 'Григорий Потапов', 'grigory.potapov@inbox.ru', '+7 (947) 777-88-99', NULL, 'ML engineer. Деплой моделей, MLOps.', 'MLOps', NOW() - INTERVAL 37 HOUR, NULL
    UNION ALL SELECT 'Ева Михайлова', 'eva.mikhailova@mail.ru', '+7 (948) 888-99-00', 'https://example.com/resumes/emikhailova.pdf', 'HR-бренд. Развитие работодателя в соцсетях.', 'HR-брендинг', NOW() - INTERVAL 38 HOUR, NULL
    UNION ALL SELECT 'Даниэль Смирнов', 'daniel.smirnov@gmail.com', '+7 (949) 999-00-11', NULL, 'Blockchain developer. Solidity, Ethereum, DeFi.', 'Blockchain', NOW() - INTERVAL 39 HOUR, NULL
    UNION ALL SELECT 'Полина Андреева', 'polina.andreeva@yandex.ru', '+7 (950) 000-11-22', NULL, 'Фотограф. Специализируюсь на портретной съёмке.', 'Фотография', NOW() - INTERVAL 40 HOUR, NULL

    UNION ALL SELECT 'Владислав Чернов', 'vlad.chernov@mail.ru', '+7 (951) 111-22-33', NULL, 'Специалист по автоматизации тестирования.', 'Test Automation', NOW() - INTERVAL 41 HOUR, NULL
    UNION ALL SELECT 'Амина Назарова', 'amina.nazarova@gmail.com', '+7 (952) 222-33-44', 'https://example.com/resumes/anazarova.pdf', 'Маркетолог в IT. Работала с SaaS-продуктами.', 'IT-маркетинг', NOW() - INTERVAL 42 HOUR, NULL
    UNION ALL SELECT 'Игорь Фомин', 'igor.fomin@inbox.ru', '+7 (953) 333-44-55', NULL, 'Специалист по работе с данными. SQL, Python, Tableau.', 'Data Analysis', NOW() - INTERVAL 43 HOUR, NULL
    UNION ALL SELECT 'Стефания Петрова', 'stefania.petrova@mail.ru', '+7 (954) 444-55-66', NULL, 'Контент-менеджер. Веду корпоративный блог.', 'Контент-менеджмент', NOW() - INTERVAL 44 HOUR, NULL
    UNION ALL SELECT 'Ярослав Лебедев', 'yaroslav.lebedev@gmail.com', '+7 (955) 555-66-77', 'https://example.com/resumes/ylebedev.pdf', 'Специалист по информационным системам.', 'Информационные системы', NOW() - INTERVAL 45 HOUR, NULL
    UNION ALL SELECT 'Василиса Орлова', 'vasilisa.orlova@yandex.ru', '+7 (956) 666-77-88', NULL, 'Лингвист-программист. Работаю с чат-ботами.', 'NLP / Чат-боты', NOW() - INTERVAL 46 HOUR, NULL
    UNION ALL SELECT 'Марк Евдокимов', 'mark.evdokimov@mail.ru', '+7 (957) 777-88-99', NULL, 'Специалист по облачным технологиям (AWS).', 'Cloud Engineering', NOW() - INTERVAL 47 HOUR, NULL
    UNION ALL SELECT 'Аделина Семёнова', 'adelina.semenova@gmail.com', '+7 (958) 888-99-00', 'https://example.com/resumes/asemenova.pdf', 'Ассистент руководителя в IT-компании.', 'Ассистент руководителя', NOW() - INTERVAL 48 HOUR, NULL
    UNION ALL SELECT 'Богдан Кузнецов', 'bogdan.kuznetsov@inbox.ru', '+7 (959) 999-00-11', NULL, 'Специалист по цифровой трансформации.', 'Цифровая трансформация', NOW() - INTERVAL 49 HOUR, NULL
    UNION ALL SELECT 'Злата Воробьёва', 'zlata.vorobieva@mail.ru', '+7 (960) 000-11-22', NULL, 'Специалист по госзакупкам в IT.', 'Госзакупки', NOW() - INTERVAL 50 HOUR, NULL

    UNION ALL SELECT 'Эдуард Савельев', 'eduard.saveliev@gmail.com', '+7 (961) 111-22-33', NULL, 'Специалист по защите персональных данных.', 'Защита ПДн', NOW() - INTERVAL 51 HOUR, NULL
    UNION ALL SELECT 'Милена Калинина', 'milena.kalinina@yandex.ru', '+7 (962) 222-33-44', 'https://example.com/resumes/mkalinina.pdf', 'Специалист по подбору персонала (IT).', 'IT-рекрутинг', NOW() - INTERVAL 52 HOUR, NULL
    UNION ALL SELECT 'Аркадий Жуков', 'arkady.zhukov@mail.ru', '+7 (963) 333-44-55', NULL, 'Специалист по технической поддержке.', 'Техподдержка', NOW() - INTERVAL 53 HOUR, NULL
    UNION ALL SELECT 'Регина Новикова', 'regina.novikova@gmail.com', '+7 (964) 444-55-66', NULL, 'Специалист по обучению и развитию (L&D).', 'L&D', NOW() - INTERVAL 54 HOUR, NULL
    UNION ALL SELECT 'Тихон Морозов', 'tikhon.morozov@inbox.ru', '+7 (965) 555-66-77', 'https://example.com/resumes/tmorozov.pdf', 'Специалист по управлению знаниями.', 'Управление знаниями', NOW() - INTERVAL 55 HOUR, NULL
    UNION ALL SELECT 'Агата Полякова', 'agata.polyakova@mail.ru', '+7 (966) 666-77-88', NULL, 'Специалист по корпоративной культуре.', 'Корпоративная культура', NOW() - INTERVAL 56 HOUR, NULL
    UNION ALL SELECT 'Лука Соколов', 'luca.sokolov@gmail.com', '+7 (967) 777-88-99', NULL, 'Специалист по open-source проектам.', 'Open Source', NOW() - INTERVAL 57 HOUR, NULL
    UNION ALL SELECT 'Вера Титова', 'vera.titova@yandex.ru', '+7 (968) 888-99-00', 'https://example.com/resumes/vtitova.pdf', 'Специалист по международным проектам.', 'Международные проекты', NOW() - INTERVAL 58 HOUR, NULL
    UNION ALL SELECT 'Семён Фролов', 'semen.frolov@mail.ru', '+7 (969) 999-00-11', NULL, 'Специалист по стандартам качества (ISO).', 'Управление качеством', NOW() - INTERVAL 59 HOUR, NULL
    UNION ALL SELECT 'Алиса Смирнова', 'alisa.smirnova@gmail.com', '+7 (970) 000-11-22', NULL, 'Специалист по внутренним коммуникациям.', 'Внутренние коммуникации', NOW() - INTERVAL 60 HOUR, NULL
) AS tmp;



ALTER TABLE vacancy_skills
DROP FOREIGN KEY vacancy_skills_ibfk_1;


ALTER TABLE vacancies
MODIFY id CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT (UUID());


ALTER TABLE vacancy_skills
MODIFY vacancy_id CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL;


ALTER TABLE vacancy_skills
ADD CONSTRAINT vacancy_skills_ibfk_1
FOREIGN KEY (vacancy_id) REFERENCES vacancies(id) ON DELETE CASCADE;



CREATE TABLE applications (
    id CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin PRIMARY KEY DEFAULT (UUID()),
    vacancy_id CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    resume_id CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    status ENUM('new', 'viewed', 'invited', 'rejected') NOT NULL DEFAULT 'new',
    applied_at DATETIME NOT NULL DEFAULT NOW(),

    -- Внешние ключи
    CONSTRAINT fk_applications_vacancy FOREIGN KEY (vacancy_id) REFERENCES vacancies(id) ON DELETE CASCADE,
    CONSTRAINT fk_applications_resume FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE,

    -- Уникальность: нельзя откликнуться дважды одним резюме на одну вакансию
    UNIQUE KEY uk_vacancy_resume (vacancy_id, resume_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



-- 1
INSERT INTO applications (vacancy_id, resume_id, status, applied_at)
SELECT v.id, r.id, 'new', NOW() - INTERVAL 1 HOUR
FROM vacancies v, resumes r
WHERE v.title = 'Backend-разработчик (Python)' AND r.specialty = 'Python-разработка' LIMIT 1;

-- 2
INSERT INTO applications (vacancy_id, resume_id, status, applied_at)
SELECT v.id, r.id, 'viewed', NOW() - INTERVAL 3 HOUR
FROM vacancies v, resumes r
WHERE v.title = 'ML инженер (нейроинтерфейсы)' AND r.specialty = 'Машинное обучение' LIMIT 1;

-- 3
INSERT INTO applications (vacancy_id, resume_id, status, applied_at)
SELECT v.id, r.id, 'invited', NOW() - INTERVAL 5 HOUR
FROM vacancies v, resumes r
WHERE v.title = 'DevOps инженер' AND r.specialty = 'DevOps' LIMIT 1;

-- 4
INSERT INTO applications (vacancy_id, resume_id, status, applied_at)
SELECT v.id, r.id, 'new', NOW() - INTERVAL 7 HOUR
FROM vacancies v, resumes r
WHERE v.title = 'Frontend разработчик (Vue.js)' AND r.specialty = 'Frontend-разработка' LIMIT 1;

-- 5
INSERT INTO applications (vacancy_id, resume_id, status, applied_at)
SELECT v.id, r.id, 'viewed', NOW() - INTERVAL 9 HOUR
FROM vacancies v, resumes r
WHERE v.title = 'Full-stack разработчик (Node.js + React)' AND r.specialty = 'Java-разработка' LIMIT 1;

-- 6
INSERT INTO applications (vacancy_id, resume_id, status, applied_at)
SELECT v.id, r.id, 'rejected', NOW() - INTERVAL 11 HOUR
FROM vacancies v, resumes r
WHERE v.title = 'QA инженер' AND r.specialty = 'QA / Тестирование' LIMIT 1;

-- 7
INSERT INTO applications (vacancy_id, resume_id, status, applied_at)
SELECT v.id, r.id, 'new', NOW() - INTERVAL 13 HOUR
FROM vacancies v, resumes r
WHERE v.title = 'Data scientist (медицинская аналитика)' AND r.specialty = 'Data Analysis' LIMIT 1;

-- 8
INSERT INTO applications (vacancy_id, resume_id, status, applied_at)
SELECT v.id, r.id, 'invited', NOW() - INTERVAL 15 HOUR
FROM vacancies v, resumes r
WHERE v.title = 'Разработчик встроенного ПО (Embedded C)' AND r.specialty = 'Embedded-системы' LIMIT 1;

-- 9
INSERT INTO applications (vacancy_id, resume_id, status, applied_at)
SELECT v.id, r.id, 'viewed', NOW() - INTERVAL 17 HOUR
FROM vacancies v, resumes r
WHERE v.title = 'Инженер по информационной безопасности' AND r.specialty = 'Кибербезопасность' LIMIT 1;

-- 10
INSERT INTO applications (vacancy_id, resume_id, status, applied_at)
SELECT v.id, r.id, 'new', NOW() - INTERVAL 19 HOUR
FROM vacancies v, resumes r
WHERE v.title = 'Разработчик компьютерного зрения' AND r.specialty = 'AI / Генеративные модели' LIMIT 1;

-- 11
INSERT INTO applications (vacancy_id, resume_id, status, applied_at)
SELECT v.id, r.id, 'new', NOW() - INTERVAL 21 HOUR
FROM vacancies v, resumes r
WHERE v.description LIKE '%мобильных%' AND r.specialty = 'Android-разработка' LIMIT 1;

-- 12
INSERT INTO applications (vacancy_id, resume_id, status, applied_at)
SELECT v.id, r.id, 'viewed', NOW() - INTERVAL 23 HOUR
FROM vacancies v, resumes r
WHERE v.description LIKE '%мобильных%' AND r.specialty = 'iOS-разработка' LIMIT 1;

-- 13
INSERT INTO applications (vacancy_id, resume_id, status, applied_at)
SELECT v.id, r.id, 'rejected', NOW() - INTERVAL 25 HOUR
FROM vacancies v, resumes r
WHERE v.title = 'Bioinformatics engineer' AND r.specialty = 'NLP / Обработка текстов' LIMIT 1;

-- 14
INSERT INTO applications (vacancy_id, resume_id, status, applied_at)
SELECT v.id, r.id, 'new', NOW() - INTERVAL 27 HOUR
FROM vacancies v, resumes r
WHERE v.title = '3D-моделлер / инженер-дизайнер' AND r.specialty = 'UI/UX-дизайн' LIMIT 1;

-- 15
INSERT INTO applications (vacancy_id, resume_id, status, applied_at)
SELECT v.id, r.id, 'invited', NOW() - INTERVAL 29 HOUR
FROM vacancies v, resumes r
WHERE v.title = 'Data scientist (медицинская аналитика)' AND r.specialty = 'Аналитика данных' LIMIT 1;


