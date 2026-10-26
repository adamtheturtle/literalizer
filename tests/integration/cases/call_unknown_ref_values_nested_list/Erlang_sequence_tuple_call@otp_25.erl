-module(fixture_call_unknown_ref_values_nested_list_erlang_sequence_tuple_call).
-export([x/0]).
process(_) -> ok.
x() ->
    Unknown_value = {},
    process({Unknown_value}).
