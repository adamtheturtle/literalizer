-module(fixture_binary_erlang_bytes_format_base64).
-export([x/0]).
x() ->
    My_data = [
        "SGVsbG8="
    ],
    My_data.
