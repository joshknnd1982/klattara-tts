"""Builds klatter.nvda-addon: NVDA is a 64-bit x86 process, so it needs an x64 DLL
even on ARM64 Windows."""
import configparser
import pathlib
import shutil
import subprocess
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
ADDON = ROOT / "nvda" / "addon"
TARGET = "x86_64-pc-windows-msvc"


def main():
    subprocess.run(["cargo", "build", "--release", "-q", "-p", "klatter-ffi", "--target", TARGET],
                   cwd=ROOT, check=True)
    shutil.copy(ROOT / "target" / TARGET / "release" / "klatter.dll",
                ADDON / "synthDrivers" / "klatter" / "klatter.dll")
    manifest = configparser.ConfigParser()
    manifest.read_string("[addon]\n" + (ADDON / "manifest.ini").read_text(encoding="utf-8"))
    version = manifest["addon"]["version"].strip('"')
    out = ROOT / "target" / f"klatter-{version}.nvda-addon"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(ADDON.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                z.write(path, path.relative_to(ADDON).as_posix())
        z.write(ROOT / "data" / "cmudict" / "LICENSE.txt", "synthDrivers/klatter/cmudict-LICENSE.txt")
    print(out)


if __name__ == "__main__":
    main()
