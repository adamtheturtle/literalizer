-module(fixture_literalize_ref_in_list_erlang_ref).
-export([x/0]).
x() ->
    My_data = [
        Val_x,
        Val_y
    ],
    My_data.
