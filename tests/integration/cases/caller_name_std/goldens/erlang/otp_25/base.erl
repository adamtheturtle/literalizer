-module(fixture_caller_name_std_erlang).
-export([x/0]).
x() ->
    Std = #{
        "a" => 1
    },
    Std.
