-module(fixture_mixed_set_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        true,
        42,
        "apple"
    ]),
    My_data.
