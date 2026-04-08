from django.db import migrations

NEW_HERO_EYEBROW = 'Система для швейного производства'
NEW_HERO_LINE1 = 'Забудьте про Excel.'
NEW_HERO_ACCENT = 'Управляйте цехом из телефона.'
NEW_HERO_SUBTITLE = (
    'ШвейМетрикс — приложение для владельцев швейных цехов и фабрик. Контролируйте заказы, выработку '
    'сотрудников и расчёт зарплат в одном месте — в реальном времени.'
)


def forwards(apps, schema_editor):
    LandingContent = apps.get_model('website', 'LandingContent')
    obj = LandingContent.objects.filter(pk=1).first()
    if not obj:
        return
    obj.hero_eyebrow = NEW_HERO_EYEBROW
    obj.hero_title_line1 = NEW_HERO_LINE1
    obj.hero_title_accent = NEW_HERO_ACCENT
    obj.hero_subtitle = NEW_HERO_SUBTITLE
    obj.save()


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('website', '0006_landing_content_concrete_copy'),
    ]

    operations = [
        migrations.RunPython(forwards, noop_reverse),
    ]
