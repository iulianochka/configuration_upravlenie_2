"""
Модуль для валидации параметров.
"""
import sys
import os
import urllib.parse
import argparse
import re

PACKAGE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")
VERSION_PATTERN = re.compile(r"^(latest|[0-9][A-Za-z0-9._+~-]*)$")


def fail(message: str) -> None:
    """Печатает ошибку и завершает программу с кодом 1."""
    print(f"Ошибка: {message}", file=sys.stderr)
    sys.exit(1)


def validate_repo(repo: str, test_mode: bool) -> None:
    """Проверяет путь к тестовому файлу или URL репозитория."""
    if test_mode:
        if repo.startswith(("http://", "https://")):
            fail("В тестовом режиме нужен путь к файлу, а не URL")
        if not os.path.isfile(repo):
            fail(f"Тестовый файл не найден: {repo}")
        return
    parsed_url = urllib.parse.urlparse(repo)
    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        fail("URL должен иметь вид http://адрес или https://адрес")


def validate_args(args: argparse.Namespace) -> None:
    """
    Проверяет корректность переданных параметров.

    :param args: объект с параметрами.
    """
    if not PACKAGE_PATTERN.match(args.package.strip()):
        fail("Недопустимое имя пакета (буквы, цифры и символы . _ + -).")
    if not VERSION_PATTERN.match(args.version.strip()):
        fail("Недопустимая версия (например: latest или 1.2.3-r0).")
    validate_repo(args.repo, args.test_mode)