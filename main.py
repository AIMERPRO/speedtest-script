import argparse

from speedtest import SpeedTest


def parse_args():
    parser = argparse.ArgumentParser(
        description="Замерятель скорости интернета — выполняет N последовательных запросов к URL."
    )
    parser.add_argument("url", help="Адрес для запросов (например, https://example.com/large.jpg)")
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        metavar="N",
        help="Количество последовательных запросов (по умолчанию: 10)",
    )
    parsed = parser.parse_args()

    if parsed.count < 1:
        parser.error("--count должен быть положительным числом")

    return parsed


if __name__ == "__main__":
    args = parse_args()
    SpeedTest(url=args.url, count=args.count).run()
