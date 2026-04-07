import logging

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import LeadForm
from .models import Capability, LandingContent, Lead
from .telegram_notify import notify_lead_created

logger = logging.getLogger(__name__)

# Резерв, если в БД ещё нет карточек возможностей (только реализованный функционал)
CAPABILITIES_FALLBACK = [
    {
        'title': 'Заказы',
        'text': (
            'Создавайте карточки заказов с параметрами изделия, сроками, клиентом и требованиями к '
            'упаковке. Менеджер видит статус — технолог видит задачи.'
        ),
    },
    {
        'title': 'Этапы производства',
        'text': (
            'Разбивайте каждый заказ на операции: крой, пошив, ОТК, утюг, упаковка. Назначайте '
            'сотрудников и фиксируйте расценки за операцию.'
        ),
    },
    {
        'title': 'Выработка по сотрудникам',
        'text': (
            'Ежедневно фиксируйте сколько единиц сделал каждый сотрудник. Смотрите статистику по '
            'дням — видите кто работает, а кто нет.'
        ),
    },
    {
        'title': 'Зарплата',
        'text': (
            'Сдельная оплата считается автоматически. Фиксированный оклад начисляется в заданный '
            'день месяца. Все начисления прозрачны для сотрудника и владельца.'
        ),
    },
    {
        'title': 'Сотрудники',
        'text': (
            'Добавляйте сотрудников, назначайте роли, отслеживайте производительность каждого. '
            'История работы сохраняется даже после увольнения.'
        ),
    },
    {
        'title': 'Аналитика',
        'text': (
            'Владелец видит общую картину: количество заказов, объём выработки, процент брака, фонд '
            'оплаты труда.'
        ),
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
