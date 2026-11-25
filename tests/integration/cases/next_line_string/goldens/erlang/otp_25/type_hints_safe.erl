-module(fixture_next_line_string_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "x" => "\x{85}"
    },
    My_data.
