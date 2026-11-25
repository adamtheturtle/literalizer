-module(fixture_call_multiline_list_argument_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process([
        1,
        2
    ]),
    process([
        3
    ]).
