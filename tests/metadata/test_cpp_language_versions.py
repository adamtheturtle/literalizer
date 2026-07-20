"""C++ language-standard target metadata."""

from literalizer.languages import Cpp


def test_cpp_language_versions_are_explicit() -> None:
    """C++ exposes the supported standards with C++20 as the default."""
    assert tuple(Cpp.version_formats) == (
        Cpp.version_formats.CPP14,
        Cpp.version_formats.CPP17,
        Cpp.version_formats.CPP20,
    )
    assert Cpp().language_version is Cpp.version_formats.CPP20


def test_cpp_language_version_is_selectable() -> None:
    """Callers can target C++14 or C++17 explicitly."""
    assert (
        Cpp(language_version=Cpp.version_formats.CPP14).language_version
        is Cpp.version_formats.CPP14
    )
    assert (
        Cpp(language_version=Cpp.version_formats.CPP17).language_version
        is Cpp.version_formats.CPP17
    )
