-module(fixture_zig_default_helper_name_arena_erlang).
-export([x/0]).
x() ->
    Arena = #{
        "a" => 1
    },
    Arena.
