-module(fixture_zig_delete_string_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "v" => "ab",
        "ab" => 1
    },
    My_data.
