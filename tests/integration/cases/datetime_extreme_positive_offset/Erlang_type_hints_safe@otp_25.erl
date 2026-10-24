-module(fixture_datetime_extreme_positive_offset_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = "2020-06-15T12:00:00+23:59",
    My_data.
