# Golden selection migration audit

This is the November 15, 2026 completion audit for [#5813](https://github.com/adamtheturtle/literalizer/issues/5813).
It records historical regression destinations, rather than defining another discovery or selection system.
Future coverage belongs in the existing manifests and harness.

The audited merged tree is `5e443e29412db78b5645c6f4a81161e235327bfc`.
Historical manifests and golden filenames come from `93aaeb5f2763feed249447f565a473fe308c8658`; the eighteen additional Rust lexical cases come from `312d7f85ab`, which introduced them.
The fix accompanying this audit removes `language_id` from the shared gate registry.
It changes no generated fixture, native runner or coverage threshold.

The ten remaining slices contain 465 historical entries, representing 443 distinct original manifests.
Their 1084 original golden filenames have retained language/version and option witnesses.
The two malformed-target cases had no success goldens and retain deterministic rejection coverage.
Current destinations comprise 312 shared manifests plus the existing malformed-target rejection manifest.
Counts by issue overlap and must not be added as independent coverage.

The frozen current tree contains 1,117 case manifests and 120,695 case-owned versioned goldens.
No case manifest has a root, reference or call `languages` selector, and no axis selects `language_id`.
Legacy selection fields remain rejected by strict manifest validation.
Seven additional regressions reject the previously accepted metadata selection route in roots, references, calls, reference/call examples and axes, including metadata-derived overrides.

## Verification method

The audit compared every historical input's format and bytes, explicit call/reference context, option-labelled golden filenames and supported version tags with its destination.
Explicit settings were compared with both the destination base context and its named examples.
A similar name or identical scalar input alone is not a coverage witness.
The destination tables include the exact regression owner, rather than unrelated manifests with coincidentally identical inputs.

Input bytes and format are unchanged except for three reviewed changes: `literalize_ref_both_forms` consistently renames the bound reference `shared` to `shared_values`; `cpp_empty_sequence_record_mixture` changes only JSON whitespace; `roc_native_record_special_floats` retains positive infinity, negative infinity and NaN and adds a finite `1.5` field.
Native date and datetime values in the record-ownership context remain typed TOML values.

Explicit call/reference settings are retained.
The following representation changes require semantic reconciliation rather than a raw table comparison:

- Grouped comments now use `call_transform_group` with the same body, inner comment and trailing suffix.
  Raw-prefix calls use `call_transform_arguments` with the original literal and suffix.
  The opaque zipped callback uses `call_transform_wrapper`, retaining its `emit` target, call/zipped arguments and zip-usage policy.
- Rust and Zig JSON reference overrides now come from `json_type` and `json_type_declaration_cross` variants.
  The original serde/std JSON modes, mutable declarations, new/both forms, indentation, bound values and repeated uses remain covered.
  The mutable commented Zig reference uses the declaration-style axis.
  Rust owned-root reuse keeps its default `LET_MUT` redefinition style.
- Rust array reuse keeps `ARRAY`, `default_sequence_element_type = "String"` and the original bound `[]` value in `literalize_ref_typed_empty_array_reuse`.
  Populated and nested empty-array witnesses are separate scenarios.

## Golden label reconciliation

Most original option/version filenames remain present verbatim.
The following changes preserve their effective configurations:

- Lexical call and reference examples add their example identity to the golden filename.
  Each original example retains its exact source transform or reference configuration, including C# interpolation/verbatim nesting, Dart raw/triple strings, Haxe regexes, SystemVerilog macros, Rust raw/byte-raw delimiters, character escapes, lifetimes and raw identifiers.
  Grammar capabilities select participation; failures do not remove a participant.
- Rust repeated tagged/array/hybrid references and V null-interface references use named reference examples.
  Their `TAGGED_ENUM`, `ARRAY`, `TUPLE_NESTED_VEC` and `INTERFACE` settings remain explicit.
- The four C++ `Cpp_tuple` families use `Cpp_heterogeneous_strategy_tuple_nested` at all three original C++ versions.
  Crystal `record_keyword_field` is now `record_keyword_fields`, retaining the keyword-field record recipe.
- The allocator collision keeps its named base fixture.
  Its historical Zig combined fixture used `my_data`, not `allocator`, and is byte-identical to the existing `default_helper_name_arena/Zig_combined@v0_12.zig` and `caller_name_std/Zig_combined@v0_12.zig`; that shared combined behavior remains owned and executed.
- Python pre-indented multiline `.txt` fragments are now complete `.py` consumers for both original Python versions.
  The unwrapped generated assignment remains inside a native caller scope, which asserts the complete original multiline string at runtime.
  Other native multiline consumers retain their compiler/runtime assertions.

## Rejections, execution and ownership

`call_target_empty` and `call_target_empty_segment` resolve to [`invalid_call_target`](../errors/rejections/invalid_call_target/rejection.toml), with independent `InvalidCallTargetError` expectations for empty and malformed dotted components.
Reserved-word cases retain independently declared success/rejection behavior and compiling successes where their target syntax is valid.

The ordinary suite checks the complete current golden matrix, rejection expectations, version/axis expansion and orphan ownership. Existing native CI jobs continue to compile or execute the owned programs. Python multiline consumers execute locally; the native multiline consumers compare the complete string value. Compiler/runtime validation and the 100% line/branch coverage policy remain required.
Hosted status must be read from the pull request head; this inventory is not itself a claim that a pending native job passed.

The retired request-alias and CI-cost proposals are outside this completion gate.
This audit introduces no aliases, duplicate-request accounting or timing framework.

Local validation on the resulting code passed 38,475 tests and 123,285 subtests, with 12,450 expected skips and 100% source/test line and branch coverage, including rejection and orphan checks. All seven new validation cases pass; restoring the removed registry entry makes all seven fail. Six additional native controls passed: complete multiline-string runtime comparisons under C++14/17/20, and Rust 2021 compilation/execution for typed empty-array reuse, an escaped-character binding and a raw-prefix existing binding.

## Historical destinations

Each table groups original manifests by their current canonical owner.
The issue inventories overlap intentionally, especially the 53 call/comment entries in #5814.

### Issue #5795

98 original entries; 114 original golden filenames.

| Current owner | Original regressions |
| --- | --- |
| [call_binding_existing_comment_inline_declaration_variants](cases/call_binding_existing_comment_inline_declaration_variants/case.toml) | `call_shared_comments_haxe_existing_comment_0_existing` |
| [call_binding_grouped_inner_comment](cases/call_binding_grouped_inner_comment/case.toml) | `call_binding_inner_comment_csharp`, `call_binding_inner_comment_dart`, `call_binding_inner_comment_haxe` |
| [call_binding_inline_comment_scalar](cases/call_binding_inline_comment_scalar/case.toml) | `call_shared_comments_csharp_existing_comment_0_new`, `call_shared_comments_dart_existing_comment_0_new`, `call_shared_comments_haxe_existing_comment_0_new` |
| [call_binding_inline_line_comment](cases/call_binding_inline_line_comment/case.toml) | `call_binding_inline_comment_csharp`, `call_binding_inline_comment_dart`, `call_binding_inline_comment_haxe` |
| [call_binding_multiple_comments_scalar](cases/call_binding_multiple_comments_scalar/case.toml) | `call_shared_comments_csharp_existing_comment_2_new`, `call_shared_comments_dart_existing_comment_2_new`, `call_shared_comments_haxe_existing_comment_2_new` |
| [call_binding_next_line_comment_scalar](cases/call_binding_next_line_comment_scalar/case.toml) | `call_shared_comments_csharp_existing_comment_1_new`, `call_shared_comments_dart_existing_comment_1_new`, `call_shared_comments_haxe_existing_comment_1_new` |
| [call_binding_next_line_line_comment](cases/call_binding_next_line_line_comment/case.toml) | `java_call_binding_trailing_comment_csharp`, `java_call_binding_trailing_comment_dart`, `java_call_binding_trailing_comment_haxe` |
| [call_binding_quoted_line_comment_marker](cases/call_binding_quoted_line_comment_marker/case.toml) | `call_binding_quoted_comment_marker_csharp`, `call_binding_quoted_comment_marker_dart`, `call_binding_quoted_comment_marker_haxe` |
| [call_binding_raw_prefix_trailing_comment_existing](cases/call_binding_raw_prefix_trailing_comment_existing/case.toml) | `call_binding_rust_raw_no_hashes_existing` |
| [call_binding_raw_prefix_trailing_comment_new](cases/call_binding_raw_prefix_trailing_comment_new/case.toml) | `call_binding_rust_raw_no_hashes_new` |
| [call_bound_literal_followup_existing](cases/call_bound_literal_followup_existing/case.toml) | `call_binding_rust_byte_raw_hashes_existing`, `call_binding_rust_character_escape_existing`, `call_binding_rust_character_hex_existing`, `call_binding_rust_character_quote_existing`, `call_binding_rust_character_unicode_existing`, `call_binding_rust_lifetime_existing`, `call_binding_rust_raw_hashes_existing`, `call_binding_rust_raw_identifier_existing` |
| [call_bound_literal_followup_new](cases/call_bound_literal_followup_new/case.toml) | `call_binding_rust_byte_raw_hashes_new`, `call_binding_rust_character_escape_new`, `call_binding_rust_character_hex_new`, `call_binding_rust_character_quote_new`, `call_binding_rust_character_unicode_new`, `call_binding_rust_lifetime_new`, `call_binding_rust_raw_hashes_new`, `call_binding_rust_raw_identifier_new` |
| [call_scalar_result_json_binding](cases/call_scalar_result_json_binding/case.toml) | `call_csharp_conditional_interpolation_binding`, `call_csharp_format_interpolation_binding`, `call_csharp_nested_interpolation_binding`, `call_csharp_verbatim_binding`, `call_csharp_verbatim_quotes_binding`, `call_dart_map_interpolation_binding`, `call_dart_nested_interpolation_binding`, `call_dart_raw_double_binding`, `call_dart_raw_interpolation_binding`, `call_dart_raw_single_binding`, `call_dart_raw_triple_double_binding`, `call_dart_raw_triple_single_binding`, `call_haxe_double_literal_binding`, `call_haxe_nested_interpolation_binding`, `call_shared_comments_csharp_conditional_comment_new`, `call_shared_comments_csharp_conditional_plain_new`, `call_shared_comments_csharp_escaped_braces_comment_new`, `call_shared_comments_csharp_escaped_braces_plain_new`, `call_shared_comments_csharp_interpolated_verbatim_comment_new`, `call_shared_comments_csharp_interpolated_verbatim_plain_new`, `call_shared_comments_csharp_nested_format_comment_new`, `call_shared_comments_csharp_nested_format_plain_new`, `call_shared_comments_csharp_verbatim_comment_new`, `call_shared_comments_csharp_verbatim_interpolated_comment_new`, `call_shared_comments_csharp_verbatim_interpolated_plain_new`, `call_shared_comments_csharp_verbatim_plain_new`, `call_shared_comments_csharp_verbatim_quotes_comment_new`, `call_shared_comments_csharp_verbatim_quotes_plain_new`, `call_shared_comments_dart_escaped_quotes_comment_new`, `call_shared_comments_dart_escaped_quotes_plain_new`, `call_shared_comments_dart_interpolation_comments_new`, `call_shared_comments_dart_map_comment_new`, `call_shared_comments_dart_map_plain_new`, `call_shared_comments_dart_nested_comment_new`, `call_shared_comments_dart_nested_plain_new`, `call_shared_comments_dart_nested_raw_comment_new`, `call_shared_comments_dart_nested_raw_plain_new`, `call_shared_comments_dart_raw_double_comment_new`, `call_shared_comments_dart_raw_double_plain_new`, `call_shared_comments_dart_raw_single_comment_new`, `call_shared_comments_dart_raw_single_plain_new`, `call_shared_comments_dart_raw_triple_double_comment_new`, `call_shared_comments_dart_raw_triple_double_plain_new`, `call_shared_comments_dart_raw_triple_single_comment_new`, `call_shared_comments_dart_raw_triple_single_plain_new`, `call_shared_comments_dart_triple_interpolation_comment_new`, `call_shared_comments_dart_triple_interpolation_plain_new`, `call_shared_comments_haxe_double_literal_comment_new`, `call_shared_comments_haxe_double_literal_plain_new`, `call_shared_comments_haxe_existing_regex_comment_new`, `call_shared_comments_haxe_existing_regex_plain_new`, `call_shared_comments_haxe_interpolation_comment_new`, `call_shared_comments_haxe_interpolation_plain_new` |
| [call_scalar_result_yaml_binding](cases/call_scalar_result_yaml_binding/case.toml) | `call_haxe_regex_binding`, `call_haxe_regex_binding_comment`, `call_sv_macro_binding_comment` |
| [call_seeded_integer_result_binding](cases/call_seeded_integer_result_binding/case.toml) | `call_shared_comments_haxe_existing_regex_comment_existing` |
| [call_seeded_nullable_result_binding](cases/call_seeded_nullable_result_binding/case.toml) | `call_shared_comments_csharp_nested_format_comment_existing` |

### Issue #5796

37 original entries; 50 original golden filenames.

| Current owner | Original regressions |
| --- | --- |
| [invalid_call_target](../errors/rejections/invalid_call_target/rejection.toml) | `call_target_empty`, `call_target_empty_segment` |
| [call_capitalized_root](cases/call_capitalized_root/case.toml) | `call_elixir_alias_call_root` |
| [call_dotted_package_symbol_tail](cases/call_dotted_package_symbol_tail/case.toml) | `call_dotted_package_symbol_tail` |
| [call_dotted_parameter_matches_root](cases/call_dotted_parameter_matches_root/case.toml) | `call_dotted_parameter_matches_root` |
| [call_ignored_parameter_collision](cases/call_ignored_parameter_collision/case.toml) | `call_elixir_ignored_parameter_collision` |
| [call_ignored_reserved_parameter](cases/call_ignored_reserved_parameter/case.toml) | `cobol_call_ignored_reserved_parameter` |
| [call_keyword_case_bare_target](cases/call_keyword_case_bare_target/case.toml) | `systemverilog_keyword_case_bare_target` |
| [call_keyword_case_dotted_member](cases/call_keyword_case_dotted_member/case.toml) | `systemverilog_keyword_case_dotted_member` |
| [call_keyword_case_parameter](cases/call_keyword_case_parameter/case.toml) | `systemverilog_keyword_case_parameter` |
| [call_keyword_prefix_member](cases/call_keyword_prefix_member/case.toml) | `call_scala_keyword_prefix_member` |
| [call_object_proto_parameter](cases/call_object_proto_parameter/case.toml) | `call_object_proto_parameter` |
| [call_parameter_bare_underscore](cases/call_parameter_bare_underscore/case.toml) | `call_parameter_bare_underscore` |
| [call_parameter_case_sensitive](cases/call_parameter_case_sensitive/case.toml) | `call_parameter_case_sensitive` |
| [call_parameter_contextual_keyword](cases/call_parameter_contextual_keyword/case.toml) | `call_parameter_contextual_keyword` |
| [call_parameter_identifier_length_64](cases/call_parameter_identifier_length_64/case.toml) | `call_parameter_identifier_length_64` |
| [call_parameter_leading_underscore](cases/call_parameter_leading_underscore/case.toml) | `call_parameter_leading_underscore` |
| [call_parameter_trailing_underscore](cases/call_parameter_trailing_underscore/case.toml) | `call_parameter_trailing_underscore` |
| [call_parameter_type_keyword](cases/call_parameter_type_keyword/case.toml) | `call_parameter_type_keyword` |
| [call_process_member](cases/call_process_member/case.toml) | `call_fsharp_future_keyword_field` |
| [call_process_root](cases/call_process_root/case.toml) | `call_fsharp_future_keyword_root` |
| [call_quoted_atom_target](cases/call_quoted_atom_target/case.toml) | `call_quoted_atom_target` |
| [call_reserved_property_name](cases/call_reserved_property_name/case.toml) | `call_reserved_property_name` |
| [call_reserved_target_bare](cases/call_reserved_target_bare/case.toml) | `call_reserved_target_bare` |
| [call_reserved_target_casefold](cases/call_reserved_target_casefold/case.toml) | `call_reserved_target_casefold` |
| [call_reserved_target_head](cases/call_reserved_target_head/case.toml) | `call_reserved_target_head` |
| [call_reserved_target_member](cases/call_reserved_target_member/case.toml) | `call_reserved_target_member` |
| [call_reserved_target_member_casefold](cases/call_reserved_target_member_casefold/case.toml) | `call_reserved_target_member_casefold` |
| [call_target_identifier_length_64](cases/call_target_identifier_length_64/case.toml) | `call_target_identifier_length_64` |
| [call_trailing_underscore_parameter](cases/call_trailing_underscore_parameter/case.toml) | `call_trailing_underscore_parameter` |
| [keyword_prefix_bare_target](cases/keyword_prefix_bare_target/case.toml) | `systemverilog_keyword_prefix_bare_target` |
| [keyword_prefix_dotted_member](cases/keyword_prefix_dotted_member/case.toml) | `systemverilog_keyword_prefix_dotted_member` |
| [keyword_prefix_parameter](cases/keyword_prefix_parameter/case.toml) | `systemverilog_keyword_prefix_parameter` |
| [keyword_prefix_variable](cases/keyword_prefix_variable/case.toml) | `systemverilog_keyword_prefix_variable` |
| [lowercase_keyword_variable](cases/lowercase_keyword_variable/case.toml) | `erlang_lowercase_keyword_variable` |
| [mixed_case_keyword_variable](cases/mixed_case_keyword_variable/case.toml) | `systemverilog_keyword_case_variable` |
| [variable_name_63_characters](cases/variable_name_63_characters/case.toml) | `fortran_variable_name_standard_limit` |

### Issue #5797

24 original entries; 41 original golden filenames.

| Current owner | Original regressions |
| --- | --- |
| [call_binding_member_carrier_name](cases/call_binding_member_carrier_name/case.toml) | `call_binding_member_zval_zig` |
| [call_generated_helper_member_zkv](cases/call_generated_helper_member_zkv/case.toml) | `call_zig_helper_member_zkv` |
| [call_generated_helper_member_zval](cases/call_generated_helper_member_zval/case.toml) | `call_zig_helper_member_zval` |
| [call_json_bound_helper_names](cases/call_json_bound_helper_names/case.toml) | `call_ref_zig_json_helper_names` |
| [call_json_helper_member_std](cases/call_json_helper_member_std/case.toml) | `call_zig_helper_member_std` |
| [call_wrapper_alternate_name_collision](cases/call_wrapper_alternate_name_collision/case.toml) | `cobol_call_wrapper_name_control` |
| [call_wrapper_target_name_collision](cases/call_wrapper_target_name_collision/case.toml) | `cobol_call_wrapper_target_collision` |
| [call_zero_argument_value_method](cases/call_zero_argument_value_method/case.toml) | `call_zero_arg_value_method` |
| [caller_name_std](cases/caller_name_std/case.toml) | `zig_default_helper_name_std` |
| [consumer_key_binding](cases/consumer_key_binding/case.toml) | `typescript_consumer_key_binding` |
| [default_helper_name_allocator](cases/default_helper_name_allocator/case.toml) | `zig_default_helper_name_allocator` |
| [default_helper_name_arena](cases/default_helper_name_arena/case.toml) | `zig_default_helper_name_arena` |
| [identifier_collision_existing_suffix](cases/identifier_collision_existing_suffix/case.toml) | `cobol_collision_existing_suffix` |
| [identifier_collision_generated_suffix](cases/identifier_collision_generated_suffix/case.toml) | `cobol_collision_generated_suffix` |
| [json_helper_name_arena](cases/json_helper_name_arena/case.toml) | `zig_json_helper_name_arena` |
| [json_helper_name_zkv](cases/json_helper_name_zkv/case.toml) | `zig_json_helper_name_zkv` |
| [json_helper_name_zval](cases/json_helper_name_zval/case.toml) | `zig_json_helper_name_zval` |
| [record_fallback_helper_name_zkv](cases/record_fallback_helper_name_zkv/case.toml) | `zig_record_fallback_helper_name_zkv` |
| [record_fallback_helper_name_zval](cases/record_fallback_helper_name_zval/case.toml) | `zig_record_fallback_helper_name_zval` |
| [record_helper_name_zkv](cases/record_helper_name_zkv/case.toml) | `zig_record_helper_name_zkv` |
| [record_helper_name_zval](cases/record_helper_name_zval/case.toml) | `zig_record_helper_name_zval` |
| [record_name_without_record_strategy](cases/record_name_without_record_strategy/case.toml) | `swift_record_name_without_record_strategy` |
| [special_float_std_binding_mapping](cases/special_float_std_binding_mapping/case.toml) | `zig_special_float_std_binding_mapping` |
| [special_float_std_binding_scalar](cases/special_float_std_binding_scalar/case.toml) | `zig_special_float_std_binding_scalar` |

### Issue #5798

57 original entries; 215 original golden filenames.

| Current owner | Original regressions |
| --- | --- |
| [call_binding_existing_seeded](cases/call_binding_existing_seeded/case.toml) | `call_binding_existing_seeded` |
| [call_carrier_nested_separate](cases/call_carrier_nested_separate/case.toml) | `call_dotted_heterogeneous_lists` |
| [call_collection_result_annotations](cases/call_collection_result_annotations/case.toml) | `call_kotlin_result_collection` |
| [call_constructor_target](cases/call_constructor_target/case.toml) | `call_constructor_target` |
| [call_datetime_epoch_boundary](cases/call_datetime_epoch_boundary/case.toml) | `call_rust_epoch_boundary` |
| [call_dotted_empty_result_binding](cases/call_dotted_empty_result_binding/case.toml) | `call_nim_dotted_empty_result_binding` |
| [call_dotted_mixed_empty_arguments](cases/call_dotted_mixed_empty_arguments/case.toml) | `call_nim_dotted_mixed_empty_arguments` |
| [call_dotted_nonempty_result_binding](cases/call_dotted_nonempty_result_binding/case.toml) | `call_nim_dotted_nonempty_result_binding` |
| [call_empty_bound_reference](cases/call_empty_bound_reference/case.toml) | `call_nim_empty_bound_reference` |
| [call_empty_statement](cases/call_empty_statement/case.toml) | `call_nim_empty_statement` |
| [call_identity_bound_method](cases/call_identity_bound_method/case.toml) | `call_cpp_identity_bound_method` |
| [call_identity_nested_method](cases/call_identity_nested_method/case.toml) | `call_cpp_identity_nested_method` |
| [call_identity_result_binding](cases/call_identity_result_binding/case.toml) | `call_cpp_identity_result_binding` |
| [call_mixed_scalar_type_arguments](cases/call_mixed_scalar_type_arguments/case.toml) | `call_powershell_type_literal_arguments` |
| [call_multislot_carrier](cases/call_multislot_carrier/case.toml) | `call_cpp_multislot_carrier` |
| [call_native_record_argument](cases/call_native_record_argument/case.toml) | `call_native_record_argument` |
| [call_native_record_curried](cases/call_native_record_curried/case.toml) | `call_native_record_curried` |
| [call_native_record_direct_mapping_argument](cases/call_native_record_direct_mapping_argument/case.toml) | `call_sml_native_record_argument` |
| [call_native_record_dotted](cases/call_native_record_dotted/case.toml) | `call_purescript_native_record_dotted` |
| [call_native_record_mixed_args](cases/call_native_record_mixed_args/case.toml) | `call_native_record_mixed_args` |
| [call_native_record_no_params](cases/call_native_record_no_params/case.toml) | `call_purescript_native_record_no_params` |
| [call_native_record_no_params_dotted](cases/call_native_record_no_params_dotted/case.toml) | `call_purescript_native_record_no_params_dotted` |
| [call_nested_list_whole_argument](cases/call_nested_list_whole_argument/case.toml) | `call_whole_nested_list_argument` |
| [call_null_and_array_arguments](cases/call_null_and_array_arguments/case.toml) | `java_call_null_and_array_arguments` |
| [call_plain_empty_result_binding](cases/call_plain_empty_result_binding/case.toml) | `call_nim_plain_empty_result_binding` |
| [call_plain_mixed_empty_arguments](cases/call_plain_mixed_empty_arguments/case.toml) | `call_nim_plain_mixed_empty_arguments` |
| [call_plain_nonempty_result_binding](cases/call_plain_nonempty_result_binding/case.toml) | `call_nim_plain_nonempty_result_binding` |
| [call_result_instance_field](cases/call_result_instance_field/case.toml) | `call_result_instance_field` |
| [call_result_static_field](cases/call_result_static_field/case.toml) | `call_result_static_field` |
| [call_scalar_carrier](cases/call_scalar_carrier/case.toml) | `call_cpp_scalar_carrier` |
| [call_scalar_result_annotations](cases/call_scalar_result_annotations/case.toml) | `call_dart_result_type` |
| [call_seeded_result_consumption](cases/call_seeded_result_consumption/case.toml) | `call_existing_binding_ada`, `call_existing_binding_bash`, `call_existing_binding_fortran`, `call_existing_binding_nim` |
| [call_string_result_binding](cases/call_string_result_binding/case.toml) | `cpp_call_string_result_binding`, `cpp_call_string_result_binding_const` |
| [call_type_alias_bound_result](cases/call_type_alias_bound_result/case.toml) | `roc_call_alias_bound` |
| [call_type_alias_discarded_result](cases/call_type_alias_discarded_result/case.toml) | `roc_call_alias_discarded` |
| [call_type_alias_reference](cases/call_type_alias_reference/case.toml) | `roc_call_alias_reference` |
| [call_unknown_ref_values_nested_list](cases/call_unknown_ref_values_nested_list/case.toml) | `call_unknown_ref_values_nested_list` |
| [call_unused_bound_reference](cases/call_unused_bound_reference/case.toml) | `call_bound_ref_unused` |
| [call_whole_empty_list_argument](cases/call_whole_empty_list_argument/case.toml) | `call_whole_empty_list_argument` |
| [call_whole_input_comment](cases/call_whole_input_comment/case.toml) | `call_whole_input_comment` |
| [call_whole_list_argument](cases/call_whole_list_argument/case.toml) | `call_whole_list_argument` |
| [call_whole_tuple_argument](cases/call_whole_tuple_argument/case.toml) | `call_cpp_whole_tuple_argument` |
| [call_whole_variant_list_argument](cases/call_whole_variant_list_argument/case.toml) | `call_whole_variant_list_argument` |
| [call_wrapped_bound_ref](cases/call_wrapped_bound_ref/case.toml) | `elm_wrapped_call_bound_ref` |
| [call_wrapped_empty_list](cases/call_wrapped_empty_list/case.toml) | `elm_wrapped_call_empty_list` |
| [call_wrapped_result](cases/call_wrapped_result/case.toml) | `elm_wrapped_call_result` |
| [call_wrapped_scalar](cases/call_wrapped_scalar/case.toml) | `elm_wrapped_call_scalar` |
| [call_wrapped_temporal_arguments](cases/call_wrapped_temporal_arguments/case.toml) | `call_wrap_in_file_temporal` |
| [call_zip_ignored_matching_text](cases/call_zip_ignored_matching_text/case.toml) | `call_zip_ignored_matching_text` |
| [call_zip_ignored_preamble](cases/call_zip_ignored_preamble/case.toml) | `call_zip_ignored_preamble` |
| [call_zip_opaque_absent](cases/call_zip_opaque_absent/case.toml) | `call_zip_opaque_absent` |
| [call_zip_opaque_emitted](cases/call_zip_opaque_emitted/case.toml) | `call_zip_opaque_emitted` |
| [call_zip_opaque_omitted](cases/call_zip_opaque_omitted/case.toml) | `call_zip_opaque_omitted` |

### Issue #5799

19 original entries; 45 original golden filenames.

| Current owner | Original regressions |
| --- | --- |
| [call_json_nested_ref_array](cases/call_json_nested_ref_array/case.toml) | `call_zig_json_nested_ref_array` |
| [call_json_nested_ref_object](cases/call_json_nested_ref_object/case.toml) | `call_zig_json_nested_ref_object` |
| [call_json_nested_ref_per_element](cases/call_json_nested_ref_per_element/case.toml) | `call_zig_json_nested_ref_per_element` |
| [call_json_repeated_array](cases/call_json_repeated_array/case.toml) | `call_csharp_json_repeated_array` |
| [call_json_repeated_null](cases/call_json_repeated_null/case.toml) | `call_csharp_json_repeated_null` |
| [call_json_repeated_object](cases/call_json_repeated_object/case.toml) | `call_csharp_json_repeated_object` |
| [call_json_repeated_scalar](cases/call_json_repeated_scalar/case.toml) | `call_csharp_json_repeated_scalar` |
| [call_ref_bound_list_null_hint](cases/call_ref_bound_list_null_hint/case.toml) | `call_ref_cpp_bound_owning_null_hint` |
| [call_ref_bound_null_list_hint](cases/call_ref_bound_null_list_hint/case.toml) | `call_ref_cpp_bound_null_owning_hint` |
| [call_ref_consumed_value](cases/call_ref_consumed_value/case.toml) | `call_ref_rust_consumed_owned` |
| [call_ref_nested_reusable](cases/call_ref_nested_reusable/case.toml) | `call_ref_rust_nested_owned` |
| [call_ref_null_argument](cases/call_ref_null_argument/case.toml) | `call_ref_v_null` |
| [call_ref_null_consumable](cases/call_ref_null_consumable/case.toml) | `call_ref_null_consumable` |
| [call_ref_ordered_map](cases/call_ref_ordered_map/case.toml) | `call_ref_cpp_ordered_map` |
| [call_ref_preserved_value](cases/call_ref_preserved_value/case.toml) | `call_ref_rust_preserved_owned` |
| [call_ref_repeated_consumable](cases/call_ref_repeated_consumable/case.toml) | `call_ref_rust_repeated_owned` |
| [call_ref_scalar_record](cases/call_ref_scalar_record/case.toml) | `call_ref_cpp_trivial_record` |
| [call_ref_string_copy_modes](cases/call_ref_string_copy_modes/case.toml) | `call_ref_cpp_string_ownership` |
| [call_ref_string_record](cases/call_ref_string_record/case.toml) | `call_ref_cpp_owning_record` |

### Issue #5801

58 original entries; 122 original golden filenames.

| Current owner | Original regressions |
| --- | --- |
| [existing_variable_self_declaring](cases/existing_variable_self_declaring/case.toml) | `existing_variable_self_declaring` |
| [immutable_sequence_declaration](cases/immutable_sequence_declaration/case.toml) | `immutable_sequence_declaration` |
| [literalize_ref_array_owned_record](cases/literalize_ref_array_owned_record/case.toml) | `literalize_ref_cpp_owning_array_record` |
| [literalize_ref_array_record_ownership](cases/literalize_ref_array_record_ownership/case.toml) | `literalize_ref_cpp_array_record_ownership` |
| [literalize_ref_both_forms](cases/literalize_ref_both_forms/case.toml) | `literalize_ref_both_forms` |
| [literalize_ref_bound_sequence](cases/literalize_ref_bound_sequence/case.toml) | `literalize_ref_const_rvalue`, `literalize_ref_static_const_rvalue` |
| [literalize_ref_explicit_precedence](cases/literalize_ref_explicit_precedence/case.toml) | `literalize_ref_const_lvalue`, `literalize_ref_static_lvalue` |
| [literalize_ref_generated_helper_names](cases/literalize_ref_generated_helper_names/case.toml) | `literalize_ref_zig_helper_names_default` |
| [literalize_ref_indented_comment_bindings](cases/literalize_ref_indented_comment_bindings/case.toml) | `literalize_ref_zig_mutable_prefixed_comments` |
| [literalize_ref_mutable_both](cases/literalize_ref_mutable_both/case.toml) | `literalize_ref_zig_mutable_both` |
| [literalize_ref_mutable_nested](cases/literalize_ref_mutable_nested/case.toml) | `literalize_ref_zig_mutable_nested` |
| [literalize_ref_mutable_record_arrays_both_forms](cases/literalize_ref_mutable_record_arrays_both_forms/case.toml) | `literalize_ref_zig_native_record_arrays_both` |
| [literalize_ref_mutable_record_distinct_array_types](cases/literalize_ref_mutable_record_distinct_array_types/case.toml) | `literalize_ref_zig_native_distinct_array_types` |
| [literalize_ref_mutable_record_heterogeneous_both_forms](cases/literalize_ref_mutable_record_heterogeneous_both_forms/case.toml) | `literalize_ref_zig_native_heterogeneous_both` |
| [literalize_ref_mutable_record_root](cases/literalize_ref_mutable_record_root/case.toml) | `literalize_ref_zig_mutable_record` |
| [literalize_ref_mutable_root](cases/literalize_ref_mutable_root/case.toml) | `literalize_ref_zig_mutable_root` |
| [literalize_ref_native_empty_array_both](cases/literalize_ref_native_empty_array_both/case.toml) | `literalize_ref_zig_native_empty_array_both` |
| [literalize_ref_native_empty_string_array_both](cases/literalize_ref_native_empty_string_array_both/case.toml) | `literalize_ref_zig_native_empty_string_array_both` |
| [literalize_ref_native_nested_arrays_both](cases/literalize_ref_native_nested_arrays_both/case.toml) | `literalize_ref_zig_native_nested_arrays_both` |
| [literalize_ref_nested_null](cases/literalize_ref_nested_null/case.toml) | `literalize_ref_nested_null` |
| [literalize_ref_nested_record_root](cases/literalize_ref_nested_record_root/case.toml) | `literalize_ref_cpp_trivial_root_record` |
| [literalize_ref_nul_string_value](cases/literalize_ref_nul_string_value/case.toml) | `literalize_ref_cpp_owned_nul_string` |
| [literalize_ref_null](cases/literalize_ref_null/case.toml) | `literalize_ref_v_null` |
| [literalize_ref_null_bound_list_hint](cases/literalize_ref_null_bound_list_hint/case.toml) | `literalize_ref_null_bound_list_hint` |
| [literalize_ref_null_hint_container](cases/literalize_ref_null_hint_container/case.toml) | `literalize_ref_null_hint_container` |
| [literalize_ref_owned_root_both](cases/literalize_ref_owned_root_both/case.toml) | `literalize_ref_cpp_both_root`, `literalize_ref_rust_root_both_owned` |
| [literalize_ref_record_value_ownership](cases/literalize_ref_record_value_ownership/case.toml) | `literalize_ref_cpp_record_ownership` |
| [literalize_ref_repeated_array_objects](cases/literalize_ref_repeated_array_objects/case.toml) | `literalize_ref_rust_repeated_array_owned` |
| [literalize_ref_repeated_array_scalars](cases/literalize_ref_repeated_array_scalars/case.toml) | `literalize_ref_rust_repeated_array_copy` |
| [literalize_ref_repeated_empty_array](cases/literalize_ref_repeated_empty_array/case.toml) | `literalize_ref_rust_repeated_empty_array_copy` |
| [literalize_ref_repeated_mixed_sequence](cases/literalize_ref_repeated_mixed_sequence/case.toml) | `literalize_ref_rust_repeated_array_enum`, `literalize_ref_rust_repeated_enum` |
| [literalize_ref_repeated_nested](cases/literalize_ref_repeated_nested/case.toml) | `literalize_ref_rust_repeated_nested` |
| [literalize_ref_repeated_nested_collection](cases/literalize_ref_repeated_nested_collection/case.toml) | `literalize_ref_rust_repeated_tuple_owned` |
| [literalize_ref_repeated_null_and_literal](cases/literalize_ref_repeated_null_and_literal/case.toml) | `literalize_ref_v_null_interface` |
| [literalize_ref_repeated_owned](cases/literalize_ref_repeated_owned/case.toml) | `literalize_ref_cpp_repeated_owned` |
| [literalize_ref_repeated_record](cases/literalize_ref_repeated_record/case.toml) | `literalize_ref_rust_repeated_record` |
| [literalize_ref_repeated_tuple_mixed](cases/literalize_ref_repeated_tuple_mixed/case.toml) | `literalize_ref_rust_repeated_tuple_copy` |
| [literalize_ref_repeated_tuple_strategy](cases/literalize_ref_repeated_tuple_strategy/case.toml) | `literalize_ref_rust_repeated_tuple_scalar` |
| [literalize_ref_repeated_value_type](cases/literalize_ref_repeated_value_type/case.toml) | `literalize_ref_rust_repeated_json` |
| [literalize_ref_root_both_forms](cases/literalize_ref_root_both_forms/case.toml) | `literalize_ref_mojo_root_both_forms` |
| [literalize_ref_string_value](cases/literalize_ref_string_value/case.toml) | `literalize_ref_cpp_string_pointer` |
| [literalize_ref_typed_empty_array_reuse](cases/literalize_ref_typed_empty_array_reuse/case.toml) | `literalize_ref_rust_repeated_empty_array_owned` |
| [literalize_ref_unresolved_unrelated_values](cases/literalize_ref_unresolved_unrelated_values/case.toml) | `literalize_ref_rust_unresolved_unrelated_values` |
| [literalize_ref_unresolved_without_values](cases/literalize_ref_unresolved_without_values/case.toml) | `literalize_ref_rust_unresolved_without_values` |
| [literalize_ref_value_type_nested_array](cases/literalize_ref_value_type_nested_array/case.toml) | `literalize_ref_zig_json_nested_array` |
| [literalize_ref_value_type_nested_object](cases/literalize_ref_value_type_nested_object/case.toml) | `literalize_ref_zig_json_nested_object` |
| [literalize_ref_value_type_nested_object_both](cases/literalize_ref_value_type_nested_object_both/case.toml) | `literalize_ref_zig_json_nested_both_object` |
| [literalize_ref_value_type_nested_object_indented](cases/literalize_ref_value_type_nested_object_indented/case.toml) | `literalize_ref_zig_json_nested_var_object` |
| [literalize_ref_value_type_root_array](cases/literalize_ref_value_type_root_array/case.toml) | `literalize_ref_zig_json_mutable_root_new`, `literalize_ref_zig_json_root_array` |
| [literalize_ref_value_type_root_both](cases/literalize_ref_value_type_root_both/case.toml) | `literalize_ref_zig_json_mutable_root_both` |
| [literalize_ref_value_type_root_null](cases/literalize_ref_value_type_root_null/case.toml) | `literalize_ref_zig_json_root_null` |
| [literalize_ref_value_type_root_object](cases/literalize_ref_value_type_root_object/case.toml) | `literalize_ref_zig_json_root_object` |
| [literalize_ref_value_type_root_string](cases/literalize_ref_value_type_root_string/case.toml) | `literalize_ref_zig_json_root_string` |

### Issue #5803

47 original entries; 192 original golden filenames.

| Current owner | Original regressions |
| --- | --- |
| [array_map_element_type](cases/array_map_element_type/case.toml) | `csharp_array_map_element_type` |
| [deep_positional_empty_lists](cases/deep_positional_empty_lists/case.toml) | `deep_positional_empty_lists` |
| [empty_map_nested_list_value](cases/empty_map_nested_list_value/case.toml) | `v_empty_map_nested_list_value` |
| [empty_map_nested_value](cases/empty_map_nested_value/case.toml) | `v_empty_map_nested_value` |
| [empty_map_scalar_variant_sibling](cases/empty_map_scalar_variant_sibling/case.toml) | `mojo_empty_map_scalar_variant_sibling` |
| [empty_map_sibling_sequence](cases/empty_map_sibling_sequence/case.toml) | `rust_empty_map_sibling_sequence` |
| [empty_nested_sequence_map_values](cases/empty_nested_sequence_map_values/case.toml) | `cpp_empty_nested_sequence_map_values` |
| [four_dimensional_empty_lists](cases/four_dimensional_empty_lists/case.toml) | `v_four_dimensional_empty_lists` |
| [mixed_scalar_carriers](cases/mixed_scalar_carriers/case.toml) | `cpp14_carrier_scalar_list` |
| [narrowed_empty_list_map_values](cases/narrowed_empty_list_map_values/case.toml) | `narrowed_empty_list_map_values` |
| [narrowed_empty_list_mixed_sibling](cases/narrowed_empty_list_mixed_sibling/case.toml) | `narrowed_empty_list_mixed_sibling` |
| [narrowed_empty_list_null_sibling](cases/narrowed_empty_list_null_sibling/case.toml) | `narrowed_empty_list_null_sibling` |
| [nested_empty_list_map_sibling](cases/nested_empty_list_map_sibling/case.toml) | `mojo_nested_empty_list_map_sibling` |
| [nested_empty_map_sibling](cases/nested_empty_map_sibling/case.toml) | `mojo_nested_empty_map_sibling` |
| [nested_positional_empty_list_cousins](cases/nested_positional_empty_list_cousins/case.toml) | `nested_positional_empty_list_cousins` |
| [nested_positional_empty_lists](cases/nested_positional_empty_lists/case.toml) | `nested_positional_empty_lists` |
| [nested_positional_empty_lists_reversed](cases/nested_positional_empty_lists_reversed/case.toml) | `nested_positional_empty_lists_reversed` |
| [nested_variant_map_empty_sibling](cases/nested_variant_map_empty_sibling/case.toml) | `mojo_nested_variant_map_empty_sibling` |
| [null_only_ordered_map](cases/null_only_ordered_map/case.toml) | `mojo_empty_filtered_ordered_map` |
| [ordered_integer_map](cases/ordered_integer_map/case.toml) | `python_eager_ordered_map_alias` |
| [partially_populated_positional_empty_lists](cases/partially_populated_positional_empty_lists/case.toml) | `partially_populated_positional_empty_lists` |
| [positional_empty_list_siblings](cases/positional_empty_list_siblings/case.toml) | `positional_empty_list_siblings` |
| [positional_empty_lists_without_exemplar](cases/positional_empty_lists_without_exemplar/case.toml) | `positional_empty_lists_without_exemplar` |
| [positional_empty_map_rows](cases/positional_empty_map_rows/case.toml) | `cpp_tuple_positional_empty_map_rows` |
| [positional_empty_rows](cases/positional_empty_rows/case.toml) | `cpp_tuple_positional_empty_rows` |
| [positional_mixed_rows](cases/positional_mixed_rows/case.toml) | `cpp_tuple_positional_mixed_rows` |
| [ragged_map_sequence_values](cases/ragged_map_sequence_values/case.toml) | `rust_ragged_map_sequence_vec` |
| [record_empty_nested_list](cases/record_empty_nested_list/case.toml) | `rust_lazy_static_empty_sibling` |
| [rectangular_map_sequence_shapes](cases/rectangular_map_sequence_shapes/case.toml) | `rust_rectangular_map_sequence_shapes` |
| [scalar_variant_list_empty_sibling](cases/scalar_variant_list_empty_sibling/case.toml) | `mojo_scalar_variant_list_empty_sibling` |
| [sequence_ragged_siblings](cases/sequence_ragged_siblings/case.toml) | `rust_tuple_ragged_siblings` |
| [sibling_list_values_same_shape](cases/sibling_list_values_same_shape/case.toml) | `sibling_list_values_same_shape` |
| [single_element_containers](cases/single_element_containers/case.toml) | `raku_single_element_containers` |
| [tuple_empty_first_sequence](cases/tuple_empty_first_sequence/case.toml) | `cpp_tuple_empty_first_sequence` |
| [tuple_empty_map_values](cases/tuple_empty_map_values/case.toml) | `cpp_tuple_empty_map_values` |
| [tuple_empty_mixed_sequence](cases/tuple_empty_mixed_sequence/case.toml) | `cpp_tuple_empty_mixed_sequence` |
| [tuple_empty_then_populated](cases/tuple_empty_then_populated/case.toml) | `rust_tuple_empty_sibling_slot`, `rust_tuple_empty_then_populated` |
| [tuple_fields_with_nested_vectors](cases/tuple_fields_with_nested_vectors/case.toml) | `rust_tuple_with_nested_vec` |
| [tuple_map_value](cases/tuple_map_value/case.toml) | `dart_tuple_map_value` |
| [tuple_nested_empty_sequences](cases/tuple_nested_empty_sequences/case.toml) | `cpp_tuple_nested_empty_sequences` |
| [tuple_nested_scope](cases/tuple_nested_scope/case.toml) | `rust_tuple_nested_scope` |
| [tuple_populated_siblings](cases/tuple_populated_siblings/case.toml) | `rust_tuple_populated_siblings` |
| [tuple_populated_then_empty](cases/tuple_populated_then_empty/case.toml) | `rust_tuple_populated_then_empty` |
| [widened_dict_elements](cases/widened_dict_elements/case.toml) | `go_widened_dict_elements` |
| [widened_map_value_hint](cases/widened_map_value_hint/case.toml) | `dart_widened_map_value_hint` |
| [widened_sibling_maps](cases/widened_sibling_maps/case.toml) | `cpp14_widened_sibling_maps` |

### Issue #5804

55 original entries; 170 original golden filenames.

| Current owner | Original regressions |
| --- | --- |
| [empty_sequence_record_mixture](cases/empty_sequence_record_mixture/case.toml) | `cpp_empty_sequence_record_mixture`, `csharp_empty_sequence_record_mixture` |
| [empty_sequence_record_mixture_reversed](cases/empty_sequence_record_mixture_reversed/case.toml) | `csharp_empty_sequence_record_mixture_reversed` |
| [native_record_binary](cases/native_record_binary/case.toml) | `roc_native_record_binary` |
| [native_record_keyword_fields](cases/native_record_keyword_fields/case.toml) | `crystal_record_keyword_fields` |
| [native_record_list](cases/native_record_list/case.toml) | `roc_native_record_list` |
| [native_record_nested_fields](cases/native_record_nested_fields/case.toml) | `opt_in_record_nested` |
| [native_record_sequence_fields](cases/native_record_sequence_fields/case.toml) | `rust_record_sequence_fields` |
| [native_record_special_float_fields](cases/native_record_special_float_fields/case.toml) | `opt_in_record_special_floats`, `roc_native_record_special_floats` |
| [native_record_temporal](cases/native_record_temporal/case.toml) | `roc_native_record_temporal` |
| [native_records_in_heterogeneous_sequences](cases/native_records_in_heterogeneous_sequences/case.toml) | `cpp_record_in_variant` |
| [nested_record_sequences](cases/nested_record_sequences/case.toml) | `nested_record_sequences`, `nested_record_sequences_scala_tuple` |
| [nested_sequence_declaration_modifiers](cases/nested_sequence_declaration_modifiers/case.toml) | `csharp_nested_tuple_field` |
| [opt_in_record_temporal](cases/opt_in_record_temporal/case.toml) | `opt_in_record_temporal` |
| [ordered_map_nested_record_fields](cases/ordered_map_nested_record_fields/case.toml) | `python_record_eager_ordered_map` |
| [ordered_map_nested_record_sequence](cases/ordered_map_nested_record_sequence/case.toml) | `cpp14_tuple_ordered_map_record` |
| [ordered_record_list_scalar](cases/ordered_record_list_scalar/case.toml) | `ordered_record_list_scalar`, `swift_ordered_record_scalar` |
| [record_beside_scalar](cases/record_beside_scalar/case.toml) | `swift_record_beside_scalar` |
| [record_constructor_text](cases/record_constructor_text/case.toml) | `swift_record_constructor_text` |
| [record_empty_dict_in_any_sequence](cases/record_empty_dict_in_any_sequence/case.toml) | `go_record_empty_dict_in_any_sequence` |
| [record_empty_list_among_scalars](cases/record_empty_list_among_scalars/case.toml) | `crystal_record_empty_list_among_scalars` |
| [record_empty_nested_list](cases/record_empty_nested_list/case.toml) | `crystal_record_empty_nested_list` |
| [record_empty_sibling_arrays](cases/record_empty_sibling_arrays/case.toml) | `csharp_record_empty_sibling_arrays` |
| [record_fallback_empty_array](cases/record_fallback_empty_array/case.toml) | `d_record_fallback_empty_array` |
| [record_fallback_set_values](cases/record_fallback_set_values/case.toml) | `zig_record_fallback_set_values` |
| [record_field_modifiers](cases/record_field_modifiers/case.toml) | `record_field_modifiers` |
| [record_field_rebindable_modifiers](cases/record_field_rebindable_modifiers/case.toml) | `record_field_rebindable_modifiers` |
| [record_independent_array_fields](cases/record_independent_array_fields/case.toml) | `cpp_record_independent_array_fields` |
| [record_list_field](cases/record_list_field/case.toml) | `python_record_list_field` |
| [record_list_ordered_map_nominal_values](cases/record_list_ordered_map_nominal_values/case.toml) | `record_list_ordered_map_nominal_values` |
| [record_nested_independent_array_fields](cases/record_nested_independent_array_fields/case.toml) | `cpp_record_nested_independent_array_fields` |
| [record_ordered_map_fields](cases/record_ordered_map_fields/case.toml) | `v_record_ordered_map_fields` |
| [record_ordered_map_nested_nominal_lists](cases/record_ordered_map_nested_nominal_lists/case.toml) | `record_ordered_map_nested_nominal_lists` |
| [record_ordered_map_nested_nominal_parent_types](cases/record_ordered_map_nested_nominal_parent_types/case.toml) | `record_ordered_map_nested_nominal_parent_types` |
| [record_ordered_map_nested_nominal_values](cases/record_ordered_map_nested_nominal_values/case.toml) | `record_ordered_map_nested_nominal_values` |
| [record_ordered_map_nominal_parent_types](cases/record_ordered_map_nominal_parent_types/case.toml) | `record_ordered_map_nominal_parent_types` |
| [record_ordered_map_nominal_values](cases/record_ordered_map_nominal_values/case.toml) | `record_ordered_map_nominal_values` |
| [record_ordered_map_parent_shapes](cases/record_ordered_map_parent_shapes/case.toml) | `swift_record_ordered_map_parent_shapes` |
| [record_primitive_sequence_fields](cases/record_primitive_sequence_fields/case.toml) | `kotlin_record_primitive_arrays` |
| [record_root_list_map_annotations](cases/record_root_list_map_annotations/case.toml) | `swift_record_root_list_map_annotations` |
| [record_root_nested_map_annotations](cases/record_root_nested_map_annotations/case.toml) | `swift_record_root_nested_map_annotations` |
| [record_root_ordered_map_annotations](cases/record_root_ordered_map_annotations/case.toml) | `swift_record_root_ordered_map_annotations` |
| [record_scalar_array_value_initialization](cases/record_scalar_array_value_initialization/case.toml) | `cpp_record_scalar_array_value_initialization` |
| [record_sequence_empty_sibling](cases/record_sequence_empty_sibling/case.toml) | `cpp_empty_record_sequence_root`, `v_empty_record_sequence_root` |
| [record_sequence_mixture_controls](cases/record_sequence_mixture_controls/case.toml) | `csharp_record_sequence_mixture_controls` |
| [record_tuple_fields](cases/record_tuple_fields/case.toml) | `kotlin_record_tuple_fields` |
| [record_tuple_scalar_leaf](cases/record_tuple_scalar_leaf/case.toml) | `tuple_record_scalar_leaf` |
| [sequence_declaration_modifiers](cases/sequence_declaration_modifiers/case.toml) | `csharp_tuple_field` |
| [widened_record_map_integer_and_null](cases/widened_record_map_integer_and_null/case.toml) | `widened_record_map_integer_and_null` |
| [widened_record_map_mixed_values](cases/widened_record_map_mixed_values/case.toml) | `widened_record_map_mixed_values` |
| [widened_record_map_null_values](cases/widened_record_map_null_values/case.toml) | `widened_record_map_null_values` |

### Issue #5809

17 original entries; 45 original golden filenames.

| Current owner | Original regressions |
| --- | --- |
| [bare_list](cases/bare_list/case.toml) | `bare_list` |
| [bare_object](cases/bare_object/case.toml) | `bare_object` |
| [bare_string](cases/bare_string/case.toml) | `bare_string` |
| [call_bound_multiline_multiple](cases/call_bound_multiline_multiple/case.toml) | `call_elm_bound_multiline_multiple` |
| [call_bound_ref_multiline_layout](cases/call_bound_ref_multiline_layout/case.toml) | `call_bound_ref_multiline_layout` |
| [custom_root_multiline_text](cases/custom_root_multiline_text/case.toml) | `dart_fixture_root_multiline` |
| [deep_singleton_sequences](cases/deep_singleton_sequences/case.toml) | `fortran_line_length_without_commas` |
| [line_length_continuation_margin](cases/line_length_continuation_margin/case.toml) | `fortran_line_length_continuation_margin` |
| [literalize_ref_pre_indented](cases/literalize_ref_pre_indented/case.toml) | `literalize_ref_pre_indented` |
| [literalize_ref_pre_indented_injected_text](cases/literalize_ref_pre_indented_injected_text/case.toml) | `roc_bound_refs_pre_indented` |
| [long_string](cases/long_string/case.toml) | `fortran_long_string` |
| [long_string_after_key](cases/long_string_after_key/case.toml) | `fortran_long_string_after_key` |
| [long_string_literal](cases/long_string_literal/case.toml) | `cobol_long_string_literal` |
| [multiline_string_pre_indent](cases/multiline_string_pre_indent/case.toml) | `multiline_string_pre_indent` |
| [native_record_custom_indent](cases/native_record_custom_indent/case.toml) | `elm_native_record_custom_indent` |
| [ordered_map_multiline_whitespace](cases/ordered_map_multiline_whitespace/case.toml) | `python_ordered_map_multiline_whitespace` |
| [wide_json_list](cases/wide_json_list/case.toml) | `rust_serde_json_wide_list` |

### Issue #5814

53 original entries; 128 original golden filenames.

| Current owner | Original regressions |
| --- | --- |
| [call_binding_existing_comment_inline_declaration_variants](cases/call_binding_existing_comment_inline_declaration_variants/case.toml) | `call_binding_existing_comment_inline_zig`, `call_shared_comments_haxe_existing_comment_0_existing` |
| [call_binding_grouped_inner_comment](cases/call_binding_grouped_inner_comment/case.toml) | `call_binding_inner_comment_c`, `call_binding_inner_comment_cpp`, `call_binding_inner_comment_csharp`, `call_binding_inner_comment_d`, `call_binding_inner_comment_dart`, `call_binding_inner_comment_haxe`, `call_binding_inner_comment_java`, `call_binding_inner_comment_systemverilog`, `call_binding_inner_comment_zig` |
| [call_binding_inline_comment_scalar](cases/call_binding_inline_comment_scalar/case.toml) | `call_shared_comments_cpp_existing_comment_0_new`, `call_shared_comments_csharp_existing_comment_0_new`, `call_shared_comments_dart_existing_comment_0_new`, `call_shared_comments_haxe_existing_comment_0_new` |
| [call_binding_inline_line_comment](cases/call_binding_inline_line_comment/case.toml) | `call_binding_inline_comment_c`, `call_binding_inline_comment_cpp`, `call_binding_inline_comment_csharp`, `call_binding_inline_comment_d`, `call_binding_inline_comment_dart`, `call_binding_inline_comment_haxe`, `call_binding_inline_comment_java`, `call_binding_inline_comment_objective_c`, `call_binding_inline_comment_systemverilog`, `call_binding_inline_comment_zig` |
| [call_binding_multiple_comments_scalar](cases/call_binding_multiple_comments_scalar/case.toml) | `call_shared_comments_cpp_existing_comment_2_new`, `call_shared_comments_csharp_existing_comment_2_new`, `call_shared_comments_dart_existing_comment_2_new`, `call_shared_comments_haxe_existing_comment_2_new` |
| [call_binding_next_line_comment_scalar](cases/call_binding_next_line_comment_scalar/case.toml) | `call_shared_comments_cpp_existing_comment_1_new`, `call_shared_comments_csharp_existing_comment_1_new`, `call_shared_comments_dart_existing_comment_1_new`, `call_shared_comments_haxe_existing_comment_1_new` |
| [call_binding_next_line_line_comment](cases/call_binding_next_line_line_comment/case.toml) | `java_call_binding_trailing_comment`, `java_call_binding_trailing_comment_c`, `java_call_binding_trailing_comment_cpp`, `java_call_binding_trailing_comment_csharp`, `java_call_binding_trailing_comment_d`, `java_call_binding_trailing_comment_dart`, `java_call_binding_trailing_comment_haxe`, `java_call_binding_trailing_comment_objective_c`, `java_call_binding_trailing_comment_systemverilog`, `java_call_binding_trailing_comment_zig` |
| [call_binding_quoted_line_comment_marker](cases/call_binding_quoted_line_comment_marker/case.toml) | `call_binding_quoted_comment_marker_c`, `call_binding_quoted_comment_marker_cpp`, `call_binding_quoted_comment_marker_csharp`, `call_binding_quoted_comment_marker_d`, `call_binding_quoted_comment_marker_dart`, `call_binding_quoted_comment_marker_haxe`, `call_binding_quoted_comment_marker_java`, `call_binding_quoted_comment_marker_objective_c`, `call_binding_quoted_comment_marker_systemverilog`, `call_binding_quoted_comment_marker_zig` |
