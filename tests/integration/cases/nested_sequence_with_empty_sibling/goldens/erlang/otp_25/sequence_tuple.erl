-module(fixture_nested_sequence_with_empty_sibling_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        {{1}},
        {{}}
    },
    My_data.
