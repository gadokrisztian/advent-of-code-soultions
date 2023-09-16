from pathlib import Path
from itertools import accumulate
import heapq as hq

with (Path(__file__).parent.joinpath("input.txt").open("r", encoding="utf-8") as file):
    print(sum(hq.nlargest(3, accumulate(file, func=lambda acc, line: acc + int(line) if line.strip() else 0, initial=0))))
