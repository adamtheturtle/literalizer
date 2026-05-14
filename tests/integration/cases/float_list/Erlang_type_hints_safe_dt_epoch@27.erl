-module(fixture_float_list_erlang_type_hints_safe_dt_epoch).
-export([x/0]).
x() ->
    My_data = [
        1.1,
        -2.2,
        3.3
    ],
    My_data.
