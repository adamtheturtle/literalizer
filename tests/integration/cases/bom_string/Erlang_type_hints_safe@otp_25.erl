-module(fixture_bom_string_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "x" => "﻿"
    },
    My_data.
