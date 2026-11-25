-module(fixture_literalize_ref_explicit_precedence_erlang_ref).
-export([x/0]).
x() ->
    Ref_data = [
        1,
        2
    ],
    My_data = Ref_data,
    My_data.
