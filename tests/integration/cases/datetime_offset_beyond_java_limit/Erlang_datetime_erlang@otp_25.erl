-module(fixture_datetime_offset_beyond_java_limit_erlang_datetime_erlang).
-export([x/0]).
x() ->
    My_data = {{2020, 6, 15}, {12, 0, 0}},
    My_data.
