from typing import Callable

import csv
import collections
import glob
import hashlib
import os
import pathlib
import sys
import time


CHUNK = 1024


TimedResult = collections.namedtuple('TimedResult', 'results, time')


def time_and_return(fun: Callable, repeat: int = 1) -> TimedResult:
    t_start = time.time()
    results = []
    for _ in range(repeat):
        results.append(fun())
    t_end = time.time()
    return TimedResult(results, t_end - t_start)


def calculate_partial(filename: str, algorithm: str) -> Callable:
    def inner():
        hasher = hashlib.new(algorithm)
        with open(filename, 'rb') as f:
            f_chunk = f.read(CHUNK)
            while f_chunk:
                hasher.update(f_chunk)
                f_chunk = f.read(CHUNK)
        return hasher.hexdigest()
    return inner


def main():
    here = pathlib.Path(__file__).parent
    dest = here / 'files'
    repeat = int(sys.argv[1])

    csv_writer = csv.writer(sys.stdout)
    csv_writer.writerow(['File size', 'Algorithm', 'Time {} runs'.format(repeat), 'Example result'])

    for filename in sorted(glob.glob(str(dest / '*'))):
        filesize = os.path.getsize(filename)
        algorithms_normalised = set([a.lower() for a in hashlib.algorithms_available])
        for algorithm in algorithms_normalised:
            hashing_function = calculate_partial(filename, algorithm)
            try:
                timed_result = time_and_return(hashing_function, repeat)
            except Exception:
                continue
            csv_writer.writerow([filesize / 1024 / 1024, algorithm, timed_result.time, timed_result.results[0]])


if __name__ == '__main__':
    main()
