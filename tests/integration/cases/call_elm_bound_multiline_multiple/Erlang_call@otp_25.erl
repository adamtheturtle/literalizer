-module(fixture_call_elm_bound_multiline_multiple_erlang_call).
-export([x/0]).
f(_) -> ok.
x() ->
    Ref_data = [
        1,
        2
    ],
    f([
        Ref_data
    ]),
    f([
        Ref_data
    ]).
