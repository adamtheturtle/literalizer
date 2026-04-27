-module(fixture_string_control_chars_erlang).
-export([x/0]).
x() ->
    My_data = [
        "line1\r\nline2",
        "line1\rline2",
        ""
    ],
    My_data.
