-module(fixture_positional_empty_lists_without_exemplar_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        {{}},
        {{}}
    },
    My_data.
