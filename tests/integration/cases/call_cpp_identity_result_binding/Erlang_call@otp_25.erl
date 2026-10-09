-module(fixture_call_cpp_identity_result_binding_erlang_call).
-export([x/0]).
'thing.go'(_) -> undefined.
x() ->
    My_data = 'thing.go'([]),
    My_data.
