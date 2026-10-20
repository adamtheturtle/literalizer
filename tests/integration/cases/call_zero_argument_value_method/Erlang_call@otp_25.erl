-module(fixture_call_zero_argument_value_method_erlang_call).
-export([x/0]).
'thing.go'() -> undefined.
x() ->
    'thing.go'().
