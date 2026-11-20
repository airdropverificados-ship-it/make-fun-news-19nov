"""Entry program for the make.fun bounty 'Sum up 19 November's world news
in one image' (make.fun/bounty/news-image-20261119) — v2 dense edition.

Copies the pre-built image (entry.png, stored in this repository) to
/output/entry.png. Deterministic: no network, no randomness, no timestamps;
both runs write the same bytes.
"""
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
DST = Path("/output/entry.png")


def main():
    DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
