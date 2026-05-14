-module(fixture_int_set_erlang_type_hints_safe_dt_epoch).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        1,
        2,
        3
    ]),
    My_data.
