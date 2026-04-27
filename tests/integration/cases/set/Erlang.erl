-module(fixture_set_erlang).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        "apple",
        "banana",
        "cherry"
    ]),
    My_data.
