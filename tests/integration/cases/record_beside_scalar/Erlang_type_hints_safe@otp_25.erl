-module(fixture_record_beside_scalar_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = [
        #{"a" => 1},
        5
    ],
    My_data.
