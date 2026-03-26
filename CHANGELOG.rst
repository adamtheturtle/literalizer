Changelog
=========

Next
----

2026.03.26
----------

- Added ``narrow_map_value_type`` option to ``Go``, ``Cpp``, ``CSharp``, ``Dart``, ``Kotlin``, ``Scala``, and ``Python``. Defaults to ``True`` (existing behavior). Set to ``False`` to always use the broad value type (e.g. ``map[string]any`` instead of ``map[string]string`` in Go, ``dict[str, Any]`` instead of ``dict[str, str]`` in Python inline type hints).

2026.03.25
----------


2026.03.23
----------


2026.03.22.1
------------


2026.03.22
----------


2026.03.21
----------


- Removed ``LanguageSpec`` dataclass. Use the ``Language`` protocol directly to define custom languages.

2026.03.20.3
------------


2026.03.20.2
------------


2026.03.20.1
------------


2026.03.20
----------


2026.03.19.1
------------


2026.03.19
----------


2026.03.18
----------


- Added ``format_sequence_entry`` to the ``Language`` protocol, mirroring the existing ``format_set_entry`` field. All built-in languages use the new ``passthrough_sequence_entry`` formatter.

2026.03.17.2
------------


2026.03.17.1
------------


2026.03.17
----------


2026.03.16.2
------------


2026.03.16.1
------------


2026.03.16
----------


2026.03.15.2
------------


2026.03.15.1
------------


2026.03.15
----------


2026.03.14
----------


2026.03.13
----------
