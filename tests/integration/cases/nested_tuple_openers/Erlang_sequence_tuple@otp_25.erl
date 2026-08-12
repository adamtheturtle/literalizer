-module(fixture_nested_tuple_openers_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        {{{1}}}
    },
    My_data.
