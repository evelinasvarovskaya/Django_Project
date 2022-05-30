from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from simple_history.models import HistoricalRecords
from .managers import UserManager

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', max_length=60,
                              unique=True)
    date_joined = models.DateTimeField(verbose_name='Дата создания',
                                       auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Последний вход',
                                      auto_now=True)

    is_active = models.BooleanField(verbose_name='Активирован', default=True)
    is_admin = models.BooleanField(default=False, verbose_name='Администратор')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()
    history = HistoricalRecords()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    middle_name = models.CharField(verbose_name='Отчество', max_length=255)
    cv = models.FileField(verbose_name='Резюме', upload_to='cvs/')
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.id}. {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    company_name = models.CharField(verbose_name='Имя компании', max_length=255)
    employees_count = models.IntegerField(verbose_name='Кол-во сотрудников компании', default=0)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.company_name)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class BlogPost(models.Model):
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок поста', max_length=255)
    text = models.TextField(verbose_name='Текст поста')
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.company.company_name} - {self.title}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Vacancy(models.Model):
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок вакансии', max_length=255)
    description = models.TextField(verbose_name='Описание вакансии')
    responses = models.ManyToManyField(Candidate, verbose_name='Отклики', blank=True)
    STATUS_CHOICES = (('MODERATING', 'Moderating'), ('ACTIVE', 'Active'), ('ARCHIVED', 'Archived'))
    status = models.CharField(verbose_name='Статус', max_length=255 ,choices=STATUS_CHOICES, default='Moderating')
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.company.company_name} - {self.title}'

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class Interview(models.Model):
    vacancy = models.ForeignKey(Vacancy, verbose_name='Вакансия', on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, verbose_name='Кандидат', on_delete=models.CASCADE)
    planned_datetime = models.DateTimeField(verbose_name='Дата и время проведения', auto_now=False, auto_now_add=False)
    STATUS_CHOICES = (('PLANNED', 'Planned'), ('IN_PROGRESS', 'In_progress'), ('FINISHED', 'Finished'))
    status = models.CharField(verbose_name='Статус', max_length=255 ,choices=STATUS_CHOICES, default='Planned')
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.vacancy.title} - {self.candidate.id}'

    class Meta:
        verbose_name = 'Собеседование'
        verbose_name_plural = 'Собеседования'
