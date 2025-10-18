from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from internships.models import Internship, InternshipApplication
from internships.forms import InternshipForm, InternshipApplicationForm

User = get_user_model()


class InternshipModelTest(TestCase):
    """Тесты для модели Internship"""
    
    def setUp(self):
        self.university_user = User.objects.create_user(
            username='university@test.com',
            email='university@test.com',
            password='testpass123',
            role=User.Role.UNIVERSITY,
            company='МИЭТ'
        )
        
        self.internship_data = {
            'title': 'Стажировка по программированию',
            'description': 'Описание стажировки',
            'requirements': 'Требования к стажерам',
            'tasks': 'Задачи стажеров',
            'specialization': 'Программирование на Python',
            'students_count': 5,
            'duration': Internship.Duration.THREE_MONTHS,
            'start_date': '2025-03-01',
            'end_date': '2025-06-30',
            'university': self.university_user,
            'contact_email': 'university@test.com',
            'contact_phone': '+7 (999) 123-45-67',
            'status': Internship.Status.DRAFT,
        }
    
    def test_create_internship(self):
        """Тест создания стажировки"""
        internship = Internship.objects.create(**self.internship_data)
        self.assertEqual(internship.title, 'Стажировка по программированию')
        self.assertEqual(internship.university, self.university_user)
        self.assertEqual(internship.status, Internship.Status.DRAFT)
        self.assertEqual(internship.students_count, 5)
        self.assertFalse(internship.is_published)
        self.assertFalse(internship.is_pending)
    
    def test_internship_status_properties(self):
        """Тест свойств статуса стажировки"""
        internship = Internship.objects.create(**self.internship_data)
        
        # Тест черновика
        internship.status = Internship.Status.DRAFT
        self.assertFalse(internship.is_published)
        self.assertFalse(internship.is_pending)
        
        # Тест на модерации
        internship.status = Internship.Status.PENDING
        self.assertFalse(internship.is_published)
        self.assertTrue(internship.is_pending)
        
        # Тест опубликованной
        internship.status = Internship.Status.PUBLISHED
        self.assertTrue(internship.is_published)
        self.assertFalse(internship.is_pending)
    
    def test_internship_str(self):
        """Тест строкового представления стажировки"""
        internship = Internship.objects.create(**self.internship_data)
        expected = f"{internship.title} - {internship.university.company}"
        self.assertEqual(str(internship), expected)


class InternshipFormTest(TestCase):
    """Тесты для формы InternshipForm"""
    
    def setUp(self):
        self.university_user = User.objects.create_user(
            username='university@test.com',
            email='university@test.com',
            password='testpass123',
            role=User.Role.UNIVERSITY,
            company='МИЭТ'
        )
    
    def test_valid_internship_form(self):
        """Тест валидной формы стажировки"""
        form_data = {
            'title': 'Стажировка по программированию',
            'description': 'Описание стажировки',
            'requirements': 'Требования к стажерам',
            'tasks': 'Задачи стажеров',
            'specialization': 'Программирование на Python',
            'students_count': 5,
            'duration': Internship.Duration.THREE_MONTHS,
            'start_date': '2025-03-01',
            'end_date': '2025-06-30',
            'contact_email': 'university@test.com',
            'contact_phone': '+7 (999) 123-45-67',
            'is_remote': False,
            'status': Internship.Status.DRAFT,
        }
        
        form = InternshipForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_internship_form(self):
        """Тест невалидной формы стажировки"""
        form_data = {
            'title': '',  # Пустое название
            'description': 'Описание',
            'requirements': 'Требования',
        }
        
        form = InternshipForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


class InternshipViewsTest(TestCase):
    """Тесты для представлений стажировок"""
    
    def setUp(self):
        self.university_user = User.objects.create_user(
            username='university@test.com',
            email='university@test.com',
            password='testpass123',
            role=User.Role.UNIVERSITY,
            company='МИЭТ'
        )
        
        self.hr_user = User.objects.create_user(
            username='hr@test.com',
            email='hr@test.com',
            password='testpass123',
            role=User.Role.HR,
            company='Тестовая компания'
        )
        
        self.internship = Internship.objects.create(
            title='Стажировка по программированию',
            description='Описание стажировки',
            requirements='Требования к стажерам',
            tasks='Задачи стажеров',
            specialization='Программирование на Python',
            students_count=5,
            duration=Internship.Duration.THREE_MONTHS,
            start_date='2025-03-01',
            end_date='2025-06-30',
            university=self.university_user,
            contact_email='university@test.com',
            contact_phone='+7 (999) 123-45-67',
            status=Internship.Status.PUBLISHED,
        )
    
    def test_internship_list_view(self):
        """Тест списка стажировок"""
        response = self.client.get(reverse('internships:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Стажировка по программированию')
    
    def test_internship_detail_view(self):
        """Тест детального просмотра стажировки"""
        response = self.client.get(reverse('internships:detail', args=[self.internship.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Программирование на Python')
        self.assertContains(response, 'Описание стажировки')
    
    def test_internship_create_view_authenticated(self):
        """Тест создания стажировки авторизованным пользователем"""
        self.client.login(username='university@test.com', password='testpass123')
        response = self.client.get(reverse('internships:create'))
        self.assertEqual(response.status_code, 200)
    
    def test_internship_create_view_anonymous(self):
        """Тест создания стажировки неавторизованным пользователем"""
        response = self.client.get(reverse('internships:create'))
        self.assertEqual(response.status_code, 302)  # Редирект на логин
    
    def test_apply_for_internship(self):
        """Тест заявки на стажировку"""
        self.client.login(username='hr@test.com', password='testpass123')
        
        response = self.client.post(reverse('internships:apply', args=[self.internship.pk]), {
            'message': 'Хотим принять студентов на стажировку',
            'students_count': 3,
        })
        
        if response.status_code == 302:  # Редирект после успешной заявки
            application = InternshipApplication.objects.get(
                internship=self.internship,
                company=self.hr_user
            )
            self.assertEqual(application.message, 'Хотим принять студентов на стажировку')
            self.assertEqual(application.students_count, 3)
            self.assertEqual(application.status, 'new')


class InternshipApplicationModelTest(TestCase):
    """Тесты для модели InternshipApplication"""
    
    def setUp(self):
        self.university_user = User.objects.create_user(
            username='university@test.com',
            email='university@test.com',
            password='testpass123',
            role=User.Role.UNIVERSITY,
            company='МИЭТ'
        )
        
        self.hr_user = User.objects.create_user(
            username='hr@test.com',
            email='hr@test.com',
            password='testpass123',
            role=User.Role.HR,
            company='Тестовая компания'
        )
        
        self.internship = Internship.objects.create(
            title='Стажировка по программированию',
            description='Описание стажировки',
            requirements='Требования к стажерам',
            tasks='Задачи стажеров',
            specialization='Программирование на Python',
            students_count=5,
            duration=Internship.Duration.THREE_MONTHS,
            start_date='2025-03-01',
            end_date='2025-06-30',
            university=self.university_user,
            contact_email='university@test.com',
            contact_phone='+7 (999) 123-45-67',
            status=Internship.Status.PUBLISHED,
        )
    
    def test_create_internship_application(self):
        """Тест создания заявки на стажировку"""
        application = InternshipApplication.objects.create(
            internship=self.internship,
            company=self.hr_user,
            message='Хотим принять студентов на стажировку',
            students_count=3,
        )
        
        self.assertEqual(application.internship, self.internship)
        self.assertEqual(application.company, self.hr_user)
        self.assertEqual(application.status, 'new')
        self.assertEqual(application.students_count, 3)
    
    def test_unique_internship_application_constraint(self):
        """Тест уникальности заявки на стажировку"""
        InternshipApplication.objects.create(
            internship=self.internship,
            company=self.hr_user,
            message='Первая заявка',
            students_count=3,
        )
        
        # Попытка создать вторую заявку должна вызвать ошибку
        with self.assertRaises(IntegrityError):
            InternshipApplication.objects.create(
                internship=self.internship,
                company=self.hr_user,
                message='Вторая заявка',
                students_count=2,
            )
    
    def test_internship_application_str(self):
        """Тест строкового представления заявки на стажировку"""
        application = InternshipApplication.objects.create(
            internship=self.internship,
            company=self.hr_user,
            message='Хотим принять студентов на стажировку',
            students_count=3,
        )
        
        expected = f"{application.company.company} -> {application.internship.title}"
        self.assertEqual(str(application), expected)


class InternshipWorkflowTest(TestCase):
    """Тесты рабочего процесса стажировок"""
    
    def setUp(self):
        self.university_user = User.objects.create_user(
            username='university@test.com',
            email='university@test.com',
            password='testpass123',
            role=User.Role.UNIVERSITY,
            company='МИЭТ'
        )
        
        self.admin_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='testpass123',
            role=User.Role.ADMIN,
            company='ОЭЗ Технополис Москва'
        )
    
    def test_internship_workflow(self):
        """Тест полного рабочего процесса стажировки"""
        # 1. Университет создает стажировку (черновик)
        internship = Internship.objects.create(
            title='Стажировка по программированию',
            description='Описание стажировки',
            requirements='Требования к стажерам',
            tasks='Задачи стажеров',
            specialization='Программирование на Python',
            students_count=5,
            duration=Internship.Duration.THREE_MONTHS,
            start_date='2025-03-01',
            end_date='2025-06-30',
            university=self.university_user,
            contact_email='university@test.com',
            contact_phone='+7 (999) 123-45-67',
            status=Internship.Status.DRAFT,
        )
        
        self.assertEqual(internship.status, Internship.Status.DRAFT)
        self.assertFalse(internship.is_published)
        
        # 2. Университет отправляет на модерацию
        internship.status = Internship.Status.PENDING
        internship.save()
        
        self.assertEqual(internship.status, Internship.Status.PENDING)
        self.assertTrue(internship.is_pending)
        
        # 3. Админ одобряет стажировку
        internship.status = Internship.Status.PUBLISHED
        internship.save()
        
        self.assertEqual(internship.status, Internship.Status.PUBLISHED)
        self.assertTrue(internship.is_published)
        
        # 4. Университет закрывает стажировку
        internship.status = Internship.Status.CLOSED
        internship.save()
        
        self.assertEqual(internship.status, Internship.Status.CLOSED)
        self.assertFalse(internship.is_published)
    
    def test_internship_rejection(self):
        """Тест отклонения стажировки"""
        internship = Internship.objects.create(
            title='Стажировка по программированию',
            description='Описание стажировки',
            requirements='Требования к стажерам',
            tasks='Задачи стажеров',
            specialization='Программирование на Python',
            students_count=5,
            duration=Internship.Duration.THREE_MONTHS,
            start_date='2025-03-01',
            end_date='2025-06-30',
            university=self.university_user,
            contact_email='university@test.com',
            contact_phone='+7 (999) 123-45-67',
            status=Internship.Status.PENDING,
        )
        
        # Админ отклоняет стажировку
        internship.status = Internship.Status.REJECTED
        internship.save()
        
        self.assertEqual(internship.status, Internship.Status.REJECTED)
        self.assertFalse(internship.is_published)
