-module(fixture_call_reserved_property_name_erlang_call).
-export([x/0]).
'foo.class'(_) -> ok.
x() ->
    'foo.class'(1).
