-module(fixture_simple_sequence_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = [
        16#1,
        "hello",
        true,
        undefined
    ],
    My_data.
