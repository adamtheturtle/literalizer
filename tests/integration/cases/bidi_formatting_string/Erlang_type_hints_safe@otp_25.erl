-module(fixture_bidi_formatting_string_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "v" => "a‪‫‬‭‮⁦⁧⁨⁩b"
    },
    My_data.
