"""Build the pinned Clang tools with the local performance fixes."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import logging
import platform
import re
import shlex
import shutil
import subprocess
import tarfile
from pathlib import Path

LOGGER = logging.getLogger(name=__name__)
VERSION = "23.1.4"
SOURCE_COMMIT = "7a941dfb2877a0b8cf30323fefa85ad019e0b0f5"
ASSETS = {
    "aarch64": (
        "ARM64",
        "0975f753e0f9b5f83146a7a2f4678bc143e713496b56520716a4de047a63f99f",
    ),
    "x86_64": (
        "X64",
        "efdd1dbd089b99bfcfcde7b8eb1236163f2e88df5a981cca4f783ec9cb5e0378",
    ),
}


class Arguments(argparse.Namespace):
    """Directories supplied by the toolchain job."""

    work_directory: Path
    output_directory: Path

    def __init__(self) -> None:
        """Initialize fields before argparse assigns both required
        paths.
        """
        super().__init__()
        self.work_directory = Path()
        self.output_directory = Path()


def run(command: list[str], /, *, cwd: Path | None) -> str:
    """Run a build command and retain useful failure output."""
    LOGGER.info("%s", shlex.join(split_command=command))
    result = subprocess.run(
        args=command,
        cwd=cwd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    LOGGER.info("%s", result.stdout)
    result.check_returncode()
    return result.stdout.strip()


def digest(path: Path, /) -> str:
    """Hash a downloaded artifact without reading it all into memory."""
    with path.open(mode="rb") as contents:
        return hashlib.file_digest(contents, "sha256").hexdigest()


def program(name: str, /) -> str:
    """Resolve the system tools explicitly selected by this builder."""
    resolved = shutil.which(cmd=name)
    if resolved is None:
        raise FileNotFoundError(name)
    return resolved


def keep_bootstrap_file(relative: Path, /) -> bool:
    """Keep development files and the bootstrap programs they require."""
    if relative.parts[0] == "include":
        return True
    if relative.parts[0] == "bin":
        return relative.name in {
            "clang",
            "clang++",
            "clang-23",
            "clang-tidy",
            "clang-tblgen",
            "llvm-ar",
            "llvm-config",
            "llvm-strip",
            "llvm-objcopy",
        }
    if relative.parts[0] != "lib":
        return False
    return (
        relative.name.endswith((".a", ".so"))
        or ".so." in relative.name
        or (len(relative.parts) > 1 and relative.parts[1] == "clang")
    )


def bootstrap(work: Path, /) -> Path:
    """Verify and extract the official release's development files."""
    architecture, expected_digest = ASSETS[platform.machine()]
    name = f"LLVM-{VERSION}-Linux-{architecture}.tar.zst"
    archive_path = work / name
    url = (
        "https://github.com/llvm/llvm-project/releases/download/"
        f"llvmorg-{VERSION}/{name}"
    )
    if not archive_path.exists():
        temporary = archive_path.with_suffix(suffix=".part")
        _ = run(
            [
                program("curl"),
                "--fail",
                "--location",
                "--retry",
                "3",
                "--connect-timeout",
                "30",
                "--max-time",
                "300",
                "--output",
                str(object=temporary),
                url,
            ],
            cwd=work,
        )
        if digest(temporary) != expected_digest:
            message = "LLVM release checksum mismatch"
            raise ValueError(message)
        _ = temporary.replace(target=archive_path)
    if digest(archive_path) != expected_digest:
        message = "Cached LLVM release checksum mismatch"
        raise ValueError(message)
    prefix = work / "bootstrap"
    marker = prefix / "release.sha256"
    if marker.exists() and marker.read_text().strip() == expected_digest:
        return prefix
    prefix.mkdir(parents=True, exist_ok=True)
    # The release uses a 1 GiB window; unrelated programs need several GiB.
    with subprocess.Popen(
        args=[
            program("zstd"),
            "--decompress",
            "--stdout",
            "--long=31",
            str(object=archive_path.resolve()),
        ],
        stdout=subprocess.PIPE,
    ) as decoder:
        if decoder.stdout is None:
            message = "LLVM archive decompressor has no output stream"
            raise RuntimeError(message)
        with tarfile.open(fileobj=decoder.stdout, mode="r|") as archive:
            for member in archive:
                parts = Path(member.name).parts
                if len(parts) <= 1:
                    continue
                relative = Path(*parts[1:])
                if keep_bootstrap_file(relative):
                    member.name = str(object=relative)
                    archive.extract(member, path=prefix, filter="data")
        if decoder.wait() != 0:
            message = "LLVM release decompression failed"
            raise RuntimeError(message)
    _ = marker.write_text(data=expected_digest + "\n")
    return prefix


def source_tree(work: Path, patch: Path, /) -> Path:
    """Apply the patch to an isolated checkout of the matching source."""
    source = work / f"source-{digest(patch)[:12]}"
    if not (source / ".git").exists():
        source.mkdir(parents=True, exist_ok=True)
        _ = run(["git", "init", str(object=source)], cwd=None)
        _ = run(["git", "sparse-checkout", "init", "--cone"], cwd=source)
        _ = run(
            [
                "git",
                "sparse-checkout",
                "set",
                "clang/lib/Sema",
                "clang/tools/driver",
                "clang-tools-extra/clang-tidy/tool",
                "clang-tools-extra/clang-tidy/utils",
                "clang/lib/StaticAnalyzer/Checkers/WebKit",
                "clang/test/SemaTemplate",
            ],
            cwd=source,
        )
        _ = run(
            [
                "git",
                "fetch",
                "--filter=blob:none",
                "--depth=1",
                "https://github.com/llvm/llvm-project.git",
                SOURCE_COMMIT,
            ],
            cwd=source,
        )
        _ = run(["git", "checkout", "--detach", "FETCH_HEAD"], cwd=source)
    if run(["git", "rev-parse", "HEAD"], cwd=source) != SOURCE_COMMIT:
        message = "Compiler source does not match the release"
        raise ValueError(message)
    already_applied = subprocess.run(
        args=[
            program("git"),
            "apply",
            "--reverse",
            "--check",
            str(object=patch),
        ],
        cwd=source,
        capture_output=True,
        check=False,
    )
    if already_applied.returncode != 0:
        _ = run(["git", "apply", "--check", str(object=patch)], cwd=source)
        _ = run(["git", "apply", str(object=patch)], cwd=source)
    return source


def patched_libraries(
    prefix: Path,
    work: Path,
    archive_members: dict[str, list[Path]],
    object_files: dict[Path, Path],
    /,
) -> Path:
    """Replace implementation objects in copies of the release
    archives.
    """
    patched_archives = work / "patched-libraries"
    patched_archives.mkdir(exist_ok=True)
    for name, members in archive_members.items():
        destination = patched_archives / name
        _ = shutil.copyfile(src=prefix / "lib" / name, dst=destination)
        # Archive replacement uses member basenames, as in the upstream build.
        replacements: list[str] = []
        for path in members:
            replacement = patched_archives / (path.name + ".o")
            _ = shutil.copyfile(src=object_files[path], dst=replacement)
            replacements.append(str(object=replacement))
        _ = run(
            [
                str(object=prefix / "bin/llvm-ar"),
                "rcs",
                str(object=destination),
                *replacements,
            ],
            cwd=None,
        )
    return patched_archives


def verify_checks(prefix: Path, binaries: Path, /) -> None:
    """Require all upstream clang-tidy checks to remain registered."""
    stock_checks = run(
        [str(object=prefix / "bin/clang-tidy"), "--list-checks", "--checks=*"],
        cwd=None,
    )
    patched_checks = run(
        [str(object=binaries / "clang-tidy"), "--list-checks", "--checks=*"],
        cwd=None,
    )
    if stock_checks != patched_checks:
        message = (
            "The rebuilt tool must retain every upstream clang-tidy check"
        )
        raise ValueError(message)


def verify_frontend(source: Path, binaries: Path, /) -> None:
    """Retain upstream SFINAE diagnostics and stack-exhaustion
    behavior.
    """
    compiler = str(object=binaries / "clang")
    cases = source / "clang/test/SemaTemplate"
    for standard in ("c++11", "c++14", "c++17", "c++20", "c++23"):
        _ = run(
            [
                compiler,
                "-cc1",
                "-fsyntax-only",
                "-verify",
                f"-std={standard}",
                str(object=cases / "diagnose-enable-if-t.cpp"),
            ],
            cwd=None,
        )
    for test in (1, 2, 3):
        _ = run(
            [
                compiler,
                "-cc1",
                "-verify",
                f"-DTEST={test}",
                str(object=cases / "stack-exhaustion.cpp"),
            ],
            cwd=None,
        )


def verify_exception_analysis(support: Path, binaries: Path, /) -> None:
    """Keep exception types and diagnostic frames through cached calls."""
    output = run(
        [
            program("timeout"),
            "--signal=KILL",
            "60s",
            str(object=binaries / "clang-tidy"),
            str(object=support / "exception-analysis.cpp"),
            "--checks=-*,bugprone-exception-escape",
            "--config={}",
            "--",
            "-std=c++20",
            "-fexceptions",
        ],
        cwd=None,
    )
    diagnosed = re.findall(
        pattern=(
            r"warning: an exception may be thrown in function '([^']+)' "
            r"which should not throw exceptions"
        ),
        string=output,
    )
    expected = {
        "escaped_after_catch",
        "escaped_rethrow",
        "caught_contexts",
        "recursive_escape",
        "repeated_escape",
    }
    if len(diagnosed) != len(expected) or set(diagnosed) != expected:
        message = "Exception analysis changed escaping or caught exceptions"
        raise ValueError(message)
    if (
        "frame #1: function 'escaped_after_catch' calls function 'leaf' here"
        not in output
        or "unhandled exception of type 'double'" not in output
    ):
        message = "Exception analysis lost a call frame or rethrow type"
        raise ValueError(message)


def compiler_flags(config: str, /) -> list[str]:
    """Match the release's language, ABI and assertion configuration."""
    if run([config, "--version"], cwd=None) != VERSION:
        message = "Unexpected bootstrap compiler version"
        raise ValueError(message)
    flags = shlex.split(s=run([config, "--cxxflags"], cwd=None))
    flags += ["-O3"]
    if run([config, "--assertion-mode"], cwd=None) == "OFF":
        flags += ["-DNDEBUG"]
    return flags


def build(work: Path, output: Path, /) -> None:
    """Relink upstream drivers with five rebuilt implementation
    objects.
    """
    support = Path(__file__).resolve().parents[1] / "ci" / "clang"
    patch = support / "performance.patch"
    prefix = bootstrap(work)
    source = source_tree(work, patch)
    compiler = str(object=prefix / "bin/clang++")
    config = str(object=prefix / "bin/llvm-config")
    flags = compiler_flags(config)
    flags_digest = hashlib.sha256(
        string="\0".join(flags).encode()
    ).hexdigest()[:12]
    objects = work / f"objects-{digest(patch)[:12]}-{flags_digest}"
    objects.mkdir(exist_ok=True)
    _ = run(
        [
            str(object=prefix / "bin/clang-tblgen"),
            "-gen-clang-opencl-builtins",
            str(object=source / "clang/lib/Sema/OpenCLBuiltins.td"),
            "-o",
            str(object=objects / "OpenCLBuiltins.inc"),
        ],
        cwd=None,
    )
    flags += ["-I" + str(object=objects)]
    sema = [
        source / f"clang/lib/Sema/{name}.cpp"
        for name in (
            "SemaLookup",
            "SemaTemplate",
            "SemaOverload",
        )
    ]
    checker = source / (
        "clang/lib/StaticAnalyzer/Checkers/WebKit/"
        "RefCntblBaseVirtualDtorChecker.cpp"
    )
    exception_analyzer = source / (
        "clang-tools-extra/clang-tidy/utils/ExceptionAnalyzer.cpp"
    )
    driver = source / "clang/tools/driver"
    driver_sources = [
        support / "driver.cpp",
        *(
            driver / f"{name}.cpp"
            for name in (
                "driver",
                "cc1_main",
                "cc1as_main",
                "cc1gen_reproducer_main",
            )
        ),
    ]
    tidy_source = source / (
        "clang-tools-extra/clang-tidy/tool/ClangTidyToolMain.cpp"
    )
    sources = [
        *sema,
        checker,
        exception_analyzer,
        *driver_sources,
        tidy_source,
    ]
    object_files = {
        path: objects / f"{index}-{path.name}.o"
        for index, path in enumerate(iterable=sources)
    }

    def compile_source(path: Path, /) -> None:
        """Compile using the release's ABI, RTTI and exception flags."""
        if (
            object_files[path].exists()
            and object_files[path].stat().st_mtime >= path.stat().st_mtime
        ):
            return
        _ = run(
            [
                compiler,
                *flags,
                "-c",
                str(object=path),
                "-o",
                str(object=object_files[path]),
            ],
            cwd=None,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        _ = list(pool.map(compile_source, sources))
    patched_archives = patched_libraries(
        prefix,
        work,
        {
            "libclangSema.a": sema,
            "libclangStaticAnalyzerCheckers.a": [checker],
            "libclangTidyUtils.a": [exception_analyzer],
        },
        object_files,
    )
    clang_archives = [
        patched_archives / path.name
        if (patched_archives / path.name).exists()
        else path
        for path in sorted((prefix / "lib").glob(pattern="libclang*.a"))
        if path.name
        not in {"libclang.a", "libclang-cpp.a", "libclangTidyPlugin.a"}
    ]
    llvm_archives = shlex.split(
        s=run([config, "--link-static", "--libfiles", "all"], cwd=None)
    )
    system_libraries = shlex.split(
        s=run([config, "--link-static", "--system-libs"], cwd=None)
    )
    libraries = [
        "-Wl,--start-group",
        *map(str, clang_archives),
        *llvm_archives,
        "-Wl,--end-group",
        *system_libraries,
        "-pthread",
    ]
    binaries = output / "bin"
    binaries.mkdir(parents=True, exist_ok=True)
    for name, members in (
        ("clang", driver_sources),
        ("clang-tidy", [tidy_source]),
    ):
        _ = run(
            [
                compiler,
                *flags,
                *[str(object=object_files[path]) for path in members],
                "-o",
                str(object=binaries / name),
                *libraries,
            ],
            cwd=None,
        )
        _ = run(
            [
                str(object=prefix / "bin/llvm-strip"),
                "--strip-debug",
                str(object=binaries / name),
            ],
            cwd=None,
        )
        _ = run([str(object=binaries / name), "--version"], cwd=None)
    (binaries / "clang++").unlink(missing_ok=True)
    (binaries / "clang++").symlink_to(target="clang")
    resource = output / "lib/clang/23"
    _ = shutil.copytree(
        src=prefix / "lib/clang/23", dst=resource, dirs_exist_ok=True
    )
    verify_checks(prefix, binaries)
    verify_frontend(source, binaries)
    verify_exception_analysis(support, binaries)
    _ = shutil.copyfile(
        src=support / "LICENSE.TXT", dst=output / "LICENSE.TXT"
    )
    metadata = {
        "llvm_version": VERSION,
        "source_commit": SOURCE_COMMIT,
        "patch_sha256": digest(patch),
        "cxx_flags": flags,
        "clang_sha256": digest(binaries / "clang"),
        "clang_tidy_sha256": digest(binaries / "clang-tidy"),
    }
    _ = (output / "build.json").write_text(
        data=json.dumps(obj=metadata, indent=2) + "\n"
    )


def main() -> None:
    """Build inside job-owned directories, leaving system tools alone."""
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--work-directory", type=Path, required=True)
    _ = parser.add_argument("--output-directory", type=Path, required=True)
    arguments = parser.parse_args(namespace=Arguments())
    work = arguments.work_directory.resolve()
    work.mkdir(parents=True, exist_ok=True)
    build(work, arguments.output_directory.resolve())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
