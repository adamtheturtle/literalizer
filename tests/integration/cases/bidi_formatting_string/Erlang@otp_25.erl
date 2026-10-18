-module(fixture_bidi_formatting_string_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "v" => "a‪‫‬‭‮⁦⁧⁨⁩b"
    },
    My_data.
