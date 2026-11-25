-module(fixture_del_nel_and_c1_control_strings_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "del" => "ab",
        "nel" => "a\x{85}b",
        "c1" => "ab"
    },
    My_data.
