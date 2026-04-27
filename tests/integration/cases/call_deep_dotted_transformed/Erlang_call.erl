-module(fixture_call_deep_dotted_transformed_erlang_call).
-export([x/0]).
'app.client.fetch'(_) -> undefined.
emit(_) -> ok.
x() ->
    emit('app.client.fetch'("hello")),
    emit('app.client.fetch'(42)),
    emit('app.client.fetch'(true)).
