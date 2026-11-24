-module(fixture_literalize_ref_scalar_erlang_ref).
-export([x/0]).
x() ->
    My_int = 42,
    My_data = My_int,
    My_data.
