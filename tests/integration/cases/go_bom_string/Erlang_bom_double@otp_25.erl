-module(fixture_go_bom_string_erlang_bom_double).
-export([x/0]).
x() ->
    My_data = #{
        "x" => "﻿"
    },
    My_data.
