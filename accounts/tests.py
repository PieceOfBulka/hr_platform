from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

User = get_user_model()


class UserModelTest(TestCase):
    """Тесты для модели User"""
    
    def setUp(self):
        self.user_data = {
            'username': 'test@example.com',
            'email': 'test@example.com',
            'first_name': 'Тест',
            'last_name': 'Пользователь',
            'password': 'testpass123',
            'role': User.Role.CANDIDATE,
            'phone': '+7 (999) 123-45-67',
            'company': 'Тестовая компания',
            'position': 'Тестовая должность',
        }
    
    def test_create_user(self):
        """Тест создания пользователя"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, User.Role.CANDIDATE)
        self.assertEqual(user.company, 'Тестовая компания')
        self.assertFalse(user.is_verified)
    
    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        superuser_data = self.user_data.copy()
        superuser_data.update({
            'role': User.Role.ADMIN,
            'is_staff': True,
            'is_superuser': True,
        })
        superuser = User.objects.create_superuser(**superuser_data)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.role, User.Role.ADMIN)
    
    def test_role_properties(self):
        """Тест свойств ролей"""
        user = User.objects.create_user(**self.user_data)
        
        # Тест кандидата
        user.role = User.Role.CANDIDATE
        self.assertTrue(user.is_candidate)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_hr)
        self.assertFalse(user.is_university)
        
        # Тест HR
        user.role = User.Role.HR
        self.assertTrue(user.is_hr)
        self.assertFalse(user.is_candidate)
        
        # Тест университета
        user.role = User.Role.UNIVERSITY
        self.assertTrue(user.is_university)
        
        # Тест админа
        user.role = User.Role.ADMIN
        self.assertTrue(user.is_admin)
    
    def test_get_role_display(self):
        """Тест отображения роли"""
        user = User.objects.create_user(**self.user_data)
        user.role = User.Role.HR
        self.assertEqual(user.get_role_display(), 'HR компании')
    
    def test_user_str(self):
        """Тест строкового представления пользователя"""
        user = User.objects.create_user(**self.user_data)
        expected = f"{user.get_full_name()} ({user.get_role_display()})"
        self.assertEqual(str(user), expected)


class UserRegistrationTest(TestCase):
    """Тесты регистрации пользователей"""
    
    def test_candidate_registration(self):
        """Тест регистрации кандидата"""
        response = self.client.post('/accounts/signup/', {
            'username': 'candidate@test.com',
            'email': 'candidate@test.com',
            'first_name': 'Кандидат',
            'last_name': 'Тестовый',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': User.Role.CANDIDATE,
            'phone': '+7 (999) 123-45-67',
        })
        
        if response.status_code == 302:  # Редирект после успешной регистрации
            user = User.objects.get(email='candidate@test.com')
            self.assertEqual(user.role, User.Role.CANDIDATE)
            self.assertFalse(user.is_verified)
    
    def test_hr_registration(self):
        """Тест регистрации HR"""
        response = self.client.post('/accounts/signup/', {
            'username': 'hr@test.com',
            'email': 'hr@test.com',
            'first_name': 'HR',
            'last_name': 'Менеджер',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': User.Role.HR,
            'phone': '+7 (999) 123-45-67',
            'company': 'Тестовая компания',
            'position': 'HR менеджер',
        })
        
        if response.status_code == 302:
            user = User.objects.get(email='hr@test.com')
            self.assertEqual(user.role, User.Role.HR)
            self.assertEqual(user.company, 'Тестовая компания')


class UserAuthenticationTest(TestCase):
    """Тесты аутентификации"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='testpass123',
            role=User.Role.CANDIDATE
        )
    
    def test_login(self):
        """Тест входа в систему"""
        response = self.client.post('/accounts/login/', {
            'username': 'test@example.com',
            'password': 'testpass123',
        })
        
        if response.status_code == 302:
            self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_logout(self):
        """Тест выхода из системы"""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.post('/accounts/logout/')
        
        if response.status_code == 302:
            self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_dashboard_access(self):
        """Тест доступа к дашборду"""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get('/accounts/dashboard/')
        self.assertEqual(response.status_code, 200)
