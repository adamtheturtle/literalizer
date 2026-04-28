-module(fixture_call_deep_dotted_method_erlang_call).
-export([x/0]).
'obj.api.client.post'(_) -> ok.
x() ->
    'obj.api.client.post'("hello"),
    'obj.api.client.post'(42),
    'obj.api.client.post'(true).
