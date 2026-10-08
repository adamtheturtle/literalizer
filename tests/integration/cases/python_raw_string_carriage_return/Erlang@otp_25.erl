-module(fixture_python_raw_string_carriage_return_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "cr" => "a\rb",
        "crlf" => "a\r\nb",
        "lf" => "a\nb"
    },
    My_data.
