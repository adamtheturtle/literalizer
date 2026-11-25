-module(fixture_nested_list_mixed_numeric_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        {1},
        {2.5}
    },
    My_data.
