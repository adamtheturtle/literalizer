-module(fixture_bool_list_erlang_type_hints_safe_dt_epoch).
-export([x/0]).
x() ->
    My_data = [
        true,
        false,
        true
    ],
    My_data.
