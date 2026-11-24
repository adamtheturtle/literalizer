-module(fixture_nested_bool_list_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        {true, false},
        {true, true}
    },
    My_data.
