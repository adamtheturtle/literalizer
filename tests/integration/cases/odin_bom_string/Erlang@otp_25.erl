-module(fixture_odin_bom_string_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "v" => "a﻿b"
    },
    My_data.
