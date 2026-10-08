-module(fixture_nim_root_dollar_ref_is_data_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "$ref" => "schema.json"
    },
    My_data.
