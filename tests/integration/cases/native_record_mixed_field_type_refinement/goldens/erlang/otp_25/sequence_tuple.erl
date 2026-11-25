-module(fixture_native_record_mixed_field_type_refinement_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = #{
        "first" => #{"items" => {1, #{"value" => 2}}},
        "second" => #{"items" => {1, #{"value" => "s"}}}
    },
    My_data.
