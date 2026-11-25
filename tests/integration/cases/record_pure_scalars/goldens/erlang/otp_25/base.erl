-module(fixture_record_pure_scalars_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "name" => "Alice",
        "age" => 30,
        "active" => true,
        "score" => 4.5
    },
    My_data.
