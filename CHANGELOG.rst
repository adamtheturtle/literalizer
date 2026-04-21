Changelog
=========

Next
----

- Added ``Dhall.HeterogeneousStrategies`` with a ``UNION_TYPE`` option
  that auto-generates a Dhall union type in the preamble whenever a
  dict, list, or sibling-list pair contains scalar values of more
  than one Dhall type.  Each heterogeneous value is wrapped at the
  call site as ``{UnionName}.{Variant} payload``; only the variants
  actually present in the data are emitted.  The union name defaults
  to ``Value`` and is configurable via the new
  ``heterogeneous_value_union_name`` constructor argument.  The
  default remains ``HeterogeneousStrategies.ERROR`` (unchanged
  behavior).

2026.04.21.5
------------


- Added ``Rust.DeclarationStyles.LAZY_STATIC``, which wraps the
  initializer in ``std::sync::LazyLock`` so module-level
  declarations can hold runtime-initialized collections such as
  ``HashMap``, ``BTreeMap``, and ``Vec``.  Unlike ``CONST`` and
  ``STATIC``, ``LAZY_STATIC`` composes with every dict, set, and
  sequence format.  ``use std::sync::LazyLock;`` is added to the
  preamble automatically.
- Added ``literalize_call`` support for Common Lisp:
  ``CommonLisp.format_call_stub`` emits ``defun`` stubs with
  ``&rest args`` so generated definitions accept any mix of positional
  and keyword arguments, and ``CommonLisp.CallStyles.PREFIX_KEYWORD``
  renders calls as ``(func :name value)``.
- Added ``literalize_call`` support for Racket:
  ``Racket.format_call_stub`` now generates
  ``make-keyword-procedure`` stub definitions, and a new
  ``PrefixCallStyle`` call-style variant handles S-expression call
  assembly ``(func arg1 arg2)`` for Lisp-family languages.

2026.04.21.4
------------


- Fixed ``pre_indent_level`` interaction with ``NewVariable`` and
  ``ExistingVariable``: a multi-line value no longer inserts the
  pre-indent between ``=`` and the value (and no longer doubly
  indents continuation lines).  Every line of the wrapped declaration
  or assignment is now uniformly offset by ``pre_indent_level``.
- **Breaking:** Replaced the three public collection-opener helpers
  ``fixed_set_open``, ``fixed_sequence_open``, and ``fixed_dict_open``
  with a single ``fixed_open``.  They had identical implementations
  and differed only in the type hint of the unused parameter.  Replace
  each call with ``fixed_open(open_str=...)``.
- ``literalize_call`` now raises ``ParameterCountMismatchError`` with
  a descriptive ``Expected N parameters but got M values`` message
  when ``parameter_names`` does not match a row's value count,
  replacing the opaque ``ValueError`` from ``zip(strict=True)``.

2026.04.21.3
------------


- Added ``Rust.HeterogeneousStrategies`` with a ``TAGGED_ENUM`` option
  that auto-generates a small tagged ``enum`` in the preamble whenever
  a dict, list, or sibling-list pair contains scalar values of more
  than one Rust type.  Each heterogeneous value is wrapped at the
  call site as ``{EnumName}::{Variant}(value)``; only the variants
  actually present in the data are emitted, with integer variants
  using Rust's narrowest-width names (``I32``, ``I64``, ``I128``).
  The enum name defaults to ``Value`` and is configurable via the new
  ``heterogeneous_value_enum_name`` constructor argument.  The
  default remains ``HeterogeneousStrategies.ERROR`` (unchanged
  behavior).
- The ``lint-julia`` CI job now executes Julia golden files instead
  of only parsing them, catching ``UndefVarError`` and other runtime
  errors.
- ``literalize_call`` now distinguishes two reasons a language has no
  call support.  The single ``UnsupportedCallStyleError`` has been
  replaced by ``CallsNotSupportedByLanguageError`` (raised for
  data/markup formats like YAML, TOML, JSON5, Norg that have no
  function call syntax) and ``CallsNotSupportedByToolError`` (raised
  for programming languages whose call rendering literalizer has not
  yet implemented).  The new ``CallSupport`` enum on a language's
  ``call_style_config`` attribute captures which case applies.
- Lint workflow now runs pre-commit hooks against the full supported
  Python matrix (3.12, 3.13, 3.14) instead of 3.13 only, to catch
  version-specific lint issues.

2026.04.21.2
------------


- Added ``literalize_call`` support for PHP: ``Php.format_call_stub``
  now generates function, class, and nested-object stubs for a call
  expression.

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
