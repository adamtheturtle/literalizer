-module(fixture_call_ref_nested_converted_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    My_var = 42,
    process([My_var, 42, "static"]).
