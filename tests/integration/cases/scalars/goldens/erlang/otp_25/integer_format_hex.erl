-module(fixture_scalars_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = [
        16#2A,
        3.14,
        true,
        false,
        "hello \"world\""
    ],
    My_data.
