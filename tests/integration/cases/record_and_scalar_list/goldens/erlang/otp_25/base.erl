-module(fixture_record_and_scalar_list_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"a" => 1},
        2
    ],
    My_data.
