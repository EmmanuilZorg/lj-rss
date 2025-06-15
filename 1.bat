@echo off
setlocal

:: === Настройки ===
set REPO_URL=https://github.com/EmmanuilZorg/lj-rss.git

echo Инициализация git репозитория...
git init

echo Добавление файлов...
git add .

echo Первый коммит...
git commit -m "init"

echo Переименование ветки в main...
git branch -M main

echo Добавление origin...
git remote add origin %REPO_URL%

echo Пуш в GitHub...
git push -u origin main

echo Готово.
pause
