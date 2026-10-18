-module(fixture_literalize_ref_null_value_erlang_ref).
-export([x/0]).
x() ->
    My_null = undefined,
    My_data = My_null,
    My_data.
