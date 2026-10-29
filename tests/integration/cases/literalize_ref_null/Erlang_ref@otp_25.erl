-module(fixture_literalize_ref_null_erlang_ref).
-export([x/0]).
x() ->
    Value = undefined,
    My_data = Value,
    My_data.
