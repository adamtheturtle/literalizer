-module(fixture_literalize_ref_unused_values_set_erlang_ref_default).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        1,
        2
    ]),
    My_data.
