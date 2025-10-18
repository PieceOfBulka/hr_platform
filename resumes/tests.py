from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from resumes.models import Resume, WorkExperience, Education
from resumes.forms import ResumeForm, WorkExperienceForm, EducationForm

User = get_user_model()


class ResumeModelTest(TestCase):
    """Тесты для модели Resume"""
    
    def setUp(self):
        self.candidate_user = User.objects.create_user(
            username='candidate@test.com',
            email='candidate@test.com',
            password='testpass123',
            role=User.Role.CANDIDATE
        )
        
        self.resume_data = {
            'user': self.candidate_user,
            'title': 'Python разработчик',
            'summary': 'Опытный Python разработчик',
            'experience_level': Resume.ExperienceLevel.MIDDLE,
            'education_level': Resume.EducationLevel.BACHELOR,
            'university': 'МГУ им. М.В. Ломоносова',
            'faculty': 'Факультет ВМК',
            'graduation_year': 2017,
            'skills': 'Python, Django, PostgreSQL',
            'languages': 'Русский (родной), Английский (intermediate)',
            'salary_expectation': 200000,
            'is_remote': True,
            'is_relocation': False,
            'is_public': True,
        }
    
    def test_create_resume(self):
        """Тест создания резюме"""
        resume = Resume.objects.create(**self.resume_data)
        self.assertEqual(resume.title, 'Python разработчик')
        self.assertEqual(resume.user, self.candidate_user)
        self.assertEqual(resume.experience_level, Resume.ExperienceLevel.MIDDLE)
        self.assertEqual(resume.education_level, Resume.EducationLevel.BACHELOR)
        self.assertTrue(resume.is_public)
        self.assertTrue(resume.is_remote)
        self.assertFalse(resume.is_relocation)
    
    def test_resume_str(self):
        """Тест строкового представления резюме"""
        resume = Resume.objects.create(**self.resume_data)
        expected = f"{resume.user.get_full_name()} - {resume.title}"
        self.assertEqual(str(resume), expected)


class WorkExperienceModelTest(TestCase):
    """Тесты для модели WorkExperience"""
    
    def setUp(self):
        self.candidate_user = User.objects.create_user(
            username='candidate@test.com',
            email='candidate@test.com',
            password='testpass123',
            role=User.Role.CANDIDATE
        )
        
        self.resume = Resume.objects.create(
            user=self.candidate_user,
            title='Python разработчик',
            summary='Опытный Python разработчик',
        )
        
        self.work_experience_data = {
            'resume': self.resume,
            'company': 'Тестовая компания',
            'position': 'Python разработчик',
            'description': 'Разработка веб-приложений',
            'start_date': '2020-01-01',
            'end_date': '2023-12-31',
            'is_current': False,
        }
    
    def test_create_work_experience(self):
        """Тест создания опыта работы"""
        work_exp = WorkExperience.objects.create(**self.work_experience_data)
        self.assertEqual(work_exp.company, 'Тестовая компания')
        self.assertEqual(work_exp.position, 'Python разработчик')
        self.assertEqual(work_exp.resume, self.resume)
        self.assertFalse(work_exp.is_current)
    
    def test_current_work_experience(self):
        """Тест текущего места работы"""
        work_exp_data = self.work_experience_data.copy()
        work_exp_data.update({
            'end_date': None,
            'is_current': True,
        })
        
        work_exp = WorkExperience.objects.create(**work_exp_data)
        self.assertTrue(work_exp.is_current)
        self.assertIsNone(work_exp.end_date)
    
    def test_work_experience_str(self):
        """Тест строкового представления опыта работы"""
        work_exp = WorkExperience.objects.create(**self.work_experience_data)
        expected = f"{work_exp.position} в {work_exp.company}"
        self.assertEqual(str(work_exp), expected)


class EducationModelTest(TestCase):
    """Тесты для модели Education"""
    
    def setUp(self):
        self.candidate_user = User.objects.create_user(
            username='candidate@test.com',
            email='candidate@test.com',
            password='testpass123',
            role=User.Role.CANDIDATE
        )
        
        self.resume = Resume.objects.create(
            user=self.candidate_user,
            title='Python разработчик',
            summary='Опытный Python разработчик',
        )
        
        self.education_data = {
            'resume': self.resume,
            'institution': 'МГУ им. М.В. Ломоносова',
            'degree': 'Бакалавр прикладной математики и информатики',
            'start_date': '2013-09-01',
            'end_date': '2017-06-30',
            'is_current': False,
        }
    
    def test_create_education(self):
        """Тест создания образования"""
        education = Education.objects.create(**self.education_data)
        self.assertEqual(education.institution, 'МГУ им. М.В. Ломоносова')
        self.assertEqual(education.degree, 'Бакалавр прикладной математики и информатики')
        self.assertEqual(education.resume, self.resume)
        self.assertFalse(education.is_current)
    
    def test_current_education(self):
        """Тест текущего образования"""
        education_data = self.education_data.copy()
        education_data.update({
            'end_date': None,
            'is_current': True,
        })
        
        education = Education.objects.create(**education_data)
        self.assertTrue(education.is_current)
        self.assertIsNone(education.end_date)
    
    def test_education_str(self):
        """Тест строкового представления образования"""
        education = Education.objects.create(**self.education_data)
        expected = f"{education.degree} в {education.institution}"
        self.assertEqual(str(education), expected)


class ResumeFormTest(TestCase):
    """Тесты для формы ResumeForm"""
    
    def setUp(self):
        self.candidate_user = User.objects.create_user(
            username='candidate@test.com',
            email='candidate@test.com',
            password='testpass123',
            role=User.Role.CANDIDATE
        )
    
    def test_valid_resume_form(self):
        """Тест валидной формы резюме"""
        form_data = {
            'title': 'Python разработчик',
            'summary': 'Опытный Python разработчик',
            'experience_level': Resume.ExperienceLevel.MIDDLE,
            'education_level': Resume.EducationLevel.BACHELOR,
            'university': 'МГУ им. М.В. Ломоносова',
            'faculty': 'Факультет ВМК',
            'graduation_year': 2017,
            'skills': 'Python, Django, PostgreSQL',
            'languages': 'Русский (родной), Английский (intermediate)',
            'salary_expectation': 200000,
            'is_remote': True,
            'is_relocation': False,
            'is_public': True,
        }
        
        form = ResumeForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_resume_form(self):
        """Тест невалидной формы резюме"""
        form_data = {
            'title': '',  # Пустое название
            'summary': 'О себе',
        }
        
        form = ResumeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


class ResumeViewsTest(TestCase):
    """Тесты для представлений резюме"""
    
    def setUp(self):
        self.candidate_user = User.objects.create_user(
            username='candidate@test.com',
            email='candidate@test.com',
            password='testpass123',
            role=User.Role.CANDIDATE
        )
        
        self.hr_user = User.objects.create_user(
            username='hr@test.com',
            email='hr@test.com',
            password='testpass123',
            role=User.Role.HR,
            company='Тестовая компания'
        )
        
        self.resume = Resume.objects.create(
            user=self.candidate_user,
            title='Python разработчик',
            summary='Опытный Python разработчик',
            is_public=True,
        )
    
    def test_resume_list_view(self):
        """Тест списка резюме"""
        self.client.login(username='hr@test.com', password='testpass123')
        response = self.client.get(reverse('resumes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python разработчик')
    
    def test_resume_detail_view(self):
        """Тест детального просмотра резюме"""
        self.client.login(username='hr@test.com', password='testpass123')
        response = self.client.get(reverse('resumes:detail', args=[self.resume.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python разработчик')
        self.assertContains(response, 'Опытный Python разработчик')
    
    def test_resume_create_view_authenticated(self):
        """Тест создания резюме авторизованным пользователем"""
        self.client.login(username='candidate@test.com', password='testpass123')
        response = self.client.get(reverse('resumes:create'))
        self.assertEqual(response.status_code, 200)
    
    def test_resume_create_view_anonymous(self):
        """Тест создания резюме неавторизованным пользователем"""
        response = self.client.get(reverse('resumes:create'))
        self.assertEqual(response.status_code, 302)  # Редирект на логин
    
    def test_resume_update_view_owner(self):
        """Тест редактирования резюме владельцем"""
        self.client.login(username='candidate@test.com', password='testpass123')
        response = self.client.get(reverse('resumes:update', args=[self.resume.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_resume_update_view_not_owner(self):
        """Тест редактирования резюме не владельцем"""
        self.client.login(username='hr@test.com', password='testpass123')
        response = self.client.get(reverse('resumes:update', args=[self.resume.pk]))
        self.assertEqual(response.status_code, 302)  # Редирект на дашборд


class ResumeWorkflowTest(TestCase):
    """Тесты рабочего процесса резюме"""
    
    def setUp(self):
        self.candidate_user = User.objects.create_user(
            username='candidate@test.com',
            email='candidate@test.com',
            password='testpass123',
            role=User.Role.CANDIDATE
        )
    
    def test_resume_creation_workflow(self):
        """Тест процесса создания резюме"""
        # 1. Создание основного резюме
        resume = Resume.objects.create(
            user=self.candidate_user,
            title='Python разработчик',
            summary='Опытный Python разработчик',
            experience_level=Resume.ExperienceLevel.MIDDLE,
            education_level=Resume.EducationLevel.BACHELOR,
            skills='Python, Django, PostgreSQL',
            is_public=True,
        )
        
        self.assertEqual(resume.title, 'Python разработчик')
        self.assertTrue(resume.is_public)
        
        # 2. Добавление опыта работы
        work_exp = WorkExperience.objects.create(
            resume=resume,
            company='Предыдущая компания',
            position='Junior Python разработчик',
            description='Разработка веб-приложений',
            start_date='2020-01-01',
            end_date='2022-12-31',
        )
        
        self.assertEqual(work_exp.resume, resume)
        self.assertEqual(work_exp.company, 'Предыдущая компания')
        
        # 3. Добавление образования
        education = Education.objects.create(
            resume=resume,
            institution='МГУ им. М.В. Ломоносова',
            degree='Бакалавр прикладной математики и информатики',
            start_date='2013-09-01',
            end_date='2017-06-30',
        )
        
        self.assertEqual(education.resume, resume)
        self.assertEqual(education.institution, 'МГУ им. М.В. Ломоносова')
        
        # 4. Проверка связанных объектов
        self.assertEqual(resume.work_experiences.count(), 1)
        self.assertEqual(resume.educations.count(), 1)
    
    def test_resume_visibility(self):
        """Тест видимости резюме"""
        # Публичное резюме
        public_resume = Resume.objects.create(
            user=self.candidate_user,
            title='Публичное резюме',
            summary='Описание',
            is_public=True,
        )
        
        # Создаем другого кандидата для приватного резюме
        another_candidate = User.objects.create_user(
            username='another@test.com',
            email='another@test.com',
            password='testpass123',
            role=User.Role.CANDIDATE
        )
        
        # Приватное резюме
        private_resume = Resume.objects.create(
            user=another_candidate,
            title='Приватное резюме',
            summary='Описание',
            is_public=False,
        )
        
        # Проверка видимости для HR
        hr_user = User.objects.create_user(
            username='hr@test.com',
            email='hr@test.com',
            password='testpass123',
            role=User.Role.HR,
            company='Тестовая компания'
        )
        
        self.client.login(username='hr@test.com', password='testpass123')
        
        # Публичное резюме должно быть видно
        response = self.client.get(reverse('resumes:detail', args=[public_resume.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Приватное резюме не должно быть видно
        response = self.client.get(reverse('resumes:detail', args=[private_resume.pk]))
        self.assertEqual(response.status_code, 403)  # Доступ запрещен
