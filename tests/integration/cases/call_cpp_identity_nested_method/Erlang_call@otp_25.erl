-module(fixture_call_cpp_identity_nested_method_erlang_call).
-export([x/0]).
'outer.thing.go'() -> undefined.
x() ->
    'outer.thing.go'().
