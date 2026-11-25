-module(fixture_set_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        "apple",
        "banana",
        "cherry"
    ]),
    My_data.
