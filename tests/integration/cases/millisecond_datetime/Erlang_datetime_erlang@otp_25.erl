-module(fixture_millisecond_datetime_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "half" => {{1979, 5, 27}, {7, 32, 0}},
        "milli" => {{1979, 5, 27}, {7, 32, 0}},
        "max_milli" => {{1979, 5, 27}, {7, 32, 0}},
        "whole" => {{1979, 5, 27}, {7, 32, 0}}
    },
    My_data.
