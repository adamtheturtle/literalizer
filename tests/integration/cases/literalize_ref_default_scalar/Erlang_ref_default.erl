-module(fixture_literalize_ref_default_scalar_erlang_ref_default).
-export([x/0]).
x() ->
    My_var = 1,
    My_data = My_var,
    My_data.
