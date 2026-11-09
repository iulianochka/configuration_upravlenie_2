"""
Визуализатор графа зависимостей пакетов.
Вариант 16, Этап 1: Минимальный прототип с конфигурацией.
"""
import argparse
from parser import validate_args, get_direct_dependencies


def parse_args() -> argparse.Namespace:
    """
    Разбирает опции командной строки.

    :return: объект с параметрами.
    """
    parser = argparse.ArgumentParser(
        description="Визуализатор графа зависимостей (Вариант 16)"
    )
    parser.add_argument(
        "--package",
        type=str,
        required=True,
        help="Имя анализируемого пакета"
    )
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="URL-адрес репозитория или путь к файлу"
    )
    parser.add_argument(
        "--version",
        type=str,
        default="latest",
        help="Версия пакета"
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Режим работы с тестовым репозиторием"
    )
    return parser.parse_args()


def print_config(args: argparse.Namespace) -> None:
    """
    Выводит параметры в формате ключ-значение.

    :param args: объект с параметрами.
    """
    print("--- Параметры запуска ---")
    print(f"package:   {args.package}")
    print(f"repo:      {args.repo}")
    print(f"version:   {args.version}")
    print(f"test_mode: {args.test_mode}")
    print("------------------------")


def main() -> None:
    """Точка входа программы."""
    args = parse_args()
    validate_args(args)
    print_config(args)

    print(f"Прямые зависимости для пакета '{args.package}':")
    deps = get_direct_dependencies(args.package, args.repo, args.test_mode)
    
    if not deps:
        print(" - (нет зависимостей)")
    else:
        for dep in deps:
            print(f" - {dep}")


if __name__ == "__main__":
    main()