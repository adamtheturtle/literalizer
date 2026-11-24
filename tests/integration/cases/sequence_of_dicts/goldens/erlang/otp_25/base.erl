-module(fixture_sequence_of_dicts_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"name" => "Alice", "age" => 30},
        #{"name" => "Bob", "age" => 25}
    ],
    My_data.
