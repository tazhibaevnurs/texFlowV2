from django.db import migrations

NEW_HERO_SUBTITLE = (
    'В одном приложении: заказы с параметрами изделия, этапы пошива, выработка по сотрудникам и расчёт '
    'сдельной и оклада. Владелец и технолог видят факт по цеху — без сводок из Excel и переписок в чатах.'
)
NEW_PRICING_TITLE = 'Оставьте заявку — подберём внедрение под ваш цех'
NEW_PRICING_TEXT = (
    'Напишите контакты и кратко, что нужно автоматизировать: заказы, этапы, выработку или зарплату. '
    'Ответим с шагами подключения и ориентиром по стоимости.'
)

OLD_HERO_SUBTITLE = (
    'Управляйте швейным цехом с помощью нашего приложения. Получайте точные данные о производстве '
    'и сосредоточьтесь на том, что важно для бизнеса.'
)
OLD_PRICING_TITLE = 'Оптимизировать · Управлять · Процветать'
OLD_PRICING_TEXT = (
    'Увеличьте эффективность и оптимизируйте процессы с нашим ERP. Оставьте заявку — подберём '
    'формат внедрения и стоимость.'
)


def forwards(apps, schema_editor):
    LandingContent = apps.get_model('website', 'LandingContent')
    obj = LandingContent.objects.filter(pk=1).first()
    if not obj:
        return
    if obj.hero_subtitle.strip() == OLD_HERO_SUBTITLE.strip():
        obj.hero_subtitle = NEW_HERO_SUBTITLE
    if obj.pricing_title.strip() == OLD_PRICING_TITLE.strip():
        obj.pricing_title = NEW_PRICING_TITLE
    if obj.pricing_text.strip() == OLD_PRICING_TEXT.strip():
        obj.pricing_text = NEW_PRICING_TEXT
    obj.save()


def backwards(apps, schema_editor):
    LandingContent = apps.get_model('website', 'LandingContent')
    obj = LandingContent.objects.filter(pk=1).first()
    if not obj:
        return
    if obj.hero_subtitle.strip() == NEW_HERO_SUBTITLE.strip():
        obj.hero_subtitle = OLD_HERO_SUBTITLE
    if obj.pricing_title.strip() == NEW_PRICING_TITLE.strip():
        obj.pricing_title = OLD_PRICING_TITLE
    if obj.pricing_text.strip() == NEW_PRICING_TEXT.strip():
        obj.pricing_text = OLD_PRICING_TEXT
    obj.save()


class Migration(migrations.Migration):
    dependencies = [
        ('website', '0005_capabilities_match_product'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
