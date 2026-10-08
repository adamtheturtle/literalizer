-module(fixture_toml_table_string_punctuation_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "comma_hash" => "a,#b",
        "comma_space_hash" => "trail, # comment",
        "escaped_quote" => "quote \" and , #",
        "next_line" => "x\x{85}y",
        "line_separator" => "x\x{2028}y",
        "paragraph_separator" => "x\x{2029}y"
    },
    My_data.
