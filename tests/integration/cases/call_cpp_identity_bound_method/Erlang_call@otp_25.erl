-module(fixture_call_cpp_identity_bound_method_erlang_call).
-export([x/0]).
'thing.go'(_) -> undefined.
x() ->
    Item = [
        1,
        2
    ],
    'thing.go'(Item).
