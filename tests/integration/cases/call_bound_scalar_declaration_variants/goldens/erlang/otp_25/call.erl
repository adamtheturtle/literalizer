-module(fixture_call_bound_scalar_declaration_variants_erlang_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Shared = 42,
    consume(Shared).
