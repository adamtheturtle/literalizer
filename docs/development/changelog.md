# Development history

Archived CI, test, and maintenance notes, including the original wording of mixed entries whose user-facing changes remain in the published changelog.
New maintenance details belong in commit messages and pull requests.

## Unreleased

- Preserve stale golden fixtures during ordinary verification and require explicit regeneration to remove them.
  ([#5321](https://github.com/adamtheturtle/literalizer/issues/5321))
- Seeded call golden fixtures require a mutable binding when their assignment introduces another declaration.
  ([#5640](https://github.com/adamtheturtle/literalizer/issues/5640))
- Golden fixture orphan checks now reject combined heterogeneous-strategy files for language versions that the renderer does not exercise.
  ([#5329](https://github.com/adamtheturtle/literalizer/issues/5329))
- Include accepted calls with unused reserved parameter labels in golden-file discovery.
  ([#5440](https://github.com/adamtheturtle/literalizer/issues/5440))
- Refresh the C++14 nested null reference golden file for the current import order.
  ([#5381](https://github.com/adamtheturtle/literalizer/issues/5381))
- Simplify reference golden input preparation to retain the existing lint complexity limit after combining reference coverage.
  ([#5342](https://github.com/adamtheturtle/literalizer/issues/5342))
- Read synthetic call-golden seed bindings before overwriting them so strict compiler and analyzer checks accept existing-variable scaffolds.
  ([#5687](https://github.com/adamtheturtle/literalizer/issues/5687))
- Run validation workflows for pull requests targeting feature branches so stacked changes receive the normal checks.
  ([#5415](https://github.com/adamtheturtle/literalizer/issues/5415))
- Match public call-target keyword validation when discovering golden-file cases.
  ([#5445](https://github.com/adamtheturtle/literalizer/issues/5445))
- Use the generated root identifier when executing Elm golden files.
  ([#5284](https://github.com/adamtheturtle/literalizer/issues/5284))
- Use golden-file binding metadata when checking Dart fixture initialization with custom root names.
  ([#5450](https://github.com/adamtheturtle/literalizer/issues/5450))
- Respect identifier case sensitivity when classifying reserved call parameter labels in golden-file discovery.
  ([#5444](https://github.com/adamtheturtle/literalizer/issues/5444))
- Call golden scaffolds validate target names in their generated declaration context.
  ([#5648](https://github.com/adamtheturtle/literalizer/issues/5648))
- Refresh C++ native record reference golden files for the current reference-binding declarations.
  ([#5344](https://github.com/adamtheturtle/literalizer/issues/5344))

## 2026.09.16

- Type the Zig inferred-element mapping with the inference domain instead of `object`.
- Type record-name callbacks with Literalizer values instead of arbitrary objects.
- Type Bash, D, and SystemVerilog language callbacks with their actual receiver and collection types.
- Type internal bound-reference name collections independently of their values.

## 2026.09.04

- TypeScript golden files are now type-checked under `tsc --strict` with a consumer probe appended after each declaration, so a literal that compiles on its own but cannot be indexed, looked up or iterated the way its shape invites fails CI.

## 2026.08.31

- No user-facing change: the V, Standard ML, Haskell, Dhall, Bash and Wren round-trip drivers no longer depend on the exact shape of the shared corpus.
  The V walker covers every element and value type the interface strategy emits and aborts on an unhandled one instead of writing `null`; the Standard ML and Haskell encoders take their clauses from the constructors the literalized type declares; the Dhall walker converts each entry directly when the document is single-family and declares no union; the Bash emitter indexes an associative array through a variable rather than an unquoted subscript and escapes every C0 control; and the Wren driver computes which keys hold a number `Num` cannot re-print rather than listing them.
- No user-facing change: the test modules that stay written out rather than becoming golden-file or TOML-driven cases now each say why in their docstring.
- Moved bare-value, rebound-anchor, and round-trip capability test matrices from Python parameter lists into validated TOML case files.
- Removed all coverage-ignore directives, deleted unreachable defensive paths, and moved the remaining boundary coverage into a shared cross-language integration fixture.

## 2026.08.29.1

- Renamed 94 news fragments from `.bugfix` to `.change` so `towncrier` includes them, and added a `prek` hook that rejects any other suffix.

## 2026.08.29

- Every language now declares for itself what it once inherited from a default held one level up, so nothing takes a behavior nobody considered for it.
  A meta-test holds every language to the list.
- No user-facing change: the `strict-kwargs` development dependency is updated, its pre-commit hook entry is corrected for the current CLI, and the calls the updated checker reports are respelled with keyword arguments.

## 2026.08.20

- The C++ lint jobs now compile against a pinned, cached `nlohmann/json` single header instead of installing the `nlohmann-json3-dev` package, removing the apt step that intermittently hung for the whole job budget.
- No user-facing change: the lint workflow's network installs are bounded and retried so a stalled registry no longer consumes a whole job, each retry is sized so every configured attempt fits inside its step budget, and the clang-tidy C job checks against a pinned, cached `cJSON` header instead of installing a package.
- No user-facing change: the `prek` version CI runs now matches the pinned development dependency, and the `check-yaml` hook skips the two capability cases whose non-finite floats its parser rejects.

## 2026.08.13.1

- Use Apache's canonical archive to install the pinned Groovy release in lint CI.

## 2026.08.12.4

- Exercise Bash's default string format in its round-trip check.

- Expand multiline-string coverage across root, nested, variable, and indented contexts, fixing invalid nested keys, Crystal JSON escapes, and Perl UTF-8 handling uncovered by executable round trips.
- Golden input coverage now lives in validated, versioned `case.toml` manifests beside each fixture.
  The migration also removes the redundant `simple_sequence` sequence-variable-name golden cases.

## 2026.08.12

- Custom language classes now declare a stable `language_id` string, and `VariantMetadata` carries only renderer capability and option-compatibility facts.
  Fields that existed solely to name or host golden fixtures, along with `empty_container_type_hint_variant_kwargs`, have moved to the test suite's own language metadata files.
- Language classes no longer declare `non_default_kwargs` or `declaration_style_sequence_format_overrides`.
  Neither described what a language can render: both named sample values the golden test suite passes in, and both now live in that suite's own per-language metadata instead.
  A custom language class no longer has to declare them.
  The compatibility rule they sat next to is unaffected, since it was always enforced in production: Rust still rejects a `CONST` or `STATIC` declaration style combined with the `VEC` sequence format.
- Golden variant-axis expansion is now declared in a validated, versioned `tests/integration/axes.toml` registry.
  Each axis names one of two typed plans and supplies that plan's parameters; the closed vocabulary of gates and overrides is resolved against registries in Python, so an unknown plan, gate kind, option, or name-template placeholder fails when the registry loads.
  Fifty-one axes moved off hand-written builders, the irregular tail stays as a registered set of typed builders that a meta-test holds to its current size, and the golden files themselves are unchanged.
- Each `literalize_call` golden case now declares the language-variant axes that drive it in its own `case.toml`, through `[[call.variants]]` tables, instead of a central list pairing case directories to builder functions by name.
  Axis names resolve against the same closed registry that already gates ordinary variant declarations, so a misspelled name fails when the manifest loads.
  The registry gained a `filtered` plan, which narrows another axis to the languages a gate admits, replacing the call-only wrappers that filtered a general builder in Python.
  The golden files are unchanged.
- The golden variant-axis registry now carries one entry per formatter option.
  The `date_format`, `datetime_format` and `bytes_format` options each read the value the language constructor took rather than the formatter the language derived from it, so an axis over one of them no longer expands a language default under a non-default variant name.
  The eighty-two golden files that re-pinned the Haskell, OCaml and SML default date, datetime and bytes rendering are gone; every other golden file is unchanged.

## 2026.07.20.1

- Add `literalize(record_null_substitutions=...)` for replacing null-valued record fields by name before validation, type inference, and rendering.
  This lets a single language-neutral fixture use target-appropriate sentinels (for example C++ `-1` integers and empty strings) while unconfigured fields and languages retain their existing null behavior (issue \#3143).

## 2026.07.14

- Group the documentation index into captioned "Guides", "Reference", and "Project / Development" sections, and correct the contributing guide to reference `prek` hooks and the `uv run --extra dev pytest` test command.
- Add a public `LiteralizeResult.sections` accessor (a tuple of the new `FileSection` dataclass) that exposes the file regions of a multi-section language's `wrap_in_file=False` output, so a caller can compose each region into its own program template instead of parsing a language-internal marker.
  COBOL under `json_type=CJSON` is the first such language, surfacing its `WORKING-STORAGE` and `PROCEDURE` regions (named by the `Cobol.CJSON_WORKING_STORAGE_SECTION` / `Cobol.CJSON_PROCEDURE_SECTION` constants); its CI round-trip helper now composes those regions directly rather than splicing into a wrapped program.
- Fold the resolution guidance for each exception into its class description (a "To resolve, ..." sentence) and render the remaining stages of the "Common errors" documentation page with `autoexception` directives instead of hand-maintained Cause / How-to-resolve tables, so each exception's meaning and recommended fix are single-sourced from `literalizer.exceptions` and can no longer drift between the page and the API reference.
- Generate the per-language heterogeneous-strategy support matrix in the documentation from the language registry at build time (rendered with the `sphinx-jinja` extension), so it can no longer drift from the `heterogeneous_strategies` enum on each language class.
  This also corrects the previously stale matrix, which omitted several languages that now expose `RECORD`.

## 2026.06.02

- Add a Bash JSON round-trip check to CI using the shared round-trip fixture, driven by the pinned `bash` interpreter.
  Because Bash associative arrays cannot nest, the check walks the known JSON shape and runs `eval` on each nested-collection string to rebuild a fresh array before re-emitting JSON.
- Add a C JSON round-trip check to CI using the shared round-trip fixture; because the literalizer's `CVal` union carries no run-time discriminator, the helper builds a parallel `cJSON` tree whose shape is generated from the parsed input (one `cJSON_Create*` call per node, reading the `CVal` slot that matches the original JSON type) and prints it with `cJSON_PrintUnformatted`.
- Add a COBOL JSON round-trip check to CI using the shared round-trip fixture, compiled and run with GnuCOBOL and re-emitting JSON via the standard `JSON GENERATE` statement.
  `JSON GENERATE` skips `FILLER` items (so the literalizer's `FILLER`-group arrays cannot be reconstructed), has no JSON boolean and no floating-point support, and mangles keys to COBOL data names, so the helper renames the recoverable top-level scalars back to their original keys with a `NAME OF` clause and excludes the array/object/boolean/float fields plus the integer-overflowing `biginteger` and the width-truncated `string_empty` / `string_unicode` values.
- Add a Fortran JSON round-trip check to CI using the shared round-trip fixture, and switch the Fortran language module to emit `real(real64)` literals (with the matching `freal` constructor signature in the `fval_m` preamble) so that double-precision values like `1.7976931348623157e+308` are no longer silently truncated to single precision.
- Add a MATLAB JSON round-trip check to CI using the shared round-trip fixture, serializing the literalized `myData` value with the built-in `jsonencode`; the 26-digit `biginteger` field is excluded because MATLAB's only numeric type is the IEEE 754 `double`, which re-emits it as `1e26`.
- Add a Mojo JSON round-trip check to CI using the shared round-trip fixture, run with `mojo run`.
  The shared input's mixed-type top-level object is literalized with the `VARIANT` heterogeneous strategy and re-emitted by copying each value out of its `Variant` slot into a CPython `dict` and calling `json.dumps` on it through Mojo's `std.python` bridge to CPython (Mojo has no JSON encoder of its own).
  The wide `biginteger` field (which overflows Mojo's 64-bit `Int`) and the array/object fields (which the `VARIANT` strategy cannot place alongside scalars in one dict) are excluded.
- Add a Nix JSON round-trip check to CI using the shared round-trip fixture, evaluating the literalized expression with `nix-instantiate --eval --strict --json` so that Nix's built-in JSON printer re-emits the value.
- Add a Norg JSON round-trip check to CI using the shared round-trip fixture.
  The literalizer stores the value inside a `@code json` ranged verbatim tag, so the check parses the generated document with the `tree-sitter-norg` grammar, pulls the embedded code block back out, and re-parses it with the standard library `json` module.
- Add a PowerShell JSON round-trip check to CI using the shared round-trip fixture, serializing the literalized `$myData` value with the built-in `ConvertTo-Json -Depth 100 -Compress`; the 26-digit `biginteger` field is excluded because PowerShell parses it as a `[double]` and re-emits it with a fractional part.
- Add a Scheme JSON round-trip check to CI using the shared round-trip fixture, driven by Guile 3 and the `guile-json` library.
- Add a SystemVerilog JSON round-trip check to CI using the shared round-trip fixture, built and run with `verilator --binary`.
  Because the literalizer's `_VVal` is a flat tagged record (it has no recursive component and no boolean tag), nested containers are serialized to opaque strings and booleans share the integer slot, so the helper generates the re-emitting walk from the parsed input's shape (one expression per top-level key, reading the `_VVal` slot that matches the original JSON type) and excludes the array/object fields, which cannot be walked back into at run time.
- Rewrite the C JSON round-trip CI check to literalize the shared fixture through `C(json_type=C.json_types.CJSON)` and print it with `cJSON_PrintUnformatted`, dropping the Python-side walker that previously built a parallel `cJSON` tree from the parsed input.
  The check still reports `C round-trip OK` with the same two excluded fields.
- Add `Cobol(json_type=CJSON)`, which renders a document as a `cJSON` node tree built through COBOL's C `CALL` interface (`cJSON_Create*` composed with `cJSON_AddItemTo*`) rather than a WORKING-STORAGE record, so arbitrary string keys, JSON booleans, real numbers, heterogeneous arrays, nested objects, and the empty string are all represented faithfully.
  The COBOL JSON round-trip now uses this mode with `cJSON_PrintUnformatted`, so it reproduces every field of the shared input except `biginteger` and `float_large_exponent`.

## 2026.05.28

- Add Ruby, TypeScript, Haskell, Perl, PHP, Go, Zig, C#, Scala, Swift, Kotlin, Rust, D, TOML, Elm, OCaml, YAML, Julia, R, and Groovy JSON round-trip checks to CI using the shared round-trip fixture.
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
- Replace the hand-rolled JSON encoder in the Java round-trip CI check with Jackson's `ObjectMapper`.
- The Kotlin JSON round-trip CI check now serializes via Jackson's `ObjectMapper` instead of a hand-rolled `toJsonElement` walker over heterogeneous `Any?` plus primitive-array types.
- Internal: rewrite the Kotlin and Zig JSON round-trip scripts on top of the `KOTLINX_JSON_ELEMENT` and `STD_JSON_VALUE` `json_type` strategies, dropping the bespoke `Any?`-to-`JsonElement` and `ZVal`-to-`std.json.Value` walkers.
  `std.json.Value.number_string` preserves the 26-digit `biginteger` field end-to-end on Zig, so that exclusion is dropped there; `kotlinx.serialization`'s `parseToJsonElement` still collapses it to a `Double`, so the Kotlin exclusion is retained.
- Add `Elm(json_type=Elm.json_types.JSON_ENCODE_VALUE)` to render values as idiomatic `elm/json` `Json.Encode.*` calls producing a `Json.Encode.Value` directly, replacing the per-fixture `Val` ADT.

## 2026.05.18

- Added support for Haxe as a new output language.
  `Haxe` renders every collection literal with an explicit `(... : Array<Dynamic>)` or `(... : Map<String, Dynamic>)` cast, so heterogeneous and empty collections type-check without per-variable annotations.
  Maps use Haxe's `["key" => value]` literal syntax and strings use the double-quoted form (no interpolation).
  Calls use positional syntax with local-function and anonymous-structure-closure stubs emitted inside `static function main()`.
  A new `lint-haxe` job in `.github/workflows/lint.yml` compiles and runs every `.hx` fixture in a single `haxe --interp` invocation.

## 2026.05.18.1

- Added two metadata properties to the `~literalizer.Language` protocol: `supports_multi_param_call_wrapper_stub` (whether the language can declare and positionally invoke a wrapper stub that receives the call's result alongside other positional arguments) and `supports_dict_literal_as_free_expression` (whether a map literal can appear as a free-standing expression rather than only on the right-hand side of a typed assignment).
  Both are test-harness metadata, like the existing `has_free_function_calls` and `supports_dotted_call_stub` properties; `~literalizer.literalize_call` does not inspect them.

## 2026.05.17

- `~literalizer.D` now accepts `variable_form` on `~literalizer.literalize_call` for both `~literalizer.NewVariable` and `~literalizer.ExistingVariable`.
  A D literal binding wraps the right-hand side to encode the parsed value's runtime type (a `JSONValue(...)` projection, or a positional `Record0(...)` struct-constructor literal under the `RECORD` strategy), which is wrong for a call whose return type is opaque to the renderer; the call result is now bound directly as `auto my_data = make_widget(...);`.
  No caller-supplied return-type hint is required: D infers the binding type from the initializer.
  Because the binding is an `auto` declaration while the `~literalizer.ExistingVariable` form is a bare assignment to an already-declared name, only the `~literalizer.NewVariable` form is golden-covered.
  Its `supports_call_variable_binding` language-class flag is now `True`; existing literal-binding and call-without-binding output is unchanged.
  Follow-up to \#1961.
  See \#2511.
- `~literalizer.SystemVerilog` now accepts `variable_form` on `~literalizer.literalize_call` for both `~literalizer.NewVariable` and `~literalizer.ExistingVariable`.
  A SystemVerilog literal binding wraps the right-hand side in a named `_VVal` struct literal derived from the parsed value's runtime type, which is wrong for a call whose return type is opaque to the renderer; the call result is now bound directly as `static _VVal my_data = make_widget(...);`.
  SystemVerilog declarations are typed and have no inference, so the binding needs an explicit declared type; no caller-supplied return-type hint is required because every generated value-returning call stub returns the universal tagged `_VVal` struct, so the binding's declared type is always `_VVal` (the same type a SystemVerilog scalar literal binding declares).
  The call stub is emitted at module scope rather than inside `initial begin`, where a `function` declaration is illegal.
  Because the binding is a typed declaration while the
- `~literalizer.Zig` now accepts `variable_form` on `~literalizer.literalize_call` for both `~literalizer.NewVariable` and `~literalizer.ExistingVariable`.
  A Zig literal binding wraps the right-hand side in a designated-initializer struct literal that encodes the value's runtime type (a tagged `ZVal` union projection, or a generated `Record0` struct literal under the `RECORD` strategy) and declares an explicit `ZVal` value type, which is wrong for a call whose return type is opaque to the renderer; the call result is now bound with a plain inferred declaration, `const my_data = make_widget(...);`.
  No caller-supplied return-type hint is required: the Zig `const`/`var` type inference supplies the binding's type.
  Because the binding is a keyword declaration while the `~literalizer.ExistingVariable` form is a bare assignment to an already-declared name, only the `~literalizer.NewVariable` form is golden-covered.
  Its `supports_call_variable_binding` language-class flag is now `True`; existing literal-binding and call-without-binding output is unchanged.
  Follow-up to \#1961.
  See \#2510.
- `~literalizer.Ada` now accepts `variable_form` on `~literalizer.literalize_call` for both `~literalizer.NewVariable` and `~literalizer.ExistingVariable`.
  An Ada literal binding wraps the right-hand side in the `A_Val` constructor chosen from the parsed literal's runtime type, which is wrong for a call whose return type is opaque to the renderer; the call result is now bound directly as `my_data : A_Val := Make_Widget (...);`.
  No caller-supplied return-type hint is required: every generated Ada call stub returns `A_Val`, so the binding's declared type is always `A_Val` (the same type an Ada literal binding declares).
  Because the binding is a typed declaration while the `~literalizer.ExistingVariable` form is a bare assignment to an already-declared name, only the `~literalizer.NewVariable` form is golden-covered.
  Its `supports_call_variable_binding` language-class flag is now `True`; existing literal-binding and call-without-binding output is unchanged.
  Follow-up to \#1961.
  See \#2509.
- `~literalizer.Fortran` now accepts `variable_form` on `~literalizer.literalize_call` for both `~literalizer.NewVariable` and `~literalizer.ExistingVariable`.
  A Fortran literal binding wraps the right-hand side in the `fval_t` constructor matching the parsed literal's type (the integer, real, or string constructor), which is wrong for a call whose return type is opaque to the renderer; the call result is now bound directly as `type(fval_t) :: my_data` followed by `my_data = make_widget(...)`.
  No caller-supplied return-type hint is required: every generated Fortran call stub returns `type(fval_t)`, so the binding's declared type is always `type(fval_t)` (the same type a Fortran literal binding declares).
  The call stub is emitted in the program's `contains` section, after the binding, so a value-returning call no longer needs an inline procedure body.
  Because the `~literalizer.NewVariable` binding is a typed declaration while the `~literalizer.ExistingVariable` form is a bare assignment to an already-declared name, only the `~literalizer.NewVariable` form is golden-covered.
  Its `supports_call_variable_binding` language-class flag is now `True`; existing literal-binding and call-without-binding output is unchanged.
  Follow-up to \#1961.
  See \#2507.
  \#2508.
- `~literalizer.C` now accepts `variable_form` on `~literalizer.literalize_call` for both `~literalizer.NewVariable` and `~literalizer.ExistingVariable`.
  A C literal binding wraps the right-hand side in a designated-initializer compound literal that encodes the value's runtime type (a tagged-union projection, or a `struct Record0 my_data = (struct Record0){...};` aggregate under the `RECORD` strategy), which is wrong for a call whose return type is opaque to the renderer; the call result is now bound directly as `CVal my_data = make_widget(...);`.
  No caller-supplied return-type hint is required: every generated call stub returns the universal tagged `CVal` union, so the binding's declared type is always `CVal` (the same type a C literal binding declares).
  Because the binding is a typed declaration while the `~literalizer.ExistingVariable` form is a bare assignment to an already-declared name, only the `~literalizer.NewVariable` form is golden-covered.
  Its `supports_call_variable_binding` language-class flag is now `True`; existing literal-binding and call-without-binding output is unchanged.
  Follow-up to \#1961.
  See \#2506.
- `~literalizer.Nim` now accepts `variable_form` on `~literalizer.literalize_call`, binding the call result directly: `var my_data = make_widget(42)`.
  The literal-binding declaration template prefixes the right-hand side with the `%*` json macro (or `@` for sequences) chosen from the parsed literal's type, which JSON-constructs a literal rather than invoking a call; the new call-specific declaration and assignment templates drop that wrapping regardless of the source data type.
  Its `supports_call_variable_binding` language-class flag is now `True`; existing literal-binding and call-without-binding output is unchanged.
  Only the `~literalizer.NewVariable` form emits a golden because the `~literalizer.ExistingVariable` bare assignment (`my_data = make_widget(42)`) to an undeclared name is not self-contained.
  Follow-up to \#1961.
  See \#2455.
- `~literalizer.Crystal` gains the `RECORD` `heterogeneous_strategy` (already on `~literalizer.Rust`, `~literalizer.Go`, `~literalizer.Kotlin`, `~literalizer.Scala`, `~literalizer.Java`, `~literalizer.Cpp` and `~literalizer.Python`).
  Each record-shaped dict (non-empty, string-keyed) becomes a generated `record` struct declared in the per-fixture module body plus a matching positional `Record0.new(value, ...)` literal, so a record-shaped dict that mixes scalars with a container is representable even though `Hash` requires a homogeneous value type.
  Field names are the dict keys verbatim, an integer field is sized to match its rendered literal (`Int32` / `Int64` / the `_i128`-suffixed `Int128`), and the struct-name prefix is configurable via the new `record_struct_name_prefix` constructor parameter; its `supports_record_struct_name_prefix` language-class flag is now `True`.
  The default (`ERROR`) strategy still raises for such a dict.
  See \#2420.

## 2026.05.16

- Internal: the `RECORD` `heterogeneous_strategy` no longer threads the already-formatted field literal into the field-type hook.
  `~literalizer.Kotlin` now derives each generated `data class` field's declared type structurally from the raw value through its own collection openers and scalar mapping (matching the Go/Java/Scala ports), and the `formatted` string is dropped from the renderer contract.
  No generated output changes.
  See \#2305.

## 2026.05.15.1

- `~literalizer.Java` now offers `VersionFormats.JDK_16` alongside `VersionFormats.JDK_11` (still the default), selected via `language_version`.
  Generated code is currently identical for both targets; the member exists so a future Java `RECORD` `heterogeneous_strategy` (whose `record` declarations require Java 16) can gate on it.
  The golden harness emits a parallel `@jdk_16` fixture set.
  See \#2313.

## 2026.05.15

- `~literalizer.literalize` now accepts an opt-in `bound_refs` mapping.
  Unlike `ref_values` (which only informs a ref's type and leaves it as a free external identifier), each name in `bound_refs` additionally has a binding emitted for it before its first use, so a single `literalize(..., bound_refs=..., wrap_in_file=True)` call produces a complete, valid file with per-language declaration sequencing (Nix nested `let`, the Fortran rule that specification statements precede executable statements, and so on).
  Binding emission only happens with `wrap_in_file=True` and a `~literalizer.NewVariable` or `~literalizer.ExistingVariable` `variable_form`; otherwise `bound_refs` degrades to type information only, exactly like `ref_values`.
  The default behavior is unchanged.
  Without `bound_refs`, a `$ref` is a free external identifier.
  The ref golden-file harness now drives every case through one `literalize` call, retiring its regex-based stub-stitching helpers.
  See \#2294.
- `~literalizer.Fortran` now offers `VersionFormats.V2003` alongside `VersionFormats.V2008` (the default).
  The 2003 target defines the `int64` kind via `selected_int_kind(18)` instead of importing it from the intrinsic `iso_fortran_env` module (whose `int64` constant is a Fortran 2008 addition), so generated code is otherwise identical and the `_int64` literal suffix is unchanged.
  The golden harness emits a parallel `@v2003` / `@v2008` fixture set and CI lints each with the matching `gfortran -std=f2003` / `-std=f2008` flag.
  See \#1931.
- The integration golden-file harness now accepts `input.toml` next to the existing `input.yaml` for cases whose input contains a value YAML 1.2 cannot natively express (currently `datetime.time`).
  New `time_list`, `time_dict`, and `times_heterogeneous_with_dates` golden cases give every supported language end-to-end coverage of `datetime.time` rendering, which surfaced and fixed several preexisting bugs in time emission: tagged-union languages (`~literalizer.Elm`, `~literalizer.OCaml`, `~literalizer.Roc`, `~literalizer.Gleam`, `~literalizer.Haskell`, `~literalizer.Zig`, `~literalizer.Sml`, `~literalizer.Ada`, `~literalizer.Fortran`, `~literalizer.ObjectiveC`) now wrap a fallback ISO 8601 time inside the value-type constructor the same way they wrap other scalars; collection type inference (C++, C#, Java, Kotlin, Scala, Dart, Go, Visual Basic, and others) now knows about `datetime.time` and narrows homogeneous collections to the correct element type; and `~literalizer.FSharp` fully qualifies `System.TimeOnly` so the rendered output no longer emits an `open System` line before `module`.
  See \#2230.
- Golden files for languages whose compiler version is pinned (Elixir, Erlang, Gleam, Kotlin, Odin, Zig) now carry the version in the filename: `{stem}@{version}{extension}` (e.g. `Odin@dev-2026-04.odin`).
  Every fixture is explicitly tied to the compiler version it was generated against.
  Each `lint.yml` job sets a job-scoped environment variable once and feeds it to both the install action and `python -m tests.integration.list_fixtures`; the test code auto-discovers the same version from sibling filenames so no separate registry file is needed.
- `lint-fast` CI job now syntax-checks and runs the Python fixtures under `tests/integration/cases`, matching the per-language gate already in place for Bash, Ruby, JavaScript, and other fixture languages.
  See \#1921.
- `lint-odin` CI job now uses `odin run .` again to catch runtime errors that `odin build .` cannot detect (e.g. nil-proc calls).
  The `laytan/setup-odin` action is pinned to `dev-2026-04`, the last Odin release where `odin run .` did not segfault on these fixtures; `release: latest` (`dev-2026-05`) crashes at runtime, and the compiler itself segfaults on some fixtures under `odin build .`.
  See \#1745.

## 2026.05.14

- The internal `~literalizer._types.Value` and `~literalizer._types.ValueInput` aliases now permit any `~literalizer._types.Scalar` as a dict key, in preparation for surface formats that admit non-string dict keys.
  A new `~literalizer.exceptions.UnrepresentableInputError` and a `supports_non_string_dict_keys` class attribute on `~literalizer.Language` (defaulting to `True`; overridden to `False` on `~literalizer.Json5`, `~literalizer.Jsonnet`, and `~literalizer.Toml`) wire a centralized guard at the dict-formatting boundary.
  The surface parsers still produce only string-keyed dicts, so behavior is unchanged.

## 2026.05.13

- The `supports_commented_dict_call_args` flag has been removed from `Language`.
  Every (language, shape) pair previously dropped by the test-discovery filter on this flag is either already short-circuited by an earlier exception path or now renders cleanly, leaving the flag with no load-bearing callers.
- The PureScript, Roc, and Elm wrapped-call indent helpers no longer carry defensive branches for blank or whitespace-leading lines.
  These helpers only ever receive single-line call expressions from `literalize_call` (which uses `CollectionLayout.COMPACT` for wrapped calls and rejects standalone comments in that path), so the empty-line and continuation arms were unreachable via the golden integration cases.
  Four unit tests in `tests/test_languages.py` that drove the Elm helpers directly with constructed multi-line input have been removed in favor of the existing golden-file contract.
- `Mojo` `~literalizer.literalize_call` now supports refs nested inside dict literals and commented dict-literal call arguments.
  The typed-stub changes merged in \#1972 made both shapes compile cleanly under `mojo run --Werror`, so the corresponding `supports_call_refs_in_dict_literals` and `supports_commented_dict_call_args` flags flip to `True` for Mojo and two new `call_*` golden cases are exercised.
- `supports_variable_names` is now `True` on `Clojure`, `CommonLisp`, `Julia`, `Racket`, `Ruby`, and `Scheme`, reflecting that these languages do support named variable wrapping via `literalize`'s `variable_form` argument (and have golden files exercising that behavior).

## 2026.04.29

- Added support for Roc as a new output language.
  `Roc` emits a `Val` tag-union type alias (`RNull`, `RBool`, `RInt`, `RFloat`, `RStr`, `RList`, `RDict`, `RSet`) inside the module body, exposing the generated value via `module [my_data]`.
  Calls use the space-separated command syntax with each argument wrapped in parentheses (`process (RInt 1) (RInt 2)`), with module-level stubs of the form `name : a, b -> {}`.
  A new `lint-roc` job in `.github/workflows/lint.yml` runs `roc check` against every `.roc` fixture using the upstream nightly tarball.
- C, C++, Objective-C, and D fixtures now emit a `main` entry point directly (`int main(void)`/`int main()`/`void main()`) instead of a `check_()`/`_check()` function that required a separate per-language driver script.
  Haskell non-call fixtures now append `main = seq my_data (return ())` to the module, and SML fixtures are emitted as top-level declarations ending with `val _ = my_data` instead of inside a `structure Check = struct … end` wrapper.
  All six driver scripts (`c_main.c`, `cpp_main.cpp`, `objc_main.m`, `d_main.d`, `sml_force.sml`, `sml_main.mlb`, `sml_call_main.mlb`) have been removed.
  CI now compiles and runs each fixture directly without a linking step against a driver object.
  `run_haskell.py` has been removed; the CI now copies each Haskell fixture to a temporary workspace (renaming to match its unique module name), generates a `Main.hs` driver that imports every fixture qualified and calls its `main`, and compiles and runs them all in a single `ghc` invocation.
- Ada output now uses Ada 2022 container aggregates (`AList'[...]`, `AMap'[...]`, `ASet'[...]`) and emits a `with A_Stub; use A_Stub;` context clause so each fixture compiles and runs against a checked-in stub package.
  The lint workflow gained a "Run Ada files" step that builds and executes every fixture, replacing the previous syntax-only check.
  The combined declaration + assignment wrapper now keeps both forms in a single procedure scope so the assignment can reach `my_data`.
- `Jsonnet` now emits `$ref` declarations as top-level `local` bindings before the call expressions, so call-mode output with `ref_declarations` is supported.
  Previously the integration harness skipped `Jsonnet` for ref-declaration cases because the array-wrapped output had no place for variable bindings.
  The `DeclarationStyles.ASSIGN` template changed from `{value}` to `local {name} = {value};`, and `Jsonnet` now overrides `wrap_calls_with_declarations` to emit those bindings before `wrap_in_file` wraps the calls in `[ … ]`.
- C single-name call stubs (e.g. `emit`, `process`) are now emitted as `static` definitions with a stub body instead of bare forward declarations, so generated fixtures can be linked and run.
  The lint workflow now compiles each C fixture against a small `c_main.c` driver and executes the resulting binary, surfacing runtime errors that the previous `-fsyntax-only` check missed.
- `CommonLisp` now wraps `{"$ref": "name"}` identifiers in earmuffs (`*name*`) at the call site so they resolve to the matching `defparameter` declaration.
  `CommonLisp` is no longer skipped by the `literalize_call` reference-argument integration tests, which now lint cleanly under SBCL.
- `Perl` `literalize_call` output now emits Perl's scalar `$` sigil before each `{"$ref": "name"}` identifier via a `format_call_ref_identifier` override, so a ref to `my_var` renders as `$my_var` at the call site and lines up with the `my $my_var = ...` declaration site.
  Generated files now pass `perl -c` under `use strict` and `Perl` is no longer excluded from the integration suite's ref-declaration golden cases.
- `lint-purescript` in `.github/workflows/lint.yml` now runs each PureScript fixture end-to-end.
  A new `Run PureScript files` step compiles each fixture with `purs compile` and loads the resulting `Check` module in Node so its top-level `my_data` binding is evaluated, catching foreign-implementation failures and other load-time crashes that the existing `check_purescript_syntax.py` compile-only check would miss.
  The shared Prelude stub used by both steps lives in a new `purescript_common.py` module.
- Added a `benchmarks` job to `.github/workflows/ci.yml` that runs the `tests/benchmarks/` suite under [CodSpeed](https://codspeed.io) via `pytest-codspeed`.
  The job posts a per-benchmark performance delta on every pull request, making it easier to spot regressions in the YAML fast path, JSON formatting, and heterogeneous-widening logic.

## 2026.04.24.1

- `lint-lua` in `.github/workflows/lint.yml` now runs each Lua fixture end-to-end via `lua`, catching runtime errors (calls to undefined functions, missing module imports, failed assertions) that the existing `luac -p` parse-only step let through, mirroring `lint-bash` / `lint-javascript` / `lint-perl` etc.

## 2026.04.24

- `lint-erlang` in `.github/workflows/lint.yml` now passes `-Werror` to `erlc`, so warnings such as `evaluation of operator '-'/1 will fail with a 'badarith' exception` fail the job instead of being silently logged.
  `Erlang` generated output for negative infinity is now the quoted atom `'-inf'` instead of the bare `-inf`, which the compiler treated as unary negation of the atom `inf` and flagged as a guaranteed runtime `badarith`.

## 2026.04.23

- `lint-haskell` in `.github/workflows/lint.yml` now passes `-Wall -Werror` to both the syntax check and the end-to-end build, so warnings such as `-Wunused-matches`, `-Woverlapping-patterns`, and `-Wtype-defaults` fail the job instead of being silently logged.
  `Haskell` generated output was updated to compile clean under `-Wall`: the `Num` / `Fractional` instances use `_` for unused parameters, the catch-all `negate _` clause is now omitted when `Val` has only numeric constructors, tuple-sequence bindings carry a `(Val, Val, ...)` annotation, call stubs get explicit type signatures, transform-wrapper stubs use a polymorphic argument type, `main` binds each call result with `_ <-`, and the `Data.Time` import set drops `secondsToDiffTime` when every datetime has microseconds.
- `lint-objectivec` in `.github/workflows/lint.yml` now passes `-Werror` to both `clang -fsyntax-only` and the end-to-end `clang` compile step so warnings such as `-Wimplicitly-unsigned-literal` fail the job instead of being silently logged.
  `ObjectiveC.format_integer` now appends a `ULL` suffix to values above `LLONG_MAX` (matching the C fallback) and raises `UnrepresentableIntegerError` for values below `LLONG_MIN`, so emitted fixtures compile cleanly under the stricter workflow.
- The `heterogeneous_strategy` variant case list now includes the `ordered_map` fixture, covering Rust `TAGGED_ENUM` and Dhall `UNION_TYPE` rendering on `!!omap` inputs.
- `lint-swift` in `.github/workflows/lint.yml` now runs its `swiftc -typecheck` step in parallel via `xargs -P`, replacing the previous serial `while` loop so the job no longer cold-starts the compiler one fixture at a time.
- `lint-swift` in `.github/workflows/lint.yml` now runs each Swift fixture end-to-end via `swift` in script mode, catching runtime errors that `swiftc -typecheck` alone could miss (for example, integer literals that overflow `Int`).
  So that every emitted fixture compiles, `Swift.format_integer` now raises `UnrepresentableIntegerError` for values outside the signed 64-bit range, matching the behavior of other languages without native arbitrary-precision integer support.
- `lint-groovy` in `.github/workflows/lint.yml` now runs each Groovy fixture end-to-end, catching runtime errors (calls to undefined functions, missing module imports, failed assertions) that the existing `groovyc` compile-only step let through.
  `Groovy.format_call_stub` now emits a single `Map _args` method parameter when `call_style` is `KEYWORD`.
  Previously the `call_keyword_args` fixture tripped `MissingMethodException` because Groovy passes named arguments as a single `LinkedHashMap` that a positional parameter list rejects.
  `POSITIONAL` stubs keep the concrete parameter list unchanged.
- `lint-objectivec` now executes each fixture end-to-end instead of only syntax-checking it, mirroring `lint-bash` / `lint-javascript` / `lint-perl` etc. To make this possible, Objective-C declarations and reassignments now box primitive scalars the same way collection entries do (`id x = 42;` → `id x = @(42);`), single-name call stubs emit a `static` definition so fixtures link, and `ObjectiveC.supports_scalar_inline_comments` is now `False`.
  Previously the trailing `//` comment swallowed the statement terminator.
  A pre-existing casing bug in the workflow's `lang_patterns` (`objective_c*.m` instead of `ObjectiveC*.m`) that silently skipped every fixture is also fixed.
- `lint-elm` in `.github/workflows/lint.yml` now runs each Elm fixture end-to-end.
  A new `Run Elm files` step compiles each fixture alongside a small `Main.elm` wrapper whose `Platform.worker` init forces `Check.my_data`, emits JavaScript via `elm make`, and executes it with Node so runtime crashes such as `Debug.todo` surface in CI.
  The `scalar_int_very_negative_large` fixture is skipped because the Elm 0.19.1 code generator emits `--<digits>` (two unary minuses) for integers at the int64 boundary, which JavaScript rejects as a prefix-decrement syntax error.
- `lint-sml` in `.github/workflows/lint.yml` now runs each Standard ML fixture end-to-end.
  Because `MLton` never evaluates a `structure`'s body unless a top-level expression forces it, the new step compiles each fixture via an ML Basis file that concatenates the fixture with a small `val _ = Check.my_data` snippet and runs the resulting binary, catching runtime errors such as references to undefined names, missing module imports, or failed assertions.
- Removed the K&R-style empty-prototype suppression directives from C and Objective-C call stubs.
  `C.format_call_preamble_stub` and `ObjectiveC.format_call_preamble_stub` now emit concrete prototypes (`CVal` parameters for C, `id` parameters for Objective-C) sized to the call's parameter list, and an internal `format_call_arg` hook wraps each call argument so the call site matches the prototype.
  Generated C and Objective-C call code now compiles cleanly under `-Wstrict-prototypes -Wdeprecated-non-prototype -Werror` without suppression.

## 2026.04.21.3

- The `lint-julia` CI job now executes Julia golden files instead of only parsing them, catching `UndefVarError` and other runtime errors.
- Lint workflow now runs pre-commit hooks against the full supported Python matrix (3.12, 3.13, 3.14) instead of 3.13 only, to catch version-specific lint issues.
