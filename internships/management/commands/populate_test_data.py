from django.core.management.base import BaseCommand
from django.apps import apps
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
import random
import re
import traceback

PROFESSIONS = [
    "Инженер-конструктор", "Технолог", "Инженер по автоматизации", "Инженер-электроник",
    "Инженер по качеству", "Производственный менеджер", "Оператор станков с ЧПУ", "Инженер по робототехнике",
    "Специалист по 3D-печати", "Инженер-химик", "Инженер по микросхемам", "Проектировщик",
    "Специалист по композитным материалам", "Механик", "Электромонтажник", "Лаборант",
    "Менеджер по снабжению", "Инженер по испытаниям", "Разработчик электроники", "Инженер-технолог машиностроения",
    "Инженер по мехатронике", "Инженер по метрологии", "Инженер по производственному контролю",
    "Оператор производственной линии", "Инженер по автоматизированным системам управления",
    "Конструктор-разработчик", "Инженер по аддитивным технологиям", "Специалист по контролю качества",
    "Инженер по проектированию", "Инженер по техническому обслуживанию"
]

COMPANIES = [
    "ТЕХНОПОЛИС МОСКВА", "Микрон", "Ситроникс", "Ангстрем", "Элтекс",
    "Радар ММС", "НПО Наука", "Москабельмет", "Элемент", "Росэлектроника",
]

CITIES = ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Kazan"]

def slugify_name(name):
    s = name.lower()
    s = re.sub(r'\s+', '_', s)
    s = re.sub(r'[^a-z0-9_]', '', s)
    return s[:30] or 'user'

def make_vacancy_payload(title):
    salary_min = random.randint(40000, 200000)
    salary_max = salary_min + random.randint(5000, 100000)
    now = timezone.now()
    return {
        "title": title,
        "description": f"{title} — интересная позиция в динамичной команде.",
        "requirements": "Опыт работы от 1 года; английский B1+.",
        "responsibilities": "Разработка, участие в планировании, код-ревью.",
        "salary_min": salary_min,
        "salary_max": salary_max,
        "experience_level": random.choice(["Junior", "Middle", "Senior"]),
        "company": random.choice(COMPANIES),
        "status": random.choice(["open", "closed"]),
        "contact_email": "hr@example.com",
        "contact_phone": "+7 900 000 00 00",
        "is_remote": random.choice([True, False]),
        "auto_close_date": (now + timedelta(days=random.randint(30, 120))).date(),
        "published_at": now,
    }

def make_internship_payload(title):
    now = timezone.now()
    duration_weeks = random.choice([4, 6, 8, 12, 16])
    start = now.date() + timedelta(days=random.randint(7, 30))
    end = start + timedelta(weeks=duration_weeks)
    return {
        "title": title,
        "description": f"{title} — стажировка с наставником и реальными задачами.",
        "requirements": "Желание учиться, базовые знания по теме.",
        "tasks": "Помощь в проектах, тестирование, написание кода.",
        "specialization": random.choice(["Research", "Development", "QA", "Design"]),
        "duration": duration_weeks,
        "start_date": start,
        "end_date": end,  # ensure NOT NULL
        "company": random.choice(COMPANIES),
        "status": random.choice(["open", "closed"]),
        "contact_email": "interns@example.com",
        "contact_phone": "+7 900 000 00 01",
        "is_remote": random.choice([True, False]),
        "published_at": now,
    }

def ensure_company_users(write, style):
    User = get_user_model()
    users = {}
    for name in COMPANIES:
        username = slugify_name(name)
        try:
            user, created = User.objects.get_or_create(username=username, defaults={"email": f"{username}@example.com"})
            if created:
                try:
                    if hasattr(User.objects, "create_user"):
                        user.set_password("password123")
                        user.save()
                except Exception:
                    pass
            users[name] = user
            write(style.SUCCESS(f"Prepared user for company '{name}' -> username='{username}' (id={user.pk})"))
        except Exception as e:
            write(style.WARNING(f"Failed to prepare user for '{name}': {e}"))
            for line in traceback.format_exc().splitlines():
                write(line)
    return users

def create_entries(app_label, model_name, count, write, style, company_users, payload_maker):
    try:
        Model = apps.get_model(app_label, model_name)
    except LookupError:
        write(style.WARNING(f"Model {app_label}.{model_name} not found"))
        return 0

    field_names = [
        f.name for f in Model._meta.get_fields()
        if getattr(f, "concrete", False) and not getattr(f, "auto_created", False)
    ]
    write(f"Found model {app_label}.{model_name}, fields: {field_names}")

    created = 0
    attempts = 0
    while created < count and attempts < count * 3:
        attempts += 1
        title = random.choice(PROFESSIONS)
        payload = payload_maker(title)
        allowed = {k: v for k, v in payload.items() if k in field_names}

        # Replace company string with User instance if company field is FK to User
        if "company" in allowed:
            try:
                field = Model._meta.get_field("company")
                rel_model = getattr(field, "related_model", None)
                User = get_user_model()
                if rel_model is not None and (rel_model == User or rel_model.__name__ == User.__name__):
                    company_name = allowed["company"]
                    user_obj = company_users.get(company_name)
                    if user_obj:
                        allowed["company"] = user_obj
                    else:
                        write(style.WARNING(f"No user found for company '{company_name}', skipping item"))
                        continue
            except Exception:
                pass

        # Ensure required fields are present (basic check)
        try:
            obj = Model.objects.create(**allowed)
            created += 1
            write(style.SUCCESS(f"Created {app_label}.{model_name} id={getattr(obj, 'id', 'n/a')} title={allowed.get('title')}"))
        except Exception as e:
            write(style.WARNING(f"Failed to create {app_label}.{model_name}: {e}"))
            for line in traceback.format_exc().splitlines():
                write(line)
            continue

    return created

class Command(BaseCommand):
    help = "Populate test data: create vacancies and internships (default 30 each)."

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=30, help="Number of items to create per model")

    def handle(self, *args, **options):
        count = options.get('count', 30)
        company_users = ensure_company_users(self.stdout.write, self.style)

        v_created = create_entries("vacancies", "Vacancy", count=count, write=self.stdout.write, style=self.style, company_users=company_users, payload_maker=make_vacancy_payload)
        i_created = create_entries("internships", "Internship", count=count, write=self.stdout.write, style=self.style, company_users=company_users, payload_maker=make_internship_payload)

        self.stdout.write(self.style.SUCCESS(f"Created {v_created} vacancies and {i_created} internships"))

import pytest
from django.contrib.auth import get_user_model
from internships.management.commands.populate_test_data import ensure_company_users, COMPANIES

class SimpleStyle:
    def SUCCESS(self, msg):
        return msg
    def WARNING(self, msg):
        return msg

@pytest.mark.django_db
def test_creates_users_and_sets_password():
    writes = []
    def write(msg):
        # cast to str in case style returns non-str
        writes.append(str(msg))

    style = SimpleStyle()
    result = ensure_company_users(write, style)

    User = get_user_model()
    # Ensure every expected company has a user entry
    assert isinstance(result, dict)
    assert set(result.keys()) == set(COMPANIES)
    assert len(result) == len(COMPANIES)

    # Check users exist and have the expected password set on creation
    for company_name, user in result.items():
        db_user = User.objects.get(pk=user.pk)
        assert db_user is not None
        assert db_user.check_password("password123") is True

    # Basic log check
    assert any("Prepared user for company" in line for line in writes)

@pytest.mark.django_db
def test_does_not_reset_password_for_existing_users():
    writes = []
    def write(msg):
        writes.append(str(msg))

    style = SimpleStyle()
    # First run: create users
    first = ensure_company_users(write, style)
    User = get_user_model()
    # Pick one company to modify
    sample_company = COMPANIES[0]
    user = User.objects.get(pk=first[sample_company].pk)

    # Change password to a different value and save
    user.set_password("newpass")
    user.save()

    # Clear logs and run again
    writes.clear()
    second = ensure_company_users(write, style)

    # Reload and verify password was not reset to the original "password123"
    reloaded = User.objects.get(pk=user.pk)
    assert reloaded.check_password("newpass") is True
    assert reloaded.check_password("password123") is False

    # Ensure returned mapping still contains the sample company
    assert sample_company in second