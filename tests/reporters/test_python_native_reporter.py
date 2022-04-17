import os
from pathlib import Path

from approvaltests import verify

from approvaltests.reporters.python_native_reporter import *
from py._path.local import LocalPath


def test_files_identical(tmpdir: LocalPath) -> None:
    file1 = os.path.join(str(tmpdir), "a.received.txt")
    file2 = os.path.join(str(tmpdir), "b.approved.txt")
    identical_contents = "abc"
    with open(file1, "w") as f1:
        f1.write(identical_contents)
    with open(file2, "w") as f2:
        f2.write(identical_contents)
    verify(calculate_diff_with_approve_instruction(file1, file2))


def test_files_differ(tmpdir: LocalPath) -> None:
    file1 = os.path.join(str(tmpdir), "a.received.txt")
    file2 = os.path.join(str(tmpdir), "b.approved.txt")
    with open(file1, "w") as f1:
        f1.write("abc\n")
    with open(file2, "w") as f2:
        f2.write("def\n")
    diff = calculate_diff_with_approve_instruction(file1, file2)
    diff = diff.replace(str(tmpdir), "tmpdir")  # use scrubber in future
    diff = diff.replace("\\", "/")
    clean_diff = ""
    for line in diff.split("\n"):
        if line.startswith("mv") or line.startswith("move"):
            clean_diff += "<move command line>"
        else:
            clean_diff += line + "\n"
    verify(clean_diff)


def test_approved_file_is_created_when_missing(tmpdir: LocalPath) -> None:
    file1 = os.path.join(str(tmpdir), "a.received.txt")
    file2 = os.path.join(str(tmpdir), "b.approved.txt")
    with open(file1, "w") as f1:
        f1.write("abc")
    reporter = PythonNativeReporter()
    reporter.report(file1, file2)
    assert Path(file2).exists()
