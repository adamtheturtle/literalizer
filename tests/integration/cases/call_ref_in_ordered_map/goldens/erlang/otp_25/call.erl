-module(fixture_call_ref_in_ordered_map_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    Big_list = [
        "x"
    ],
    process([{"m", Big_list}]).
