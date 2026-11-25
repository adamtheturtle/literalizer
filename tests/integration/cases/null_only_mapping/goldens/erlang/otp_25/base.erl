-module(fixture_null_only_mapping_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "value" => undefined
    },
    My_data.
