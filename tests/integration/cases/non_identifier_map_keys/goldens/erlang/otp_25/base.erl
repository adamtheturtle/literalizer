-module(fixture_non_identifier_map_keys_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a-b" => 1,
        "two words" => 2,
        "she said \"hi\"" => 3,
        "" => 4,
        "valid_key" => 5
    },
    My_data.
