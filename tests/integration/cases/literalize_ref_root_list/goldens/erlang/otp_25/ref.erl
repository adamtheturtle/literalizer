-module(fixture_literalize_ref_root_list_erlang_ref).
-export([x/0]).
x() ->
    Whole = [
        1,
        2
    ],
    My_data = Whole,
    My_data.
