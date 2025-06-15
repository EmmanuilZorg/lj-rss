# LiveJournal RSS Feed Generator

Автоматически собирает посты с LiveJournal и публикует RSS-ленту на GitHub Pages.

## Установка

```bash
pip install -r requirements.txt
python generate_rss.py
```

## Деплой

- GitHub Actions обновляет ленту каждый час.
- Подключи GitHub Pages к корню репозитория, чтобы использовать `https://yourusername.github.io/feed.xml`.

## Конфигурация

Отредактируй `url` в `generate_rss.py` и селекторы в `scraping.py`.