-module(fixture_literalize_ref_cpp_string_pointer_erlang_ref).
-export([x/0]).
x() ->
    Shared = "s",
    My_data = #{
        "value" => Shared
    },
    My_data.
