-module(fixture_default_helper_name_allocator_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 1
    },
    My_data.
