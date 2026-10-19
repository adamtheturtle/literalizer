-module(fixture_nested_record_sequences_erlang).
-export([x/0]).
x() ->
    My_data = [
        [#{"a" => 1}],
        [#{"a" => 2}]
    ],
    My_data.
