-module(check).
-export([x/0]).
'app.client.fetch'(_) -> ok.
x() ->
    'app.client.fetch'("hello"),
    'app.client.fetch'(42),
    'app.client.fetch'(true).
