"""
Модуль для валидации параметров.
"""
import sys
import os
import urllib.parse
import argparse


def validate_args(args: argparse.Namespace) -> None:
    """
    Проверяет корректность переданных параметров.

    :param args: объект с параметрами.
    """
    if not args.package.strip():
        print("Ошибка: Имя пакета не может быть пустым.", file=sys.stderr)
        sys.exit(1)

    if not args.version.strip():
        print("Ошибка: Версия пакета не может быть пустой.", file=sys.stderr)
        sys.exit(1)

    if args.test_mode:
        if not os.path.exists(args.repo):
            print(
                f"Ошибка: Тестовый файл не найден: {args.repo}",
                file=sys.stderr
            )
            sys.exit(1)
    else:
        parsed_url = urllib.parse.urlparse(args.repo)
        if parsed_url.scheme not in ("http", "https"):
            print(
                "Ошибка: URL должен начинаться с http:// или https://",
                file=sys.stderr
            )
            sys.exit(1)


def get_direct_dependencies(package: str, repo: str, test_mode: bool) -> list:
    """
    Извлекает прямые зависимости для пакета из тестового файла.

    :param package: имя пакета.
    :param repo: путь к файлу или URL.
    :param test_mode: флаг тестового режима.
    :return: список имен пакетов-зависимостей.
    """
    dependencies = []
    
    if test_mode:
        with open(repo, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                if ":" in line:
                    pkg_name, deps_str = line.split(":", 1)
                    pkg_name = pkg_name.strip()
                    
                    if pkg_name == package:
                        deps_str = deps_str.strip()
                        if deps_str:
                            deps = deps_str.split(",")
                            for dep in deps:
                                dependencies.append(dep.strip())
                        break
                        
    return dependencies