import statistics
import sys
import time

import requests


class SpeedTest:
    def __init__(self, url: str, count: int = 10):
        self.url = url
        self.count = count
        self._times: list[float] = []
        self._total_bytes: int = 0

    def run(self):
        print(f"Адрес  : {self.url}")
        print(f"Запросы: {self.count}")
        print("-" * 50)

        for i in range(1, self.count + 1):
            self._fetch(i)

        self._print_results()

    def _fetch(self, index: int):
        try:
            start = time.perf_counter()
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(self.url, headers=headers, timeout=30)
            elapsed = time.perf_counter() - start
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"  [{index:2d}/{self.count}] ОШИБКА: {e}", file=sys.stderr)
            return

        size = len(response.content)
        self._times.append(elapsed)
        self._total_bytes += size

        print(f"  [{index:2d}/{self.count}]  {elapsed:.3f} с   {size / 1_048_576:.2f} МБ")

    def _print_results(self):
        if not self._times:
            print("Все запросы завершились ошибкой.", file=sys.stderr)
            sys.exit(1)

        avg_time = statistics.mean(self._times)
        total_mb = self._total_bytes / 1_048_576
        speed_mbps = total_mb / sum(self._times)

        print("-" * 50)
        print(f"Выполнено запросов   : {len(self._times)}/{self.count}")
        print(f"Среднее время запроса: {avg_time:.3f} с")
        print(f"Скачано данных       : {total_mb:.2f} МБ")
        print(f"Средняя скорость     : {speed_mbps:.2f} МБ/с")
