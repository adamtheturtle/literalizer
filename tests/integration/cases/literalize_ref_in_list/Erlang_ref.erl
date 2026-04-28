-module(fixture_literalize_ref_in_list_erlang_ref).
-export([x/0]).
x() ->
    My_data = [
        X,
        Y
    ],
    My_data.
