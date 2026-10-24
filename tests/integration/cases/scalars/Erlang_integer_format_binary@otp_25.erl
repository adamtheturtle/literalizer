-module(fixture_scalars_erlang_integer_format_binary).
-export([x/0]).
x() ->
    My_data = [
        2#101010,
        3.14,
        true,
        false,
        "hello \"world\""
    ],
    My_data.
