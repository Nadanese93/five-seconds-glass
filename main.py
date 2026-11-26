import os
import sys

ENTRY = "That glass was blocking the fire exit, so I cleared it \u2014 I run safety in this house, and the floor is the assembly point."

MAX_LENGTH = 200


class BlankError(ValueError):
    """Entry is empty or whitespace-only."""


class MultiLineError(ValueError):
    """Entry contains a newline or carriage return."""


class LengthError(ValueError):
    """Entry exceeds the maximum length."""


class VerificationError(RuntimeError):
    """Written entry.txt does not match the intended entry bytes."""


def validate(entry):
    if not entry or not entry.strip():
        raise BlankError("entry is blank or whitespace-only")
    if "\n" in entry or "\r" in entry:
        raise MultiLineError("entry must be a single line")
    if not 1 <= len(entry) <= MAX_LENGTH:
        raise LengthError("entry length must be 1-%d characters" % MAX_LENGTH)


def verify_written(path, intended):
    with open(path, "rb") as f:
        actual = f.read()
    if actual != intended.encode("utf-8"):
        raise VerificationError("entry.txt bytes differ from intended entry")


def main():
    validate(ENTRY)
    out_dir = os.environ["MAKEFUN_OUTPUT_DIR"]
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    verify_written(path, ENTRY)


if __name__ == "__main__":
    main()
