"""Проверка: отправить тестовое сообщение в Telegram (те же TELEGRAM_* что у заявок)."""

from django.conf import settings
from django.core.management.base import BaseCommand

from ...telegram_notify import _chat_id_value, _send_message


class Command(BaseCommand):
    help = 'Отправить тест «Швей Метрикс: тест уведомления» в TELEGRAM_CHAT_ID'

    def handle(self, *args, **options):
        token = (getattr(settings, 'TELEGRAM_BOT_TOKEN', '') or '').strip()
        chat_raw = (getattr(settings, 'TELEGRAM_CHAT_ID', '') or '').strip()
        if not token:
            self.stderr.write(self.style.ERROR('Нет TELEGRAM_BOT_TOKEN'))
            return
        if not chat_raw:
            self.stderr.write(self.style.ERROR('Нет TELEGRAM_CHAT_ID'))
            return

        self.stdout.write(f'Токен: {token[:12]}…{token[-6:]}')
        self.stdout.write(f'CHAT_ID (сырой): {chat_raw!r}')

        text = 'Швей Метрикс: тест уведомления с Django. Если видите это — токен и chat_id верны.'
        ok_any = False
        for part in [p.strip() for p in chat_raw.split(',') if p.strip()]:
            cid = _chat_id_value(part)
            if cid is None:
                self.stderr.write(self.style.WARNING(f'Пропуск неверного: {part!r}'))
                continue
            self.stdout.write(f'Отправка в chat_id={cid!r} …')
            if _send_message(token, cid, text):
                self.stdout.write(self.style.SUCCESS('  OK'))
                ok_any = True
            else:
                self.stderr.write(self.style.ERROR('  Ошибка (см. лог выше ERROR)'))

        if ok_any:
            self.stdout.write(self.style.SUCCESS('\nГотово. Проверьте чат в Telegram.'))
        else:
            self.stderr.write(
                self.style.ERROR(
                    '\nЧастые причины: 1) токен от ДРУГОГО бота, не из группы; '
                    '2) бот удалён из группы; 3) неверный chat_id; 4) на Vercel не заданы env.'
                )
            )
