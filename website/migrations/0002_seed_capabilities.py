from django.db import migrations


def seed_capabilities(apps, schema_editor):
    Capability = apps.get_model('website', 'Capability')
    if Capability.objects.exists():
        return
    rows = [
        ('Управление заказами', 'Автоматизация заказов и контрактов с клиентами и поставщиками.'),
        ('Учёт и контроль запасов', 'Учёт и автоматическое пополнение запасов.'),
        ('Мониторинг операций', 'Анализ и улучшение производственных процессов.'),
        ('Планирование производства', 'Оптимизация производственных процессов и загрузки.'),
        ('CRM', 'Эффективное взаимодействие с клиентами и управление продажами.'),
        ('Учёт и анализ продаж', 'Учёт продаж и аналитика для маркетинга.'),
        ('Бухгалтерия и финансы', 'Бухгалтерия и финансовый учёт предприятия.'),
        ('Управление бюджетом', 'Управление бюджетом и финансами предприятия.'),
        ('Ресурсы цеха', 'Управление ресурсами предприятия.'),
        ('Анализ и отчётность', 'Анализ данных и отчётность для руководства.'),
    ]
    for i, (title, text) in enumerate(rows):
        Capability.objects.create(title=title, text=text, sort_order=i * 10, is_active=True)


def unseed_capabilities(apps, schema_editor):
    Capability = apps.get_model('website', 'Capability')
    Capability.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_capabilities, unseed_capabilities),
    ]
