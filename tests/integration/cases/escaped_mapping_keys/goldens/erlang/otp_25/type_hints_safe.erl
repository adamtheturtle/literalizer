-module(fixture_escaped_mapping_keys_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "quote\"backslash\\" => 1,
        "line\nbreak" => 2,
        "$(literal)${text}" => 3,
        "RStr prefix" => 4
    },
    My_data.
