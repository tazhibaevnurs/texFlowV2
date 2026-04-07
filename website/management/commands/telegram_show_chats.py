"""
Показать последние обновления бота (getUpdates), чтобы найти chat_id группы или лички.

Перед запуском в группе отправьте команду, которую бот точно увидит, например:
  /start@ИмяВашегоБота
или отключите режим приватности у бота в @BotFather: /setprivacy → Disable.
"""

from __future__ import annotations

import json
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand


def _tg_json(token: str, method: str):
    url = f'https://api.telegram.org/bot{token}/{method}'
    with urllib.request.urlopen(url, timeout=15) as resp:
        return json.loads(resp.read().decode('utf-8'))


class Command(BaseCommand):
    help = 'Вывести getUpdates от Telegram (найти TELEGRAM_CHAT_ID для группы или лички)'

    def handle(self, *args, **options):
        token = (getattr(settings, 'TELEGRAM_BOT_TOKEN', '') or '').strip()
        if not token:
            self.stderr.write(self.style.ERROR('Задайте TELEGRAM_BOT_TOKEN в .env или окружении.'))
            return

        try:
            wh = _tg_json(token, 'getWebhookInfo')
        except OSError as e:
            self.stderr.write(self.style.ERROR(f'Ошибка getWebhookInfo: {e}'))
            return

        wh_info = (wh.get('result') or {}) if wh.get('ok') else {}
        wh_url = (wh_info.get('url') or '').strip()
        if wh_url:
            self.stdout.write(
                self.style.WARNING(
                    f'У бота включён webhook — обновления не попадают в getUpdates в браузере.\n'
                    f'URL: {wh_url}\n'
                    'Откройте ОДИН раз в браузере (сбросит webhook):\n'
                    f'  https://api.telegram.org/bot{token}/deleteWebhook\n'
                    'Затем напишите боту в ЛИЧКУ команду /start и снова откройте getUpdates.\n\n'
                )
            )

        try:
            data = _tg_json(token, 'getUpdates')
        except OSError as e:
            self.stderr.write(self.style.ERROR(f'Ошибка getUpdates: {e}'))
            return

        if not data.get('ok'):
            self.stderr.write(self.style.ERROR(str(data)))
            return

        updates = data.get('result') or []
        if not updates:
            self.stdout.write(
                'Пока result пустой — бот ещё не получил ни одного подходящего события.\n\n'
                'Самый надёжный шаг: откройте бота в ЛИЧНЫХ сообщениях и отправьте: /start\n'
                'Потом снова откройте getUpdates в браузере.\n\n'
                'Для группы:\n'
                '1) Добавьте этого же бота в группу.\n'
                '2) Отправьте: /start@username_бота (username из @BotFather).\n'
                '   Либо @BotFather → Bot Settings → Group Privacy → Disable.\n\n'
                'Снова запустите: py -3 manage.py telegram_show_chats\n'
            )
            return

        self.stdout.write(self.style.SUCCESS(f'Найдено обновлений: {len(updates)}\n'))
        seen = set()
        for u in updates[-20:]:
            msg = u.get('message') or u.get('edited_message') or {}
            chat = msg.get('chat') or {}
            cid = chat.get('id')
            ctype = chat.get('type')
            title = chat.get('title') or chat.get('username') or ''
            if cid is not None and cid not in seen:
                seen.add(cid)
                self.stdout.write(
                    f'  chat_id = {cid!r}  type={ctype!r}  {title}\n'
                )

        self.stdout.write(
            '\nПодставьте нужный chat_id в TELEGRAM_CHAT_ID (для группы обычно отрицательное число, '
            'например -100xxxxxxxxxx).\n'
        )
