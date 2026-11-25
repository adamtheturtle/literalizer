-module(fixture_string_embedded_nul_erlang_string_embedded_nul).
-export([x/0]).
x() ->
    My_data = #{
        "x" => "\x{0}",
        "y" => "\x{0}1"
    },
    My_data.
