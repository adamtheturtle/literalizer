-module(fixture_literalize_ref_repeated_null_and_literal_erlang_ref).
-export([x/0]).
x() ->
    Value = undefined,
    My_data = [
        Value,
        Value,
        undefined
    ],
    My_data.
