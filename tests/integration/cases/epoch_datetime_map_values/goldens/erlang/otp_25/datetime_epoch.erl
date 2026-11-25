-module(fixture_epoch_datetime_map_values_erlang_datetime_epoch).
-export([x/0]).
x() ->
    My_data = #{
        "within_i32" => 1705320000,
        "beyond_i32" => 4085195400
    },
    My_data.
