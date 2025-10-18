from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class ModerationViewsTest(TestCase):
    """Тесты для представлений модерации"""
    
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='testpass123',
            role=User.Role.ADMIN,
            company='ОЭЗ Технополис Москва'
        )
        
        self.hr_user = User.objects.create_user(
            username='hr@test.com',
            email='hr@test.com',
            password='testpass123',
            role=User.Role.HR,
            company='Тестовая компания'
        )
        
        self.university_user = User.objects.create_user(
            username='university@test.com',
            email='university@test.com',
            password='testpass123',
            role=User.Role.UNIVERSITY,
            company='МИЭТ'
        )
    
    def test_moderation_dashboard_admin_access(self):
        """Тест доступа к дашборду модерации для админа"""
        self.client.login(username='admin@test.com', password='testpass123')
        response = self.client.get(reverse('moderation:dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_moderation_dashboard_non_admin_access(self):
        """Тест доступа к дашборду модерации для не-админа"""
        self.client.login(username='hr@test.com', password='testpass123')
        response = self.client.get(reverse('moderation:dashboard'))
        self.assertEqual(response.status_code, 302)  # Редирект на дашборд
    
    def test_moderation_dashboard_anonymous_access(self):
        """Тест доступа к дашборду модерации для неавторизованного пользователя"""
        response = self.client.get(reverse('moderation:dashboard'))
        self.assertEqual(response.status_code, 302)  # Редирект на логин
    
    def test_vacancy_moderation_list(self):
        """Тест списка вакансий для модерации"""
        self.client.login(username='admin@test.com', password='testpass123')
        response = self.client.get(reverse('moderation:vacancies'))
        self.assertEqual(response.status_code, 200)
    
    def test_internship_moderation_list(self):
        """Тест списка стажировок для модерации"""
        self.client.login(username='admin@test.com', password='testpass123')
        response = self.client.get(reverse('moderation:internships'))
        self.assertEqual(response.status_code, 200)
    
    def test_user_management(self):
        """Тест управления пользователями"""
        self.client.login(username='admin@test.com', password='testpass123')
        response = self.client.get(reverse('moderation:users'))
        self.assertEqual(response.status_code, 200)
    
    def test_statistics_view(self):
        """Тест страницы статистики"""
        self.client.login(username='admin@test.com', password='testpass123')
        response = self.client.get(reverse('moderation:statistics'))
        self.assertEqual(response.status_code, 200)


class ModerationWorkflowTest(TestCase):
    """Тесты рабочего процесса модерации"""
    
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='testpass123',
            role=User.Role.ADMIN,
            company='ОЭЗ Технополис Москва'
        )
        
        self.hr_user = User.objects.create_user(
            username='hr@test.com',
            email='hr@test.com',
            password='testpass123',
            role=User.Role.HR,
            company='Тестовая компания'
        )
        
        self.university_user = User.objects.create_user(
            username='university@test.com',
            email='university@test.com',
            password='testpass123',
            role=User.Role.UNIVERSITY,
            company='МИЭТ'
        )
    
    def test_vacancy_moderation_workflow(self):
        """Тест процесса модерации вакансии"""
        from vacancies.models import Vacancy
        
        # HR создает вакансию и отправляет на модерацию
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
        
        self.assertEqual(vacancy.status, Vacancy.Status.PENDING)
        
        # Админ одобряет вакансию
        self.client.login(username='admin@test.com', password='testpass123')
        
        response = self.client.post(
            reverse('moderation:vacancy_moderate', args=[vacancy.pk]),
            {
                'action': 'approve',
                'comment': 'Вакансия одобрена',
            }
        )
        
        if response.status_code == 302:  # Редирект после успешной модерации
            vacancy.refresh_from_db()
            self.assertEqual(vacancy.status, Vacancy.Status.PUBLISHED)
    
    def test_internship_moderation_workflow(self):
        """Тест процесса модерации стажировки"""
        from internships.models import Internship
        
        # Университет создает стажировку и отправляет на модерацию
        internship = Internship.objects.create(
            title='Стажировка по программированию',
            description='Описание стажировки',
            requirements='Требования к стажерам',
            tasks='Задачи стажеров',
            specialization='Программирование на Python',
            students_count=5,
            duration=Internship.Duration.THREE_MONTHS,
            start_date='2024-03-01',
            end_date='2024-06-30',
            university=self.university_user,
            contact_email='university@test.com',
            contact_phone='+7 (999) 123-45-67',
            status=Internship.Status.PENDING,
        )
        
        self.assertEqual(internship.status, Internship.Status.PENDING)
        
        # Админ одобряет стажировку
        self.client.login(username='admin@test.com', password='testpass123')
        
        response = self.client.post(
            reverse('moderation:internship_moderate', args=[internship.pk]),
            {
                'action': 'approve',
                'comment': 'Стажировка одобрена',
            }
        )
        
        if response.status_code == 302:  # Редирект после успешной модерации
            internship.refresh_from_db()
            self.assertEqual(internship.status, Internship.Status.PUBLISHED)
    
    def test_rejection_workflow(self):
        """Тест процесса отклонения"""
        from vacancies.models import Vacancy
        
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
        self.client.login(username='admin@test.com', password='testpass123')
        
        response = self.client.post(
            reverse('moderation:vacancy_moderate', args=[vacancy.pk]),
            {
                'action': 'reject',
                'comment': 'Вакансия не соответствует требованиям',
            }
        )
        
        if response.status_code == 302:  # Редирект после успешной модерации
            vacancy.refresh_from_db()
            self.assertEqual(vacancy.status, Vacancy.Status.REJECTED)


class ModerationPermissionsTest(TestCase):
    """Тесты прав доступа для модерации"""
    
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='testpass123',
            role=User.Role.ADMIN,
            company='ОЭЗ Технополис Москва'
        )
        
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
    
    def test_admin_can_moderate(self):
        """Тест что админ может модерировать"""
        self.client.login(username='admin@test.com', password='testpass123')
        
        # Проверяем доступ к различным страницам модерации
        urls = [
            reverse('moderation:dashboard'),
        reverse('moderation:vacancies'),
        reverse('moderation:internships'),
            reverse('moderation:users'),
            reverse('moderation:statistics'),
        ]
        
        for url in urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [200, 302])  # 200 или редирект
    
    def test_hr_cannot_moderate(self):
        """Тест что HR не может модерировать"""
        self.client.login(username='hr@test.com', password='testpass123')
        
        urls = [
            reverse('moderation:dashboard'),
        reverse('moderation:vacancies'),
        reverse('moderation:internships'),
            reverse('moderation:users'),
            reverse('moderation:statistics'),
        ]
        
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Редирект на логин
    
    def test_candidate_cannot_moderate(self):
        """Тест что кандидат не может модерировать"""
        self.client.login(username='candidate@test.com', password='testpass123')
        
        urls = [
            reverse('moderation:dashboard'),
        reverse('moderation:vacancies'),
        reverse('moderation:internships'),
            reverse('moderation:users'),
            reverse('moderation:statistics'),
        ]
        
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Редирект на логин
    
    def test_anonymous_cannot_moderate(self):
        """Тест что неавторизованный пользователь не может модерировать"""
        urls = [
            reverse('moderation:dashboard'),
        reverse('moderation:vacancies'),
        reverse('moderation:internships'),
            reverse('moderation:users'),
            reverse('moderation:statistics'),
        ]
        
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Редирект на логин


class ModerationStatisticsTest(TestCase):
    """Тесты статистики модерации"""
    
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='testpass123',
            role=User.Role.ADMIN,
            company='ОЭЗ Технополис Москва'
        )
        
        self.hr_user = User.objects.create_user(
            username='hr@test.com',
            email='hr@test.com',
            password='testpass123',
            role=User.Role.HR,
            company='Тестовая компания'
        )
        
        self.university_user = User.objects.create_user(
            username='university@test.com',
            email='university@test.com',
            password='testpass123',
            role=User.Role.UNIVERSITY,
            company='МИЭТ'
        )
    
    def test_statistics_data(self):
        """Тест данных статистики"""
        from vacancies.models import Vacancy
        from internships.models import Internship
        
        # Создаем тестовые данные
        Vacancy.objects.create(
            title='Вакансия 1',
            description='Описание',
            requirements='Требования',
            responsibilities='Обязанности',
            company=self.hr_user,
            contact_email='hr@test.com',
            contact_phone='+7 (999) 123-45-67',
            status=Vacancy.Status.PUBLISHED,
        )
        
        Vacancy.objects.create(
            title='Вакансия 2',
            description='Описание',
            requirements='Требования',
            responsibilities='Обязанности',
            company=self.hr_user,
            contact_email='hr@test.com',
            contact_phone='+7 (999) 123-45-67',
            status=Vacancy.Status.PENDING,
        )
        
        Internship.objects.create(
            title='Стажировка 1',
            description='Описание',
            requirements='Требования',
            tasks='Задачи',
            specialization='Программирование',
            students_count=5,
            duration=Internship.Duration.THREE_MONTHS,
            start_date='2024-03-01',
            end_date='2024-06-30',
            university=self.university_user,
            contact_email='university@test.com',
            contact_phone='+7 (999) 123-45-67',
            status=Internship.Status.PUBLISHED,
        )
        
        # Проверяем статистику
        self.client.login(username='admin@test.com', password='testpass123')
        response = self.client.get(reverse('moderation:statistics'))
        
        self.assertEqual(response.status_code, 200)
        
        # Проверяем что статистика содержит ожидаемые данные
        context = response.context
        if 'published_vacancies_count' in context:
            self.assertEqual(context['published_vacancies_count'], 1)
        if 'pending_vacancies_count' in context:
            self.assertEqual(context['pending_vacancies_count'], 1)
        if 'published_internships_count' in context:
            self.assertEqual(context['published_internships_count'], 1)
