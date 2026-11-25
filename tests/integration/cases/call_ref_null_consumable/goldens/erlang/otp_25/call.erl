-module(fixture_call_ref_null_consumable_erlang_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    My_null = undefined,
    Regular_null = undefined,
    consume(My_null),
    consume(Regular_null).
