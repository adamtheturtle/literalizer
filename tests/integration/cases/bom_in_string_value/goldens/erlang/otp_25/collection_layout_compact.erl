-module(fixture_bom_in_string_value_erlang_collection_layout_compact).
-export([x/0]).
x() ->
    My_data = #{
        "v" => "a﻿b"
    },
    My_data.
