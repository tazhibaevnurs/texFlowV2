from django.db import migrations


def replace_capabilities(apps, schema_editor):
    Capability = apps.get_model('website', 'Capability')
    Capability.objects.all().delete()
    rows = [
        (
            'Управление заказами',
            'Автоматизация заказов и контрактов с клиентами и поставщиками.',
        ),
        (
            'Планирование производства',
            'Оптимизация производственных процессов и загрузки.',
        ),
        (
            'Мониторинг операций',
            'Анализ и улучшение производственных процессов.',
        ),
        (
            'Учёт и анализ продаж',
            'Учёт продаж и аналитика для маркетинга.',
        ),
        (
            'Расчёт заработной платы',
            'Сдельная и оклад начисляются в приложении — суммы прозрачны сотруднику и владельцу.',
        ),
        (
            'Управление сотрудниками',
            'Добавление сотрудников, роли и доступ к производственным данным.',
        ),
        (
            'Анализ и отчётность',
            'Анализ данных и отчётность для руководства.',
        ),
    ]
    for i, (title, text) in enumerate(rows):
        Capability.objects.create(title=title, text=text, sort_order=i * 10, is_active=True)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('website', '0004_capabilities_truthful_copy'),
    ]

    operations = [
        migrations.RunPython(replace_capabilities, noop_reverse),
    ]
