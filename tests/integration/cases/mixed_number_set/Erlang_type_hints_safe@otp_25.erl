-module(fixture_mixed_number_set_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        2.5,
        1
    ]),
    My_data.
