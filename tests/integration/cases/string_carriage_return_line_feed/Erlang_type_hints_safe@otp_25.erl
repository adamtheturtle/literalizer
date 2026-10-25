-module(fixture_string_carriage_return_line_feed_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "cr" => "a\rb",
        "crlf" => "a\r\nb",
        "lf" => "a\nb"
    },
    My_data.
