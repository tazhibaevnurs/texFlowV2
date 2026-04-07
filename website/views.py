import logging

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import LeadForm
from .models import Capability, LandingContent, Lead
from .telegram_notify import notify_lead_created

logger = logging.getLogger(__name__)

# Резерв, если в БД ещё нет карточек возможностей
CAPABILITIES_FALLBACK = [
    {
        'title': 'Управление заказами',
        'text': 'Автоматизация заказов и контрактов с клиентами и поставщиками.',
    },
    {
        'title': 'Учёт и контроль запасов',
        'text': 'Учёт и автоматическое пополнение запасов.',
    },
    {
        'title': 'Мониторинг операций',
        'text': 'Анализ и улучшение производственных процессов.',
    },
    {
        'title': 'Планирование производства',
        'text': 'Оптимизация производственных процессов и загрузки.',
    },
    {
        'title': 'CRM',
        'text': 'Эффективное взаимодействие с клиентами и управление продажами.',
    },
    {
        'title': 'Учёт и анализ продаж',
        'text': 'Учёт продаж и аналитика для маркетинга.',
    },
    {
        'title': 'Бухгалтерия и финансы',
        'text': 'Бухгалтерия и финансовый учёт предприятия.',
    },
    {
        'title': 'Управление бюджетом',
        'text': 'Управление бюджетом и финансами предприятия.',
    },
    {
        'title': 'Ресурсы цеха',
        'text': 'Управление ресурсами предприятия.',
    },
    {
        'title': 'Анализ и отчётность',
        'text': 'Анализ данных и отчётность для руководства.',
    },
]


def _get_capabilities():
    qs = Capability.objects.filter(is_active=True).order_by('sort_order', 'id')
    if qs.exists():
        return list(qs)
    return CAPABILITIES_FALLBACK


def index(request):
    landing = LandingContent.load()

    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead: Lead = form.save(commit=False)
            lead.source = 'landing'
            lead.ip_address = _get_client_ip(request)
            lead.user_agent = (request.META.get('HTTP_USER_AGENT') or '')[:2000]
            lead.save()
            if not notify_lead_created(lead):
                logger.error(
                    'Заявка #%s сохранена, но уведомление в Telegram не отправилось — см. лог сервера.',
                    lead.pk,
                )
                if settings.DEBUG:
                    messages.warning(
                        request,
                        'Заявка сохранена. Уведомление в Telegram не дошло — проверьте .env '
                        '(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID) и консоль runserver.',
                    )
            messages.success(request, 'Мы свяжемся с вами в ближайшее время.')
            return redirect('index')
        messages.error(request, 'Проверьте email и поля формы.')
    else:
        form = LeadForm()

    return render(
        request,
        'index.html',
        {
            'content': landing,
            'capabilities': _get_capabilities(),
            'lead_form': form,
        },
    )


def _get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')
