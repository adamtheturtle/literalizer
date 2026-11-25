-module(fixture_null_mapping_key_erlang).
-export([x/0]).
x() ->
    My_data = #{
        undefined => "null value",
        "None" => "string value"
    },
    My_data.
