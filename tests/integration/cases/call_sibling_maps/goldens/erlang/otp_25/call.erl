-module(fixture_call_sibling_maps_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process(#{"value" => 1}),
    process(#{"value" => "hello"}).
