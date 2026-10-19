-module(fixture_next_line_string_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "x" => "\x{85}"
    },
    My_data.
