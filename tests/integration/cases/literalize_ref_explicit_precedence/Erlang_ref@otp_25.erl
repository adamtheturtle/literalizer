-module(fixture_literalize_ref_explicit_precedence_erlang_ref).
-export([x/0]).
x() ->
    X = [
        1,
        2
    ],
    My_data = X,
    My_data.
