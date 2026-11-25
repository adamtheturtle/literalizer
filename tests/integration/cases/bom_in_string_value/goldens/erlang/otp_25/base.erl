-module(fixture_bom_in_string_value_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "v" => "a﻿b"
    },
    My_data.
