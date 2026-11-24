-module(fixture_set_mixed_int_widths_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        1,
        1099511627776
    ]),
    My_data.
