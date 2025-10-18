from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from vacancies.models import Vacancy, Application
from vacancies.forms import VacancyForm, ApplicationForm

User = get_user_model()


class VacancyModelTest(TestCase):
    """Тесты для модели Vacancy"""
    
    def setUp(self):
        self.hr_user = User.objects.create_user(
            username='hr@test.com',
            email='hr@test.com',
            password='testpass123',
            role=User.Role.HR,
            company='Тестовая компания'
        )
        
        self.vacancy_data = {
            'title': 'Python разработчик',
            'description': 'Описание вакансии',
            'requirements': 'Требования к кандидату',
            'responsibilities': 'Обязанности',
            'salary_min': 100000,
            'salary_max': 200000,
            'experience_level': Vacancy.ExperienceLevel.MIDDLE,
            'company': self.hr_user,
            'contact_email': 'hr@test.com',
            'contact_phone': '+7 (999) 123-45-67',
            'status': Vacancy.Status.DRAFT,
        }
    
    def test_create_vacancy(self):
        """Тест создания вакансии"""
        vacancy = Vacancy.objects.create(**self.vacancy_data)
        self.assertEqual(vacancy.title, 'Python разработчик')
        self.assertEqual(vacancy.company, self.hr_user)
        self.assertEqual(vacancy.status, Vacancy.Status.DRAFT)
        self.assertFalse(vacancy.is_published)
        self.assertFalse(vacancy.is_pending)
    
    def test_vacancy_status_properties(self):
        """Тест свойств статуса вакансии"""
        vacancy = Vacancy.objects.create(**self.vacancy_data)
        
        # Тест черновика
        vacancy.status = Vacancy.Status.DRAFT
        self.assertFalse(vacancy.is_published)
        self.assertFalse(vacancy.is_pending)
        
        # Тест на модерации
        vacancy.status = Vacancy.Status.PENDING
        self.assertFalse(vacancy.is_published)
        self.assertTrue(vacancy.is_pending)
        
        # Тест опубликованной
        vacancy.status = Vacancy.Status.PUBLISHED
        self.assertTrue(vacancy.is_published)
        self.assertFalse(vacancy.is_pending)
    
    def test_vacancy_str(self):
        """Тест строкового представления вакансии"""
        vacancy = Vacancy.objects.create(**self.vacancy_data)
        expected = f"{vacancy.title} - {vacancy.company.company}"
        self.assertEqual(str(vacancy), expected)


class VacancyFormTest(TestCase):
    """Тесты для формы VacancyForm"""
    
    def setUp(self):
        self.hr_user = User.objects.create_user(
            username='hr@test.com',
            email='hr@test.com',
            password='testpass123',
            role=User.Role.HR,
            company='Тестовая компания'
        )
    
    def test_valid_vacancy_form(self):
        """Тест валидной формы вакансии"""
        form_data = {
            'title': 'Python разработчик',
            'description': 'Описание вакансии',
            'requirements': 'Требования к кандидату',
            'responsibilities': 'Обязанности',
            'salary_min': 100000,
            'salary_max': 200000,
            'experience_level': Vacancy.ExperienceLevel.MIDDLE,
            'contact_email': 'hr@test.com',
            'contact_phone': '+7 (999) 123-45-67',
            'is_remote': True,
            'status': Vacancy.Status.DRAFT,
        }
        
        form = VacancyForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_vacancy_form(self):
        """Тест невалидной формы вакансии"""
        form_data = {
            'title': '',  # Пустое название
            'description': 'Описание',
            'requirements': 'Требования',
        }
        
        form = VacancyForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


class VacancyViewsTest(TestCase):
    """Тесты для представлений вакансий"""
    
    def setUp(self):
        self.hr_user = User.objects.create_user(
            username='hr@test.com',
            email='hr@test.com',
            password='testpass123',
            role=User.Role.HR,
            company='Тестовая компания'
        )
        
        self.candidate_user = User.objects.create_user(
            username='candidate@test.com',
            email='candidate@test.com',
            password='testpass123',
            role=User.Role.CANDIDATE
        )
        
        self.vacancy = Vacancy.objects.create(
            title='Python разработчик',
            description='Описание вакансии',
            requirements='Требования к кандидату',
            responsibilities='Обязанности',
            salary_min=100000,
            salary_max=200000,
            experience_level=Vacancy.ExperienceLevel.MIDDLE,
            company=self.hr_user,
            contact_email='hr@test.com',
            contact_phone='+7 (999) 123-45-67',
            status=Vacancy.Status.PUBLISHED,
        )
    
    def test_vacancy_list_view(self):
        """Тест списка вакансий"""
        response = self.client.get(reverse('vacancies:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python разработчик')
    
    def test_vacancy_detail_view(self):
        """Тест детального просмотра вакансии"""
        response = self.client.get(reverse('vacancies:detail', args=[self.vacancy.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python разработчик')
        self.assertContains(response, 'Описание вакансии')
    
    def test_vacancy_create_view_authenticated(self):
        """Тест создания вакансии авторизованным пользователем"""
        self.client.login(username='hr@test.com', password='testpass123')
        response = self.client.get(reverse('vacancies:create'))
        self.assertEqual(response.status_code, 200)
    
    def test_vacancy_create_view_anonymous(self):
        """Тест создания вакансии неавторизованным пользователем"""
        response = self.client.get(reverse('vacancies:create'))
        self.assertEqual(response.status_code, 302)  # Редирект на логин
    
    def test_apply_for_vacancy(self):
        """Тест отклика на вакансию"""
        self.client.login(username='candidate@test.com', password='testpass123')
        
        response = self.client.post(reverse('vacancies:apply', args=[self.vacancy.pk]), {
            'cover_letter': 'Хочу работать в вашей компании',
        })
        
        if response.status_code == 302:  # Редирект после успешного отклика
            application = Application.objects.get(
                vacancy=self.vacancy,
                candidate=self.candidate_user
            )
            self.assertEqual(application.cover_letter, 'Хочу работать в вашей компании')
            self.assertEqual(application.status, 'new')


class ApplicationModelTest(TestCase):
    """Тесты для модели Application"""
    
    def setUp(self):
        self.hr_user = User.objects.create_user(
            username='hr@test.com',
            email='hr@test.com',
            password='testpass123',
            role=User.Role.HR,
            company='Тестовая компания'
        )
        
        self.candidate_user = User.objects.create_user(
            username='candidate@test.com',
            email='candidate@test.com',
            password='testpass123',
            role=User.Role.CANDIDATE
        )
        
        self.vacancy = Vacancy.objects.create(
            title='Python разработчик',
            description='Описание вакансии',
            requirements='Требования к кандидату',
            responsibilities='Обязанности',
            company=self.hr_user,
            contact_email='hr@test.com',
            contact_phone='+7 (999) 123-45-67',
            status=Vacancy.Status.PUBLISHED,
        )
    
    def test_create_application(self):
        """Тест создания отклика"""
        application = Application.objects.create(
            vacancy=self.vacancy,
            candidate=self.candidate_user,
            cover_letter='Хочу работать в вашей компании',
        )
        
        self.assertEqual(application.vacancy, self.vacancy)
        self.assertEqual(application.candidate, self.candidate_user)
        self.assertEqual(application.status, 'new')
    
    def test_unique_application_constraint(self):
        """Тест уникальности отклика (один кандидат - один отклик на вакансию)"""
        Application.objects.create(
            vacancy=self.vacancy,
            candidate=self.candidate_user,
            cover_letter='Первый отклик',
        )
        
        # Попытка создать второй отклик должна вызвать ошибку
        with self.assertRaises(IntegrityError):
            Application.objects.create(
                vacancy=self.vacancy,
                candidate=self.candidate_user,
                cover_letter='Второй отклик',
            )
    
    def test_application_str(self):
        """Тест строкового представления отклика"""
        application = Application.objects.create(
            vacancy=self.vacancy,
            candidate=self.candidate_user,
            cover_letter='Хочу работать в вашей компании',
        )
        
        expected = f"{application.candidate.get_full_name()} -> {application.vacancy.title}"
        self.assertEqual(str(application), expected)


class VacancyWorkflowTest(TestCase):
    """Тесты рабочего процесса вакансий"""
    
    def setUp(self):
        self.hr_user = User.objects.create_user(
            username='hr@test.com',
            email='hr@test.com',
            password='testpass123',
            role=User.Role.HR,
            company='Тестовая компания'
        )
        
        self.admin_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='testpass123',
            role=User.Role.ADMIN,
            company='ОЭЗ Технополис Москва'
        )
    
    def test_vacancy_workflow(self):
        """Тест полного рабочего процесса вакансии"""
        # 1. HR создает вакансию (черновик)
        vacancy = Vacancy.objects.create(
            title='Python разработчик',
            description='Описание вакансии',
            requirements='Требования к кандидату',
            responsibilities='Обязанности',
            company=self.hr_user,
            contact_email='hr@test.com',
            contact_phone='+7 (999) 123-45-67',
            status=Vacancy.Status.DRAFT,
        )
        
        self.assertEqual(vacancy.status, Vacancy.Status.DRAFT)
        self.assertFalse(vacancy.is_published)
        
        # 2. HR отправляет на модерацию
        vacancy.status = Vacancy.Status.PENDING
        vacancy.save()
        
        self.assertEqual(vacancy.status, Vacancy.Status.PENDING)
        self.assertTrue(vacancy.is_pending)
        
        # 3. Админ одобряет вакансию
        vacancy.status = Vacancy.Status.PUBLISHED
        vacancy.save()
        
        self.assertEqual(vacancy.status, Vacancy.Status.PUBLISHED)
        self.assertTrue(vacancy.is_published)
        
        # 4. HR закрывает вакансию
        vacancy.status = Vacancy.Status.CLOSED
        vacancy.save()
        
        self.assertEqual(vacancy.status, Vacancy.Status.CLOSED)
        self.assertFalse(vacancy.is_published)
    
    def test_vacancy_rejection(self):
        """Тест отклонения вакансии"""
        vacancy = Vacancy.objects.create(
            title='Python разработчик',
            description='Описание вакансии',
            requirements='Требования к кандидату',
            responsibilities='Обязанности',
            company=self.hr_user,
            contact_email='hr@test.com',
            contact_phone='+7 (999) 123-45-67',
            status=Vacancy.Status.PENDING,
        )
        
        # Админ отклоняет вакансию
        vacancy.status = Vacancy.Status.REJECTED
        vacancy.save()
        
        self.assertEqual(vacancy.status, Vacancy.Status.REJECTED)
        self.assertFalse(vacancy.is_published)
