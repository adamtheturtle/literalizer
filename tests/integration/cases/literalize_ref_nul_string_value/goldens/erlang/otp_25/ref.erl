-module(fixture_literalize_ref_nul_string_value_erlang_ref).
-export([x/0]).
x() ->
    Shared = "a\x{0}b",
    My_data = #{
        "value" => Shared
    },
    My_data.
