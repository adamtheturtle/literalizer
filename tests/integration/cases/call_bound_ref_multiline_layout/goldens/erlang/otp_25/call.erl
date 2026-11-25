-module(fixture_call_bound_ref_multiline_layout_erlang_call).
-export([x/0]).
f(_) -> ok.
x() ->
    Ref_data = [
        [
            1,
            2
        ],
        [
            3,
            4
        ]
    ],
    f([
        [
            Ref_data
        ]
    ]).
