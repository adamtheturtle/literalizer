-module(fixture_literalize_ref_in_mixed_list_erlang_ref).
-export([x/0]).
x() ->
    X = #{
        "_" => "_"
    },
    My_data = [
        X,
        1,
        2
    ],
    My_data.
