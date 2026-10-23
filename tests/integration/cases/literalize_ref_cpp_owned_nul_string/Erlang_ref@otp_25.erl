-module(fixture_literalize_ref_cpp_owned_nul_string_erlang_ref).
-export([x/0]).
x() ->
    Shared = "a\x{0}b",
    My_data = #{
        "value" => Shared
    },
    My_data.
