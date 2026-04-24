-module(check).
-export([x/0]).
'app.client.fetch'(_) -> undefined.
emit(_) -> ok.
x() ->
    emit('app.client.fetch'("hello")),
    emit('app.client.fetch'(42)),
    emit('app.client.fetch'(true)).
