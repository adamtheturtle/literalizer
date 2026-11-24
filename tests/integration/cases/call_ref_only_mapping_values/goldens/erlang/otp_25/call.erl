-module(fixture_call_ref_only_mapping_values_erlang_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Item = 42,
    consume(#{"field" => Item}).
