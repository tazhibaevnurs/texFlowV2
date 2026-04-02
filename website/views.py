from django.contrib import messages
from django.shortcuts import redirect, render

CAPABILITIES = [
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


def index(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip()
        if email:
            messages.success(request, 'Спасибо! Мы свяжемся с вами по указанному адресу.')
        else:
            messages.error(request, 'Укажите корректный email.')
        return redirect('index')
    return render(request, 'index.html', {'capabilities': CAPABILITIES})
