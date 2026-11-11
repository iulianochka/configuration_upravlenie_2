"""
Модуль получения прямых зависимостей пакета (этап 2).

Данные можно получить двумя способами:
1. Из реального репозитория Alpine Linux по URL.
2. Из тестового файла (режим --test-mode).
"""
import io
import tarfile
import urllib.request

from parser import fail

INDEX_ARCHIVE_NAME = "APKINDEX.tar.gz"
INDEX_FILE_NAME = "APKINDEX"
TIMEOUT_SECONDS = 30
LATEST = "latest"
VERSION_SIGNS = "<>=~"


def read_test_file(package: str, path: str) -> list:
    """
    Читает прямые зависимости пакета из тестового файла.

    Каждая строка файла имеет вид "A: B, C": слева пакет,
    справа через запятую его зависимости.

    :param package: имя пакета.
    :param path: путь к тестовому файлу.
    :return: список имён зависимостей.
    """
    dependencies = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if ":" not in line:
                continue
            name, deps_text = line.split(":", 1)
            if name.strip() != package:
                continue
            for dep in deps_text.split(","):
                dep = dep.strip()
                if dep:
                    dependencies.append(dep)
            break
    return dependencies


def make_index_url(repo: str) -> str:
    """
    Делает адрес файла APKINDEX.tar.gz из адреса репозитория.

    Пример: .../main/x86_64 -> .../main/x86_64/APKINDEX.tar.gz

    :param repo: адрес репозитория.
    :return: адрес файла с индексом пакетов.
    """
    if repo.endswith(INDEX_ARCHIVE_NAME):
        return repo
    if not repo.endswith("/"):
        repo = repo + "/"
    return repo + INDEX_ARCHIVE_NAME


def download_index_text(url: str) -> str:
    """
    Скачивает архив APKINDEX.tar.gz и возвращает текст из него.

    Внутри архива лежит текстовый файл APKINDEX со списком всех пакетов.
    Параметр ignore_zeros нужен, потому что архив Alpine состоит из двух
    склеенных частей (подпись и сам индекс).

    :param url: адрес файла APKINDEX.tar.gz.
    :return: текст индекса.
    """
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
            archive_bytes = response.read()
        archive = tarfile.open(
            fileobj=io.BytesIO(archive_bytes),
            mode="r:gz",
            ignore_zeros=True
        )
        index_file = archive.extractfile(INDEX_FILE_NAME)
        text = index_file.read().decode("utf-8")
        archive.close()
    except (OSError, tarfile.TarError, KeyError, UnicodeDecodeError) as error:
        fail(f"Не удалось получить данные из {url}: {error}")
    return text


def parse_index_text(text: str) -> list:
    """
    Разбивает текст APKINDEX на пакеты.

    Пакеты в тексте разделены пустой строкой. Каждая строка пакета
    имеет вид "буква:значение", например "P:curl" (имя пакета),
    "V:8.5.0-r0" (версия), "D:libcurl musl" (зависимости).

    :param text: текст индекса.
    :return: список пакетов, каждый пакет - словарь {буква: значение}.
    """
    packages = []
    current = {}
    for line in text.splitlines():
        if line == "":
            if current:
                packages.append(current)
            current = {}
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            current[key] = value
    if current:
        packages.append(current)
    return packages


def find_package(packages: list, name: str, version: str):
    """
    Ищет пакет с нужным именем и версией.

    :param packages: список пакетов из индекса.
    :param name: имя пакета.
    :param version: версия или "latest" (подойдёт любая).
    :return: найденный пакет или None.
    """
    for package in packages:
        if package.get("P") != name:
            continue
        if version == LATEST or package.get("V") == version:
            return package
    return None


def clean_dependency(text: str) -> str:
    """
    Убирает из зависимости условие на версию.

    Пример: "musl>=1.2" -> "musl".

    :param text: зависимость как она записана в индексе.
    :return: имя зависимости без условия на версию.
    """
    for sign in VERSION_SIGNS:
        position = text.find(sign)
        if position != -1:
            text = text[:position]
    return text


def get_alpine_dependencies(package: str, repo: str, version: str) -> list:
    """
    Получает прямые зависимости пакета из репозитория Alpine.

    Шаги: скачать индекс, разобрать его, найти пакет, взять поле D.
    Зависимости-конфликты (начинаются с "!") пропускаются.

    :param package: имя пакета.
    :param repo: адрес репозитория.
    :param version: версия пакета или "latest".
    :return: список имён зависимостей.
    """
    text = download_index_text(make_index_url(repo))
    packages = parse_index_text(text)
    found = find_package(packages, package, version)
    if found is None:
        fail(f"Пакет {package} версии {version} не найден в репозитории")
    dependencies = []
    for raw in found.get("D", "").split():
        if raw.startswith("!"):
            continue
        dependencies.append(clean_dependency(raw))
    return dependencies


def get_direct_dependencies(
    package: str, repo: str, test_mode: bool, version: str = LATEST
) -> list:
    """
    Возвращает прямые зависимости пакета.

    :param package: имя пакета.
    :param repo: адрес репозитория или путь к тестовому файлу.
    :param test_mode: True - читать тестовый файл, False - Alpine по URL.
    :param version: версия пакета (только для Alpine).
    :return: список имён зависимостей.
    """
    if test_mode:
        return read_test_file(package, repo)
    return get_alpine_dependencies(package, repo, version)
