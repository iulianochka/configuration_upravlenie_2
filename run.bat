@echo off
chcp 65001 >nul

echo Тест 1: Успешный запуск (тестовый режим)
echo ^> python src\main.py --package A --repo tests\test_graph.txt --test-mode
python src\main.py --package A --repo tests\test_graph.txt --test-mode

echo.
echo Тест 2: Ошибка - не указан --package
echo ^> python src\main.py --repo tests\test_graph.txt --test-mode
python src\main.py --repo tests\test_graph.txt --test-mode

echo.
echo Тест 3: Ошибка - пустое имя пакета
echo ^> python src\main.py --package "" --repo tests\test_graph.txt --test-mode
python src\main.py --package "" --repo tests\test_graph.txt --test-mode

echo.
echo Тест 4: Ошибка - недопустимые символы в имени пакета
echo ^> python src\main.py --package "a b" --repo tests\test_graph.txt --test-mode
python src\main.py --package "a b" --repo tests\test_graph.txt --test-mode

echo.
echo Тест 5: Ошибка - не указан --repo
echo ^> python src\main.py --package A --test-mode
python src\main.py --package A --test-mode

echo.
echo Тест 6: Ошибка - тестовый файл не найден
echo ^> python src\main.py --package A --repo tests\no_file.txt --test-mode
python src\main.py --package A --repo tests\no_file.txt --test-mode

echo.
echo Тест 7: Ошибка - вместо файла указана папка
echo ^> python src\main.py --package A --repo tests --test-mode
python src\main.py --package A --repo tests --test-mode

echo.
echo Тест 8: Ошибка - неверный URL
echo ^> python src\main.py --package A --repo abc
python src\main.py --package A --repo abc

echo.
echo Тест 9: Ошибка - URL без адреса
echo ^> python src\main.py --package A --repo http://
python src\main.py --package A --repo http://

echo.
echo Тест 10: Ошибка - неверная версия
echo ^> python src\main.py --package A --repo tests\test_graph.txt --version "!!!" --test-mode
python src\main.py --package A --repo tests\test_graph.txt --version "!!!" --test-mode

echo.
echo Тест 11: Ошибка - URL указан вместе с тестовым режимом
echo ^> python src\main.py --package A --repo https://example.com --test-mode
python src\main.py --package A --repo https://example.com --test-mode

pause