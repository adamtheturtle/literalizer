-module(fixture_zig_default_helper_name_allocator_erlang).
-export([x/0]).
x() ->
    Allocator = #{
        "a" => 1
    },
    Allocator.
