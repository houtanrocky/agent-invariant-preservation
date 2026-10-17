"""Build an editable wheel; optional workaround for managed Windows temp-directory ACLs."""

import argparse
import os
import tempfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sandbox-temp-acl",
        action="store_true",
        help="Windows only: inherit workspace ACLs for disposable .local build directories",
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    local = root / ".local"
    temp = local / "tmp"
    wheels = local / "wheels"
    temp.mkdir(parents=True, exist_ok=True)
    wheels.mkdir(parents=True, exist_ok=True)
    original_mkdir = os.mkdir
    old_tempdir = tempfile.tempdir
    old_cwd = Path.cwd()

    def inherited_acl_mkdir(path, mode=0o777, *, dir_fd=None):
        if mode == 0o700 and Path(path).resolve().is_relative_to(local.resolve()):
            mode = 0o777
        return original_mkdir(path, mode, dir_fd=dir_fd)

    if args.sandbox_temp_acl and os.name != "nt":
        parser.error("--sandbox-temp-acl is only needed for the managed Windows sandbox")
    try:
        if args.sandbox_temp_acl:
            os.mkdir = inherited_acl_mkdir
        tempfile.tempdir = str(temp)
        os.chdir(root)
        from setuptools.build_meta import build_editable

        print(wheels / build_editable(str(wheels)))
    finally:
        os.mkdir = original_mkdir
        tempfile.tempdir = old_tempdir
        os.chdir(old_cwd)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
