-module(fixture_narrowed_empty_list_null_sibling_erlang_sequence_tuple).
-export([x/0]).
x() ->
    My_data = {
        {undefined},
        {}
    },
    My_data.
