from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random

from vacancies.models import Vacancy
from internships.models import Internship
from resumes.models import Resume, WorkExperience, Education
from skills.models import Skill

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие данные перед заполнением',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Очистка существующих данных...')
            Vacancy.objects.all().delete()
            Internship.objects.all().delete()
            Resume.objects.all().delete()
            WorkExperience.objects.all().delete()
            Education.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Создание пользователей...')
        self.create_users()
        
        self.stdout.write('Создание навыков...')
        self.create_skills()
        
        self.stdout.write('Создание вакансий...')
        self.create_vacancies()
        
        self.stdout.write('Создание стажировок и практик...')
        self.create_internships()
        
        self.stdout.write('Создание резюме...')
        self.create_resumes()
        
        self.stdout.write('Данные успешно созданы!')

    def create_users(self):
        """Создание пользователей разных ролей"""
        
        # HR пользователи
        hr_companies = [
            ('hr@yandex.ru', 'Анна', 'Петрова', 'Яндекс', 'HR-менеджер'),
            ('hr@mail.ru', 'Дмитрий', 'Сидоров', 'Mail.ru Group', 'Senior HR Manager'),
            ('hr@sber.ru', 'Елена', 'Козлова', 'Сбербанк', 'HR Director'),
            ('hr@tinkoff.ru', 'Михаил', 'Иванов', 'Тинькофф', 'HR Specialist'),
            ('hr@ozon.ru', 'Ольга', 'Смирнова', 'OZON', 'HR Manager'),
            ('hr@wildberries.ru', 'Алексей', 'Кузнецов', 'Wildberries', 'HR Lead'),
            ('hr@vk.ru', 'Татьяна', 'Морозова', 'VK', 'HR Business Partner'),
            ('hr@rambler.ru', 'Сергей', 'Волков', 'Rambler', 'HR Manager'),
            ('hr@avito.ru', 'Наталья', 'Новикова', 'Авито', 'HR Director'),
            ('hr@1c.ru', 'Андрей', 'Лебедев', '1С', 'HR Manager'),
        ]
        
        for email, first_name, last_name, company, position in hr_companies:
            User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'company': company,
                    'position': position,
                    'role': 'hr',
                    'phone': f'+7 (495) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}',
                    'is_verified': True,
                    'is_active': True,
                }
            )

        # Представители вузов
        universities = [
            ('university@msu.ru', 'Иван', 'Петров', 'МГУ им. М.В. Ломоносова', 'Начальник отдела практик'),
            ('university@hse.ru', 'Мария', 'Сидорова', 'НИУ ВШЭ', 'Координатор стажировок'),
            ('university@mipt.ru', 'Александр', 'Козлов', 'МФТИ', 'Заместитель декана'),
            ('university@msuai.ru', 'Елена', 'Иванова', 'МГУАИ', 'Руководитель практик'),
            ('university@bmstu.ru', 'Дмитрий', 'Смирнов', 'МГТУ им. Н.Э. Баумана', 'Начальник УПП'),
            ('university@mirea.ru', 'Ольга', 'Кузнецова', 'МИРЭА', 'Координатор практик'),
            ('university@misis.ru', 'Сергей', 'Морозов', 'НИТУ МИСИС', 'Заместитель директора'),
            ('university@miet.ru', 'Татьяна', 'Волкова', 'МИЭТ', 'Руководитель практик'),
            ('university@mpei.ru', 'Андрей', 'Новиков', 'НИУ МЭИ', 'Начальник отдела'),
            ('university@mgimo.ru', 'Наталья', 'Лебедева', 'МГИМО', 'Координатор стажировок'),
        ]
        
        for email, first_name, last_name, company, position in universities:
            User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'company': company,
                    'position': position,
                    'role': 'university',
                    'phone': f'+7 (495) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}',
                    'is_verified': True,
                    'is_active': True,
                }
            )

        # Соискатели
        candidates = [
            ('candidate1@mail.ru', 'Алексей', 'Петров', 'Соискатель'),
            ('candidate2@mail.ru', 'Мария', 'Сидорова', 'Соискатель'),
            ('candidate3@mail.ru', 'Дмитрий', 'Козлов', 'Соискатель'),
            ('candidate4@mail.ru', 'Елена', 'Иванова', 'Соискатель'),
            ('candidate5@mail.ru', 'Михаил', 'Смирнов', 'Соискатель'),
            ('candidate6@mail.ru', 'Ольга', 'Кузнецова', 'Соискатель'),
            ('candidate7@mail.ru', 'Сергей', 'Морозов', 'Соискатель'),
            ('candidate8@mail.ru', 'Татьяна', 'Волкова', 'Соискатель'),
            ('candidate9@mail.ru', 'Андрей', 'Новиков', 'Соискатель'),
            ('candidate10@mail.ru', 'Наталья', 'Лебедева', 'Соискатель'),
            ('candidate11@mail.ru', 'Иван', 'Соколов', 'Соискатель'),
            ('candidate12@mail.ru', 'Анна', 'Попова', 'Соискатель'),
            ('candidate13@mail.ru', 'Владимир', 'Васильев', 'Соискатель'),
            ('candidate14@mail.ru', 'Екатерина', 'Семенова', 'Соискатель'),
            ('candidate15@mail.ru', 'Николай', 'Голубев', 'Соискатель'),
        ]
        
        for email, first_name, last_name, position in candidates:
            User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'position': position,
                    'role': 'candidate',
                    'phone': f'+7 (9{random.randint(10, 99)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}',
                    'is_verified': True,
                    'is_active': True,
                }
            )

    def create_skills(self):
        """Создание навыков"""
        # IT навыки (5% от общего количества)
        it_skills = [
            'Python', 'JavaScript', 'React', 'Django', 'PostgreSQL', 'Docker', 'Git'
        ]
        
        # Производственные навыки (95% от общего количества)
        production_skills = [
            'Сварка', 'Токарные работы', 'Фрезерные работы', 'Слесарные работы',
            'Электромонтаж', 'Покраска', 'Сборка', 'Клепка', 'Контроль качества',
            'Наладка оборудования', 'Работа на станках ЧПУ', 'Складской учет',
            'Логистика', 'Планирование производства', 'Техническое обслуживание',
            'Чтение чертежей', 'Работа с измерительными приборами', 'Безопасность труда',
            'Маркетинг', 'Продажи', 'Бухгалтерский учет', 'Экономический анализ',
            'Управление персоналом', 'Проектное управление', 'Документооборот',
            'Работа с металлом', 'Работа с пластмассой', 'Работа с деревом',
            'Промышленная автоматизация', 'Робототехника', 'Мехатроника',
            'Материаловедение', 'Технология производства', 'Стандартизация',
            'Сертификация', 'Экология производства', 'Охрана труда',
            'Пожарная безопасность', 'Электробезопасность', 'Первая помощь',
            'English', 'German', 'French', 'Spanish', 'Chinese', 'Japanese'
        ]
        
        # Объединяем все навыки
        skills_data = it_skills + production_skills
        
        for skill_name in skills_data:
            Skill.objects.get_or_create(name=skill_name)

    def create_vacancies(self):
        """Создание вакансий"""
        hr_users = User.objects.filter(role='hr')
        if not hr_users.exists():
            return

        # IT вакансии (5% от общего количества)
        it_vacancies = [
            {
                'title': 'Frontend разработчик',
                'description': 'Разработка пользовательских интерфейсов с использованием современных технологий.',
                'requirements': 'Опыт работы с React, JavaScript, HTML/CSS. Знание TypeScript будет плюсом.',
                'experience_level': 'middle',
                'salary_min': 120000,
                'salary_max': 180000,
                'is_remote': True,
            },
            {
                'title': 'Backend разработчик',
                'description': 'Разработка серверной части веб-приложений.',
                'requirements': 'Опыт работы с Python/Django или Node.js. Знание баз данных.',
                'experience_level': 'middle',
                'salary_min': 130000,
                'salary_max': 200000,
                'is_remote': False,
            },
        ]

        # Производственные вакансии (95% от общего количества)
        production_vacancies = [
            {
                'title': 'Маркетолог',
                'description': 'Разработка и реализация маркетинговых стратегий для продвижения продукции.',
                'requirements': 'Высшее образование в области маркетинга. Опыт работы в производственной сфере.',
                'experience_level': 'middle',
                'salary_min': 60000,
                'salary_max': 90000,
                'is_remote': False,
            },
            {
                'title': 'Инженер-технолог',
                'description': 'Разработка технологических процессов производства и контроль качества.',
                'requirements': 'Высшее техническое образование. Опыт работы в производстве.',
                'experience_level': 'middle',
                'salary_min': 70000,
                'salary_max': 110000,
                'is_remote': False,
            },
            {
                'title': 'Сборщик-клепальщик',
                'description': 'Сборка и клепка металлических конструкций согласно техническим требованиям.',
                'requirements': 'Среднее специальное образование. Опыт работы с металлом.',
                'experience_level': 'junior',
                'salary_min': 45000,
                'salary_max': 65000,
                'is_remote': False,
            },
            {
                'title': 'Сервисный инженер',
                'description': 'Обслуживание и ремонт производственного оборудования.',
                'requirements': 'Техническое образование. Опыт работы с промышленным оборудованием.',
                'experience_level': 'middle',
                'salary_min': 55000,
                'salary_max': 85000,
                'is_remote': False,
            },
            {
                'title': 'Маляр',
                'description': 'Покраска и отделка поверхностей в соответствии с технологическими требованиями.',
                'requirements': 'Опыт работы маляром. Знание материалов и технологий покраски.',
                'experience_level': 'junior',
                'salary_min': 40000,
                'salary_max': 60000,
                'is_remote': False,
            },
            {
                'title': 'Оператор станков ЧПУ',
                'description': 'Управление станками с числовым программным управлением.',
                'requirements': 'Среднее специальное образование. Опыт работы на станках ЧПУ.',
                'experience_level': 'middle',
                'salary_min': 50000,
                'salary_max': 75000,
                'is_remote': False,
            },
            {
                'title': 'Кладовщик',
                'description': 'Учет, хранение и выдача материалов и готовой продукции.',
                'requirements': 'Опыт работы на складе. Знание складского учета.',
                'experience_level': 'junior',
                'salary_min': 35000,
                'salary_max': 50000,
                'is_remote': False,
            },
            {
                'title': 'Контролер качества',
                'description': 'Контроль качества выпускаемой продукции и соответствие стандартам.',
                'requirements': 'Техническое образование. Опыт работы в области контроля качества.',
                'experience_level': 'middle',
                'salary_min': 50000,
                'salary_max': 80000,
                'is_remote': False,
            },
            {
                'title': 'Слесарь-сборщик',
                'description': 'Сборка и монтаж механических узлов и агрегатов.',
                'requirements': 'Среднее специальное образование. Опыт слесарных работ.',
                'experience_level': 'middle',
                'salary_min': 45000,
                'salary_max': 70000,
                'is_remote': False,
            },
            {
                'title': 'Электромонтер',
                'description': 'Монтаж, обслуживание и ремонт электрооборудования.',
                'requirements': 'Образование по специальности "Электромонтер". Группа допуска по электробезопасности.',
                'experience_level': 'middle',
                'salary_min': 50000,
                'salary_max': 80000,
                'is_remote': False,
            },
            {
                'title': 'Сварщик',
                'description': 'Сварочные работы различных видов металлов и сплавов.',
                'requirements': 'Удостоверение сварщика. Опыт сварочных работ.',
                'experience_level': 'middle',
                'salary_min': 55000,
                'salary_max': 85000,
                'is_remote': False,
            },
            {
                'title': 'Токарь',
                'description': 'Обработка деталей на токарных станках по чертежам.',
                'requirements': 'Среднее специальное образование. Опыт работы на токарных станках.',
                'experience_level': 'middle',
                'salary_min': 50000,
                'salary_max': 75000,
                'is_remote': False,
            },
            {
                'title': 'Фрезеровщик',
                'description': 'Обработка деталей на фрезерных станках.',
                'requirements': 'Образование по специальности "Фрезеровщик". Опыт работы на фрезерных станках.',
                'experience_level': 'middle',
                'salary_min': 50000,
                'salary_max': 75000,
                'is_remote': False,
            },
            {
                'title': 'Наладчик оборудования',
                'description': 'Наладка и регулировка производственного оборудования.',
                'requirements': 'Техническое образование. Опыт наладки промышленного оборудования.',
                'experience_level': 'senior',
                'salary_min': 70000,
                'salary_max': 100000,
                'is_remote': False,
            },
            {
                'title': 'Мастер смены',
                'description': 'Руководство производственной сменой и контроль выполнения плана.',
                'requirements': 'Высшее техническое образование. Опыт руководства персоналом.',
                'experience_level': 'senior',
                'salary_min': 80000,
                'salary_max': 120000,
                'is_remote': False,
            },
            {
                'title': 'Логист',
                'description': 'Организация логистических процессов и управление поставками.',
                'requirements': 'Высшее образование. Опыт работы в логистике.',
                'experience_level': 'middle',
                'salary_min': 60000,
                'salary_max': 90000,
                'is_remote': False,
            },
            {
                'title': 'Экономист',
                'description': 'Планирование и анализ экономических показателей производства.',
                'requirements': 'Высшее экономическое образование. Опыт работы в производственной сфере.',
                'experience_level': 'middle',
                'salary_min': 65000,
                'salary_max': 95000,
                'is_remote': False,
            },
            {
                'title': 'Бухгалтер',
                'description': 'Ведение бухгалтерского учета и составление отчетности.',
                'requirements': 'Высшее экономическое образование. Опыт бухгалтерского учета.',
                'experience_level': 'middle',
                'salary_min': 55000,
                'salary_max': 80000,
                'is_remote': False,
            },
        ]

        # Объединяем все вакансии
        vacancies_data = it_vacancies + production_vacancies

        for vacancy_data in vacancies_data:
            company = random.choice(hr_users)
            Vacancy.objects.get_or_create(
                title=vacancy_data['title'],
                company=company,
                defaults={
                    **vacancy_data,
                    'status': 'published',
                    'published_at': timezone.now() - timedelta(days=random.randint(1, 30)),
                }
            )

    def create_internships(self):
        """Создание стажировок и практик"""
        hr_users = User.objects.filter(role='hr')
        university_users = User.objects.filter(role='university')
        
        if not hr_users.exists() or not university_users.exists():
            return

        # Стажировки от HR (5% IT, 95% производственные)
        internships_data = [
            {
                'type': 'internship',
                'title': 'Стажировка Frontend разработчика',
                'description': 'Практическое изучение разработки пользовательских интерфейсов.',
                'requirements': 'Базовые знания HTML, CSS, JavaScript. Желание изучать React.',
                'tasks': 'Разработка компонентов интерфейса, работа с API, участие в code review.',
                'specialization': 'Frontend разработка',
                'duration': '3',
                'is_remote': True,
            },
            {
                'type': 'internship',
                'title': 'Стажировка инженера-технолога',
                'description': 'Изучение технологических процессов производства.',
                'requirements': 'Техническое образование. Интерес к производственным процессам.',
                'tasks': 'Изучение технологий, работа с документацией, участие в оптимизации процессов.',
                'specialization': 'Технология производства',
                'duration': '3',
                'is_remote': False,
            },
            {
                'type': 'internship',
                'title': 'Стажировка оператора станков ЧПУ',
                'description': 'Обучение работе на станках с числовым программным управлением.',
                'requirements': 'Среднее специальное образование. Базовые знания математики.',
                'tasks': 'Изучение программного обеспечения, настройка станков, обработка деталей.',
                'specialization': 'Обработка металлов',
                'duration': '2',
                'is_remote': False,
            },
            {
                'type': 'internship',
                'title': 'Стажировка контролера качества',
                'description': 'Изучение методов контроля качества продукции.',
                'requirements': 'Техническое образование. Внимательность к деталям.',
                'tasks': 'Контроль качества, работа с измерительными приборами, ведение документации.',
                'specialization': 'Контроль качества',
                'duration': '2',
                'is_remote': False,
            },
            {
                'type': 'internship',
                'title': 'Стажировка маркетолога',
                'description': 'Изучение маркетинговых стратегий в производственной сфере.',
                'requirements': 'Образование в области маркетинга или экономики.',
                'tasks': 'Анализ рынка, разработка маркетинговых кампаний, работа с клиентами.',
                'specialization': 'Маркетинг',
                'duration': '3',
                'is_remote': True,
            },
        ]

        # Практики от университетов (5% IT, 95% производственные)
        practices_data = [
            {
                'type': 'practice',
                'title': 'Практика по программированию',
                'description': 'Практическое изучение основ программирования и разработки ПО.',
                'requirements': 'Знание основ программирования, математики.',
                'tasks': 'Изучение алгоритмов, разработка простых приложений, работа в команде.',
                'specialization': 'Программирование',
                'duration': '2',
                'is_remote': False,
            },
            {
                'type': 'practice',
                'title': 'Практика по машиностроению',
                'description': 'Изучение основ машиностроения и производственных процессов.',
                'requirements': 'Знание математики, физики. Интерес к техническим дисциплинам.',
                'tasks': 'Изучение оборудования, работа с чертежами, участие в производственном процессе.',
                'specialization': 'Машиностроение',
                'duration': '3',
                'is_remote': False,
            },
            {
                'type': 'practice',
                'title': 'Практика по технологии производства',
                'description': 'Изучение технологических процессов и методов производства.',
                'requirements': 'Знание химии, физики. Базовые знания материаловедения.',
                'tasks': 'Изучение технологий, работа с материалами, контроль качества.',
                'specialization': 'Технология производства',
                'duration': '2',
                'is_remote': False,
            },
            {
                'type': 'practice',
                'title': 'Практика по автоматизации',
                'description': 'Изучение систем автоматизации производственных процессов.',
                'requirements': 'Знание основ автоматизации, программирования.',
                'tasks': 'Изучение систем управления, программирование ПЛК, настройка оборудования.',
                'specialization': 'Автоматизация',
                'duration': '3',
                'is_remote': False,
            },
            {
                'type': 'practice',
                'title': 'Практика по экономике предприятия',
                'description': 'Изучение экономических процессов на производственном предприятии.',
                'requirements': 'Знание экономики, математики. Интерес к бизнес-процессам.',
                'tasks': 'Анализ экономических показателей, планирование, работа с документацией.',
                'specialization': 'Экономика',
                'duration': '2',
                'is_remote': True,
            },
            {
                'type': 'practice',
                'title': 'Практика по маркетингу',
                'description': 'Изучение маркетинговых стратегий и продвижения продукции.',
                'requirements': 'Знание основ маркетинга, коммуникативные навыки.',
                'tasks': 'Анализ рынка, разработка маркетинговых материалов, работа с клиентами.',
                'specialization': 'Маркетинг',
                'duration': '2',
                'is_remote': True,
            },
        ]

        # Создаем стажировки от HR
        for internship_data in internships_data:
            company = random.choice(hr_users)
            start_date = timezone.now().date() + timedelta(days=random.randint(7, 30))
            end_date = start_date + timedelta(days=int(internship_data['duration']) * 30)
            
            Internship.objects.get_or_create(
                title=internship_data['title'],
                organization=company,
                defaults={
                    **internship_data,
                    'start_date': start_date,
                    'end_date': end_date,
                    'contact_email': company.email,
                    'contact_phone': company.phone,
                    'status': 'published',
                    'published_at': timezone.now() - timedelta(days=random.randint(1, 15)),
                }
            )

        # Создаем практики от университетов
        for practice_data in practices_data:
            university = random.choice(university_users)
            start_date = timezone.now().date() + timedelta(days=random.randint(7, 30))
            end_date = start_date + timedelta(days=int(practice_data['duration']) * 30)
            
            Internship.objects.get_or_create(
                title=practice_data['title'],
                organization=university,
                defaults={
                    **practice_data,
                    'start_date': start_date,
                    'end_date': end_date,
                    'contact_email': university.email,
                    'contact_phone': university.phone,
                    'status': 'published',
                    'published_at': timezone.now() - timedelta(days=random.randint(1, 15)),
                }
            )

    def create_resumes(self):
        """Создание резюме для соискателей"""
        candidates = User.objects.filter(role='candidate')
        skills = list(Skill.objects.all())
        
        if not candidates.exists() or not skills:
            return

        # IT резюме (5% от общего количества)
        it_resume_titles = [
            'Frontend разработчик',
            'Backend разработчик',
        ]
        
        # Производственные резюме (95% от общего количества)
        production_resume_titles = [
            'Маркетолог',
            'Инженер-технолог',
            'Сборщик-клепальщик',
            'Сервисный инженер',
            'Маляр',
            'Оператор станков ЧПУ',
            'Кладовщик',
            'Контролер качества',
            'Слесарь-сборщик',
            'Электромонтер',
            'Сварщик',
            'Токарь',
            'Фрезеровщик',
            'Наладчик оборудования',
            'Мастер смены',
            'Логист',
            'Экономист',
            'Бухгалтер',
            'Менеджер по продажам',
            'Специалист по закупкам',
            'Инженер по охране труда',
            'Технолог',
            'Механик',
            'Оператор производственной линии',
            'Упаковщик',
            'Грузчик',
            'Водитель погрузчика',
            'Складской работник',
            'Приемщик товара',
            'Комплектовщик',
        ]
        
        # Объединяем все резюме
        resume_titles = it_resume_titles + production_resume_titles

        for candidate in candidates:
            # Создаем резюме
            resume_title = random.choice(resume_titles)
            resume, created = Resume.objects.get_or_create(
                user=candidate,
                defaults={
                    'title': resume_title,
                    'summary': f'Опытный специалист в области {resume_title.lower()}. Готов к новым вызовам и профессиональному росту.',
                    'is_public': random.choice([True, False]),
                }
            )

            if created:
                # Добавляем случайные навыки
                candidate_skills = random.sample(skills, random.randint(3, 8))
                resume.skills.set(candidate_skills)

                # Создаем опыт работы
                if random.choice([True, False]):
                    WorkExperience.objects.create(
                        resume=resume,
                        company=f'Компания {random.randint(1, 100)}',
                        position=resume_title,
                        start_date=timezone.now().date() - timedelta(days=random.randint(365, 1095)),
                        end_date=timezone.now().date() - timedelta(days=random.randint(30, 365)),
                        description='Выполнение задач по разработке и поддержке проектов.',
                    )

                # Создаем образование
                if resume_title in it_resume_titles:
                    # IT образование
                    universities = ['МГУ', 'МФТИ', 'НИУ ВШЭ', 'МГТУ', 'МИРЭА', 'МГИМО']
                    field_of_study = 'Информатика и вычислительная техника'
                else:
                    # Производственное образование
                    universities = ['МГТУ им. Н.Э. Баумана', 'МИРЭА', 'МГУАИ', 'МГТУ', 'МГУ', 'НИУ ВШЭ']
                    fields_of_study = [
                        'Машиностроение', 'Технология машиностроения', 'Автоматизация технологических процессов',
                        'Электроэнергетика и электротехника', 'Технология производства', 'Металлургия',
                        'Химическая технология', 'Экономика', 'Менеджмент', 'Маркетинг', 'Бухгалтерский учет'
                    ]
                    field_of_study = random.choice(fields_of_study)
                
                Education.objects.create(
                    resume=resume,
                    institution=random.choice(universities),
                    degree='Бакалавр',
                    field_of_study=field_of_study,
                    start_date=timezone.now().date() - timedelta(days=random.randint(1460, 2190)),
                    end_date=timezone.now().date() - timedelta(days=random.randint(365, 1095)),
                )
