Changelog
=========

.. towncrier release notes start

2026.07.24.2
------------

No significant changes.

2026.07.24.1
------------

No significant changes.

2026.07.24
----------

No significant changes.

2026.07.22
----------

No significant changes.

2026.07.21.2
------------

No significant changes.

2026.07.21.1
------------

No significant changes.

2026.07.21
----------

No significant changes.

2026.07.20.1
------------

- Add ``literalize(record_null_substitutions=...)`` for replacing null-valued
  record fields by name before validation, type inference, and rendering. This
  lets a single language-neutral fixture use target-appropriate sentinels (for
  example C++ ``-1`` integers and empty strings) while unconfigured fields and
  languages retain their existing null behavior (issue #3143).

2026.07.20
----------

No significant changes.

2026.07.15
----------

- Under the Rust ``RECORD`` heterogeneous strategy, a list of records whose uniform top-level keys hold nested maps of divergent or disjoint shape under one key no longer raises ``HeterogeneousSiblingListsError``.  A shared inference pass detects a nested sibling-map family that cannot share one record shape and widens it to ``HashMap<&'static str, Value>``, wrapping the map's scalar leaves in the generated ``Value`` enum, so the enclosing record survives and the sibling list renders as compiling Rust.  This is the reference implementation; the remaining ``RECORD`` languages gain the same widening in later increments.

- Under Go's ``RECORD`` heterogeneous strategy, nested sibling maps with divergent or disjoint record shapes now widen to ``map[string]any`` instead of raising ``HeterogeneousSiblingListsError``.  Their uniform enclosing records remain generated structs, and the result compiles with the standard Go toolchain.

- Under Java's ``RECORD`` heterogeneous strategy, nested sibling maps with divergent or disjoint record shapes now widen to ``java.util.Map<String, Object>`` instead of emitting incompatible generated record types.  Their uniform enclosing records remain generated records, and the result compiles with the standard Java toolchain.

- C#'s ``RECORD`` heterogeneous strategy now widens incompatible nested sibling maps to ``Dictionary<string, object>`` while preserving the uniform outer record.

- Kotlin's ``RECORD`` heterogeneous strategy now widens incompatible nested sibling maps to ``Map<String, Any?>`` while preserving the uniform outer record.

- Scala's ``RECORD`` heterogeneous strategy now widens incompatible nested sibling maps to ``Map[String, Any]`` while preserving the uniform outer record.

- Swift's ``RECORD`` heterogeneous strategy now widens incompatible nested sibling maps to ``[String: Any]`` while preserving the uniform outer record.

- C++'s ``RECORD`` heterogeneous strategy now widens incompatible nested sibling maps to ``std::map`` values backed by a shared ``std::variant``, while preserving the uniform outer struct.

- Zig's ``RECORD`` heterogeneous strategy now widens incompatible nested sibling maps to its generated ``ZVal`` tagged union while preserving the uniform outer struct.

- Crystal's ``RECORD`` heterogeneous strategy now widens incompatible nested sibling maps to a ``Hash`` over a generated native scalar union while preserving the uniform outer record.

- D's ``RECORD`` heterogeneous strategy now widens incompatible nested sibling maps to ``JSONValue`` while preserving the uniform outer struct.

- Nim's ``RECORD`` heterogeneous strategy now widens incompatible nested sibling maps to ``Table[string, Value]`` using its generated object-variant carrier while preserving the uniform outer record.

- V's ``RECORD`` heterogeneous strategy now widens incompatible nested sibling maps to ``map[string]IVal`` using its existing interface carrier while preserving the uniform outer struct.

- Odin's ``RECORD`` heterogeneous strategy now widens incompatible nested sibling maps to ``map[string]any`` while preserving the uniform outer struct.

- C's ``RECORD`` heterogeneous strategy now widens incompatible nested sibling maps to the existing ``CVal``/``CKV`` tagged-union map representation, while preserving the uniform outer struct.

2026.07.14
----------

- Add an "Understanding the result" documentation page that defines each ``LiteralizeResult`` field, explains when ``preamble`` and ``body_preamble`` are populated and that they must precede ``code`` to compile, and shows how ``wrap_in_file=True`` assembles those fields into output that compiles for you.

- Document the ``variable_form`` argument with a "Binding the result to a variable" section that contrasts ``NewVariable``, ``ExistingVariable``, and ``BothVariableForms`` and shows the output each produces.

- Group the documentation index into captioned "Guides", "Reference", and "Project / Development" sections, and correct the contributing guide to reference ``prek`` hooks and the ``uv run --extra dev pytest`` test command.

- Move the language-definition (extension) API reference out of the consumer-facing API reference page and into the ``Languages`` guide, co-locating the ``Language`` protocol, the ``LanguageCls`` class, the ``*FormatConfig`` building blocks, and ``fixed_open`` with the narrative "Custom language implementations" how-to that already explains them.

- Add a public ``LiteralizeResult.sections`` accessor (a tuple of the new ``FileSection`` dataclass) that exposes the file regions of a multi-section language's ``wrap_in_file=False`` output, so a caller can compose each region into its own program template instead of parsing a language-internal marker.  COBOL under ``json_type=CJSON`` is the first such language, surfacing its ``WORKING-STORAGE`` and ``PROCEDURE`` regions (named by the ``Cobol.CJSON_WORKING_STORAGE_SECTION`` / ``Cobol.CJSON_PROCEDURE_SECTION`` constants); its CI round-trip helper now composes those regions directly rather than splicing into a wrapped program.

- Fold the resolution guidance for each exception into its class description (a "To resolve, ..." sentence) and render the remaining stages of the "Common errors" documentation page with ``autoexception`` directives instead of hand-maintained Cause / How-to-resolve tables, so each exception's meaning and recommended fix are single-sourced from ``literalizer.exceptions`` and can no longer drift between the page and the API reference.

- Generate the per-language heterogeneous-strategy support matrix in the documentation from the language registry at build time (rendered with the ``sphinx-jinja`` extension), so it can no longer drift from the ``heterogeneous_strategies`` enum on each language class.  This also corrects the previously stale matrix, which omitted several languages that now expose ``RECORD``.

- Fix Go output for nested maps whose sibling dict values have different value types: each inner map is now widened to ``map[string]any`` so the literal matches the enclosing container's declared type and compiles, instead of narrowing each inner map to its own value type (issue #2878).

- Fix Rust ``TAGGED_ENUM`` output for nested maps whose sibling dict values have different value types: the scalar leaves of every sibling map are now wrapped in the ``Value`` enum so each inner map is ``HashMap<&str, Value>`` and the sibling maps share one value type, instead of leaving individually homogeneous maps at their own narrower type and emitting code that does not compile (issue #2879).

- Under the Rust ``RECORD`` heterogeneous strategy, dict keys that collide with Rust keywords (e.g. ``type``, ``match``) now render as raw identifiers (``r#type``) in both the generated struct declarations and the struct literals, so the output compiles. Keys that no struct field name can express (``crate``, ``self``, ``super``, ``Self``, ``_``, or keys that are not identifier-shaped text) raise ``UnrepresentableInputError`` instead of emitting code that fails to compile.

- Fix Kotlin output for nested maps used where a nested map type is declared: a map value now keeps its ``Map<String, ...>`` type instead of collapsing to the ``Any?`` fallback, so an element map matches the declared ``mapOf<String, Map<String, Any?>>`` type and compiles (issue #2890).

- Raise ``HeterogeneousSiblingMapsError`` when a C++ container holds sibling maps whose value types force a widened dict slot the language cannot represent, instead of silently emitting a ``std::variant`` map literal that does not compile. Go and Kotlin widen these maps to their ``map[string]any`` / ``Any?`` fallback, but C++'s variant typing has no single value type every sibling map converts to, so ``literalize`` now rejects the input (use the ``RECORD`` strategy or a ``json_type`` to represent it).

- Fix Mojo ``VARIANT`` output for nested maps whose sibling dict values have different value types: the scalar leaves of every sibling map are now wrapped in the ``Value`` alias so each inner ``Dict`` shares one value type, instead of leaving individually homogeneous maps at their own narrower type and emitting code that does not compile (issue #2895).

- Fix V ``INTERFACE`` output for nested maps whose sibling dict values have different value types: the scalar leaves of every sibling map are now wrapped in ``IVal`` so each inner ``map`` shares one value type, instead of leaving individually homogeneous maps at their own narrower type and emitting code that does not compile (issue #2896).

- Fix Dhall ``UNION_TYPE`` output for nested maps whose sibling dict values have different value types: the scalar leaves of every sibling map are now wrapped in the ``Value`` union so each inner record shares one field type, instead of leaving individually homogeneous maps at their own narrower type and emitting code that does not type-check (issue #2897).

- Fix Nim ``OBJECT_VARIANT`` output for nested maps whose sibling dict values have different value types: the scalar leaves of every sibling map are now wrapped in the object-variant ``Value`` so each inner ``Table`` shares one value type, instead of leaving individually homogeneous maps at their own narrower type and emitting code that does not compile (issue #2898).

2026.06.02
----------

- Add a Bash JSON round-trip check to CI using the shared round-trip fixture, driven by the pinned ``bash`` interpreter. Because Bash associative arrays cannot nest, the check walks the known JSON shape and runs ``eval`` on each nested-collection string to rebuild a fresh array before re-emitting JSON.

- Add a C JSON round-trip check to CI using the shared round-trip fixture; because the literalizer's ``CVal`` union carries no run-time discriminator, the helper builds a parallel ``cJSON`` tree whose shape is generated from the parsed input (one ``cJSON_Create*`` call per node, reading the ``CVal`` slot that matches the original JSON type) and prints it with ``cJSON_PrintUnformatted``.

- Add a COBOL JSON round-trip check to CI using the shared round-trip fixture, compiled and run with GnuCOBOL and re-emitting JSON via the standard ``JSON GENERATE`` statement.  ``JSON GENERATE`` skips ``FILLER`` items (so the literalizer's ``FILLER``-group arrays cannot be reconstructed), has no JSON boolean and no floating-point support, and mangles keys to COBOL data names, so the helper renames the recoverable top-level scalars back to their original keys with a ``NAME OF`` clause and excludes the array/object/boolean/float fields plus the integer-overflowing ``biginteger`` and the width-truncated ``string_empty`` / ``string_unicode`` values.

- Add a Fortran JSON round-trip check to CI using the shared round-trip fixture, and switch the Fortran language module to emit ``real(real64)`` literals (with the matching ``freal`` constructor signature in the ``fval_m`` preamble) so that double-precision values like ``1.7976931348623157e+308`` are no longer silently truncated to single precision.

- Add a MATLAB JSON round-trip check to CI using the shared round-trip fixture, serializing the literalized ``myData`` value with the built-in ``jsonencode``; the 26-digit ``biginteger`` field is excluded because MATLAB's only numeric type is the IEEE 754 ``double``, which re-emits it as ``1e26``.

- Add a Mojo JSON round-trip check to CI using the shared round-trip fixture, run with ``mojo run``.  The shared input's mixed-type top-level object is literalized with the ``VARIANT`` heterogeneous strategy and re-emitted by copying each value out of its ``Variant`` slot into a CPython ``dict`` and calling ``json.dumps`` on it through Mojo's ``std.python`` bridge to CPython (Mojo has no JSON encoder of its own).  The wide ``biginteger`` field (which overflows Mojo's 64-bit ``Int``) and the array/object fields (which the ``VARIANT`` strategy cannot place alongside scalars in one dict) are excluded.

- Add a Nix JSON round-trip check to CI using the shared round-trip fixture, evaluating the literalized expression with ``nix-instantiate --eval --strict --json`` so that Nix's built-in JSON printer re-emits the value.

- Add a Norg JSON round-trip check to CI using the shared round-trip fixture.  The literalizer stores the value inside a ``@code json`` ranged verbatim tag, so the check parses the generated document with the ``tree-sitter-norg`` grammar, pulls the embedded code block back out, and re-parses it with the standard library ``json`` module.

- Add a PowerShell JSON round-trip check to CI using the shared round-trip fixture, serializing the literalized ``$myData`` value with the built-in ``ConvertTo-Json -Depth 100 -Compress``; the 26-digit ``biginteger`` field is excluded because PowerShell parses it as a ``[double]`` and re-emits it with a fractional part.

- Add a Scheme JSON round-trip check to CI using the shared round-trip fixture, driven by Guile 3 and the ``guile-json`` library.

- Add a SystemVerilog JSON round-trip check to CI using the shared round-trip fixture, built and run with ``verilator --binary``.  Because the literalizer's ``_VVal`` is a flat tagged record (it has no recursive component and no boolean tag), nested containers are serialized to opaque strings and booleans share the integer slot, so the helper generates the re-emitting walk from the parsed input's shape (one expression per top-level key, reading the ``_VVal`` slot that matches the original JSON type) and excludes the array/object fields, which cannot be walked back into at run time.

- Rework the Forth language to emit a structured visitor stream. The literalized ``: my_data ... ;`` definition now calls small constructor words (``+obj``/``-obj``/``+arr``/``-arr``/``+key``/``+int``/``+float``/``+str``/``+bool``/``+null``) that preserve the document structure, instead of the previous flat sequence of stack pushes that dropped all array and object boundaries.  The constructor words are a protocol the caller binds: literalizer ships a default binding (``src/literalizer/languages/forth_prelude.fs``) that writes JSON through the Forth Foundation Library ``jos`` module, so a literalized definition prints the document as JSON out of the box, while a caller can redefine any word to build a Forth-side structure or emit another format.

- Add ``Odin(json_type=Odin.json_types.JSON_VALUE)``, the Odin sibling of the existing Zig / C++ / Haskell / OCaml / PureScript JSON-value modes, so output renders the literalized document as a single ``json.parse_string`` call against an embedded JSON text rather than the default ``map[string]any`` / ``[dynamic]any`` shape.  The rendered binding therefore has the static type ``json.Value`` (the ``core:encoding/json`` sum type), so the value flows directly through ``json.marshal`` instead of needing a hand-rolled ``any``-walker, and ``heterogeneous_strategy=RECORD`` is rejected because the generated ``struct`` declarations cannot coexist with the single parsed value.

- Expose the nested ``JsonTypes`` and ``BoolFormats`` enum classes (plus their snake_case ``json_types`` / ``bool_formats`` aliases) on every ``Language`` subclass, using an empty enum for languages that do not support these options. Consumers can now enumerate these options uniformly across languages without reflection helpers.

- Add a ``json_type=Scheme.json_types.GUILE_JSON`` option to the Scheme language that renders objects as Scheme association lists, arrays as vectors, and null as ``'null`` so the literalized binding can be handed directly to guile-json's ``scm->json`` without an intermediate shape walker.

- Change the default ``Scheme`` dict and ordered-map rendering from a flat alternating ``(list "k" v "k" v ...)`` to an association list of cons pairs (``(list (cons "k" v) ...)``). Each entry is now a ``pair?`` rather than a bare scalar, so a non-empty mapping is locally distinguishable from a heterogeneous sequence, and the form is what ``assoc`` / ``alist->hash-table`` expect. The empty case stays ``(list)`` for both an empty dict and an empty sequence.

- Add ``C(json_type=C.json_types.CJSON)``, which renders the literalized document as a portable ``cJSON_Create*(...)`` node tree (one ``cJSON *`` statement per node, composed with ``cJSON_AddItemToArray`` / ``cJSON_AddItemToObject``) under ``#include <cjson/cJSON.h>`` instead of the default tagged ``CVal`` union. Integers are widened to ``double`` (``cJSON`` has no integer constructor) and ``heterogeneous_strategy=RECORD`` is rejected because the generated ``struct`` declarations cannot coexist with the ``cJSON`` value type.

- Rewrite the C JSON round-trip CI check to literalize the shared fixture through ``C(json_type=C.json_types.CJSON)`` and print it with ``cJSON_PrintUnformatted``, dropping the Python-side walker that previously built a parallel ``cJSON`` tree from the parsed input. The check still reports ``C round-trip OK`` with the same two excluded fields.

- Size COBOL ``PIC X(n)`` alphanumeric clauses by the UTF-8 byte length of the string rather than its character count, so that string literals containing characters that take more than one UTF-8 byte are no longer given an undersized picture and silently truncated by GnuCOBOL at runtime.

- Give colliding COBOL data names a numeric suffix so that two distinct JSON object keys that map to the same COBOL data name (because the character rewriting or the 30-character name limit collapses them together) no longer produce two sibling items with the same name in one group, which GnuCOBOL rejects as ambiguous when the name is referenced.

- Add ``Cobol(json_type=CJSON)``, which renders a document as a ``cJSON`` node tree built through COBOL's C ``CALL`` interface (``cJSON_Create*`` composed with ``cJSON_AddItemTo*``) rather than a WORKING-STORAGE record, so arbitrary string keys, JSON booleans, real numbers, heterogeneous arrays, nested objects, and the empty string are all represented faithfully.  The COBOL JSON round-trip now uses this mode with ``cJSON_PrintUnformatted``, so it reproduces every field of the shared input except ``biginteger`` and ``float_large_exponent``.

- Lead the README and documentation home page with a minimal ``literalize`` call so that the required arguments are obvious at a glance, and move the format-option configuration into a follow-up example instead of mixing default-valued arguments into the first example.

- Collapsed the repetitive per-language "JSON value types" documentation section into a single lookup table, keeping prose only for the unusual OCaml and D cases.

- Document when to choose a ``heterogeneous_strategy`` versus a ``json_type`` for mixed-type data: the heterogeneous strategies page now carries a "Which should I use?" note contrasting the statically typed wrappers with the single runtime JSON value type, and the two documentation sections cross-link each other.

- Add a "Common errors and how to resolve them" documentation page mapping each user-facing exception to its cause and the recommended fix.

- Add TOML and JSON5 input examples to the documentation, showing that TOML comments are preserved and that JSON5's relaxed syntax (comments, single-quoted strings, trailing commas, and hexadecimal numbers) is accepted.

- Restructured the API reference into labeled sections (core functions, result type, variable forms, identifier cases, function calls, formatting configuration, language definition and exceptions) and stopped surfacing undocumented internals on the page.

- Remove the incomplete custom-language sketch from the "Custom language implementations" documentation; it imported private, underscore-prefixed modules.  The section now points readers to the built-in language modules as the worked example.

2026.05.28
----------

- Add Ruby, TypeScript, Haskell, Perl, PHP, Go, Zig, C#, Scala, Swift, Kotlin, Rust, D, TOML, Elm, OCaml, YAML, Julia, R, and Groovy JSON round-trip checks to CI using the shared round-trip fixture.

- Add ``Rust(json_type=Rust.json_types.SERDE_JSON_VALUE)`` to render values through ``serde_json::json!`` instead of Rust's narrow collection types.

- Add ``Perl(bool_format=...)`` so booleans can round-trip through JSON and YAML libraries.  The default ``Perl.BoolFormats.INTEGER`` keeps the historic bare ``1`` / ``0`` output; ``JSON_PP_REF`` renders ``\1`` / ``\0`` scalar references (the conventional form used by ``JSON::PP``, ``JSON::XS``, ``Cpanel::JSON::XS``, and ``Mojo::JSON``); ``JSON_PP_SINGLETON`` renders the ``JSON::PP::true`` / ``JSON::PP::false`` blessed singletons with a ``use JSON::PP;`` preamble.

- Add ``Cpp(json_type=Cpp.json_types.NLOHMANN_JSON)`` to render values through ``nlohmann::json::parse`` instead of C++'s narrow ``std::vector`` / ``std::map`` / ``std::unordered_map`` collection types.

- Add ``Java(json_type=Java.json_types.JACKSON_JSON_NODE)`` to render values through Jackson's ``ObjectMapper.readTree`` so the binding has the static type ``com.fasterxml.jackson.databind.JsonNode`` instead of Java's narrow ``List`` / ``Map`` types.

- Add ``CSharp(json_type=CSharp.json_types.SYSTEM_TEXT_JSON_NODE)`` to render values through ``System.Text.Json.Nodes.JsonNode`` instead of C#'s narrow collection types.

- Add ``Kotlin(json_type=Kotlin.json_types.KOTLINX_JSON_ELEMENT)`` to render values through ``Json.parseToJsonElement`` so the binding has the static type ``kotlinx.serialization.json.JsonElement`` instead of Kotlin's narrow ``List`` / ``Map`` types.

- Add ``Scala(json_type=Scala.json_types.CIRCE)`` to render values through Circe ``Json.obj`` / ``Json.arr`` / ``Json.fromXxx`` instead of Scala's narrow collection types.

- Add ``Haskell(json_type=Haskell.json_types.AESON_VALUE)`` to render values through the ``aesonQQ`` quasi-quote bracket from ``Data.Aeson.QQ`` so the binding has the static type ``Data.Aeson.Value`` instead of Haskell's narrow custom ``Val`` algebraic type.

- Add ``Zig(json_type=Zig.json_types.STD_JSON_VALUE)`` to render values through ``std.json.parseFromSlice`` so the binding has the static type ``std.json.Value`` instead of Zig's narrow ``ZVal`` tagged union.

- Add ``Nim(json_type=Nim.json_types.JSON_NODE)`` to render values through the standard-library ``json.JsonNode`` and the ``%*`` macro instead of Nim's narrow collection types.

- Add ``Crystal(json_type=Crystal.json_types.JSON_ANY)`` to render values through ``JSON.parse(%(...))`` into Crystal's standard-library ``JSON::Any`` instead of native ``Array`` and ``Hash`` collections.

- Add ``D(json_type=None)`` to render D data through narrow native collections (raw scalars, ``T[]`` arrays, ``V[K]`` associative arrays) instead of the default ``std.json.JSONValue`` wrapper, giving D users the same two-mode choice the other ``json_type``-supporting languages have.  D's polarity is reversed: ``json_type=D.json_types.STD_JSON_VALUE`` (the default) matches the other languages' opt-in JSON value rendering, while ``json_type=None`` matches their typed-collection defaults.

- Add an opt-in ``Perl.string_formats.DOUBLE_UTF8`` variant that emits non-ASCII characters literally in double-quoted strings and contributes ``use utf8;`` to the file preamble whenever the literalized value contains a non-ASCII string.

- Add an Ada JSON round-trip check to CI using the shared round-trip fixture.

- Add a Clojure JSON round-trip check to CI using the shared round-trip fixture.

- Add a Common Lisp JSON round-trip check to CI using the shared round-trip fixture.

- Add a Crystal JSON round-trip check to CI using the shared round-trip fixture.

- Add a Dart JSON round-trip check to CI using the shared round-trip fixture.

- Add a Dhall JSON round-trip check to CI using a scalar-only subset of the shared round-trip fixture.

- Add an Elixir JSON round-trip check to CI using the shared round-trip fixture.

- Add an Erlang JSON round-trip check to CI using the shared round-trip fixture.

- Add a Forth JSON round-trip check to CI using the shared round-trip fixture.

- Add an F# JSON round-trip check to CI using the shared round-trip fixture.

- Add a Gleam JSON round-trip check to CI using the shared round-trip fixture.

- Add an HCL JSON round-trip check to CI using the shared round-trip fixture.

- Add a Lua JSON round-trip check to CI using the shared round-trip fixture.

- Add a Nim JSON round-trip check to CI using the shared round-trip fixture.

- Add an Objective-C JSON round-trip check to CI using the shared round-trip fixture.

- Add an Odin JSON round-trip check to CI using the shared round-trip fixture.

- Add a Racket JSON round-trip check to CI using the shared round-trip fixture.

- Add a Raku JSON round-trip check to CI using the shared round-trip fixture.

- Add a Roc JSON round-trip check to CI using the shared round-trip fixture.

- Add a Standard ML JSON round-trip check to CI using the shared round-trip fixture.

- Add a Tcl JSON round-trip check to CI using the shared round-trip fixture.

- Add a V JSON round-trip check to CI using the shared round-trip fixture.

- Add a Visual Basic JSON round-trip check to CI using the shared round-trip fixture.

- Add a Wren JSON round-trip check to CI using the shared round-trip fixture.

- Replace the hand-rolled JSON encoder in the Java round-trip CI check with Jackson's ``ObjectMapper``.

- The Kotlin JSON round-trip CI check now serializes via Jackson's ``ObjectMapper`` instead of a hand-rolled ``toJsonElement`` walker over heterogeneous ``Any?`` plus primitive-array types.

- Raise ``UnrepresentableEmptyDictError`` at literalize time when an empty mapping appears anywhere in the input for the Lua, PHP, and R language specifications.  These languages have a single runtime collection type that cannot distinguish an empty mapping from an empty sequence, so emitting an empty-table literal would silently lose the mapping/sequence distinction on round-trip through any JSON encoder.  The new exception is exposed from :mod:`literalizer.exceptions`.

- Raise ``UnrepresentableIntegerError`` at literalize time for integers outside the target language's representable range on the Go, TypeScript, Rust, D, and C++ language specifications, replacing silent emission of literals the target compiler would reject or silently truncate.  Go and D now emit a ``UL``/``uint64(...)`` literal for positives up to ``ulong.max``/``math.MaxUint64`` and raise above that; C++ retains its existing ``ULL`` fallback and now raises above ``ULLONG_MAX``; Rust raises above the ``i128`` range; TypeScript raises above ``Number.MAX_SAFE_INTEGER`` (``2**53 - 1``).

- Always emit a dotted mantissa in float scientific-notation literals (``1.0e+16`` rather than ``1e+16``) so the output parses as a float in Ada, Cobol, Elixir, Erlang, Gleam, Nix, and YAML.  Gleam additionally strips the ``+`` from positive exponents to satisfy its parser, which lets ``Gleam``'s JSON round-trip handle the full IEEE 754 ``double`` range.

- Internal: rewrite the Kotlin and Zig JSON round-trip scripts on top of the ``KOTLINX_JSON_ELEMENT`` and ``STD_JSON_VALUE`` ``json_type`` strategies, dropping the bespoke ``Any?``-to-``JsonElement`` and ``ZVal``-to-``std.json.Value`` walkers.  ``std.json.Value.number_string`` preserves the 26-digit ``biginteger`` field end-to-end on Zig, so that exclusion is dropped there; ``kotlinx.serialization``'s ``parseToJsonElement`` still collapses it to a ``Double``, so the Kotlin exclusion is retained.

- Add ``Erlang(json_type=Erlang.json_types.OTP_JSON)`` to render strings, ISO dates, datetimes, times, and base64-encoded bytes as UTF-8 binary literals (``<<"..."/utf8>>``), null as the bare atom ``null``, and sets as JSON arrays, so the rendered value feeds straight into Erlang's built-in ``json:encode/1`` (available since ``OTP_27``) without a normalization pass.

- Add ``OCaml(json_type=OCaml.json_types.YOJSON_SAFE_T)`` to render values directly as ``Yojson.Safe.t`` polymorphic-variant literals (``Bool``, ``Int``, ``Float``, ``String``, ``Null``, ``List``, ``Assoc``, ``Intlit``) so the binding has the static type ``Yojson.Safe.t`` instead of OCaml's generated ``val_t`` algebraic type; arbitrary-precision integers route through the ``Intlit`` escape hatch.

- Document the F# ``Val`` discriminated union's JSON serialization limitations: the ``FMap`` tuple-list shape (chosen to preserve insertion order) and ``FSharp.SystemTextJson``'s ``Untagged`` encoding both prevent ``System.Text.Json.JsonSerializer.Serialize`` from producing valid JSON without a custom converter.  The ``FSharp`` language module now describes both pitfalls and points users at the ``writeVal`` helper in ``scripts/run_fsharp_roundtrip.py`` as a starting template.

- Add ``Elm(json_type=Elm.json_types.JSON_ENCODE_VALUE)`` to render values as idiomatic ``elm/json`` ``Json.Encode.*`` calls producing a ``Json.Encode.Value`` directly, replacing the per-fixture ``Val`` ADT.

- Add ``FSharp(json_type=FSharp.json_types.SYSTEM_TEXT_JSON_NODE)`` to render values through ``System.Text.Json.Nodes.JsonNode`` instead of F#'s generated tagged ``Val`` discriminated union.

- Add ``Gleam(json_type=Gleam.json_types.GLEAM_JSON_JSON)`` to render values directly as ``gleam_json`` builder calls (``json.object``, ``json.preprocessed_array``, ``json.int``, ``json.string``, ...) so the binding has the static type ``gleam/json.Json`` instead of Gleam's generated ``GVal`` tagged ADT.

- Add ``PureScript(json_type=PureScript.json_types.ARGONAUT_JSON)`` to render values through a ``fromRight jsonNull (jsonParser "...")`` expression so the binding has the static type ``Data.Argonaut.Core.Json`` instead of PureScript's narrow custom ``Val`` algebraic type.

- Raise ``UnrepresentableEmptyDictError`` at literalize time when an empty mapping appears anywhere in the input for the Ada language specification.  The Ada literalizer's unified ``A_Val`` aggregate cannot distinguish an empty ``AMap'[]`` from an empty ``AList'[]`` at run time, so emitting an empty-mapping literal would silently lose the mapping/sequence distinction on round-trip.  Ada now joins Lua, PHP, and R in raising rather than emitting an ambiguous literal.

2026.05.21.1
------------

- Added ``format_constructor_target`` to the :class:`~literalizer.Language` protocol. It returns the language-specific target string for a zero-argument constructor call, suitable for passing to :func:`~literalizer.literalize_call` as ``target_function``. The default is ``ClassName``; Java, JavaScript, TypeScript, C#, Scala, Go, Ruby, and Rust override it for their common constructor forms (``new ClassName``, ``NewClassName``, ``ClassName.new``, and ``ClassName::new``).

2026.05.21
----------

No significant changes.

2026.05.20.1
------------

- Speed up backslash string formatting for strings that do not need escaping.

2026.05.20
----------

- Reduce recursive renderer overhead for large JSON inputs.

2026.05.18.1
------------


- :class:`~literalizer.languages.rust.Rust` now exposes a non-empty
  ``Modifiers`` enum with a single ``MUT`` member.  Passing
  ``NewVariable(name=..., modifiers={Rust.Modifiers.MUT})`` (or the same
  via :func:`~literalizer.literalize_call`) renders a mutable binding
  (``let mut name = ...;``) instead of the immutable default
  (``let name = ...;``), so a value constructed and bound through the
  variable form can then be mutated through that binding.  The modifier
  applies to the default ``LET`` declaration style; other declaration
  styles ignore it.

- Added two metadata properties to the :class:`~literalizer.Language`
  protocol: ``supports_multi_param_call_wrapper_stub`` (whether the
  language can declare and positionally invoke a wrapper stub that
  receives the call's result alongside other positional arguments) and
  ``supports_dict_literal_as_free_expression`` (whether a map literal
  can appear as a free-standing expression rather than only on the
  right-hand side of a typed assignment).  Both are test-harness
  metadata, like the existing ``has_free_function_calls`` and
  ``supports_dotted_call_stub`` properties;
  :func:`~literalizer.literalize_call` does not inspect them.

2026.05.18
----------


- :func:`~literalizer.literalize_call` can now bind a zero-argument
  call to a ``variable_form``.  Previously a ``variable_form`` was
  rejected outright with ``per_element=True`` and the whole-value path
  (``per_element=False``) always passed one argument, so the
  zero-argument constructor case (``p2 = Playlist()``,
  ``let p2 = Playlist::new();``) had no representation.  A
  ``variable_form`` is now accepted whenever the input produces exactly
  one call: ``per_element=False`` as before, or ``per_element=True``
  over a single-element source (a ``[[]]`` source yields the
  zero-argument constructor).  Zero calls or more than one call are
  rejected with
  :class:`~literalizer.exceptions.UnsupportedCallShapeError`.
  As part of this, a call-result binding no longer carries a type
  annotation derived from the call's *argument* data (which a strict
  type-checker rejected, since the annotation describes the argument,
  not the call's return type): :class:`~literalizer.Python` now binds
  the call result with a plain ``name = value`` and the annotation-only
  preamble it would have required is no longer emitted.

- :func:`~literalizer.literalize_call` now honors
  ``collection_layout=CollectionLayout.COMPACT`` for the ``$zipped``
  literal exposed on :class:`~literalizer.CallContext`.  Previously a
  mapping paired through ``zip_source`` always rendered multi-line,
  even though the call-argument mapping rendered by the same call was
  single-line under the same setting, which split a one-line
  ``call_transform`` across several physical lines.  The ``$zipped``
  literal is now rendered through the same whole-value path as call
  arguments, so a compact mapping stays on one line.

- Added support for Haxe as a new output language.  ``Haxe`` renders
  every collection literal with an explicit ``(... : Array<Dynamic>)``
  or ``(... : Map<String, Dynamic>)`` cast, so heterogeneous and empty
  collections type-check without per-variable annotations.  Maps use
  Haxe's ``["key" => value]`` literal syntax and strings use the
  double-quoted form (no interpolation).  Calls use positional syntax
  with local-function and anonymous-structure-closure stubs emitted
  inside ``static function main()``.  A new ``lint-haxe`` job in
  ``.github/workflows/lint.yml`` compiles and runs every ``.hx``
  fixture in a single ``haxe --interp`` invocation.

2026.05.17.1
------------


- :class:`~literalizer.CSharp` array sequence-format no longer emits
  ``using System;`` or ``using System.Collections.Generic;``.  A C#
  array literal (``new T[] {...}``) is a built-in language feature and
  requires no ``using`` directives, so those lines were dead noise on
  the array path (for example a ``Dictionary`` whose values are arrays
  picked up a spurious ``using System;``).  ``using
  System.Collections.Generic;`` is still emitted for the collection
  types that need it (``List<T>``, ``Dictionary<TKey, TValue>``, and
  the set types), and ``using System;`` for ``System`` scalar types
  such as ``DateOnly``.  The array empty form is now the typed
  literal ``new T[] {}`` rather than ``Array.Empty<T>()``, keeping the
  array path free of any ``System`` reference.  See #2524.
- :func:`~literalizer.literalize_call` now accepts a ``bound_refs``
  argument, the call-side counterpart of
  :func:`~literalizer.literalize`'s own ``bound_refs``.  With
  ``wrap_in_file=True`` it renders a complete, self-contained file:
  each ref is declared (cased via ``ref_case``) ahead of the calls, a
  no-op stub for the target function is injected, and one reconciled
  preamble (header and body) is placed in front, so callers no longer
  hand-roll a duplicate-removal pass.  Entries double as ``ref_values``
  and are emitted in iteration order.  Recomputing the body preamble
  across the union of types and reconciling the data-dependent header
  block into a single copy covering every type replaces the previous
  multi-line preamble-filter heuristic.  The same single-copy
  reconciliation now also backs :func:`~literalizer.literalize`'s own
  ``bound_refs`` declaration composition, removing the last
  preamble-filter heuristic there with no change to generated output.
  See #1946.
- The ``supports_call_variable_binding`` language-class flag has been
  removed.  Every language now binds a :func:`~literalizer.literalize_call`
  result directly with no literal-only wrapping, so the flag was
  ``True`` for all languages and its
  :class:`~literalizer.exceptions.UnsupportedCallShapeError` rejection
  path was unreachable.  No generated output changes.  See #2521.

2026.05.17
----------


- :class:`~literalizer.D` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call` for both
  :class:`~literalizer.NewVariable` and
  :class:`~literalizer.ExistingVariable`.  A D literal binding wraps
  the right-hand side to encode the parsed value's runtime type (a
  ``JSONValue(...)`` projection, or a positional ``Record0(...)``
  struct-constructor literal under the ``RECORD`` strategy), which is
  wrong for a call whose return type is opaque to the renderer; the
  call result is now bound directly as ``auto my_data =
  make_widget(...);``.  No caller-supplied return-type hint is
  required: D infers the binding type from the initializer.  Because
  the binding is an ``auto`` declaration while the
  :class:`~literalizer.ExistingVariable` form is a bare assignment to
  an already-declared name, only the :class:`~literalizer.NewVariable`
  form is golden-covered.  Its ``supports_call_variable_binding``
  language-class flag is now ``True``; existing literal-binding and
  call-without-binding output is unchanged.  Follow-up to #1961.  See
  #2511.
- :class:`~literalizer.SystemVerilog` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call` for both
  :class:`~literalizer.NewVariable` and
  :class:`~literalizer.ExistingVariable`.  A SystemVerilog literal
  binding wraps the right-hand side in a named ``_VVal`` struct literal
  derived from the parsed value's runtime type, which is wrong for a
  call whose return type is opaque to the renderer; the call result is
  now bound directly as
  ``static _VVal my_data = make_widget(...);``.  SystemVerilog
  declarations are typed and have no inference, so the binding needs an
  explicit declared type; no caller-supplied return-type hint is
  required because every generated value-returning call stub returns
  the universal tagged ``_VVal`` struct, so the binding's declared type
  is always ``_VVal`` (the same type a SystemVerilog scalar literal
  binding declares).  The call stub is emitted at module scope rather
  than inside ``initial begin``, where a ``function`` declaration is
  illegal.  Because the binding is a typed declaration while the
- :class:`~literalizer.Zig` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call` for both
  :class:`~literalizer.NewVariable` and
  :class:`~literalizer.ExistingVariable`.  A Zig literal binding wraps
  the right-hand side in a designated-initializer struct literal that
  encodes the value's runtime type (a tagged ``ZVal`` union projection,
  or a generated ``Record0`` struct literal under the ``RECORD``
  strategy) and declares an explicit ``ZVal`` value type, which is
  wrong for a call whose return type is opaque to the renderer; the
  call result is now bound with a plain inferred declaration,
  ``const my_data = make_widget(...);``.  No caller-supplied return-type
  hint is required: the Zig ``const``/``var`` type inference supplies
  the binding's type.  Because the binding is a keyword declaration
  while
  the :class:`~literalizer.ExistingVariable` form is a bare assignment
  to an already-declared name, only the
  :class:`~literalizer.NewVariable` form is golden-covered.  Its
  ``supports_call_variable_binding`` language-class flag is now
  ``True``; existing literal-binding and call-without-binding output is
  unchanged.  Follow-up to #1961.  See #2510.
- :class:`~literalizer.Ada` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call` for both
  :class:`~literalizer.NewVariable` and
  :class:`~literalizer.ExistingVariable`.  An Ada literal binding wraps
  the right-hand side in the ``A_Val`` constructor chosen from the
  parsed literal's runtime type, which is wrong for a call whose return
  type is opaque to the renderer; the call result is now bound directly
  as ``my_data : A_Val := Make_Widget (...);``.  No caller-supplied
  return-type hint is required: every generated Ada call stub returns
  ``A_Val``, so the binding's declared type is always ``A_Val`` (the
  same type an Ada literal binding declares).  Because the binding is a
  typed declaration while the :class:`~literalizer.ExistingVariable`
  form is a bare assignment to an already-declared name, only the
  :class:`~literalizer.NewVariable` form is golden-covered.  Its
  ``supports_call_variable_binding`` language-class flag is now
  ``True``; existing literal-binding and call-without-binding output is
  unchanged.  Follow-up to #1961.  See #2509.
- :class:`~literalizer.Fortran` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call` for both
  :class:`~literalizer.NewVariable` and
  :class:`~literalizer.ExistingVariable`.  A Fortran literal binding
  wraps the right-hand side in the ``fval_t`` constructor matching the
  parsed literal's type (the integer, real, or string constructor),
  which is wrong for a call whose return type is opaque to the
  renderer; the call result is now bound directly as
  ``type(fval_t) :: my_data`` followed by
  ``my_data = make_widget(...)``.  No caller-supplied return-type hint
  is required: every generated Fortran call stub returns
  ``type(fval_t)``, so the binding's declared type is always
  ``type(fval_t)`` (the same type a Fortran literal binding declares).
  The call stub is emitted in the program's ``contains`` section, after
  the binding, so a value-returning call no longer needs an inline
  procedure body.  Because the :class:`~literalizer.NewVariable` binding
  is a typed declaration while the
  :class:`~literalizer.ExistingVariable` form is a bare assignment to an
  already-declared name, only the :class:`~literalizer.NewVariable`
  form is golden-covered.  Its ``supports_call_variable_binding``
  language-class flag is now ``True``; existing literal-binding and
  call-without-binding output is unchanged.  Follow-up to #1961.  See
  #2507.
  #2508.
- :class:`~literalizer.C` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call` for both
  :class:`~literalizer.NewVariable` and
  :class:`~literalizer.ExistingVariable`.  A C literal binding wraps
  the right-hand side in a designated-initializer compound literal that
  encodes the value's runtime type (a tagged-union projection, or a
  ``struct Record0 my_data = (struct Record0){...};`` aggregate under
  the ``RECORD`` strategy), which is wrong for a call whose return type
  is opaque to the renderer; the call result is now bound directly as
  ``CVal my_data = make_widget(...);``.  No caller-supplied return-type
  hint is required: every generated call stub returns the universal
  tagged ``CVal`` union, so the binding's declared type is always
  ``CVal`` (the same type a C literal binding declares).  Because the
  binding is a typed
  declaration while the :class:`~literalizer.ExistingVariable` form is a
  bare assignment to an already-declared name, only the
  :class:`~literalizer.NewVariable` form is golden-covered.  Its
  ``supports_call_variable_binding`` language-class flag is now
  ``True``; existing literal-binding and call-without-binding output is
  unchanged.  Follow-up to #1961.  See #2506.
- :class:`~literalizer.Elixir` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call` for both
  :class:`~literalizer.NewVariable` and
  :class:`~literalizer.ExistingVariable`.  The call stub is emitted at
  module scope and the binding lives inside the generated ``def x do``
  entry function, so ``my_data = make_widget(42)`` no longer needs a
  ``def`` nested inside another ``def``.  Because Elixir rebinds names
  with ``=``, the :class:`~literalizer.ExistingVariable` output is
  identical to the :class:`~literalizer.NewVariable` output.  Its
  ``supports_call_variable_binding`` language-class flag is now
  ``True``; existing literal-binding and call-without-binding output is
  unchanged.  Follow-up to #1961.  See #2226.
- :class:`~literalizer.Python` now emits ``from __future__ import
  annotations`` only when the rendered code actually contains an
  annotation: a ``RECORD``-strategy ``@dataclasses.dataclass`` block
  or an inline variable type hint (an empty-collection helper hint, or
  any declaration under ``variable_type_hints=ALWAYS``).  Call-only
  output and annotation-free literals no longer carry the unused
  future import.  See #2495.
- :class:`~literalizer.Forth` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call` for both
  :class:`~literalizer.NewVariable` and
  :class:`~literalizer.ExistingVariable`, binding the call result with
  the same colon definition Forth already uses for literal bindings:
  ``: my_data 42 make_widget ;``.  This is a deferred word that
  re-executes ``make_widget`` on every invocation, and (because Forth
  has no reassignment in this model) the
  :class:`~literalizer.ExistingVariable` output is identical to the
  :class:`~literalizer.NewVariable` output; Forth's ``VALUE``/``TO``
  idiom was rejected because it holds only a single cell and cannot
  represent the string/dict/sequence values the colon form already
  covers.  Its ``supports_call_variable_binding`` language-class flag
  is now ``True``; existing literal-binding output is unchanged.
  Follow-up to #1961.  See #2456.
- :class:`~literalizer.Nim` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call`, binding the call result
  directly: ``var my_data = make_widget(42)``.  The literal-binding
  declaration template prefixes the right-hand side with the ``%*``
  json macro (or ``@`` for sequences) chosen from the parsed literal's
  type, which JSON-constructs a literal rather than invoking a call;
  the new call-specific declaration and assignment templates drop that
  wrapping regardless of the source data type.  Its
  ``supports_call_variable_binding`` language-class flag is now
  ``True``; existing literal-binding and call-without-binding output is
  unchanged.  Only the :class:`~literalizer.NewVariable` form emits a
  golden because the :class:`~literalizer.ExistingVariable` bare
  assignment (``my_data = make_widget(42)``) to an undeclared name is
  not self-contained.  Follow-up to #1961.  See #2455.
- :class:`~literalizer.Zig` gains the ``RECORD``
  ``heterogeneous_strategy`` (already on :class:`~literalizer.Rust`,
  :class:`~literalizer.Go`, :class:`~literalizer.Kotlin`,
  :class:`~literalizer.Scala`, :class:`~literalizer.Java`,
  :class:`~literalizer.Python` and :class:`~literalizer.Cpp`).  The
  default (``ERROR``) strategy keeps the homogeneous ``ZVal``
  tagged-union model; under ``RECORD`` each record-shaped dict
  (non-empty, string-keyed) becomes a generated ``const RecordN =
  struct { ... };`` declared in the preamble plus a matching
  ``Record0{ .field = value, ... }`` literal whose fields are raw Zig
  values, so a record-shaped dict that mixes scalars with a container
  is representable.  Field names are the dict keys verbatim and field
  types are inferred structurally from the value (``i64``/``u64``,
  ``f64``, ``bool``, ``[]const u8``, ``?i64``, ``[]const T`` slices,
  ``struct { ... }`` tuples for heterogeneous lists, nested
  ``RecordN``).  Without the ``ZVal`` union the whole value is raw, so
  a non-record collection is a ``&.{ ... }`` slice / ``.{ ... }``
  tuple and the binding drops its ``: ZVal`` annotation; the
  class-name prefix is configurable via the new
  ``record_struct_name_prefix`` constructor parameter and its
  ``supports_record_struct_name_prefix`` language-class flag is now
  ``True``.  See #2477.
- Fixed the :class:`~literalizer.Zig` ``RECORD`` field type of an
  integer-list record field whose first element is small but a later
  element exceeds the signed 64-bit range: it is now ``[]const u64``
  (typed from the widest element) instead of the ``[]const i64`` that
  inferring from the first element alone produced.  See #2488.
- :class:`~literalizer.Odin` gains the ``RECORD``
  ``heterogeneous_strategy`` (already on :class:`~literalizer.Rust`,
  :class:`~literalizer.Go`, :class:`~literalizer.Kotlin`,
  :class:`~literalizer.Scala`, :class:`~literalizer.Java`,
  :class:`~literalizer.Python` and :class:`~literalizer.Cpp`).  Each
  record-shaped dict (non-empty, string-keyed) becomes a generated
  package-scope ``struct`` declared in the preamble plus a matching
  ``Record0{ field = value, ... }`` literal, so a record-shaped dict
  that mixes scalars with a container is representable even though
  ``map[string]V`` requires homogeneous values.  Field names are the
  dict keys verbatim, and the class-name prefix is configurable via
  the new ``record_struct_name_prefix`` constructor parameter; its
  ``supports_record_struct_name_prefix`` language-class flag is now
  ``True``.  A list or ordered-map record field keeps Odin's standard
  ``[dynamic]any{...}`` / ``map[string]any{...}`` rendering and is
  typed as the matching ``any`` container (no element type is
  inferred), and an integer field beyond the signed 64-bit range is
  typed ``u64`` to match its literal.  The default (``ERROR``)
  ``map[string]any`` output is unchanged.  See #2481.
- :class:`~literalizer.StubReturn` is now part of the public API.  It
  was already the parameter type of the public
  :class:`~literalizer.Language` protocol's ``format_call_stub`` and
  ``format_call_preamble_stub`` methods, so it is now re-exported from
  the package root for consumers implementing that protocol.  See
  #1947.
- :class:`~literalizer.D` gains the ``RECORD``
  ``heterogeneous_strategy`` (already on :class:`~literalizer.Rust`,
  :class:`~literalizer.Go`, :class:`~literalizer.Kotlin`,
  :class:`~literalizer.Scala`, :class:`~literalizer.Java`,
  :class:`~literalizer.Python` and :class:`~literalizer.Cpp`).  The
  default (``ERROR``) strategy keeps the homogeneous
  ``std.json.JSONValue`` model; under ``RECORD`` each record-shaped
  dict (non-empty, string-keyed) becomes a generated
  ``struct RecordN { ... }`` declared in the preamble plus a matching
  positional ``Record0(value, ...)`` constructor literal whose fields
  are raw D values, so a record-shaped dict that mixes scalars with a
  container is representable.  Field names are the dict keys verbatim
  and field types are inferred structurally from the value (``long``/
  ``ulong``, ``double``, ``bool``, ``string``, ``typeof(null)``,
  ``T[]`` arrays, nested ``RecordN``).  Without the ``JSONValue``
  wrapper the whole value is raw and the binding drops its
  ``JSONValue``; the class-name prefix is configurable via the new
  ``record_struct_name_prefix`` constructor parameter and its
  ``supports_record_struct_name_prefix`` language-class flag is now
  ``True``.  A heterogeneous scalar list, a set, an ordered map or a
  non-record dict has no raw D representation and raises
  :class:`~literalizer.exceptions.UnrepresentableInputError` (the
  cross-language decision for these is tracked in #2317).  See #2478.
- :class:`~literalizer.Crystal` gains the ``RECORD``
  ``heterogeneous_strategy`` (already on :class:`~literalizer.Rust`,
  :class:`~literalizer.Go`, :class:`~literalizer.Kotlin`,
  :class:`~literalizer.Scala`, :class:`~literalizer.Java`,
  :class:`~literalizer.Cpp` and :class:`~literalizer.Python`).  Each
  record-shaped dict (non-empty, string-keyed) becomes a generated
  ``record`` struct declared in the per-fixture module body plus a
  matching positional ``Record0.new(value, ...)`` literal, so a
  record-shaped dict that mixes scalars with a container is
  representable even though ``Hash`` requires a homogeneous value
  type.  Field names are the dict keys verbatim, an integer field is
  sized to match its rendered literal (``Int32`` / ``Int64`` / the
  ``_i128``-suffixed ``Int128``), and the struct-name prefix is
  configurable via the new ``record_struct_name_prefix`` constructor
  parameter; its ``supports_record_struct_name_prefix``
  language-class flag is now ``True``.  The default (``ERROR``)
  strategy still raises for such a dict.  See #2420.
- :class:`~literalizer.Cpp` gains the ``RECORD``
  ``heterogeneous_strategy`` (already on :class:`~literalizer.Rust`,
  :class:`~literalizer.Go`, :class:`~literalizer.Kotlin`,
  :class:`~literalizer.Scala`, :class:`~literalizer.Java` and
  :class:`~literalizer.Python`).  Each record-shaped dict (non-empty,
  string-keyed) becomes a generated aggregate ``struct`` declared in
  the preamble plus a matching ``Record0{.field = value, ...}``
  C++20 designated-initializer literal, so a record-shaped dict that
  mixes scalars with a container is representable even though
  ``std::map`` requires homogeneous values.  Field names are the dict
  keys verbatim, scalar members carry a ``{}`` in-class initializer
  (so the aggregate satisfies clang-tidy's member-init check), and the
  class-name prefix is configurable via the new
  ``record_struct_name_prefix`` constructor parameter; its
  ``supports_record_struct_name_prefix`` language-class flag is now
  ``True``.  A list whose every element is a record-shaped dict is
  opened with ``std::vector{`` so class-template argument deduction
  infers ``std::vector<RecordN>``.  The default (``ERROR``)
  ``std::variant`` output is unchanged.  See #2420.
- :class:`~literalizer.CSharp` gains the ``RECORD``
  ``heterogeneous_strategy`` (already on :class:`~literalizer.Rust`,
  :class:`~literalizer.Go`, :class:`~literalizer.Kotlin`,
  :class:`~literalizer.Scala`, :class:`~literalizer.Java`,
  :class:`~literalizer.Python` and :class:`~literalizer.Cpp`).  Each
  record-shaped dict (non-empty, string-keyed) becomes a generated
  positional ``record`` declared in the preamble plus a matching
  ``new Record0(value, ...)`` literal, so a record-shaped dict that
  mixes scalars with a container is representable even though
  ``Dictionary`` requires a homogeneous value type.  Component names
  are the PascalCase form of the dict keys; auto names are
  ``Record0``, ``Record1``, ...  ``sequence_format`` is forced to
  ``ARRAY`` under this strategy so a list-valued component has a typed
  array form, and a list whose every element is a record-shaped dict
  is opened with an implicitly-typed array ``new[] { ... }`` so C#
  infers ``RecordN[]``.  The default (``ERROR``) ``Dictionary``
  output is unchanged.  See #2475.
- :class:`~literalizer.Swift` gains the ``RECORD``
  ``heterogeneous_strategy`` (already on :class:`~literalizer.Rust`,
  :class:`~literalizer.Go`, :class:`~literalizer.Kotlin`,
  :class:`~literalizer.Scala`, :class:`~literalizer.Java`,
  :class:`~literalizer.Python` and :class:`~literalizer.Cpp`).  Each
  record-shaped dict (non-empty, string-keyed) becomes a generated
  ``struct`` declared in the preamble plus a matching
  ``Record0(field: value, ...)`` initializer literal, so a
  record-shaped dict that mixes scalars with a container is
  representable as a typed value even though ``Dictionary`` requires a
  homogeneous value type.  Field names are the dict keys verbatim, a
  field whose value is a list of record-shaped dicts of one shape is
  typed ``[RecordN]``, and the struct-name prefix is configurable via
  the new ``record_struct_name_prefix`` constructor parameter; its
  ``supports_record_struct_name_prefix`` language-class flag is now
  ``True``.  The default (``ERROR``) ``Any`` output is unchanged.  See
  #2474.
- :class:`~literalizer.C` gains the ``RECORD``
  ``heterogeneous_strategy`` (already on :class:`~literalizer.Rust`,
  :class:`~literalizer.Go`, :class:`~literalizer.Kotlin`,
  :class:`~literalizer.Scala`, :class:`~literalizer.Java`,
  :class:`~literalizer.Python`, :class:`~literalizer.Cpp` and
  :class:`~literalizer.Swift`).  Each record-shaped dict (non-empty,
  string-keyed) becomes a generated aggregate ``struct`` declared in
  the preamble plus a matching ``(struct Record0){.field = value,
  ...}`` C99 designated-initializer compound literal, so a
  record-shaped dict that mixes scalars with a container is rendered
  with cleanly typed members rather than the tagged ``CVal`` union.
  Field names are the dict keys verbatim and each generated ``struct``
  is auto-named ``Record0``, ``Record1``, ...  A scalar member maps to
  its exact C type, a nested record dict to its generated ``struct``
  type, and a list whose every element is a record-shaped dict to a
  fixed-size ``struct`` array member.  Every other container (a scalar
  or heterogeneous list, or an empty list) is typed a pointer to
  ``CVal`` and rendered as a ``CVal`` array literal, reusing C's
  existing tagged union for arbitrary heterogeneity.  Because that
  fixed-size ``struct`` array is sized from the shape's first-seen
  instance, two same-shape records whose shared all-record-list field
  has differing lengths are rejected with
  :class:`~literalizer.exceptions.UnrepresentableInputError` rather
  than emitting C that fails to compile or misrepresents the input
  (cf. the set / non-record-dict field boundary tracked in #2317).
  The default (``ERROR``) ``CVal`` output is unchanged.  See #2476.
- :class:`~literalizer.V` gains the ``RECORD``
  ``heterogeneous_strategy`` (already on :class:`~literalizer.Rust`,
  :class:`~literalizer.Go`, :class:`~literalizer.Kotlin`,
  :class:`~literalizer.Scala`, :class:`~literalizer.Java`,
  :class:`~literalizer.Python` and :class:`~literalizer.Cpp`).  Each
  record-shaped dict (non-empty, string-keyed) becomes a generated
  file-scope ``struct`` declared in the preamble plus a matching
  ``Record0{ field: value, ... }`` literal, so a record-shaped dict
  that mixes scalars with a container is representable even though a
  ``map`` requires a homogeneous value type.  Field names are the
  dict keys verbatim; a field is typed from its value (an integer by
  its own magnitude so a wide value keeps its ``i64(...)`` / ``u64(...)``
  cast, a nested record by its generated name, a list of record-shaped
  dicts as ``[]RecordN``, ``None`` as ``voidptr``, an empty list as
  ``[]IVal``), and the struct-name prefix is configurable via the new
  ``record_struct_name_prefix`` constructor parameter; its
  ``supports_record_struct_name_prefix`` language-class flag is now
  ``True``.  An ``EPOCH`` datetime is now routed through the integer
  formatter so a post-2038 value keeps the ``i64(...)`` cast V
  requires.  The default (``ERROR``) and ``INTERFACE`` outputs are
  unchanged.  See #2480.
- :class:`~literalizer.Nim` gains the ``RECORD``
  ``heterogeneous_strategy`` (already on :class:`~literalizer.Rust`,
  :class:`~literalizer.Go`, :class:`~literalizer.Kotlin`,
  :class:`~literalizer.Scala`, :class:`~literalizer.Java`,
  :class:`~literalizer.Python`, :class:`~literalizer.Cpp`,
  :class:`~literalizer.Swift`, :class:`~literalizer.D` and
  :class:`~literalizer.V`).  Each record-shaped dict (non-empty,
  string-keyed) becomes a generated module-scope
  ``type Record0 = object`` declaration plus a matching
  ``Record0(field: value, ...)`` literal, so a record-shaped dict that
  mixes scalars with a container is representable even though a Nim
  ``Table`` requires a homogeneous value type.  Field names are the
  dict keys in ``camelCase`` and a list field is element-typed
  (``seq[int]``, ``seq[RecordN]``); the class-name prefix is
  configurable via the new ``record_struct_name_prefix`` constructor
  parameter, so its ``supports_record_struct_name_prefix``
  language-class flag is now ``True``.  Collections render with their
  native Nim constructors (``@[...]``, ``{...}.toTable``) as under
  ``OBJECT_VARIANT``, but no scalar is wrapped and no ``json``/``%*``
  is emitted.  A null field is the Nim ``pointer`` type; a set,
  ordered-map or non-record-dict field, and a ``NIM``-table-literal
  date/datetime field, are rejected as out of scope for the base port
  (consistent with the other non-Rust ports; see #2317).  The default
  (``ERROR``) JSON output is unchanged.  See #2479.
- :class:`~literalizer.ObjectiveC` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call`, emitting ``id my_data =
  make_widget(@42);`` directly.  The literal-binding declaration boxes
  a primitive right-hand side via ``@(...)`` because an ``id`` is a
  pointer type, but a call expression already yields an object pointer,
  so the boxing is dropped for the call-result binding.  Its
  ``supports_call_variable_binding`` language-class flag is now
  ``True``; existing literal-binding output is unchanged.  See #2223.
- :class:`~literalizer.Erlang` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call` for both
  :class:`~literalizer.NewVariable` and
  :class:`~literalizer.ExistingVariable`, binding the call result with
  ``My_data = make_widget(...)``.  A ``wrap_in_file=True`` Erlang
  scaffold hoists the generated call stub to module scope between
  ``-export`` and ``x()`` (previously the literal-binding scaffold
  nested it inside the ``x/0`` clause, producing invalid Erlang) while
  keeping the binding and the trailing ``My_data.`` return inside
  ``x()``.  See #2454.
- :class:`~literalizer.Tcl` and :class:`~literalizer.Bash` now accept
  ``variable_form`` on :func:`~literalizer.literalize_call` for both
  :class:`~literalizer.NewVariable` and
  :class:`~literalizer.ExistingVariable`.  Their literal-binding
  templates treat the right-hand side as a value word, so a call result
  is now bound through command substitution instead: Tcl emits ``set
  my_data [make_widget 42]`` and Bash emits ``declare
  my_data="$(make_widget 42)"`` (a bare ``my_data="$(...)"`` for an
  :class:`~literalizer.ExistingVariable`).  Their
  ``supports_call_variable_binding`` language-class flag is now
  ``True``; existing literal-binding output is unchanged.  Follow-up to
  #1961.  See #2222.

2026.05.16.1
------------


- The mapping arm of the public ``ValueInput`` type (accepted by
  ``ref_values`` and ``bound_refs``) is now a covariant-key read-only
  ``ValueItemsMap`` protocol instead of an invariant ``Mapping``, so
  nested ``dict`` literals with any scalar key type (``str``, ``int``,
  mixed, ...) are accepted by type checkers without an explicit
  annotation.  This is a type-only relaxation that accepts strictly
  more inputs; runtime behavior is unchanged.
- :class:`~literalizer.Scala` gains the same ``record_shape_names``
  constructor parameter, a ``Mapping[frozenset[str], str]`` from a
  record shape's key-set to a custom ``case class`` name.  A mapped
  shape is declared and rendered with the given name instead of the
  auto-generated ``RecordN``; the ``record_struct_name_prefix`` counter
  advances only for the shapes with no custom name.  Names are
  validated as PascalCase Scala identifiers that do not collide with
  the auto ``{prefix}{N}`` pattern or each other, raising
  :class:`~literalizer.exceptions.InvalidRecordNameError`.  Its
  ``supports_record_shape_names`` language-class flag is now ``True``.
  See #2332.
- :class:`~literalizer.Python` gains an opt-in ``RECORD``
  ``heterogeneous_strategy`` (already on :class:`~literalizer.Rust`,
  :class:`~literalizer.Go`, :class:`~literalizer.Kotlin`,
  :class:`~literalizer.Scala` and :class:`~literalizer.Java`).  Each
  record-shaped dict (non-empty, string-keyed) becomes a generated
  frozen ``@dataclasses.dataclass`` declared in the preamble (with an
  ``import dataclasses``) plus a matching ``RecordN(field=value, ...)``
  literal; field names are the dict keys verbatim and the class-name
  prefix is configurable via the new ``record_struct_name_prefix``
  constructor parameter.  Python's ``dict`` is already heterogeneous,
  so every record-shaped dict is representable as a plain ``dict``;
  this is purely an idiomatic-output choice, the strategy is opt-in,
  and the default (``ERROR``) plain-``dict`` output is unchanged.  See
  #2419.

- :class:`~literalizer.Java` gains the same ``record_shape_names``
  constructor parameter (already on :class:`~literalizer.Rust`,
  :class:`~literalizer.Go` and :class:`~literalizer.Kotlin`), a
  ``Mapping[frozenset[str], str]`` from a record shape's key-set to a
  custom ``record`` name.  A mapped shape is declared and rendered with
  the given name instead of the auto-generated ``RecordN``; the
  ``record_struct_name_prefix`` counter advances only for the shapes
  with no custom name.  Names are validated as PascalCase Java
  identifiers that do not collide with the auto ``{prefix}{N}`` pattern,
  the wrapper class name (``module_name``), or each other, raising
  :class:`~literalizer.exceptions.InvalidRecordNameError`.  Its
  ``supports_record_shape_names`` language-class flag is now ``True``.
  See #2333.

2026.05.16
----------


- :class:`~literalizer.Elm` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call`, emitting the inference-style
  binding ``my_data = make_widget (EInt 42)`` without a ``name : Val``
  annotation (the call's return type is not known to the renderer).
  A ``wrap_in_file=True`` Elm scaffold places the binding inside the
  ``main`` ``let`` block so the call is still exercised when the
  module is run.  See #2245.
- :class:`~literalizer.Cpp` now supports the ``TUPLE``
  ``heterogeneous_strategy``: a fixed-length heterogeneous scalar array
  that is a dict value or the document root is rendered as
  ``std::make_tuple(...)`` typed ``std::tuple<T0, ...>`` (with
  ``#include <tuple>`` emitted by the data-dependent preamble) instead
  of ``std::vector<std::variant<...>>``.  C++'s ``TUPLE`` strategy
  does not compose ``RECORD``, so the preamble fires off the tuple ids
  alone, even when the data has no record-shaped dicts.  The default
  (``ERROR``) ``std::variant`` output is unchanged.  See #2329.
- :class:`~literalizer.Scala` now supports the ``TUPLE``
  ``heterogeneous_strategy``, which composes ``RECORD``: a
  fixed-length heterogeneous scalar array that is a record field,
  another dict value, or the document root is rendered as a native
  tuple ``(e0, e1, ...)`` typed ``(T0, T1, ...)`` (a tuple-valued
  ``case class`` field is declared with the tuple type) instead of
  raising or widening to ``List[Any]``.  Scala 3 (the only version
  this language targets) imposes no tuple-length limit -- lengths past
  22 are transparently backed by ``TupleXXL`` -- so every fixed-length
  heterogeneous scalar array is representable.  The default
  (``ERROR``) output is unchanged.  See #2330.
- :class:`~literalizer.TypeScript` now supports the ``TUPLE``
  ``heterogeneous_strategy``: a fixed-length heterogeneous scalar array
  that is a dict value or the document root is rendered as an
  ``[e0, e1, ...] as const`` tuple literal, which TypeScript infers as
  a ``readonly [T0, T1, ...]`` tuple type, instead of a widened
  ``(T0 | T1)[]`` array.  TypeScript has no ``RECORD`` strategy and
  ``as const`` needs no imports, so there is no data-dependent
  preamble.  The default (``ERROR``) union-array output is unchanged.
  See #2328.
- :class:`~literalizer.Kotlin` now supports the ``TUPLE``
  ``heterogeneous_strategy``, composing ``RECORD``: a fixed-length
  heterogeneous scalar array that is a dict value or the document root
  is rendered as a two-element ``Pair(...)`` or three-element
  ``Triple(...)`` typed ``Pair<...>`` / ``Triple<...>``, and a record
  field whose value is such an array becomes a tuple-typed field.
  Kotlin has no general N-tuple, so an array of any other length
  raises
  :class:`~literalizer.exceptions.TupleArityNotRepresentableError`
  rather than degrading to a homogeneous list.  The default
  (``ERROR``) output is unchanged.  See #2331.
- :func:`~literalizer.literalize_call` gains a ``comment_source``
  argument: a sequence of trailing source-code comments, one per
  generated call, paired positionally.  Each non-empty entry is
  emitted as a line comment **after** the statement terminator using
  the target language's comment syntax (``#``, ``//``, ``--``, ...),
  falling back to that language's block-comment form (``/* ... */``)
  where there is no line comment.  This places the comment where only
  the core can put it -- a ``call_transform`` only sees the
  pre-terminator call expression, so a transform that appended a line
  comment would have the terminator commented out.  An empty entry
  emits no comment.  A length mismatch raises
  :class:`~literalizer.exceptions.CommentSourceLengthMismatchError`
  and a multi-line entry raises
  :class:`~literalizer.exceptions.CommentSourceMultilineError`.
  Languages that assemble the call sequence into a single
  clause/list/expression (so a separator, terminator or closer would
  follow the comment on the same line and be swallowed) reject a
  non-empty ``comment_source`` with
  :class:`~literalizer.exceptions.UnsupportedCallShapeError`; the
  supported set is the languages whose
  :attr:`~literalizer.Language.supports_standalone_comments_in_wrapped_calls`
  is ``True``.  See #2369.
- :class:`~literalizer.FSharp` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call` for both
  :class:`~literalizer.NewVariable` and
  :class:`~literalizer.ExistingVariable`, emitting the inference-style
  binding ``let my_data = make_widget(42)`` without the ``name: Val``
  type annotation or tagged-enum constructor wrapper that literal
  bindings use (the call's return type is not known to the renderer).
  Existing literal-binding output for F# is unchanged.  See #2249.
- :class:`~literalizer.PureScript` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call`, emitting the inference-style
  binding ``my_data = make_widget (PInt 42)`` without a ``name :: Type``
  annotation (the call's return type is not known to the renderer).
  ``wrap_in_file=True`` PureScript scaffolds add ``import Prelude`` so
  the call stub's ``Unit`` result type resolves; literal-binding output
  is unchanged.  See #2247.
- :class:`~literalizer.Rust` under the ``RECORD``
  ``heterogeneous_strategy`` now raises
  :class:`~literalizer.exceptions.UnrepresentableInputError` for a
  set-valued record field, and for a record field whose value is a
  dict that is not record-eligible (empty, non-string-keyed, or an
  ordered map), instead of emitting a struct whose declared field
  type disagrees with the rendered ``HashSet``/``BTreeSet``/``HashMap``
  literal and fails to compile.
- :class:`~literalizer.Roc` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call`, emitting the inference-style
  binding ``my_data = make_widget (RInt 42i128)`` without a
  ``my_data : Val`` annotation (the call's return type is not known to
  the renderer, and Roc infers it).  The ``Val`` tag-union alias is
  omitted from such scaffolds because nothing annotates with ``: Val``;
  existing literal-binding output is unchanged.  See #2250.
- :class:`~literalizer.Sml` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call`, emitting the inference-style
  binding ``val my_data = make_widget(42)`` without the ``: val_t``
  annotation or ``datatype`` constructor wrapping used for literal
  bindings (the call's return type is not known to the renderer, so
  SML infers it).  See #2248.
- :class:`~literalizer.OCaml` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call`, for both
  :class:`~literalizer.NewVariable` and
  :class:`~literalizer.ExistingVariable`, emitting the inference-style
  binding ``let my_data = make_widget(42)`` without the ``: val_t``
  annotation or tag constructor used for literal bindings (the call's
  return type is not known to the renderer, so OCaml infers it).
  The call-binding bypass now also covers the assignment template via
  the new ``format_call_variable_assignment`` hook, so OCaml's
  non-bare ``let x : val_t = ...`` assignment no longer leaks a tag
  constructor onto a call result.  Existing literal-binding output for
  every language is unchanged.  See #2246.

- :class:`~literalizer.Java` and :class:`~literalizer.Scala` no longer
  emit output that fails to compile for a post-2038
  :class:`~datetime.datetime`
  under the ``RECORD`` ``heterogeneous_strategy`` with
  ``datetime_format=EPOCH``.  The epoch seconds now carry the language's
  wide-integer suffix and the record component widens accordingly
  (``long`` / ``Long``) once the value leaves signed 32-bit range, so
  the declared component type always matches the rendered literal.
  In-range epochs are unaffected.  See #2338.
- :class:`~literalizer.Go` no longer emits output that fails to compile
  for a record field holding a positive integer beyond the signed
  64-bit range under the ``RECORD`` ``heterogeneous_strategy``.  Such a
  value renders through the ``uint64(...)`` overflow fallback, and the
  generated struct field is now typed ``uint64`` to match it instead
  of ``int`` / ``int64``.  Record integer fields formatted with a
  non-default ``integer_format``, ``numeric_separator`` or
  ``numeric_literal_suffix`` keep their value-derived field type.
  In-range integers are unaffected.  See #2306.
- :class:`~literalizer.Kotlin`, :class:`~literalizer.Java` and
  :class:`~literalizer.Scala` no longer emit output that fails to
  compile for a record field holding an integer beyond the signed
  64-bit range under the ``RECORD`` ``heterogeneous_strategy``.  The
  generated ``data class`` / ``record`` / ``case class`` field is now
  typed ``BigInteger`` / ``BigInteger`` / ``BigInt`` to match the
  arbitrary-precision overflow-fallback literal instead of
  ``Long`` / ``long``.  In-range integers are unaffected.  See #2376.
- Internal: the ``RECORD`` ``heterogeneous_strategy`` no longer threads
  the already-formatted field literal into the field-type hook.
  :class:`~literalizer.Kotlin` now derives each generated ``data class``
  field's declared type structurally from the raw value through its own
  collection openers and scalar mapping (matching the Go/Java/Scala
  ports), and the ``formatted`` string is dropped from the renderer
  contract.  No generated output changes.  See #2305.

2026.05.15.2
------------


- :class:`~literalizer.Rust` gains the ``TUPLE`` ``heterogeneous_strategy``.
  A fixed-length heterogeneous **scalar** array that is a dict value, a
  record field value, or the document root (every element scalar,
  spanning at least two scalar buckets) is rendered as a native tuple
  ``(e0, e1, ...)`` typed ``(T0, T1, ...)`` instead of raising.  It
  composes with ``RECORD``: a record field whose value is such an array
  becomes a tuple-typed struct field.  Heterogeneous arrays nested
  inside another list, or containing a non-scalar element, stay out of
  scope and still raise.  This lands the shared, language-agnostic
  machinery with Rust as the reference implementation; one
  language port follows per PR.  See #2327.
- :func:`~literalizer.literalize_call`'s ``zip_values`` parameter is
  replaced by a ``zip_source`` / ``zip_input_format`` pair, mirroring
  the primary ``source`` / ``input_format``.  ``zip_source`` is parsed
  internally with the *same* parser as ``source`` (so YAML ``!!omap``,
  datetime/bytes coercion, JSON5, TOML, ... behave identically by
  construction); its parsed top-level elements pair positionally with
  the generated calls (element-by-element when ``per_element`` is
  ``True``, otherwise the whole parsed value pairs with the single
  call) and are surfaced on :attr:`~literalizer.CallContext.zipped`
  exactly as before.  Callers no longer need to parse a companion file
  themselves or reach into private parsing internals.  Supplying
  ``zip_source`` without ``zip_input_format`` raises the new
  :class:`~literalizer.exceptions.ZipSourceWithoutInputFormatError`;
  the existing
  :class:`~literalizer.exceptions.ZipValuesWithoutCallTransformError`
  and :class:`~literalizer.exceptions.ZipValuesLengthMismatchError`
  contracts are unchanged, and a ``per_element=True`` ``zip_source``
  that does not parse to a list raises
  :class:`~literalizer.exceptions.PerElementNotListError`.  See #2340.

- :class:`~literalizer.Go` gains the ``record_shape_names`` constructor
  parameter (already on :class:`~literalizer.Rust`), a
  ``Mapping[frozenset[str], str]`` from a record shape's key-set to a
  custom struct name.  A mapped shape is declared and rendered with the
  given name instead of the auto-generated ``RecordN``; the
  ``record_struct_name_prefix`` counter advances only for the shapes
  with no custom name.  Names are validated as PascalCase Go
  identifiers that do not
  collide with the auto ``{prefix}{N}`` pattern or each other, raising
  :class:`~literalizer.exceptions.InvalidRecordNameError`.  A new
  ``supports_record_shape_names`` language-class flag mirrors the
  constructor.  See #2324.

- :class:`~literalizer.Kotlin` gains the same ``record_shape_names``
  constructor parameter, a ``Mapping[frozenset[str], str]`` from a
  record shape's key-set to a custom ``data class`` name.  A mapped
  shape is declared and rendered with the given name instead of the
  auto-generated ``RecordN``; the ``record_struct_name_prefix`` counter
  advances only for the shapes with no custom name.  Names are
  validated as PascalCase Kotlin identifiers that do not collide with
  the auto ``{prefix}{N}`` pattern or each other, raising
  :class:`~literalizer.exceptions.InvalidRecordNameError`.  Its
  ``supports_record_shape_names`` language-class flag is now ``True``.
  See #2324.

- :class:`~literalizer.Kotlin` now declares a ``data class`` field
  whose value is a custom-named nested record with that nested
  record's ``record_shape_names`` name (e.g. ``Entry``).  Previously
  such a field fell through to ``Double`` because the custom name does
  not match the auto-generated ``{prefix}{N}`` head, so the generated
  Kotlin did not compile.  See #2348.

2026.05.15.1
------------


- :class:`~literalizer.Java` gains the ``RECORD`` ``heterogeneous_strategy``
  (already on :class:`~literalizer.Rust` and :class:`~literalizer.Go`).
  Each record-shaped dict (non-empty, string-keyed) becomes a generated
  top-level ``record RecordN(type field, ...) {}`` declaration plus a
  matching positional ``new RecordN(value, ...)`` literal, so a dict
  whose values mix scalars and containers is representable instead of
  raising.  Component names keep the original keys and the
  record-name prefix is configurable via the new
  ``record_struct_name_prefix`` constructor parameter.  Generated
  ``record`` declarations require Java 16, so a ``RECORD`` spec pins
  ``language_version`` to ``JDK_16``.  See #2300.

- :func:`~literalizer.literalize_call`'s ``call_transform`` now receives
  a :class:`~literalizer.CallContext` instead of the bare call string.
  The context exposes ``call`` (the rendered call expression, formerly
  the sole argument), the zero-based ``index``, the input ``row``, and
  ``zipped``.  A new ``zip_values`` parameter pairs a second,
  equal-length sequence positionally with the generated calls; each
  entry is rendered as a language-native literal and surfaced on
  :attr:`~literalizer.CallContext.zipped`, so a transform can print an
  expected value beside each call's actual return value.  ``zip_values``
  requires a ``call_transform`` and must match the call count, raising
  the new :class:`~literalizer.exceptions.ZipValuesWithoutCallTransformError`
  / :class:`~literalizer.exceptions.ZipValuesLengthMismatchError`.
  ``call_transform`` is now supported only for call styles whose form
  is an expression that can be wrapped (positional, keyword, object);
  the sentinel-probe wrapper synthesis for prefix/postfix/command
  styles has been removed, and those styles now reject
  ``call_transform`` with
  :class:`~literalizer.exceptions.UnsupportedCallShapeError`.
  :func:`~literalizer.literalize_call` no longer raises
  ``DottedCallStubNotSupportedError`` or
  ``FreeFunctionCallNotSupportedError`` (a context-aware
  ``call_transform`` is opaque, so the core cannot inspect the
  wrapper); those exceptions are removed.  The
  ``supports_dotted_call_stub`` / ``has_free_function_calls`` language
  attributes are retained as descriptive metadata for callers that
  generate wrapper stubs.  See #2293.

- :class:`~literalizer.Kotlin` gains the ``RECORD``
  ``heterogeneous_strategy`` (already on :class:`~literalizer.Rust` and
  :class:`~literalizer.Go`).  Each record-shaped dict (non-empty,
  string-keyed) becomes a generated ``data class RecordN(val ...)``
  declared in the preamble plus a matching ``RecordN(field = value,
  ...)`` literal, so a dict whose values mix scalars and containers is
  representable instead of raising.  Field names keep the original
  dict keys and the data-class-name prefix is configurable via the new
  ``record_struct_name_prefix`` constructor parameter.  See #2298.
- :class:`~literalizer._language.LanguageCls` now exposes a
  ``supports_record_struct_name_prefix`` flag alongside the existing
  ``supports_*`` family.  Runtime-dispatched callers that look up a
  language by name can use it to decide whether to pass the
  ``record_struct_name_prefix`` constructor keyword argument without
  inspecting dataclass fields or the ``__init__`` signature.  It is
  ``True`` on :class:`~literalizer.Go`, :class:`~literalizer.Kotlin`,
  and :class:`~literalizer.Rust`, and ``False`` on every other language.

- :class:`~literalizer.Java` now offers ``VersionFormats.JDK_16``
  alongside ``VersionFormats.JDK_11`` (still the default), selected
  via ``language_version``.  Generated code is currently identical for
  both targets; the member exists so a future Java ``RECORD``
  ``heterogeneous_strategy`` (whose ``record`` declarations require
  Java 16) can gate on it.  The golden harness emits a parallel
  ``@jdk_16`` fixture set.  See #2313.

2026.05.15
----------

- :func:`~literalizer.literalize` now accepts an opt-in ``bound_refs``
  mapping.  Unlike ``ref_values`` (which only informs a ref's type and
  leaves it as a free external identifier), each name in ``bound_refs``
  additionally has a binding emitted for it before its first use, so a
  single ``literalize(..., bound_refs=..., wrap_in_file=True)`` call
  produces a complete, valid file with per-language declaration
  sequencing (Nix nested ``let``, the Fortran rule that specification
  statements precede executable statements, and so on).  Binding
  emission only happens with ``wrap_in_file=True`` and a
  :class:`~literalizer.NewVariable` or
  :class:`~literalizer.ExistingVariable` ``variable_form``; otherwise
  ``bound_refs`` degrades to type information only, exactly like
  ``ref_values``.  The default (no ``bound_refs``) is unchanged: a
  ``$ref`` stays a free external identifier.  The ref golden-file
  harness now drives every case through one ``literalize`` call,
  retiring its regex-based stub-stitching helpers.  See #2294.

- :class:`~literalizer.Go` gains the ``RECORD`` ``heterogeneous_strategy``
  (already on :class:`~literalizer.Rust`).  Each record-shaped dict
  (non-empty, string-keyed) becomes a generated ``type RecordN struct
  { ... }`` declared in the preamble plus a matching ``RecordN{Field:
  value, ...}`` literal, so a dict whose values mix scalars and
  containers is representable instead of raising.  Field names are
  exported (PascalCase) and the struct-name prefix is configurable via
  the new ``record_struct_name_prefix`` constructor parameter.  See
  #2297.

- :class:`~literalizer.Scala` gains the ``RECORD``
  ``heterogeneous_strategy`` (already on :class:`~literalizer.Rust` and
  :class:`~literalizer.Go`).  Each record-shaped dict (non-empty,
  string-keyed) becomes a generated ``case class RecordN(field: Type,
  ...)`` declared in the enclosing ``object`` plus a matching
  ``RecordN(field = value, ...)`` literal, so a dict whose values mix
  scalars and containers is representable instead of raising.  Field
  names are the dict keys verbatim and the ``case class``-name prefix
  is configurable via the new ``record_struct_name_prefix``
  constructor parameter.  See #2299.

- :class:`~literalizer.Rust` accepts a ``record_shape_names`` constructor
  parameter — a mapping from each record's key-set
  (:class:`frozenset` [:class:`str`]) to a user-chosen ``struct`` name —
  so the ``RECORD`` heterogeneous strategy can emit
  ``struct Entry { ... }`` instead of the auto-generated ``Record0``,
  ``Record1``, ... names.  Shape names that are not PascalCase Rust
  identifiers, that collide with ``heterogeneous_value_enum_name``,
  that duplicate another mapped name, or that match a Rust reserved
  keyword raise the new :class:`~literalizer.exceptions.InvalidRecordNameError`.
  The existing ``record_struct_name_prefix`` is validated the same way.
  See #2236.

- :class:`~literalizer.Fortran` now offers
  ``VersionFormats.V2003`` alongside ``VersionFormats.V2008``
  (the default).  The 2003 target defines the ``int64`` kind via
  ``selected_int_kind(18)`` instead of importing it from the intrinsic
  ``iso_fortran_env`` module (whose ``int64`` constant is a Fortran
  2008 addition), so generated code is otherwise identical and the
  ``_int64`` literal suffix is unchanged.  The golden harness emits a
  parallel ``@v2003`` / ``@v2008`` fixture set and CI lints each with
  the matching ``gfortran -std=f2003`` / ``-std=f2008`` flag.  See
  #1931.

- The integration golden-file harness now accepts ``input.toml`` next to
  the existing ``input.yaml`` for cases whose input contains a value
  YAML 1.2 cannot natively express (currently :class:`datetime.time`).
  New ``time_list``, ``time_dict``, and ``times_heterogeneous_with_dates``
  golden cases give every supported language end-to-end coverage of
  ``datetime.time`` rendering, which surfaced and fixed several
  preexisting bugs in time emission: tagged-union languages
  (:class:`~literalizer.Elm`, :class:`~literalizer.OCaml`,
  :class:`~literalizer.Roc`, :class:`~literalizer.Gleam`,
  :class:`~literalizer.Haskell`, :class:`~literalizer.Zig`,
  :class:`~literalizer.Sml`, :class:`~literalizer.Ada`,
  :class:`~literalizer.Fortran`, :class:`~literalizer.ObjectiveC`)
  now wrap a fallback ISO 8601 time inside the value-type constructor
  the same way they wrap other scalars; collection type inference
  (C++, C#, Java, Kotlin, Scala, Dart, Go, Visual Basic, and others)
  now knows about :class:`datetime.time` and narrows homogeneous
  collections to the correct element type; and :class:`~literalizer.FSharp`
  fully qualifies ``System.TimeOnly`` so the rendered output no longer
  emits an ``open System`` line before ``module``.  See #2230.

- :class:`~literalizer.Haskell` now accepts ``variable_form`` on
  :func:`~literalizer.literalize_call`, emitting the inference-style
  binding ``my_data = make_widget (42)`` without a ``name :: Type``
  annotation (the call's return type is not known to the renderer).
  ``wrap_in_file=True`` Haskell scaffolds emit a
  ``{-# OPTIONS_GHC -Wno-missing-signatures #-}`` pragma so the
  inferred binding compiles under ``-Wall -Werror``.  See #2244.

- :class:`datetime.time` is now a first-class :type:`Scalar` value.
  Languages with a native time-only type emit native literals
  (Python ``datetime.time(...)``, TOML unquoted ``HH:MM:SS``,
  .NET ``new TimeOnly(...)`` / ``TimeOnly(...)`` / ``New TimeOnly(...)``
  for :class:`~literalizer.CSharp`, :class:`~literalizer.FSharp`,
  :class:`~literalizer.VisualBasic`, and ``LocalTime.of(...)`` for
  :class:`~literalizer.Java`, :class:`~literalizer.Kotlin`,
  :class:`~literalizer.Scala`, :class:`~literalizer.Groovy`); other
  languages fall back to the existing ISO 8601 quoted-string form.
  TOML ``time`` inputs now round-trip through
  :class:`~literalizer.Toml` as native time literals instead of being
  re-emitted as quoted ISO 8601 strings.  Typed collection openers in
  languages such as :class:`~literalizer.CSharp`,
  :class:`~literalizer.Java`, :class:`~literalizer.Kotlin`, and
  :class:`~literalizer.Scala` now narrow uniform time-only sequences
  to the language's time type (e.g. ``TimeOnly[]`` /
  ``Array<LocalTime>``) instead of falling back to a generic
  ``Object``/``Any`` opener.
- Golden files for languages whose compiler version is pinned (Elixir,
  Erlang, Gleam, Kotlin, Odin, Zig) now carry the version in the
  filename: ``{stem}@{version}{extension}`` (e.g.
  ``Odin@dev-2026-04.odin``).  Every fixture is explicitly tied to
  the compiler version it was generated against.  Each ``lint.yml``
  job sets a job-scoped environment variable once and feeds it to
  both the install action and
  ``python -m tests.integration.list_fixtures``; the test code
  auto-discovers the same version from sibling filenames so no
  separate registry file is needed.

- :class:`~literalizer.Fortran`'s ``language_version`` default is now
  ``Fortran.VersionFormats.V2008`` (was ``V2003``) so it matches the
  Fortran 2008 features the generator actually emits (e.g. ``int64``
  from ``iso_fortran_env``). ``V2003`` has been removed from
  ``Fortran.VersionFormats``.

- ``lint-fast`` CI job now syntax-checks and runs the Python fixtures
  under ``tests/integration/cases``, matching the per-language gate
  already in place for Bash, Ruby, JavaScript, and other fixture
  languages.  See #1921.

- ``lint-odin`` CI job now uses ``odin run .`` again to catch runtime
  errors that ``odin build .`` cannot detect (e.g. nil-proc calls).
  The ``laytan/setup-odin`` action is pinned to ``dev-2026-04``, the
  last Odin release where ``odin run .`` did not segfault on these
  fixtures; ``release: latest`` (``dev-2026-05``) crashes at runtime, and
  the compiler itself segfaults on some fixtures under
  ``odin build .``.  See #1745.

2026.05.14.1
------------


2026.05.14
----------



- YAML inputs with non-string dict keys (integers, dates, booleans)
  now flow through to the target language's value-formatting path
  instead of being silently converted to string form.  Languages that
  can represent the key natively (Python, Ruby, Clojure, Lua, Bash,
  and others) produce the corresponding literal; languages whose dict
  syntax requires string keys or a homogeneous typed map raise
  :exc:`~literalizer.exceptions.UnrepresentableInputError`.  The
  affected opt-out targets are the JSON family (already
  :class:`~literalizer.Json5`, :class:`~literalizer.Jsonnet`,
  :class:`~literalizer.Toml`), the string-keyed attribute-set
  languages (:class:`~literalizer.Nix`, :class:`~literalizer.Dhall`,
  :class:`~literalizer.Cobol`), the statically-typed-map languages
  whose typed-map syntax has not yet been generalized
  (:class:`~literalizer.Go`, :class:`~literalizer.Kotlin`,
  :class:`~literalizer.CSharp`, :class:`~literalizer.Haskell`,
  :class:`~literalizer.Scala`, :class:`~literalizer.Dart`,
  :class:`~literalizer.VisualBasic`, :class:`~literalizer.FSharp`,
  :class:`~literalizer.Zig`, :class:`~literalizer.Odin`,
  :class:`~literalizer.Nim`, :class:`~literalizer.D`,
  :class:`~literalizer.TypeScript`,
  :class:`~literalizer.JavaScript`), the languages that reject
  specific non-string key types at the language level
  (:class:`~literalizer.Php` rejects ``DateTime`` keys,
  :class:`~literalizer.V` rejects ``bool`` keys), and the languages
  whose value ADTs do not currently model non-string keys
  (:class:`~literalizer.OCaml`, :class:`~literalizer.Sml`,
  :class:`~literalizer.R`).

- :func:`~literalizer.literalize_call` now accepts a ``variable_form``
  argument (``NewVariable`` or ``ExistingVariable``) that wraps the
  rendered call in an idiomatic per-language variable binding (e.g.
  ``let my_data = make_widget(42);``,
  ``const my_data = make_widget({ count: 42 });``,
  ``my_data = make_widget(count=42)``).  Mutability and inference
  style are controlled by the per-language ``declaration_style`` and
  ``Modifiers`` enums on the supplied ``Language`` instance.
  ``BothVariableForms`` is rejected -- emitting both a declaration
  and an assignment would invoke the target function twice -- as is
  ``per_element=True`` (no per-element name vector) and any language
  whose call form is a statement rather than an expression
  (``call_returns_expression=False``).  All three are surfaced as
  :exc:`~literalizer.exceptions.UnsupportedCallShapeError`.  The same
  exception is raised for languages whose declaration template wraps
  or transforms the right-hand side in a way that is only valid for
  literal values -- Tcl (needs ``[...]`` command substitution), Bash
  (needs ``$(...)`` command substitution), Objective-C (``@(...)``
  boxing of primitives), tagged-enum heterogeneous-strategy languages
  (Roc, Haskell, Elm, SML, OCaml, PureScript, F#), C / SystemVerilog /
  Fortran / Ada / Zig / D (struct-initializer or constructor wrapping
  derived from the value's literal type), Elixir (call stubs need
  module scope, not the variable's function body), Erlang, Forth, and
  Nim.  Closes
  `#1961 <https://github.com/adamtheturtle/literalizer/issues/1961>`_.

- The internal :data:`~literalizer._types.Value` and
  :data:`~literalizer._types.ValueInput` aliases now permit any
  :data:`~literalizer._types.Scalar` as a dict key, in preparation for
  surface formats that admit non-string dict keys.  A new
  :exc:`~literalizer.exceptions.UnrepresentableInputError` and a
  ``supports_non_string_dict_keys`` class attribute on
  :class:`~literalizer.Language` (defaulting to ``True``; overridden to
  ``False`` on :class:`~literalizer.Json5`,
  :class:`~literalizer.Jsonnet`, and :class:`~literalizer.Toml`) wire a
  centralized guard at the dict-formatting boundary.  The surface
  parsers still produce only string-keyed dicts, so behavior is
  unchanged.

- :func:`~literalizer.literalize` now accepts a ``ref_values`` mapping
  from ref identifier to the value declared elsewhere for that ref.
  Languages whose ``$ref`` rendering depends on the referenced type
  (V's ``.clone()`` for arrays and maps, Mojo's ``^`` for non-trivial
  values, C++'s ``std::move`` for ``non-trivially-copyable`` values)
  consult it to choose the right form; when omitted these languages
  keep their type-agnostic default.  ``V`` now emits a bare identifier
  for scalar refs (``int``, ``bool``, ``f64``) because ``int.clone()``
  is rejected by the V compiler; ``Mojo`` drops ``^`` for
  register-trivial scalars where it is a hard error under ``--Werror``;
  ``Cpp`` drops ``std::move`` for ``trivially-copyable`` scalars where
  clang-tidy's ``hicpp-move-const-arg`` rejects it.  Preamble inference
  also walks the resolved ``ref_values`` so sum-type body declarations
  (Haskell's ``data Val``, OCaml's ``val_t``, Roc's ``Val``, …) include
  the variants needed by the referenced types.
  ``SystemVerilog``'s :func:`literalize` rejects scalar ``$ref`` markers
  via :exc:`~literalizer.exceptions.CallArgNotSupportedError`: SV keys
  the variable declaration off the marker dict's shape (``_VKV name[]``)
  and cannot produce a coherent declaration for a scalar referent.

- The
  :attr:`~literalizer._language.Language.format_call_ref_identifier`,
  :attr:`~literalizer._language.Language.format_call_arg_ref_identifier`,
  and
  :attr:`~literalizer._language.Language.format_call_arg_ref_identifier_consumable`
  hooks now receive a second positional argument: the ``Value`` behind
  the ref (or ``None`` when the caller did not supply ``ref_values``).
  This is a breaking change for custom :class:`~literalizer.Language`
  implementations that override these hooks; most overrides ignore the
  new argument.

- :class:`~literalizer.V` now defaults
  ``heterogeneous_strategy`` to
  ``V.heterogeneous_strategies.ERROR`` and reports
  ``dict_supports_heterogeneous_values=False`` and
  ``supports_heterogeneity=False`` on its sequence and set formats.
  V is statically typed and rejects unwrapped heterogeneous
  collections, so rendering them now raises rather than emitting
  code the V compiler will not accept.  Callers that want to
  materialize heterogeneous data must opt in to
  ``V.heterogeneous_strategies.INTERFACE``, which wraps values with
  ``IVal(...)`` and emits the ``interface IVal {}`` declaration as
  before.

2026.05.13.1
------------


- :class:`~literalizer._language.LanguageCls` now exposes
  ``supports_empty_dict_key``, ``supports_call_style``,
  ``supports_default_dict_key_type``, ``supports_default_dict_value_type``,
  ``supports_default_sequence_element_type``,
  ``supports_default_set_element_type``, and
  ``supports_default_ordered_map_value_type`` flags alongside the existing
  ``supports_module_name``.  Runtime-dispatched callers that look up a
  language by name can use these to decide whether to pass the matching
  constructor keyword argument without inspecting dataclass fields or the
  ``__init__`` signature.

2026.05.13
----------


- :class:`~literalizer.Haskell` ``CURRIED``
  :class:`~literalizer.CallStyle` now emits a thunk binding
  (``process :: IO Val`` / ``process = ...``) for zero-parameter
  calls instead of a malformed signature with an empty argument
  type (``process ::  -> IO Val``).
- :func:`~literalizer.literalize` now raises
  :class:`~literalizer.exceptions.WrapInFileWithoutVariableNotSupportedError`
  when ``wrap_in_file=True`` is combined with ``variable_form=None`` for
  a target language that cannot represent a bare value at file-statement
  scope.  Each :class:`~literalizer._language.Language` declares its
  ability to render this shape via a new
  ``supports_no_variable_wrap_in_file`` flag.  Strict-typed compiled
  languages (Rust, C, C++, Haskell, OCaml, Swift, Ada, D, Dart, C#, Elm,
  Mojo, Nim, Objective-C, Odin, SML, V, Zig, Go, Java, Kotlin, F#,
  Scala, Erlang, Gleam, Roc, PureScript, Tcl, Bash, VB, SystemVerilog,
  Occam) opt out, along with Cobol, Fortran, Php, Lua, Toml, and Dhall
  — each of which produced a file whose linter rejected the resulting
  bare-value rendering even though the issue text initially listed them
  as opt-in.  The renderer no longer silently emits invalid output for
  any of these.

- :class:`~literalizer.Haskell`, :class:`~literalizer.FSharp`,
  :class:`~literalizer.OCaml`, and :class:`~literalizer.Sml` now expose
  a ``CURRIED`` :class:`~literalizer.CallStyle` alongside the existing
  ``POSITIONAL`` member.  Selecting it emits curried application calls
  (``process arg1 arg2``) with curried stubs in place of the tuple
  form.  :class:`~literalizer.Haskell` defaults to ``CURRIED`` since
  curried application is the idiomatic call form in Haskell; F#, OCaml,
  and SML keep ``POSITIONAL`` as the default.

- :class:`~literalizer.Elm` :func:`~literalizer.literalize_call` now
  emits curried-application calls (``process (EInt 1) (EInt 2)``) with
  curried type stubs (``process : a -> b -> ()``) in place of the prior
  tuple-form (``process (EInt 1, EInt 2)``).  Elm tuple literals cap at
  three elements, so the tuple form had no representation for calls
  with four or more parameters; the curried form composes naturally
  with ``|>`` and matches the convention used by ``elm-format`` and the
  standard library.

- The ``Language.max_call_parameters`` attribute has been removed.  No
  remaining language sets a maximum parameter count, so the
  upstream ``UnsupportedCallShapeError`` check in
  :func:`~literalizer.literalize_call` and the corresponding
  ``language_cls.max_call_parameters`` introspection no longer have a
  load-bearing caller.

- The ``supports_commented_dict_call_args`` flag has been removed from
  ``Language``.  Every (language, shape) pair previously dropped by the
  test-discovery filter on this flag is either already short-circuited
  by an earlier exception path or now renders cleanly, leaving the flag
  with no load-bearing callers.

- :func:`~literalizer.literalize_call` now raises
  :class:`~literalizer.exceptions.UnsupportedCallShapeError` when the
  innermost segment of ``target_function`` collides with one of the
  target language's reserved identifiers.  The renderer previously
  produced output that would not parse in the target language.

- :func:`~literalizer.literalize_call` now raises
  :class:`~literalizer.exceptions.UnsupportedCallShapeError` when a
  ``call_transform`` wrapper is supplied for a language whose calls are
  statements rather than expressions (i.e. ``call_returns_expression``
  is ``False``).  The wrapper cannot consume the call as a value in
  that case, and the renderer previously emitted invalid output.

- :func:`~literalizer.literalize_call` no longer rejects identity
  ``call_transform`` values on Ada, Fortran, and SystemVerilog.  Bare
  procedure-call statements (``Process(x);``, ``call process(x)``,
  ``process(x);``) are valid in all three languages, so the prior
  rejection encoded a constraint that does not exist.  The
  ``Language.allows_bare_call_statement`` flag introduced alongside that
  check has been removed.

- The PureScript, Roc, and Elm wrapped-call indent helpers no longer
  carry defensive branches for blank or whitespace-leading lines.
  These helpers only ever receive single-line call expressions from
  ``literalize_call`` (which uses :attr:`CollectionLayout.COMPACT` for
  wrapped calls and rejects standalone comments in that path), so the
  empty-line and continuation arms were unreachable via the golden
  integration cases.  Four unit tests in ``tests/test_languages.py``
  that drove the Elm helpers directly with constructed multi-line
  input have been removed in favor of the existing golden-file
  contract.

- ``Mojo`` :func:`~literalizer.literalize_call` now supports refs nested
  inside dict literals and commented dict-literal call arguments.  The
  typed-stub work landed in #1972 made both shapes compile cleanly under
  ``mojo run --Werror``, so the corresponding
  ``supports_call_refs_in_dict_literals`` and
  ``supports_commented_dict_call_args`` flags flip to ``True`` for Mojo
  and two new ``call_*`` golden cases are exercised.

- ``Mojo`` and ``C++`` :func:`~literalizer.literalize_call` no longer
  wrap a consumable ``$ref`` in the language's consume form when the
  underlying value's type would make the wrapping a hard error or a
  ``clang-tidy`` lint failure.  In Mojo, ``^`` is dropped for
  register-trivial scalars (``Int``, ``Bool``, ``Float64``) because
  Mojo 0.26.1.0+ rejects "transfer from a value of trivial register
  type" under ``--Werror``.  In C++, ``std::move`` is dropped for
  register-trivial types (``bool``, integer, ``double``,
  ``std::chrono::year_month_day``,
  ``std::chrono::system_clock::time_point``) which
  ``performance-move-const-arg`` / ``hicpp-move-const-arg`` reject.
  Non-trivial refs (e.g. ``List[...]``, ``Dict[...]``, strings, bytes)
  keep their consume form.  ``Language`` exposes a new
  :attr:`~literalizer._language.Language.consumable_ref_value_inhibits_consuming_form`
  predicate that languages override to opt into per-value routing; the
  default (:data:`~literalizer._language.never_inhibits_consuming_form`)
  preserves the existing behavior.

- Renamed ``VariableTypeHints.AUTO`` to ``VariableTypeHints.NEVER`` for
  every language.  The behavior is unchanged; the new name describes
  the option (no annotation, defer to the language's inference) rather
  than implying intent, and pairs symmetrically with ``ALWAYS``.

- Every language's ``VariableTypeHints`` enum now exposes a third value,
  ``SAFE``, alongside ``NEVER`` and ``ALWAYS``.  ``SAFE`` annotates only
  when the language's own inference would widen the variable to a
  permissive type (e.g. ``unknown[]`` for an empty TypeScript array,
  ``Object[]`` for an empty Java array), making downstream consumption
  safer than ``NEVER`` without the noise of ``ALWAYS``.  The predicate is
  per-language: ``TypeScript`` and ``Java`` annotate empty list / set /
  dict literals; for every other language ``SAFE`` currently produces
  the same output as ``NEVER`` while leaving room for a future
  per-language predicate.

- ``Nim`` :func:`~literalizer.literalize_call` now emits the
  object-variant ``type`` declaration when the ``OBJECT_VARIANT``
  heterogeneous strategy is active, so the rendered call references a
  defined wrapping type.

- ``Mojo`` typed call stubs now cover ``bool``, ``float``, ``bytes``,
  ``date``, and ``datetime`` argument values (mapped to ``Bool``,
  ``Float64``, and ``String`` respectively), and apply to dotted-method
  stubs as well as free-function stubs.  The generic
  ``[*Ts: AnyType](*args: *Ts)`` form is still emitted when scalar
  types disagree across calls or any argument is non-scalar.

- ``Mojo`` :meth:`~literalizer.Language.format_call_preamble_stub` now
  raises
  :class:`~literalizer.exceptions.HeterogeneousScalarCollectionError`
  under the default ``ERROR`` ``heterogeneous_strategy`` when concrete
  Mojo argument types diverge across calls at one parameter slot
  (including divergent shapes such as scalar in one call and list in
  another).  ``VARIANT`` callers continue to fall back to the generic
  ``[*Ts: AnyType](*args: *Ts)`` form for cross-call divergence pending
  follow-up wrap machinery.

- :func:`~literalizer.literalize_call` now raises a typed
  :class:`~literalizer.exceptions.UnsupportedCallShapeError`
  when ``wrap_in_file=True`` and the YAML source carries standalone
  comments but the target language sets
  ``supports_standalone_comments_in_wrapped_calls = False`` (currently
  ``Elm``, ``Erlang``, ``Haskell``, ``Jsonnet``, ``PureScript``, and
  ``Roc``).  :class:`~literalizer.LiteralizeResult` now exposes
  :attr:`~literalizer.LiteralizeResult.contains_standalone_comments`
  so callers that wrap manually via
  :meth:`~literalizer.Language.wrap_calls_with_declarations` can apply
  the same guard.

- :func:`~literalizer.literalize` now raises a typed
  :class:`~literalizer.exceptions.VariableNameNotSupportedError`
  when ``variable_form`` is supplied but the target language sets
  ``supports_variable_names = False`` (currently ``Json5``,
  ``Jsonnet``, and ``Yaml``).  The capability flag is now enforced
  rather than declarative.

- ``supports_variable_names`` is now ``True`` on ``Clojure``,
  ``CommonLisp``, ``Julia``, ``Racket``, ``Ruby``, and ``Scheme``,
  reflecting that these languages do support named variable wrapping
  via ``literalize``'s ``variable_form`` argument (and have golden
  files exercising that behavior).

- Separated syntactic ``ref_case`` validity from stylistic preference.
  :class:`~literalizer.Language` now exposes
  :attr:`~literalizer.Language.supported_ref_cases` -- a frozenset of
  cases that produce a syntactically legal identifier -- alongside the
  existing :attr:`~literalizer.Language.identifier_cases`, which now
  documents stylistic preference only.  ``literalize`` and
  ``literalize_call`` validate ``ref_case`` against
  ``supported_ref_cases``, so cases that are syntactically legal but
  non-idiomatic (e.g. ``IdentifierCase.CAMEL`` in Python) are now
  accepted.  Two shared constants,
  :data:`~literalizer.NON_KEBAB_REF_CASES` and
  :data:`~literalizer.ALL_REF_CASES`, cover the common settings.

- :func:`~literalizer.literalize_call` now raises a typed
  :class:`~literalizer.exceptions.DottedCallTargetNotSupportedError`
  when ``target_function`` contains a dot but the target language sets
  ``supports_dotted_calls = False`` (currently only ``Hcl``).  The
  capability flag is now enforced rather than declarative.

- :func:`~literalizer.literalize_call` now raises a typed
  :class:`~literalizer.exceptions.DottedCallStubNotSupportedError`
  when ``call_transform`` produces a dotted wrapper name (e.g.
  ``tracer.emit``) but the target language sets
  ``supports_dotted_call_stub = False``.  The capability flag is now
  enforced rather than declarative.

- :func:`~literalizer.literalize_call` now raises a typed
  :class:`~literalizer.exceptions.FreeFunctionCallNotSupportedError`
  when ``call_transform`` produces a bare wrapper name with no dot
  (e.g. ``emit``) but the target language sets
  ``has_free_function_calls = False`` (currently only ``Wren``).  The
  capability flag is now enforced rather than declarative.

- Removed the redundant ``supports_default_set_element_type``,
  ``supports_default_sequence_element_type``,
  ``supports_default_dict_value_type``, ``supports_default_dict_key_type``,
  and ``supports_default_ordered_map_value_type`` class attributes from
  ``LanguageCls`` and all language implementations.  Direct constructor
  calls already surface unsupported ``default_*_type`` keyword arguments
  through type checking, making these probe flags unnecessary.

- :func:`~literalizer.literalize_call` accepts a new ``ref_values``
  mapping from ``{"$ref": "name"}`` identifiers to the source values
  declared elsewhere.  Supplied ref values now participate in
  data-driven preamble inference, so generated body declarations such
  as Haskell's ``data Val = ...`` include types reachable only through
  refs while the rendered call still emits the bare identifier.

2026.05.01.1
------------


2026.05.01
----------


2026.04.30.3
------------


2026.04.30.2
------------


2026.04.30.1
------------


- :func:`~literalizer.literalize_call` accepts a new ``consumable_refs``
  parameter listing the ref identifiers the call may move from.  In C++,
  only refs in this set -- and only when they appear in exactly one call
  argument across the rendered calls -- are wrapped in ``std::move(...)``;
  all other refs emit as the bare identifier so the variable remains
  valid for any subsequent use (whether in a later per-element call
  within the same ``literalize_call`` block, or elsewhere in the
  surrounding source).  Mojo's ``^`` transfer operator is treated the
  same way.  This is a breaking change: previously C++ unconditionally
  wrapped every call-argument ref in ``std::move(...)``, which produced
  use-after-move when the same variable was referenced by more than
  one per-element call.  Pass ``consumable_refs={"my_var"}`` to
  restore the previous behavior for ``my_var``.
- :func:`~literalizer.literalize` and :func:`~literalizer.literalize_call`
  now accept a ``ref_key`` parameter (``str``, default ``"$ref"``).  The
  marker key used to identify variable-reference mappings in the input data
  is now user-configurable: a single-key dict whose key equals *ref_key*
  and whose value is a string is treated as a ref marker.  Pass
  ``ref_case`` only when the identifier name should be converted before
  rendering.
- Every built-in language class now exposes a ``VersionFormats`` enum and a
  configurable ``language_version`` constructor parameter that selects which
  version of the target language the generated code is written for.  For
  example, ``Ada().language_version`` defaults to
  ``Ada.version_formats.ADA_2022``, whose ``.value`` is ``"Ada 2022"``.
  Each language currently defines a single version; additional versions
  may be added in future releases.  Both ``version_formats`` and
  ``language_version`` are part of the :class:`~literalizer.Language`
  protocol, so custom language implementations must also define them.

2026.04.30
----------

- :func:`~literalizer.literalize_call` now expands ``{"$ref": "name"}``
  markers that appear nested inside list elements or dict values of an
  argument, in addition to the existing support for top-level argument
  refs.  ``ref_case`` conversion and preamble stripping apply recursively
  to nested refs just as they do to top-level ones.

2026.04.29
----------

- :func:`~literalizer.literalize` now accepts a ``ref_case`` parameter
  (:class:`~literalizer.IdentifierCase`).  When set, any
  ``{"$ref": "name"}`` mapping in the input data -- at the top level or
  nested inside dicts and lists -- is rendered as a bare identifier
  instead of a literal dict.  The identifier is case-converted to match
  the language's conventions (e.g. ``my_var`` becomes ``myVar`` for
  JavaScript).  Languages apply their own sigil prefix via
  ``format_call_ref_identifier`` (e.g. ``$my_var`` for PHP).  Without
  ``ref_case``, ``$ref`` mappings are treated as ordinary literal dicts,
  preserving backwards compatibility.  Passing a case not in
  ``language.identifier_cases`` raises
  :exc:`~literalizer.exceptions.UnsupportedIdentifierCaseError`.
- Added support for Roc as a new output language.  ``Roc`` emits a
  ``Val`` tag-union type alias (``RNull``, ``RBool``, ``RInt``,
  ``RFloat``, ``RStr``, ``RList``, ``RDict``, ``RSet``) inside the
  module body, exposing the generated value via ``module [my_data]``.
  Calls use the space-separated command syntax with each argument
  wrapped in parentheses (``process (RInt 1) (RInt 2)``), with
  module-level stubs of the form ``name : a, b -> {}``.  A new
  ``lint-roc`` job in ``.github/workflows/lint.yml`` runs ``roc check``
  against every ``.roc`` fixture using the upstream nightly tarball.
- C, C++, Objective-C, and D fixtures now emit a ``main`` entry point
  directly (``int main(void)``/``int main()``/``void main()``) instead
  of a ``check_()``/``_check()`` function that required a separate
  per-language driver script.  Haskell non-call fixtures now append
  ``main = seq my_data (return ())`` to the module, and SML fixtures
  are emitted as top-level declarations ending with ``val _ = my_data``
  instead of inside a ``structure Check = struct … end`` wrapper.  All
  six driver scripts (``c_main.c``, ``cpp_main.cpp``, ``objc_main.m``,
  ``d_main.d``, ``sml_force.sml``, ``sml_main.mlb``,
  ``sml_call_main.mlb``) have been removed.  CI now compiles and runs
  each fixture directly without a linking step against a driver object.
  ``run_haskell.py`` has been removed; the CI now copies each Haskell
  fixture to a temporary workspace (renaming to match its unique module
  name), generates a ``Main.hs`` driver that imports every fixture
  qualified and calls its ``main``, and compiles and runs them all in a
  single ``ghc`` invocation.
- Ada output now uses Ada 2022 container aggregates (``AList'[...]``,
  ``AMap'[...]``, ``ASet'[...]``) and emits a ``with A_Stub; use
  A_Stub;`` context clause so each fixture compiles and runs against
  a checked-in stub package.  The lint workflow gained a "Run Ada
  files" step that builds and executes every fixture, replacing the
  previous syntax-only check.  The combined declaration + assignment
  wrapper now keeps both forms in a single procedure scope so the
  assignment can reach ``my_data``.
- ``Jsonnet`` now emits ``$ref`` declarations as top-level ``local``
  bindings before the call expressions, so call-mode output with
  ``ref_declarations`` is supported.  Previously the integration
  harness skipped ``Jsonnet`` for ref-declaration cases because the
  array-wrapped output had no place for variable bindings.  The
  ``DeclarationStyles.ASSIGN`` template changed from ``{value}`` to
  ``local {name} = {value};``, and ``Jsonnet`` now overrides
  ``wrap_calls_with_declarations`` to emit those bindings before
  ``wrap_in_file`` wraps the calls in ``[ … ]``.
- C single-name call stubs (e.g. ``emit``, ``process``) are now emitted
  as ``static`` definitions with a stub body instead of bare forward
  declarations, so generated fixtures can be linked and run.  The lint
  workflow now compiles each C fixture against a small ``c_main.c``
  driver and executes the resulting binary, surfacing runtime errors
  that the previous ``-fsyntax-only`` check missed.
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
  targets, so a user-written ``throttler.check(...)`` is rendered as
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
