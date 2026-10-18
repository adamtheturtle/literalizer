-module(fixture_bidi_formatting_string_with_nul_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "v" => "a‪\x{0}é😀b"
    },
    My_data.
