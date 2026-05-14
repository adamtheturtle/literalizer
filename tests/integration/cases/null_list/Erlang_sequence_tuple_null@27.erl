-module(fixture_null_list_erlang_sequence_tuple_null).
-export([x/0]).
x() ->
    My_data = {
        undefined,
        undefined
    },
    My_data.
