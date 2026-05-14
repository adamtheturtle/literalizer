-module(fixture_call_ref_nested_in_dict_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    My_var = 42,
    process(#{"key" => My_var, "count" => 42}).
