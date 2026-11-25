-module(fixture_four_dimensional_empty_lists_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        {{{}}},
        {{{}}}
    },
    My_data.
