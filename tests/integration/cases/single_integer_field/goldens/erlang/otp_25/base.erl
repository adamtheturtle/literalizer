-module(fixture_single_integer_field_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "x" => 1
    },
    My_data.
