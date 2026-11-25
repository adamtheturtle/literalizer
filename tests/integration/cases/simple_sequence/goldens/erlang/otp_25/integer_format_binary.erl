-module(fixture_simple_sequence_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = [
        2#1,
        "hello",
        true,
        undefined
    ],
    My_data.
