-module(fixture_nested_positional_empty_lists_reversed_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        {{1}},
        {{}}
    },
    My_data.
