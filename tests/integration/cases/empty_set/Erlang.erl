-module(fixture_empty_set_erlang).
-export([x/0]).
x() ->
    My_data = sets:from_list([]),
    My_data.
