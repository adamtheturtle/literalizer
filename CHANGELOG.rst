Changelog
=========

Next
----

- Sibling sequences that appear as values of the same dict now widen
  to a common element type at each matching position, so a caller
  iterating the dict values tuple-style sees a consistent element
  type at each positional slot instead of one branch narrowed to a
  concrete type and another collapsed to the fallback.  The widening
  uses the language's fallback sequence opener when the inferred
  types diverge and is skipped for variant-typed languages (e.g.
  C++) whose fallback opener is element-specific rather than
  universally accepting.
- ``literalize_call`` now accepts ``{"$ref": "name"}`` markers at
  argument positions, emitting ``name`` as a bare identifier instead
  of formatting the value as a literal.  Refs and literals can be
  mixed in the same call, and the marker is detected across all four
  input formats (JSON, JSON5, YAML, TOML).  Ref dicts are excluded
  from data-shape validation and data-driven preamble inference so
  they do not drag in imports for the ``{str: str}`` shape of the
  marker itself.
- ``lint-objectivec`` in ``.github/workflows/lint.yml`` now passes
  ``-Werror`` to both ``clang -fsyntax-only`` and the end-to-end
  ``clang`` compile step so warnings such as
  ``-Wimplicitly-unsigned-literal`` fail the job instead of being
  silently logged.  ``ObjectiveC.format_integer`` now appends a
  ``ULL`` suffix to values above ``LLONG_MAX`` (matching the C
  fallback) and raises ``UnrepresentableIntegerError`` for values
  below ``LLONG_MIN``, so emitted fixtures compile cleanly under the
  stricter workflow.
- Added ``Nim.HeterogeneousStrategies`` with an ``OBJECT_VARIANT``
  option that auto-generates a Nim object variant in the preamble
  whenever a dict, list, or sibling-list pair contains scalar values
  of more than one Nim type.  Each heterogeneous value is wrapped at
  the call site as ``{VariantName}(kind: vkX, xVal: value)``; only
  the branches actually present in the data are emitted.  The
  strategy switches the dict syntax from ``%* {key: value}`` to
  ``{key: value}.toTable`` (importing ``tables`` instead of ``json``)
  so the object variants can be stored directly, and nested sequences
  render as ``@[...]`` at every level.  The variant-type name
  defaults to ``Value`` and is configurable via the new
  ``heterogeneous_value_variant_name`` constructor argument.
  ``OBJECT_VARIANT`` is incompatible with
  ``DeclarationStyles.CONST`` because ``.toTable`` and ``@[]`` are
  runtime constructors; the constructor raises
  ``IncompatibleFormatsError`` for that combination.  The default
  remains ``HeterogeneousStrategies.ERROR`` (unchanged behavior).
- The ``heterogeneous_strategy`` variant case list now includes the
  ``ordered_map`` fixture, covering Rust ``TAGGED_ENUM`` and Dhall
  ``UNION_TYPE`` rendering on ``!!omap`` inputs.
- ``lint-swift`` in ``.github/workflows/lint.yml`` now runs its
  ``swiftc -typecheck`` step in parallel via ``xargs -P``, replacing
  the previous serial ``while`` loop so the job no longer cold-starts
  the compiler one fixture at a time.
- ``lint-swift`` in ``.github/workflows/lint.yml`` now runs each
  Swift fixture end-to-end via ``swift`` in script mode, catching
  runtime errors that ``swiftc -typecheck`` alone could miss
  (for example, integer literals that overflow ``Int``).  So that
  every emitted fixture compiles, ``Swift.format_integer`` now
  raises ``UnrepresentableIntegerError`` for values outside the
  signed 64-bit range, matching the behavior of other languages
  without native arbitrary-precision integer support.
- ``lint-groovy`` in ``.github/workflows/lint.yml`` now runs each
  Groovy fixture end-to-end, catching runtime errors (calls to
  undefined functions, missing module imports, failed assertions)
  that the existing ``groovyc`` compile-only step let through.
  ``Groovy.format_call_stub`` now emits a single ``Map _args`` method
  parameter when ``call_style`` is ``KEYWORD`` — previously the
  ``call_keyword_args`` fixture tripped ``MissingMethodException``
  because Groovy passes named arguments as a single ``LinkedHashMap``
  that a positional parameter list rejects.  ``POSITIONAL`` stubs
  keep the concrete parameter list unchanged.
- ``lint-objectivec`` now executes each fixture end-to-end instead of
  only syntax-checking it, mirroring ``lint-bash`` /
  ``lint-javascript`` / ``lint-perl`` etc.  To make this possible,
  Objective-C declarations and reassignments now box primitive
  scalars the same way collection entries do
  (``id x = 42;`` → ``id x = @(42);``), single-name call stubs emit a
  ``static`` definition so fixtures link, and
  ``ObjectiveC.supports_scalar_inline_comments`` is now ``False`` —
  previously the trailing ``//`` comment swallowed the statement
  terminator.  A pre-existing casing bug in the workflow's
  ``lang_patterns`` (``objective_c*.m`` instead of ``ObjectiveC*.m``)
  that silently skipped every fixture is also fixed.
- ``lint-elm`` in ``.github/workflows/lint.yml`` now runs each Elm
  fixture end-to-end.  A new ``Run Elm files`` step compiles each
  fixture alongside a small ``Main.elm`` wrapper whose
  ``Platform.worker`` init forces ``Check.my_data``, emits
  JavaScript via ``elm make``, and executes it with Node so
  runtime crashes such as ``Debug.todo`` surface in CI.  The
  ``scalar_int_very_negative_large`` fixture is skipped because
  the Elm 0.19.1 code generator emits ``--<digits>`` (two unary
  minuses) for integers at the int64 boundary, which JavaScript
  rejects as a prefix-decrement syntax error.
- ``lint-sml`` in ``.github/workflows/lint.yml`` now runs each
  Standard ML fixture end-to-end.  Because ``MLton`` never evaluates
  a ``structure``'s body unless a top-level expression forces it,
  the new step compiles each fixture via an ML Basis file that
  concatenates the fixture with a small ``val _ = Check.my_data``
  snippet and runs the resulting binary, catching runtime errors
  such as references to undefined names, missing module imports,
  or failed assertions.
- Removed the K&R-style empty-prototype suppression directives from
  C and Objective-C call stubs.
  ``C.format_call_preamble_stub`` and
  ``ObjectiveC.format_call_preamble_stub`` now emit concrete
  prototypes (``CVal`` parameters for C, ``id`` parameters for
  Objective-C) sized to the call's parameter list, and an internal
  ``format_call_arg`` hook wraps each call argument so the call site
  matches the prototype.  Generated C and Objective-C call code now
  compiles cleanly under ``-Wstrict-prototypes
  -Wdeprecated-non-prototype -Werror`` without suppression.
- C++ container types now pick the narrowest integer type that holds
  the actual values in each collection: ``int`` when every value fits
  in 32 bits, otherwise ``long long``.  This mirrors the existing
  per-value suffix logic in Rust and fixes a case where
  ``std::variant<int, …>`` could not hold literals above ``INT_MAX``.
  ``Cpp.NumericLiteralSuffixes.AUTO`` still emits ``long`` + ``L``
  suffix for every integer.
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
- Added ``literalize_call`` support for Clojure:
  ``Clojure.format_call_stub`` emits ``defn`` stubs with ``[& _args]``
  so generated definitions accept any mix of positional and keyword
  arguments, and ``Clojure.CallStyles.PREFIX_KEYWORD`` renders calls
  as ``(func :name value)``.
- Added ``literalize_call`` support for Objective-C:
  ``ObjectiveC.format_call_preamble_stub`` emits C-style forward
  declarations and nested ``struct`` chains with function-pointer
  leaves for dotted targets, and ``ObjectiveC.CallStyles.POSITIONAL``
  renders calls as ``func(arg1, arg2)``.
- Added ``literalize_call`` support for Perl:
  ``Perl.format_call_stub`` emits an empty ``sub {}`` declaration for
  each dot-separated part of the target name, so call expressions
  (including dotted targets, where ``.`` is Perl's string
  concatenation operator) compile cleanly under ``perl -c``.

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
