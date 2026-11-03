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