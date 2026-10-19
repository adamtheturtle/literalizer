-module(fixture_bom_string_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "x" => "﻿"
    },
    My_data.
