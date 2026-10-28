"""Собирает все пять презентаций, проверяет макет и рендерит превью.

Запуск: python3 presentation/variants/build_all.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

DECKS = [
    ('deck_swiss', '01_Swiss_типографика.pptx', 'swiss', '255,255,255'),
    ('deck_industrial', '02_Industrial_фото.pptx', 'industrial', '18,16,16'),
    ('deck_editorial', '03_Editorial_журнал.pptx', 'editorial', '247,242,232'),
    ('deck_neon', '04_Neon_data.pptx', 'neon', '5,7,14'),
    ('deck_report', '05_Report_отчёт.pptx', 'report', '251,248,242'),
]


def run(mod, name, sub, bg):
    out = ROOT / 'presentation' / name
    subprocess.run([sys.executable, str(HERE / f'{mod}.py')], check=True,
                   stdout=subprocess.DEVNULL)
    chk = subprocess.run([sys.executable, str(HERE / 'check.py'), str(out)],
                         capture_output=True, text=True).stdout.strip()
    issues = chk.splitlines()
    n = issues[0].split(':')[1].strip().split()[0] if issues else '?'
    subprocess.run([sys.executable, str(HERE / 'proof.py'), str(out), sub, bg],
                   check=True, stdout=subprocess.DEVNULL)
    print(f'{name:<32} замечаний: {n}')
    for line in issues[1:]:
        print('   ', line.strip())


if __name__ == '__main__':
    for args in DECKS:
        run(*args)
