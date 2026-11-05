-module(fixture_call_empty_ref_key_erlang_collection_layout_multiline_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    External_value = 1,
    consume(External_value).
