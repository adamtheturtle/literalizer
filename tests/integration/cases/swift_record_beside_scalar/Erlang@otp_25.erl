-module(fixture_swift_record_beside_scalar_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"a" => 1},
        5
    ],
    My_data.
