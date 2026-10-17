-module(fixture_non_identifier_mapping_key_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "not-a-field" => 1
    },
    My_data.
