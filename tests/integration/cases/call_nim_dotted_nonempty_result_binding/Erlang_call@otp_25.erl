-module(fixture_call_nim_dotted_nonempty_result_binding_erlang_call).
-export([x/0]).
'thing.go'(_) -> undefined.
x() ->
    My_data = 'thing.go'([1]),
    My_data.
