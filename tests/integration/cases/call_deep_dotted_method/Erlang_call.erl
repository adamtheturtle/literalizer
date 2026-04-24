-module(check).
-export([x/0]).
'obj.api.client.post'(_) -> ok.
x() ->
    'obj.api.client.post'("hello"),
    'obj.api.client.post'(42),
    'obj.api.client.post'(true).
