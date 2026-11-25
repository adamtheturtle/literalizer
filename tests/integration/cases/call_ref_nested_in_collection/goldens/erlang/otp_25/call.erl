-module(fixture_call_ref_nested_in_collection_erlang_call).
-export([x/0]).
process(_, _) -> ok.
x() ->
    Big_list = [
        "x"
    ],
    process(#{"k" => Big_list}, 2).
