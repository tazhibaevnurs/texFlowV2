from django.db import models


class LandingContent(models.Model):
    """Единственная запись: тексты главной страницы (редактируются в админке)."""

    class Meta:
        verbose_name = 'Контент лендинга'
        verbose_name_plural = 'Контент лендинга'

    hero_eyebrow = models.CharField(
        'Бейдж над заголовком',
        max_length=255,
        default='Система для швейного производства',
    )
    hero_title_line1 = models.CharField(
        'Заголовок (первая строка)',
        max_length=255,
        default='Забудьте про Excel.',
    )
    hero_title_accent = models.CharField(
        'Заголовок (акцентная строка)',
        max_length=255,
        default='Управляйте цехом из телефона.',
    )
    hero_subtitle = models.TextField(
        'Подзаголовок под H1',
        default=(
            'ШвейМетрикс — приложение для владельцев швейных цехов и фабрик. Контролируйте заказы, выработку '
            'сотрудников и расчёт зарплат в одном месте — в реальном времени.'
        ),
    )
    pricing_eyebrow = models.CharField(
        'Бейдж блока заявки',
        max_length=255,
        blank=True,
        default='',
    )
    pricing_title = models.CharField(
        'Заголовок блока заявки',
        max_length=255,
        default='Начните прямо сейчас',
    )
    pricing_promo = models.CharField(
        'Акцент под заголовком (блок заявки)',
        max_length=255,
        default='Первые 14 дней — бесплатно',
    )
    pricing_text = models.TextField(
        'Текст блока заявки',
        default=(
            'Оставьте заявку — мы свяжемся в течение часа, настроим ваше рабочее пространство и ответим на все вопросы.'
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

    class EmployeeBand(models.TextChoices):
        LT10 = 'lt10', 'до 10'
        M10_30 = 'm10_30', '10–30'
        M30_100 = 'm30_100', '30–100'
        GT100 = 'gt100', 'более 100'

    email = models.EmailField('Email', blank=True)
    name = models.CharField('Имя', max_length=255, blank=True)
    phone = models.CharField('Телефон', max_length=64, blank=True)
    employee_band = models.CharField(
        'Количество сотрудников в цеху',
        max_length=32,
        choices=EmployeeBand.choices,
        blank=True,
        null=True,
    )
    employee_count = models.PositiveIntegerField(
        'Количество сотрудников (устар.)',
        null=True,
        blank=True,
        help_text='Раньше вводилось числом; для новых заявок используйте диапазон.',
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
        label = self.email or self.phone or self.name or f'#{self.pk}'
        return f'{label} ({self.get_status_display()})'
