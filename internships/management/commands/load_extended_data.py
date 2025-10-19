import json
import traceback
import random
from pathlib import Path
from django.core.management.base import BaseCommand
from django.apps import apps
from django.utils.dateparse import parse_datetime, parse_date
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.db.models import DateField, DateTimeField
from django.contrib.auth import get_user_model
from django.db import IntegrityError

def safe_parse(val, Model, field_name):
    try:
        field = Model._meta.get_field(field_name)
    except Exception:
        return val
    from django.db.models import DateTimeField, DateField
    if isinstance(field, DateTimeField) and isinstance(val, str):
        return parse_datetime(val)
    if isinstance(field, DateField) and isinstance(val, str):
        return parse_date(val)
    return val

def ensure_user_for_company(name):
    User = get_user_model()
    username = (name or "").lower().replace(" ", "_")[:30] or "user"
    user, created = User.objects.get_or_create(username=username, defaults={"email": f"{username}@example.com"})
    if created:
        try:
            user.set_password("password123")
            user.save()
        except Exception:
            pass
    return user

def convert_value_for_field(Model, field_name, value):
    """
    Возвращает (target_field_name, converted_value).
    - Для Date/DateTime конвертирует строку.
    - Для ForeignKey с целочисленным PK возвращает "<field>_id".
    - Для ForeignKey на User и строкового имени возвращает ("<field>", User instance).
    - В остальных случаях возвращает исходные.
    """
    try:
        field = Model._meta.get_field(field_name)
    except Exception:
        return field_name, value

    # date / datetime
    if isinstance(field, DateTimeField) and isinstance(value, str):
        return field_name, parse_datetime(value)
    if isinstance(field, DateField) and isinstance(value, str):
        return field_name, parse_date(value)

    # ForeignKey handling
    if isinstance(field, ForeignKey):
        rel_model = getattr(field, "related_model", None)
        User = get_user_model()
        # integer PK -> use <field>_id
        if isinstance(value, int):
            return f"{field_name}_id", value
        # string value for FK to User -> ensure/create user
        if rel_model is not None and (rel_model == User or rel_model.__name__ == User.__name__):
            if isinstance(value, str) and value:
                user_obj = ensure_user_for_company(value)
                return field_name, user_obj
    return field_name, value

def create_or_get_user_with_id(uid, username=None, email=None):
    """
    Ensure a User with PK=uid exists. If username collides, generate a unique username.
    Returns User instance.
    """
    User = get_user_model()
    try:
        existing = User.objects.filter(pk=uid).first()
        if existing:
            return existing

        # pick base username
        base = username or f"user_{uid}"
        uname = base
        attempt = 0
        while User.objects.filter(username=uname).exists():
            attempt += 1
            uname = f"{base}_{attempt}_{random.randint(1,9999)}"
            if attempt > 10:
                break

        udata = {'id': uid, 'username': uname, 'email': email or f"{uname}@example.com"}
        # try create with explicit pk; if fails due to rare race, fallback to get_or_create by username
        try:
            return User.objects.create(**udata)
        except IntegrityError:
            user, _ = User.objects.get_or_create(username=uname, defaults=udata)
            # if pk mismatch, try to set/update fields (don't change pk)
            return user
    except Exception:
        # last resort: return any existing user or create a new one without fixed pk
        try:
            return User.objects.get(pk=uid)
        except Exception:
            return get_user_model().objects.create(username=f"user_fallback_{random.randint(1000,9999)}", email="auto@example.com")

class Command(BaseCommand):
    help = "Load fixture list JSON but ignore unknown fields (supports Django fixture list format)."

    def add_arguments(self, parser):
        parser.add_argument('--file', '-f', type=str, default='fixtures/extended_test_data.json')

    def handle(self, *args, **options):
        file_path = Path(options['file'])
        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        try:
            data = json.loads(file_path.read_text(encoding='utf-8'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to parse JSON: {e}"))
            return

        totals = {"vacancies": 0, "internships": 0}
        User = get_user_model()

        for item in data:
            try:
                model_str = item.get('model')
                if not model_str:
                    continue
                app_label, model_name = model_str.split('.', 1)
                Model = apps.get_model(app_label, model_name)
                fields = item.get('fields', {})
                item_pk = item.get('pk')  # preserve fixture PK when needed

                allowed = {}
                model_field_names = {f.name for f in Model._meta.get_fields() if getattr(f, 'concrete', False) and not getattr(f, 'auto_created', False)}

                # iterate fields, support alias 'university' -> 'company' for internships
                for orig_k, v in fields.items():
                    k = orig_k
                    if model_name.lower() == 'internship' and orig_k == 'university' and 'company' in model_field_names:
                        k = 'company'
                    new_k, new_v = convert_value_for_field(Model, k, v)
                    # allow if exact field exists
                    if new_k in model_field_names:
                        allowed[new_k] = new_v
                        continue
                    # allow fk_id when base field exists (e.g. company_id)
                    if new_k.endswith('_id') and new_k[:-3] in model_field_names:
                        allowed[new_k] = new_v
                        continue
                    # otherwise skip unknown fields

                # preserve PK for accounts.user so integer references from fixtures work
                if app_label == 'accounts' and model_name.lower() == 'user' and item_pk:
                    # only set id if model has 'id' concrete field and we didn't already set it
                    if 'id' in model_field_names and 'id' not in allowed:
                        allowed['id'] = item_pk

                if not allowed:
                    continue

                # If allowed contains FK _id to User but that user PK doesn't exist yet — create placeholder
                # Find FK fields on this model that reference User
                for f in Model._meta.get_fields():
                    if getattr(f, 'concrete', False) and isinstance(f, ForeignKey):
                        rel = getattr(f, 'related_model', None)
                        if rel is not None and (rel == User or rel.__name__ == User.__name__):
                            fk_id_key = f"{f.name}_id"
                            # if we have fk_id and no such user in DB, create placeholder with that id
                            if fk_id_key in allowed:
                                uid = allowed[fk_id_key]
                                try:
                                    if not User.objects.filter(pk=uid).exists():
                                        # create placeholder with specific id safely
                                        create_or_get_user_with_id(uid, username=f"user_{uid}", email=f"user_{uid}@example.com")
                                except Exception:
                                    pass
                            # if allowed contains f.name with integer (bad case), convert to f"{name}_id"
                            if f.name in allowed and isinstance(allowed[f.name], int):
                                allowed[f"{f.name}_id"] = allowed.pop(f.name)

                # Prevent creating duplicate one-to-one/unique relations (e.g. Resume.user unique)
                # If model has OneToOneField or a ForeignKey with unique=True referencing User and allowed contains user_id, skip create if exists
                skip_create = False
                for f in Model._meta.get_fields():
                    if getattr(f, 'concrete', False) and (isinstance(f, OneToOneField) or getattr(f, 'unique', False)):
                        # check if field references User
                        rel = getattr(f, 'related_model', None)
                        if rel is not None and (rel == User or rel.__name__ == User.__name__):
                            key_id = f"{f.name}_id"
                            if key_id in allowed:
                                uid = allowed[key_id]
                                if Model.objects.filter(**{f.name: uid}).exists() or Model.objects.filter(**{key_id: uid}).exists():
                                    skip_create = True
                                    break

                if skip_create:
                    self.stdout.write(self.style.WARNING(f"Skipping create for {item.get('model')} because unique relation exists for user_id {allowed.get('user_id') or allowed.get('company_id')}"))
                    continue

                # Special handling for custom User model to avoid unexpected _id keys and to set password correctly
                if app_label == 'accounts' and model_name.lower() == 'user':
                    user_field_names = {f.name for f in User._meta.get_fields() if getattr(f, 'concrete', False) and not getattr(f, 'auto_created', False)}
                    user_allowed = {k: v for k, v in allowed.items() if k in user_field_names}
                    # if fixture has 'password' hashed value, set it directly; otherwise create_user to hash raw password
                    try:
                        if 'id' in user_allowed and User.objects.filter(pk=user_allowed['id']).exists():
                            # update existing user instead of creating new one
                            uid = user_allowed.pop('id')
                            User.objects.filter(pk=uid).update(**user_allowed)
                        else:
                            # ensure username uniqueness when creating
                            if 'username' in user_allowed and User.objects.filter(username=user_allowed['username']).exists():
                                base = user_allowed['username']
                                attempt = 0
                                uname = base
                                while User.objects.filter(username=uname).exists():
                                    attempt += 1
                                    uname = f"{base}_{attempt}_{random.randint(1,9999)}"
                                    if attempt > 10:
                                        break
                                user_allowed['username'] = uname

                            if 'password' in user_allowed:
                                user_kwargs = {k: v for k, v in user_allowed.items() if k != 'password'}
                                user = User(**user_kwargs)
                                user.password = user_allowed['password']
                                user.save()
                            else:
                                if 'username' in user_allowed and hasattr(User.objects, 'create_user'):
                                    User.objects.create_user(**user_allowed)
                                else:
                                    User.objects.create(**user_allowed)
                    except IntegrityError:
                        self.stdout.write(self.style.WARNING(f"User creation/update IntegrityError for pk {user_allowed.get('id')}, username {user_allowed.get('username')}"))
                    except Exception:
                        self.stdout.write(self.style.WARNING(f"User creation/update failed: {traceback.format_exc()}"))
                else:
                    # Regular model create
                    try:
                        Model.objects.create(**allowed)
                    except IntegrityError as e:
                        self.stdout.write(self.style.WARNING(f"IntegrityError creating {item.get('model')}: {e}"))
                        continue

                if app_label == 'vacancies' and model_name.lower() in ('vacancy',):
                    totals['vacancies'] += 1
                if app_label == 'internships' and model_name.lower() in ('internship',):
                    totals['internships'] += 1
            except Exception:
                self.stdout.write(self.style.WARNING(f"Failed to create {item.get('model')}: {traceback.format_exc()}"))
                continue

        self.stdout.write(self.style.SUCCESS(f"Loaded: {totals['vacancies']} vacancies, {totals['internships']} internships"))