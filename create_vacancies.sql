-- заполнение вакансиями и навыками


INSERT INTO vacancies (company_id, title, description, contact_info, status, publish_until, created_at, published_at)
VALUES
((SELECT id FROM companies WHERE contact_email='hr@nanocomposite.ru' LIMIT 1), 'Инженер-технолог по композитам', 'Разработка и оптимизация технологии производства композитных материалов нового поколения.', 'hr@nanocomposite.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@nanocomposite.ru' LIMIT 1), 'Специалист по контролю качества', 'Контроль параметров композитных изделий, проведение лабораторных испытаний.', 'hr@nanocomposite.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@medplant.ru' LIMIT 1), 'Инженер-конструктор медицинских изделий', 'Проектирование биосовместимых имплантов и корпусов устройств.', 'hr@medplant.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@medplant.ru' LIMIT 1), 'Оператор производственной линии', 'Работа на оборудовании по изготовлению медицинских изделий, контроль качества.', 'hr@medplant.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@sensor-tech.ru' LIMIT 1), 'Инженер-электронщик', 'Разработка сенсорных систем и тестирование прототипов.', 'hr@sensor-tech.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@inkoro.ru' LIMIT 1), 'Разработчик встроенного ПО (Embedded C)', 'Разработка микропрограмм для микроконтроллеров STM32, тестирование и отладка.', 'hr@inkoro.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@test-contact.ru' LIMIT 1), 'Инженер-разработчик тестовых систем', 'Разработка автоматизированных стендов, программирование ПЛК.', 'hr@test-contact.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@test-contact.ru' LIMIT 1), 'Тестировщик электроники', 'Проведение функциональных и электрических испытаний плат.', 'hr@test-contact.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@ecoplast.ru' LIMIT 1), 'Инженер-технолог по полимерам', 'Настройка экструзионных линий, контроль качества пластмасс.', 'hr@ecoplast.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@akrusbiomed.ru' LIMIT 1), 'Биотехнолог-аналитик', 'Проведение лабораторных анализов, контроль биореакторных процессов.', 'hr@akrusbiomed.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@goodwin-europe.ru' LIMIT 1), 'Инженер-программист АСУ ТП', 'Разработка ПО для промышленных контроллеров Siemens S7.', 'hr@goodwin-europe.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@sci-entertain.ru' LIMIT 1), 'Разработчик интерактивных приложений', 'Создание STEM-проектов с использованием Unity и AR-технологий.', 'hr@sci-entertain.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@rustech.ru' LIMIT 1), 'DevOps инженер', 'Поддержка CI/CD, контейнеризация, автоматизация инфраструктуры.', 'hr@rustech.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@gematech.ru' LIMIT 1), 'Инженер по лабораторным системам', 'Поддержка и настройка аналитических приборов.', 'hr@gematech.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@orthomoda.ru' LIMIT 1), '3D-моделлер / инженер-дизайнер', 'Создание цифровых моделей ортопедических изделий.', 'hr@orthomoda.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@amedart.ru' LIMIT 1), 'Инженер-технолог', 'Технологическая подготовка производства хирургических инструментов.', 'hr@amedart.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@biforcom.tech' LIMIT 1), 'Bioinformatics engineer', 'Анализ геномных данных, разработка скриптов на Python.', 'hr@biforcom.tech', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@microbor.ru' LIMIT 1), 'Инженер-микроэлектронщик', 'Проектирование и тестирование микросхем.', 'hr@microbor.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@diagnostica-m.ru' LIMIT 1), 'QA инженер', 'Тестирование лабораторных систем, автоматизация тестов.', 'hr@diagnostica-m.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@iva-tech.ru' LIMIT 1), 'Backend-разработчик (Python)', 'Разработка микросервисов для промышленных решений.', 'hr@iva-tech.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@fotoexpert.ru' LIMIT 1), 'Разработчик компьютерного зрения', 'Обработка изображений, нейросети, OpenCV.', 'hr@fotoexpert.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@euroelectro.ru' LIMIT 1), 'Инженер-электрик', 'Проектирование электрических схем и подбор оборудования.', 'hr@euroelectro.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@piezus.ru' LIMIT 1), 'Инженер по сенсорам', 'Разработка пьезоэлектрических систем и электроники управления.', 'hr@piezus.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@additive-eng.ru' LIMIT 1), 'Инженер 3D-печати', 'Подготовка 3D-моделей, работа с промышленными принтерами.', 'hr@additive-eng.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@digital-solutions.ru' LIMIT 1), 'Full-stack разработчик (Node.js + React)', 'Разработка внутренних порталов и клиентских приложений.', 'hr@digital-solutions.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@neoros.tech' LIMIT 1), 'ML инженер (нейроинтерфейсы)', 'Моделирование и обучение нейронных сетей для обработки сигналов мозга.', 'hr@neoros.tech', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@npo-composite.ru' LIMIT 1), 'Технолог-композитчик', 'Контроль параметров отверждения, ведение технологической документации.', 'hr@npo-composite.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@oncotarget.ru' LIMIT 1), 'Data scientist (медицинская аналитика)', 'Обработка медицинских данных, обучение ML-моделей.', 'hr@oncotarget.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@hirana-plus.ru' LIMIT 1), 'Frontend разработчик (Vue.js)', 'Разработка интерфейсов для медицинских приборов.', 'hr@hirana-plus.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@tzmoi.ru' LIMIT 1), 'Инженер по информационной безопасности', 'Настройка систем защиты и мониторинга инцидентов.', 'hr@tzmoi.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@rada-pharma.ru' LIMIT 1), 'Химик-аналитик', 'Контроль качества фармацевтических препаратов.', 'hr@rada-pharma.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@mesoformula.ru' LIMIT 1), 'Технолог-химик', 'Разработка и тестирование косметических формул.', 'hr@mesoformula.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@ntc-hightech.ru' LIMIT 1), 'Инженер-электроник', 'Разработка печатных плат, схемотехника, пайка прототипов.', 'hr@ntc-hightech.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@lasertech.ru' LIMIT 1), 'Инженер-оптик', 'Настройка лазерных систем и тестирование.', 'hr@lasertech.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@asez.ru' LIMIT 1), 'Инженер по энергоэффективности', 'Мониторинг энергопотребления, оптимизация систем.', 'hr@asez.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@promis.ru' LIMIT 1), 'Системный аналитик', 'Описание бизнес-процессов, формирование ТЗ.', 'hr@promis.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@signal-iot.ru' LIMIT 1), 'Инженер IoT', 'Разработка и настройка устройств связи и сенсоров.', 'hr@signal-iot.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@eltex.ru' LIMIT 1), 'Разработчик сетевого ПО (C++)', 'Создание драйверов и сетевых сервисов.', 'hr@eltex.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@eltex-energo.ru' LIMIT 1), 'Инженер-программист SCADA', 'Проектирование систем управления энергетикой.', 'hr@eltex-energo.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@promsvyaz.ru' LIMIT 1), 'Network Engineer', 'Настройка маршрутизаторов, VLAN, VPN.', 'hr@promsvyaz.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@intech-ai.ru' LIMIT 1), 'AI Research Engineer', 'Разработка интеллектуальных алгоритмов управления.', 'hr@intech-ai.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@kaspersky.ru' LIMIT 1), 'Security Engineer', 'Анализ уязвимостей, тестирование на проникновение.', 'hr@kaspersky.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@plc-tech.ru' LIMIT 1), 'Инженер-программист ПЛК', 'Разработка логики управления промышленными системами.', 'hr@plc-tech.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@diaclone.ru' LIMIT 1), 'Инженер по автоматизации тестов', 'Автоматизация проверок медицинских устройств.', 'hr@diaclone.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@vismo.ai' LIMIT 1), 'Computer Vision Engineer', 'Видеоаналитика, нейросети, Python / TensorFlow.', 'hr@vismo.ai', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@center-diagnostica.ru' LIMIT 1), 'Инженер-системотехник', 'Настройка оборудования для диагностики, поддержка сервисов.', 'hr@center-diagnostica.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@biomed.ru' LIMIT 1), 'Инженер КИПиА', 'Обслуживание контрольно-измерительных систем.', 'hr@biomed.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@ime.ru' LIMIT 1), 'Инженер-исследователь', 'Разработка микроэлектронных приборов и прототипов.', 'hr@ime.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@integral.ru' LIMIT 1), 'Разработчик VHDL / FPGA', 'Программирование ПЛИС и тестирование цифровых схем.', 'hr@integral.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@microwave-comp.ru' LIMIT 1), 'Инженер-радиотехник', 'Разработка СВЧ-устройств и тестирование параметров.', 'hr@microwave-comp.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@gravion.tech' LIMIT 1), 'Физик-инженер (квантовые сенсоры)', 'Работа с квантовыми детекторами и оптическими системами.', 'hr@gravion.tech', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW()),
((SELECT id FROM companies WHERE contact_email='hr@optel.ru' LIMIT 1), 'Оптик-системный инженер', 'Проектирование оптоэлектронных приборов.', 'hr@optel.ru', 'published', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW());



INSERT INTO vacancy_skills (vacancy_id, skill_id, is_required, priority)
VALUES
-- Backend-разработчик (Python) в IВА Технолоджис
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@iva-tech.ru' LIMIT 1) AND title='Backend-разработчик (Python)' LIMIT 1),
  1, TRUE, 5
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@iva-tech.ru' LIMIT 1) AND title='Backend-разработчик (Python)' LIMIT 1),
  28, TRUE, 4
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@iva-tech.ru' LIMIT 1) AND title='Backend-разработчик (Python)' LIMIT 1),
  18, TRUE, 4
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@iva-tech.ru' LIMIT 1) AND title='Backend-разработчик (Python)' LIMIT 1),
  11, TRUE, 3
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@iva-tech.ru' LIMIT 1) AND title='Backend-разработчик (Python)' LIMIT 1),
  21, FALSE, 2
),

-- Разработчик компьютерного зрения (Фотоэксперт)
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@fotoexpert.ru' LIMIT 1) AND title='Разработчик компьютерного зрения' LIMIT 1),
  37, TRUE, 5
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@fotoexpert.ru' LIMIT 1) AND title='Разработчик компьютерного зрения' LIMIT 1),
  38, TRUE, 5
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@fotoexpert.ru' LIMIT 1) AND title='Разработчик компьютерного зрения' LIMIT 1),
  32, TRUE, 4
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@fotoexpert.ru' LIMIT 1) AND title='Разработчик компьютерного зрения' LIMIT 1),
  33, FALSE, 3
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@fotoexpert.ru' LIMIT 1) AND title='Разработчик компьютерного зрения' LIMIT 1),
  18, TRUE, 3
),

-- DevOps инженер (Русская технологическая компания)
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@rustech.ru' LIMIT 1) AND title='DevOps инженер' LIMIT 1),
  65, TRUE, 4
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@rustech.ru' LIMIT 1) AND title='DevOps инженер' LIMIT 1),
  16, TRUE, 4
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@rustech.ru' LIMIT 1) AND title='DevOps инженер' LIMIT 1),
  17, TRUE, 5
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@rustech.ru' LIMIT 1) AND title='DevOps инженер' LIMIT 1),
  46, FALSE, 3
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@rustech.ru' LIMIT 1) AND title='DevOps инженер' LIMIT 1),
  50, FALSE, 2
),

-- ML инженер (Неорос)
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@neoros.tech' LIMIT 1) AND title='ML инженер (нейроинтерфейсы)' LIMIT 1),
  40, TRUE, 5
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@neoros.tech' LIMIT 1) AND title='ML инженер (нейроинтерфейсы)' LIMIT 1),
  41, TRUE, 5
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@neoros.tech' LIMIT 1) AND title='ML инженер (нейроинтерфейсы)' LIMIT 1),
  36, TRUE, 4
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@neoros.tech' LIMIT 1) AND title='ML инженер (нейроинтерфейсы)' LIMIT 1),
  39, FALSE, 3
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@neoros.tech' LIMIT 1) AND title='ML инженер (нейроинтерфейсы)' LIMIT 1),
  18, TRUE, 3
),

-- Embedded (INKORO)
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@inkoro.ru' LIMIT 1) AND title='Разработчик встроенного ПО (Embedded C)' LIMIT 1),
  94, TRUE, 5
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@inkoro.ru' LIMIT 1) AND title='Разработчик встроенного ПО (Embedded C)' LIMIT 1),
  95, TRUE, 4
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@inkoro.ru' LIMIT 1) AND title='Разработчик встроенного ПО (Embedded C)' LIMIT 1),
  96, TRUE, 4
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@inkoro.ru' LIMIT 1) AND title='Разработчик встроенного ПО (Embedded C)' LIMIT 1),
  18, TRUE, 3
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@inkoro.ru' LIMIT 1) AND title='Разработчик встроенного ПО (Embedded C)' LIMIT 1),
  98, FALSE, 2
),

-- Computer Vision (Vismo)
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@vismo.ai' LIMIT 1) AND title='Computer Vision Engineer' LIMIT 1),
  37, TRUE, 5
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@vismo.ai' LIMIT 1) AND title='Computer Vision Engineer' LIMIT 1),
  32, TRUE, 4
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@vismo.ai' LIMIT 1) AND title='Computer Vision Engineer' LIMIT 1),
  33, TRUE, 4
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@vismo.ai' LIMIT 1) AND title='Computer Vision Engineer' LIMIT 1),
  18, TRUE, 3
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@vismo.ai' LIMIT 1) AND title='Computer Vision Engineer' LIMIT 1),
  11, FALSE, 2
),

-- QA (Диагностика-М)
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@diagnostica-m.ru' LIMIT 1) AND title='QA инженер' LIMIT 1),
  93, TRUE, 4
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@diagnostica-m.ru' LIMIT 1) AND title='QA инженер' LIMIT 1),
  79, TRUE, 3
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@diagnostica-m.ru' LIMIT 1) AND title='QA инженер' LIMIT 1),
  80, TRUE, 3
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@diagnostica-m.ru' LIMIT 1) AND title='QA инженер' LIMIT 1),
  18, TRUE, 2
),

-- Инженер-программист АСУ ТП (Goodwin)
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@goodwin-europe.ru' LIMIT 1) AND title='Инженер-программист АСУ ТП' LIMIT 1),
  93, TRUE, 5
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@goodwin-europe.ru' LIMIT 1) AND title='Инженер-программист АСУ ТП' LIMIT 1),
  18, TRUE, 4
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@goodwin-europe.ru' LIMIT 1) AND title='Инженер-программист АСУ ТП' LIMIT 1),
  97, FALSE, 3
),

-- Frontend (Хирана+)
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@hirana-plus.ru' LIMIT 1) AND title='Frontend разработчик (Vue.js)' LIMIT 1),
  26, TRUE, 4
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@hirana-plus.ru' LIMIT 1) AND title='Frontend разработчик (Vue.js)' LIMIT 1),
  18, TRUE, 3
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@hirana-plus.ru' LIMIT 1) AND title='Frontend разработчик (Vue.js)' LIMIT 1),
  11, FALSE, 2
),

-- Инженер-электроник (НТЦ ХайТэк)
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@ntc-hightech.ru' LIMIT 1) AND title='Инженер-электроник' LIMIT 1),
  108, TRUE, 4
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@ntc-hightech.ru' LIMIT 1) AND title='Инженер-электроник' LIMIT 1),
  18, TRUE, 3
),
(
  (SELECT id FROM vacancies WHERE company_id=(SELECT id FROM companies WHERE contact_email='hr@ntc-hightech.ru' LIMIT 1) AND title='Инженер-электроник' LIMIT 1),
  11, FALSE, 2
);



