Changelog
=========

Next
----

- The ``lint-julia`` CI job now executes Julia golden files instead
  of only parsing them, catching ``UndefVarError`` and other runtime
  errors.

2026.04.21.1
------------


2026.04.21
----------


- Added a per-language ``Modifiers`` enum exposed on each language
  class (alongside ``DateFormats``, ``SequenceFormats``, etc.).
  ``Java.Modifiers`` has ``PUBLIC``/``PRIVATE``/``PROTECTED``/
  ``STATIC``/``FINAL``; ``CSharp.Modifiers`` adds ``CONST`` and
  ``READONLY``; ``Cpp.Modifiers`` has ``STATIC``/``CONST``.  Languages
  without modifier vocabulary expose an empty ``Modifiers`` enum.
- ``NewVariable`` and ``BothVariableForms`` now accept a ``modifiers``
  keyword argument.  Values that are not members of the target
  language's ``Modifiers`` enum are silently ignored, matching how
  other language format enums behave.
- Removed automatic coercion of heterogeneous data to strings.  The
  ``error_on_coercion`` parameter has been removed from ``literalize``;
  ``literalize`` now always raises a subclass of
  ``HeterogeneousCollectionError`` when the data cannot be represented
  in the target language's collection formats.
- Replaced ``HeterogeneousCoercionError`` with precise exceptions:
  ``HeterogeneousCollectionError`` (base class),
  ``HeterogeneousScalarCollectionError``,
  ``HeterogeneousSiblingListsError``, ``MixedDictValuesError``,
  ``MixedListValuesError``, ``MixedDictShapesError``, and
  ``HeterogeneousSetError``.
- Renamed ``SetFormatConfig.coerce_mixed_to_str`` to
  ``SetFormatConfig.supports_heterogeneity`` (with inverted semantics).

2026.04.18
----------


2026.04.15
----------


2026.04.14
----------


2026.04.13
----------


2026.04.06
----------


- Added new output languages: Dhall, Elm, Gleam, JSON5, Jsonnet, Odin, PureScript, Raku, Scheme, SystemVerilog.
- Unified ``literalize_json``, ``literalize_yaml``, and ``literalize_toml`` into a single ``literalize`` function with an ``InputFormat`` parameter.
- Added TOML input support (``InputFormat.TOML``) with comment preservation.
- Added JSON5 input format (``InputFormat.JSON5``).
- Added ``body_preamble``, ``bare_code``, ``declaration_code``, and ``pre_declaration_comments`` attributes to ``LiteralizeResult``.
- Added ``requires_uniform_record_shapes`` and ``declared_type`` to ``SequenceFormatConfig``.
- Added ``supports_scalar_before_comments`` and ``supports_scalar_inline_comments`` language properties.

2026.03.30
----------


- Added ``default_ordered_map_value_type`` parameter to Go for configuring the element type in ordered map literals.
- Added ``supports_default_ordered_map_value_type`` and ``supports_default_ordered_map_key_type`` class attributes to ``LanguageCls``.

2026.03.29
----------


2026.03.26.2
------------


2026.03.26.1
------------


- Renamed ``VariableTypeHints.NONE`` to ``AUTO`` and ``VariableTypeHints.INLINE`` to ``ALWAYS``.

2026.03.26
----------


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
