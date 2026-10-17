-module(fixture_noncolliding_stringified_mapping_keys_erlang).
-export([x/0]).
x() ->
    My_data = #{
        1 => "integer",
        "2" => "string"
    },
    My_data.
