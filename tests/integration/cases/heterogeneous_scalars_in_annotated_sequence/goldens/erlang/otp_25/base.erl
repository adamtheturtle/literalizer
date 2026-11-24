-module(fixture_heterogeneous_scalars_in_annotated_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        true,
        1.5,
        undefined,
        "2020-01-01",
        "2020-01-01T00:00:00+00:00",
        []
    ],
    My_data.
