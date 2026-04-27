-module(check).
-export([x/0]).
'my_app.http_client.fetch'(_) -> ok.
x() ->
    'my_app.http_client.fetch'("hello"),
    'my_app.http_client.fetch'(42),
    'my_app.http_client.fetch'(true).
