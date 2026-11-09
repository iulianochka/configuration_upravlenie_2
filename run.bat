@echo off

echo Тест 1: Успешный запуск (получаем зависимости)
python src\main.py --package A --repo tests\test_graph.txt --test-mode

echo.
echo Тест 2: Ошибка (файл не найден)
python src\main.py --package A --repo tests\no_file.txt --test-mode