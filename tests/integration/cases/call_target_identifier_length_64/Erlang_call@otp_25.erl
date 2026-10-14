-module(fixture_call_target_identifier_length_64_erlang_call).
-export([x/0]).
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff(_) -> ok.
x() ->
    ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff(1).
