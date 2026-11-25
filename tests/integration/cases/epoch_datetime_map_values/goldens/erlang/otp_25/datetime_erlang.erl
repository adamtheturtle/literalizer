-module(fixture_epoch_datetime_map_values_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "within_i32" => {{2024, 1, 15}, {12, 0, 0}},
        "beyond_i32" => {{2099, 6, 15}, {8, 30, 0}}
    },
    My_data.
