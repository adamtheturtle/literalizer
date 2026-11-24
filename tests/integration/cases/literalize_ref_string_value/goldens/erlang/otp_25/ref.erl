-module(fixture_literalize_ref_string_value_erlang_ref).
-export([x/0]).
x() ->
    Shared = "s",
    My_data = #{
        "value" => Shared
    },
    My_data.
