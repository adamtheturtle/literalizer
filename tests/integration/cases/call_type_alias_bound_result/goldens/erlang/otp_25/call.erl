-module(fixture_call_type_alias_bound_result_erlang_call).
-export([x/0]).
process(_) -> undefined.
x() ->
    My_data = process(1),
    My_data.
