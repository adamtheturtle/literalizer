Changelog
=========

Next
----

- ``Jsonnet`` now emits ``$ref`` declarations as top-level ``local``
  bindings before the call expressions, so call-mode output with
  ``ref_declarations`` is supported.  Previously the integration
  harness skipped ``Jsonnet`` for ref-declaration cases because the
  array-wrapped output had no place for variable bindings.  The
  ``DeclarationStyles.ASSIGN`` template changed from ``{value}`` to
  ``local {name} = {value};``, and ``Jsonnet`` now overrides
  ``wrap_calls_with_declarations`` to emit those bindings before
  ``wrap_in_file`` wraps the calls in ``[ … ]``.
- ``Crystal.wrap_in_file`` now wraps content in a
  ``module Check ... end`` block with ``extend self``, matching what
  Erlang, Scala, and Haskell already do.  ``Crystal`` gains a
  ``module_name`` constructor argument (default ``"Check"``) to
  control the wrapper name.  Callers that relied on
  ``literalize(language=Crystal(), wrap_in_file=True)`` returning bare
  content will now receive a ``module`` block.
- Java sets and dicts no longer emit a trailing comma when
  ``trailing_comma=TrailingCommas.YES`` is requested.  ``Set.of(...)``
  and ``Map.ofEntries(...)`` are method calls and the previous output
  was rejected by ``javac``.  ``SetFormatConfig`` and
  ``DictFormatConfig`` gain a ``supports_trailing_comma`` field
  (defaults to ``True``) mirroring ``SequenceFormatConfig``; formats
  built around method-call syntax can opt out.
- Added ``CallStyleEnum`` as the base class for per-language
  ``CallStyles`` enums.  Its :attr:`config` accessor returns the
  enum member's value typed as the :data:`CallStyle` union, removing
  the ``cast("CallStyle", self.call_style.value)`` boilerplate
  previously duplicated in every multi-style language module.
- ``module_name`` has moved from a parameter on ``literalize`` and
  ``literalize_call`` to a constructor argument on the ten languages
  whose ``wrap_in_file`` introduces a named scope: ``C``, ``Cpp``,
  ``D``, ``Erlang``, ``Fortran``, ``FSharp``, ``Java``, ``ObjectiveC``,
  ``Occam`` and ``SystemVerilog``.  Pass it when constructing the
  language (e.g. ``Java(module_name="Foo")``); it defaults to
  ``"Module"``.  Languages whose wrappers do not introduce a named
  scope no longer accept ``module_name`` at all, so passing it where
  it has no effect is now a ``TypeError`` instead of being silently
  ignored.  ``Language.wrap_in_file`` and
  ``Language.wrap_combined_in_file`` lose the ``module_name``
  parameter; the named-scope languages read ``self.module_name``
  instead.  Languages must now be instantiated before being passed to
  ``literalize`` (``language=Python()`` rather than
  ``language=Python``).
- OCaml integer values outside the signed 64-bit range now raise
  ``UnrepresentableIntegerError`` instead of emitting an
  ``int_of_string`` fallback that overflowed OCaml's 63-bit native
  ``int`` at runtime and silently misrepresented the data.
- ``literalize_call`` now supports Visual Basic.  The default style is
  positional (``foo(1, 2)``); ``VisualBasic.CallStyles.NAMED`` enables
  VB's named-argument syntax (``foo(x:=1, y:=2)``).  Generated stubs
  are emitted as module-level ``Class`` and ``Function`` blocks and
  the call body is placed inside ``Sub _calls()`` because VB does not
  allow bare expression statements at module scope.
- Added ``literalize_call`` support for ``Zig``.  ``Zig.CallStyles``
  now exposes a ``POSITIONAL`` member backed by
  :class:`PositionalCallStyle`, and ``format_call_preamble_stub``
  emits file-scope Zig stub declarations because Zig disallows
  nested function definitions inside ``main``.  Dotted targets like
  ``app.client.fetch`` are realized as a nested ``struct`` chain rooted at
  a module-level constant, and call arguments are wrapped in the
  ``ZVal`` union so anonymous union literals coerce to a concrete
  type at the call site.
- ``literalize_call`` now emits R stub declarations
  (``name <- function(...) NULL``) for the called function and any
  call-transform wrappers, so generated R call output runs cleanly
  under ``Rscript`` without ``could not find function`` errors.
- Removed ``R.TrailingCommas.YES``: R's ``list()`` rejects empty
  arguments, so ``list(1, 2,)`` parses but raises at runtime.  Only
  ``R.TrailingCommas.NO`` remains.
- Fixed Dhall typed-empty literals for doubly-nested lists.  Input like
  ``[[[1, 2]], [], [[3, 4]]]`` previously rendered the empty sibling as
  ``[] : List List Integer``, which is invalid Dhall (parses as
  ``(List List) Integer``).  The inner ``List`` type is now
  parenthesized, producing ``[] : List (List Integer)``.
- ``infer_element_type`` no longer gives up when a nested list is empty
  alongside non-empty homogeneous siblings: empty inner lists are now
  skipped during inference, so input like ``[[1, 2], [], [3, 4]]``
  resolves to ``ListType(inner=int)`` instead of falling back to
  ``None`` (mixed types).  When the rendered list literal contains an
  empty inner list beside non-empty list siblings, the empty inner now
  inherits the typed sequence opener of its siblings, so generated
  literals type-check cleanly under strongly typed languages
  (``new int[]{}`` instead of ``new Object[]{}`` for Java,
  ``std::vector<int>{}`` for C++, ``[]int{}`` for Go, ``vec![]`` for
  Rust, ``New Integer() {}`` for Visual Basic, etc.).
- Documented the preamble-duplication sharp edge that arises when a
  caller composes :func:`literalize` (declaring a ``{"$ref": "name"}``
  variable) with :func:`literalize_call` (referencing it) into a
  single source file: each call independently computes its own
  ``preamble`` and ``body_preamble``, so the combined output contains
  duplicates that strict compilers reject and a linter flags.  The
  ``literalize_call`` reference now points at the new
  "Composing declarations and calls" section in
  ``docs/source/function-call-use-case.rst``, which shows a worked
  Haskell example with the combined ``body_preamble`` blocks already
  deduplicated.
- ``CommonLisp`` now wraps ``{"$ref": "name"}`` identifiers in earmuffs
  (``*name*``) at the call site so they resolve to the matching
  ``defparameter`` declaration.  ``CommonLisp`` is no longer skipped by
  the ``literalize_call`` reference-argument integration tests, which
  now lint cleanly under SBCL.
- ``Erlang`` now capitalizes ``{"$ref": "name"}`` call arguments so
  they reference the declared variable instead of parsing as a
  lowercase atom, matching the existing ``My_var = ...`` capitalization
  on the declaration site.  ``Erlang.format_variable_declaration`` now
  emits the trailing ``,`` separator itself so multiple declarations can
  precede a call; :meth:`Erlang.wrap_in_file` is adjusted accordingly
  and the rendered output is unchanged for the single-declaration case.
- ``Perl`` ``literalize_call`` output now emits Perl's scalar ``$``
  sigil before each ``{"$ref": "name"}`` identifier via a
  ``format_call_ref_identifier`` override, so a ref to ``my_var``
  renders as ``$my_var`` at the call site and lines up with the
  ``my $my_var = ...`` declaration site.  Generated files now pass
  ``perl -c`` under ``use strict`` and ``Perl`` is no longer excluded
  from the integration suite's ref-declaration golden cases.
- Added ``literalize_call`` support for ``Matlab``.  ``Matlab.CallStyles``
  now has a ``POSITIONAL`` member backed by a :class:`PositionalCallStyle`,
  and ``format_call_stub`` emits ``name = @(varargin) [];`` assignments so
  every target (including dotted paths like ``app.client.fetch``) is a
  bound function handle before it is invoked.  MATLAB's auto-vivifying
  struct-field assignment means a single line defines the entire chain
  regardless of depth, so the stub is one statement per call target.
- ``lint-purescript`` in ``.github/workflows/lint.yml`` now runs each
  PureScript fixture end-to-end.  A new ``Run PureScript files`` step
  compiles each fixture with ``purs compile`` and loads the resulting
  ``Check`` module in Node so its top-level ``my_data`` binding is
  evaluated, catching foreign-implementation failures and other
  load-time crashes that the existing ``check_purescript_syntax.py``
  compile-only check would miss.  The shared Prelude stub used by both
  steps lives in a new ``purescript_common.py`` module.
- Added a ``benchmarks`` job to ``.github/workflows/ci.yml`` that runs
  the ``tests/benchmarks/`` suite under `CodSpeed
  <https://codspeed.io>`_ via ``pytest-codspeed``.  The job posts a
  per-benchmark performance delta on every pull request, making it
  easier to spot regressions in the YAML fast path, JSON formatting,
  and heterogeneous-widening logic.
- ``C``, ``Cpp``, and ``ObjectiveC``
  ``wrap_in_file`` / ``wrap_combined_in_file`` output now emits
  ``(void)<variable_name>;`` after the declaration (and between the
  declaration and the re-assignment in the combined form) so the
  initial value is read before it is overwritten.  clang-tidy's
  ``clang-analyzer-deadcode.DeadStores`` check, previously suppressed
  in ``.clang-tidy`` because the combined form and unused C++ scalars
  triggered dead-store warnings, is now enforced.

2026.04.24.1
------------


- ``Gleam`` now emits a ``pub type GVal`` declaration containing only
  the constructors actually needed for the data, rather than always
  emitting all eight variants.  Scalar-only inputs (e.g.  ``GInt(42)``)
  now produce a one-constructor type, bringing Gleam in line with Elm
  and Haskell.
- ``lint-lua`` in ``.github/workflows/lint.yml`` now runs each Lua
  fixture end-to-end via ``lua``, catching runtime errors (calls to
  undefined functions, missing module imports, failed assertions)
  that the existing ``luac -p`` parse-only step let through,
  mirroring ``lint-bash`` / ``lint-javascript`` / ``lint-perl`` etc.
- ``literalize_call(..., wrap_in_file=True)`` now injects a no-op
  stub for the ``target_function`` into the wrapped file, so the
  generated source compiles against strict checkers on its own.
  Callers that supply a ``call_transform`` are still responsible for
  providing a definition for the wrapper function the transform
  introduces.
- Added ``literalize_call`` support for ``Bash``.  A new
  :class:`CommandCallStyle` tagged-union member renders calls as
  ``target arg1 arg2`` with space-separated arguments and no
  surrounding parentheses; with a ``call_transform`` like
  ``lambda c: f"emit({c})"`` the inner call is wrapped in
  ``$(...)`` command substitution (``emit "$(target arg1 arg2)"``).
  Bash's ``format_call_stub`` emits ``name() { :; }`` function
  stubs that accept any arguments so generated files parse with
  ``bash -n`` and run under ``bash``.  A new
  ``CallArgNotSupportedError`` is raised at literalize time when a
  list, dict, or set is passed as a Bash call argument — Bash has
  no inline compound-literal syntax in command invocations, so
  silently emitting ``cmd (1 2 3)`` (which parses as a nested
  ``(...)`` child-process group) would leave users with a broken
  script; callers must declare the collection as a variable and
  pass a ``$ref`` marker instead.
- ``literalize_call`` gains a ``ref_case`` keyword argument that
  converts ``{"$ref": "name"}`` identifiers to the target language's
  idiomatic case at render time via ``pyhumps``.  Pass
  ``IdentifierCase.SNAKE``, ``CAMEL``, ``PASCAL``, ``UPPER_SNAKE``, or
  ``KEBAB`` to drive one YAML source through multiple languages
  without re-authoring the ref names (e.g. the same ``user_obj`` ref
  renders as ``user_obj`` for Python, ``userObj`` for JavaScript,
  ``UserObj`` for Go).  Each language exposes the subset it
  understands via its ``identifier_cases`` tuple; passing an
  unsupported case raises ``UnsupportedIdentifierCaseError``.  When
  ``ref_case=None`` (the default) ref names are emitted verbatim,
  preserving existing behavior.
- ``Mojo`` now supports an opt-in
  ``HeterogeneousStrategies.VARIANT`` that wraps mixed scalars in an
  auto-generated ``comptime Value = Variant[...]`` over only the Mojo
  types actually present in the data, with a
  ``from std.utils.variant import Variant`` preamble line.  Each
  wrapped scalar renders as ``Value(...)`` (with an explicit
  ``String(...)`` or ``Float64(...)`` cast when needed to select the
  intended Variant alternative, and ``NoneType()`` for nulls), so
  heterogeneous dicts and lists become homogeneous in the Variant
  type.  The alias name is configurable via
  ``Mojo.heterogeneous_value_variant_name`` (default ``"Value"``).
  The default ``ERROR`` strategy still raises on heterogeneous input.
- ``C`` generated output now routes positive integers above
  ``LLONG_MAX`` (e.g. ``2**63``) through a new ``unsigned long long``
  union field instead of narrowing them into the signed ``long long``
  field.  The ``CVal`` union gains a ``u`` member alongside ``i``, and
  a new ``uint_field`` constructor argument lets users rename it.
  clang-tidy's ``bugprone-narrowing-conversions`` and
  ``cppcoreguidelines-narrowing-conversions`` checks, previously
  suppressed in ``.clang-tidy`` because the union-initializer literal
  silently truncated those values, are now enforced for both ``C``
  and ``Cpp`` output.
- ``Cpp`` generated output now wraps the ``INFINITY`` and ``NAN``
  ``<cmath>`` macros in ``static_cast<double>`` (with the negation
  applied outside the cast for ``-INFINITY``) so that brace-init of
  ``std::vector<double>`` does not trip clang-tidy's
  narrowing-conversions check on the implicit ``float``-to-``double``
  conversion.
- ``Erlang`` now supports ``literalize_call``.  Calls use positional
  argument syntax (``f(A, B)``); dotted targets like
  ``app.client.fetch`` are emitted as quoted-atom function names
  (``'app.client.fetch'(...)``) since Erlang atoms do not allow
  unquoted dots.  Call stubs are emitted as module-level function
  definitions placed between ``-export`` and ``x()``, and ``x()``
  separates call statements with ``,`` terminated by ``.``.
- Added ``literalize_call`` support for Gleam:
  ``Gleam.format_call_preamble_stub`` emits module-level ``pub fn``
  declarations with fresh type variables per parameter and a
  ``panic`` body, and ``Gleam.format_call_target`` flattens dotted
  targets (e.g. ``app.client.fetch``) to underscored identifiers
  (``app_client_fetch``) because Gleam identifiers cannot contain
  ``.``.  ``Gleam.CallStyles.POSITIONAL`` renders calls as
  ``func(arg1, arg2)``.
- ``ObjectiveC`` call stubs now emit ``k``-prefixed, title-cased root
  names for the ``static const struct`` globals that back dotted call
  targets, so a user-written ``throttler.check(...)`` literalizes to
  ``kThrottler.check(...)`` (and ``app.client.fetch`` to
  ``kApp.client.fetch``).  clang-tidy's
  ``google-objc-global-variable-declaration`` check, previously
  suppressed in ``.clang-tidy`` because the bare root names did not
  conform, is now enforced.

2026.04.24
----------


- ``literalize_call`` with ``per_element=True`` now widens Rust's
  ``TAGGED_ENUM`` scalar wrapping across sibling calls at matching
  argument slots.  Previously the wrap analysis ran per call, so a
  locally-homogeneous sibling dict would emit unwrapped scalars
  even when another call at the same slot was heterogeneous — a
  second ``m.process(HashMap::from([("a", "x")]))`` would not match
  the ``&HashMap<&'static str, Value>`` parameter implied by the
  first heterogeneous call.  Mirrors the dict-opener widening
  already applied for typed dict languages on the per-element call
  path.
- ``lint-erlang`` in ``.github/workflows/lint.yml`` now passes
  ``-Werror`` to ``erlc``, so warnings such as ``evaluation of operator
  '-'/1 will fail with a 'badarith' exception`` fail the job instead of
  being silently logged.  ``Erlang`` generated output for negative
  infinity is now the quoted atom ``'-inf'`` instead of the bare
  ``-inf``, which the compiler treated as unary negation of the atom
  ``inf`` and flagged as a guaranteed runtime ``badarith``.

2026.04.23
----------


- Sibling sequences that appear as values of the same dict now widen
  to a common element type at each matching position, so a caller
  iterating the dict values tuple-style sees a consistent element
  type at each positional slot instead of one branch narrowed to a
  concrete type and another collapsed to the fallback.  The widening
  uses the language's fallback sequence opener when the inferred
  types diverge and is skipped for variant-typed languages (e.g.
  C++) whose fallback opener is element-specific rather than
  universally accepting.
- ``lint-haskell`` in ``.github/workflows/lint.yml`` now passes
  ``-Wall -Werror`` to both the syntax check and the end-to-end build,
  so warnings such as ``-Wunused-matches``, ``-Woverlapping-patterns``,
  and ``-Wtype-defaults`` fail the job instead of being silently
  logged.  ``Haskell`` generated output was updated to compile clean
  under ``-Wall``: the ``Num`` / ``Fractional`` instances use ``_``
  for unused parameters, the catch-all ``negate _`` clause is now
  omitted when ``Val`` has only numeric constructors, tuple-sequence
  bindings carry a ``(Val, Val, ...)`` annotation, call stubs get
  explicit type signatures, transform-wrapper stubs use a polymorphic
  argument type, ``main`` binds each call result with ``_ <-``, and
  the ``Data.Time`` import set drops ``secondsToDiffTime`` when every
  datetime has microseconds.
- ``Java`` declarations and reassignments whose value ends in a ``//``
  line comment now place the terminating ``;`` on the code line rather
  than on the comment line, where ``javac`` previously parsed it as
  part of the comment and rejected the program with ``';' expected``.
- ``Mojo.skip_null_dict_values`` is now ``True`` so dicts containing
  null values render as the empty ``Dict[String, String]()`` literal
  (previously they emitted ``{"k": None, ...}``, which the Mojo
  compiler rejects because ``NoneType`` is not a usable dict value
  type).  Mixed-type inputs continue to raise
  ``HeterogeneousScalarCollectionError`` as before; this only affects
  dicts whose values are entirely ``null``.
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
