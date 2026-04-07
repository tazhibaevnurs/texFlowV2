from django.db import models


class LandingContent(models.Model):
    """Единственная запись: тексты главной страницы (редактируются в админке)."""

    class Meta:
        verbose_name = 'Контент лендинга'
        verbose_name_plural = 'Контент лендинга'

    hero_eyebrow = models.CharField(
        'Бейдж над заголовком',
        max_length=255,
        default='ERP для швейного производства',
    )
    hero_title_line1 = models.CharField(
        'Заголовок (первая строка)',
        max_length=255,
        default='Производство сложное.',
    )
    hero_title_accent = models.CharField(
        'Заголовок (акцентная строка)',
        max_length=255,
        default='Управлять им — проще.',
    )
    hero_subtitle = models.TextField(
        'Подзаголовок под H1',
        default=(
            'Управляйте швейным цехом с помощью нашего приложения. Получайте точные данные о производстве '
            'и сосредоточьтесь на том, что важно для бизнеса.'
        ),
    )
    pricing_eyebrow = models.CharField(
        'Бейдж блока заявки',
        max_length=255,
        default='Связаться',
    )
    pricing_title = models.CharField(
        'Заголовок блока заявки',
        max_length=255,
        default='Оптимизировать · Управлять · Процветать',
    )
    pricing_text = models.TextField(
        'Текст блока заявки',
        default=(
            'Увеличьте эффективность и оптимизируйте процессы с нашим ERP. Оставьте заявку — подберём '
            'формат внедрения и стоимость.'
        ),
    )

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'Контент лендинга'


class Capability(models.Model):
    """Карточки «Чем вы можете управлять»."""

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Возможность'
        verbose_name_plural = 'Возможности (лендинг)'

    sort_order = models.PositiveIntegerField('Порядок', default=0)
    title = models.CharField('Заголовок', max_length=255)
    text = models.TextField('Описание')
    is_active = models.BooleanField('Показывать', default=True)

    def __str__(self):
        return self.title


class Lead(models.Model):
    """Заявки с формы на лендинге."""

    class Status(models.TextChoices):
        NEW = 'new', 'Новая'
        IN_PROGRESS = 'in_progress', 'В работе'
        DONE = 'done', 'Обработана'
        REJECTED = 'rejected', 'Отклонена'

    email = models.EmailField('Email')
    name = models.CharField('Имя', max_length=255, blank=True)
    phone = models.CharField('Телефон', max_length=64, blank=True)
    employee_count = models.PositiveIntegerField(
        'Количество сотрудников',
        null=True,
        blank=True,
        help_text='Число сотрудников на производстве (если указано)',
    )
    message = models.TextField('Сообщение', blank=True)
    status = models.CharField(
        'Статус',
        max_length=32,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    admin_notes = models.TextField('Заметки (только для админки)', blank=True)
    source = models.CharField('Источник', max_length=64, default='landing', blank=True)
    ip_address = models.GenericIPAddressField('IP', null=True, blank=True, unpack_ipv4=True)
    user_agent = models.TextField('User-Agent', blank=True)
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.email} ({self.get_status_display()})'
