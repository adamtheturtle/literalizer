-module(fixture_opt_in_record_example_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "name" => "Ada",
        "active" => true,
        "scores" => [1, 2, 3]
    },
    My_data.
