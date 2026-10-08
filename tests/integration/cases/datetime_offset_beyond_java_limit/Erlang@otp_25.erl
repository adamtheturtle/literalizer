-module(fixture_datetime_offset_beyond_java_limit_erlang).
-export([x/0]).
x() ->
    My_data = "2020-06-15T12:00:00+23:59",
    My_data.
