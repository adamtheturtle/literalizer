-module(fixture_call_dotted_mixed_empty_arguments_erlang_collection_layout_compact_call).
-export([x/0]).
'thing.go'(_, _, _) -> undefined.
x() ->
    'thing.go'([], [1], []),
    'thing.go'(["text"], [2], []),
    'thing.go'([], ["text"], []),
    'thing.go'(["text"], [2], [3]).
