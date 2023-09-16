from pathlib import Path
from itertools import accumulate

with (Path(__file__).parent.joinpath("input.txt").open("r", encoding="utf-8") as file):
    print(max(accumulate(file, func=lambda acc, line: acc + int(line) if line.strip() else 0, initial=0)))

