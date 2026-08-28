-module(fixture_call_variable_form_new_multi_arg_erlang_call).
-export([x/0]).
record_entry(_, _, _) -> undefined.
x() ->
    My_data = record_entry("a", 1, true),
    My_data.
