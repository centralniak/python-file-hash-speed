from typing import Generator

import os
import pathlib
import string


ALPHANUM = string.ascii_letters + string.digits
ALPHANUM_LEN = len(ALPHANUM)
CHUNK = 1024 * 1024
SIZE = (100, 1024)  # in megabytes
STEP = 100


def write_to(filename: pathlib.Path, contents_generator: Generator[str, None, None]):
    with open(filename, 'w') as f:
        for chunk in contents_generator:
            f.write(chunk)


def noise_generator(length: int) -> Generator[str, None, None]:
    for x in range(int(length / CHUNK)):
        yield ALPHANUM[x % ALPHANUM_LEN] * CHUNK


def main():
    here = pathlib.Path(__file__).parent
    dest = here / 'files'

    os.makedirs(dest, exist_ok=True)

    start, stop = SIZE
    for filesize in range(start, stop, STEP):
        filename = dest / '{}MB.file'.format(filesize)
        write_to(filename, noise_generator(filesize * 1024 * 1024))


if __name__ == '__main__':
    main()
