"""Отправка уведомлений о заявках в Telegram (Bot API)."""

from __future__ import annotations

import html
import json
import logging
import urllib.error
import urllib.request

from django.conf import settings

from .models import Lead

logger = logging.getLogger(__name__)


def _esc(s) -> str:
    return html.escape(str(s if s is not None else ''), quote=False)


def _build_lead_message_html(lead: Lead) -> str:
    """HTML для Telegram (parse_mode=HTML). Все пользовательские поля экранируются."""
    rows: list[str] = [
        '<b>📩 Новая заявка с лендинга</b>',
        '',
        f'<b>Номер заявки</b> · <code>#{_esc(lead.pk)}</code>',
        '',
        f'<b>Email</b>',
        f'<code>{_esc(lead.email) if lead.email else "—"}</code>',
    ]
    if lead.name:
        rows.extend(['', f'<b>Имя</b>', f'{_esc(lead.name)}'])
    if lead.phone:
        rows.extend(['', f'<b>Телефон</b>', f'<code>{_esc(lead.phone)}</code>'])
    if lead.employee_band:
        rows.extend(
            [
                '',
                f'<b>Количество сотрудников</b>',
                f'{_esc(lead.get_employee_band_display())}',
            ]
        )
    elif lead.employee_count is not None:
        rows.extend(['', f'<b>Количество сотрудников</b>', f'<code>{_esc(lead.employee_count)}</code>'])
    if lead.message:
        msg = str(lead.message).strip()
        if len(msg) > 1500:
            msg = msg[:1497] + '…'
        rows.extend(['', f'<b>Сообщение клиента</b>', f'<pre>{_esc(msg)}</pre>'])
    if lead.ip_address:
        rows.extend(['', f'<b>IP</b> · <code>{_esc(lead.ip_address)}</code>'])
    rows.extend(['', f'<b>Источник</b> · {_esc(lead.source or "landing")}'])
    return '\n'.join(rows)


def _build_lead_message_plain(lead: Lead) -> str:
    """Простой текст (fallback, если HTML не принят API)."""
    lines: list[str] = [
        '📩 Новая заявка с лендинга',
        '',
        f'Номер заявки: #{lead.pk}',
        '',
        f'Email: {lead.email or "—"}',
    ]
    if lead.name:
        lines.extend(['', f'Имя: {lead.name}'])
    if lead.phone:
        lines.extend(['', f'Телефон: {lead.phone}'])
    if lead.employee_band:
        lines.extend(['', f'Количество сотрудников: {lead.get_employee_band_display()}'])
    elif lead.employee_count is not None:
        lines.extend(['', f'Количество сотрудников: {lead.employee_count}'])
    if lead.message:
        msg = str(lead.message).strip()
        if len(msg) > 1500:
            msg = msg[:1497] + '…'
        lines.extend(['', 'Сообщение клиента:', msg])
    if lead.ip_address:
        lines.extend(['', f'IP: {lead.ip_address}'])
    lines.extend(['', f'Источник: {lead.source or "landing"}'])
    return '\n'.join(lines)


def _chat_id_value(raw: str):
    raw = (raw or '').strip()
    if not raw:
        return None
    if raw.startswith('@'):
        return raw
    if raw.lstrip('-').isdigit():
        return int(raw)
    return raw


def _send_message(token: str, chat_id, text: str, *, parse_mode: str | None = None) -> bool:
    """Отправка сообщения. При ошибке разбора HTML можно повторить без parse_mode."""
    err = _send_message_ex(token, chat_id, text, parse_mode=parse_mode)
    return err is None


def _send_message_ex(
    token: str, chat_id, text: str, *, parse_mode: str | None = None
) -> str | None:
    """Возвращает None при успехе, иначе текст ошибки Telegram (для fallback по HTML)."""
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'disable_web_page_preview': True,
    }
    if parse_mode:
        payload['parse_mode'] = parse_mode
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode('utf-8', errors='replace')
            if resp.status != 200:
                logger.warning('Telegram: HTTP %s — %s', resp.status, body[:500])
                return body[:500]
            try:
                parsed = json.loads(body)
            except json.JSONDecodeError:
                logger.warning('Telegram: не JSON в ответе: %s', body[:500])
                return 'invalid json'
            if not parsed.get('ok'):
                desc = parsed.get('description', body[:500])
                logger.error('Telegram sendMessage не ok: %s', desc)
                return str(desc)
            return None
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='replace') if e.fp else ''
        logger.warning('Telegram HTTPError %s: %s', e.code, err_body[:500])
        try:
            parsed = json.loads(err_body)
            return str(parsed.get('description', err_body[:500]))
        except json.JSONDecodeError:
            return err_body[:500] or f'HTTP {e.code}'
    except OSError:
        logger.exception('Telegram: сетевая ошибка при отправке')
        return 'network error'


def _is_html_parse_error(description: str) -> bool:
    d = (description or '').lower()
    # Telegram: "Can't parse entities" / рус. варианты
    return 'parse' in d and 'entit' in d


def notify_lead_created(lead: Lead) -> bool:
    """
    Отправляет сообщение в один или несколько чатов (личка, группа, канал).
    TELEGRAM_CHAT_ID можно несколько через запятую: -1001234567890,232731680

    Не бросает исключения наружу. Возвращает True, если хотя бы одна отправка успешна.
    """
    token = (getattr(settings, 'TELEGRAM_BOT_TOKEN', None) or '').strip()
    chat_raw = (getattr(settings, 'TELEGRAM_CHAT_ID', None) or '').strip()
    if not token or not chat_raw:
        logger.warning(
            'Telegram: пропуск — задайте TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID в .env '
            '(локально) или в переменных окружения на сервере (Vercel → Settings → Environment).'
        )
        return False

    text = _build_lead_message_html(lead)
    # Лимит Telegram ~4096 символов; при переполнении убираем разметку не рвём — укорачиваем pre
    if len(text) > 4000:
        text = text[:3997] + '…'

    text_plain = _build_lead_message_plain(lead)
    if len(text_plain) > 4000:
        text_plain = text_plain[:3997] + '…'

    parts = [p.strip() for p in chat_raw.split(',') if p.strip()]
    ok_any = False
    for part in parts:
        chat_id = _chat_id_value(part)
        if chat_id is None:
            logger.warning('Telegram: пропуск неверного chat_id: %r', part)
            continue
        err = _send_message_ex(token, chat_id, text, parse_mode='HTML')
        if err is None:
            ok_any = True
            continue
        if _is_html_parse_error(err):
            logger.warning(
                'Telegram: HTML не принят (%s), повтор без разметки', err[:200]
            )
            if _send_message(token, chat_id, text_plain):
                ok_any = True
            else:
                logger.warning('Telegram: не удалось отправить в chat_id=%r', chat_id)
        else:
            logger.warning(
                'Telegram: не удалось отправить в chat_id=%r: %s', chat_id, err[:200]
            )

    return ok_any
