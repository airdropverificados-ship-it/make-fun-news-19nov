"""Entry program for the make.fun bounty "Sum up 19 November's world news
in one image" (make.fun/bounty/news-image-20261119) — v2 dense edition.

The finished image (entry.png, kept in this repository) is copied to
/output/entry.png. The run is deterministic: no network access, no
randomness, no timestamps, so repeated runs produce identical bytes.
After the copy, the program checks that the copy has exactly the same
byte count as the original and fails with a non-zero exit status if the
two sizes differ.
"""
import shutil
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
SOURCE_IMAGE = REPO_DIR / "entry.png"
TARGET_IMAGE = Path("/output/entry.png")


def run():
    TARGET_IMAGE.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_IMAGE, TARGET_IMAGE)
    original_bytes = SOURCE_IMAGE.stat().st_size
    copied_bytes = TARGET_IMAGE.stat().st_size
    if copied_bytes != original_bytes:
        print(
            f"error: copied file size does not match the original: "
            f"{SOURCE_IMAGE} is {original_bytes} bytes but "
            f"{TARGET_IMAGE} is {copied_bytes} bytes",
            file=sys.stderr,
        )
        raise SystemExit(1)
    print(
        f"ok: {TARGET_IMAGE} written ({copied_bytes} bytes) — "
        f"size verified against {SOURCE_IMAGE}"
    )


if __name__ == "__main__":
    run()
