@echo off
chcp 65001 >nul

echo Тест 1: Зависимости пакета A (тестовый файл)
echo ^> python src\main.py --package A --repo tests\test_graph.txt --test-mode
python src\main.py --package A --repo tests\test_graph.txt --test-mode

echo.
echo Тест 2: Пакет без зависимостей (тестовый файл)
echo ^> python src\main.py --package D --repo tests\test_graph.txt --test-mode
python src\main.py --package D --repo tests\test_graph.txt --test-mode

echo.
echo Тест 3: Зависимости пакета curl из Alpine (нужен интернет)
echo ^> python src\main.py --package curl --repo https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/x86_64
python src\main.py --package curl --repo https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/x86_64

echo.
echo Тест 4: Ошибка - пакет не найден в репозитории
echo ^> python src\main.py --package no-such-package-xyz --repo https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/x86_64
python src\main.py --package no-such-package-xyz --repo https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/x86_64

echo.
echo Тест 5: Ошибка - версия не найдена
echo ^> python src\main.py --package curl --version 0.0.1 --repo https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/x86_64
python src\main.py --package curl --version 0.0.1 --repo https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/x86_64

echo.
echo Тест 6: Ошибка - репозиторий недоступен
echo ^> python src\main.py --package curl --repo http://localhost:1
python src\main.py --package curl --repo http://localhost:1

pause