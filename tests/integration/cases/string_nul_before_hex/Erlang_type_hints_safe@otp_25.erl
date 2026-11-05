-module(fixture_string_nul_before_hex_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "x" => "before\x{0}after"
    },
    My_data.
