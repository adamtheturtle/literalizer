-module(fixture_nested_i32_and_i64_records_erlang).
-export([x/0]).
x() ->
    My_data = [
        [#{"value" => 1}],
        [#{"value" => 1099511627776}]
    ],
    My_data.
