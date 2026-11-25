-module(fixture_tuple_record_seq_sibling_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "scores" => [10, 20, 30],
        "args" => [1, "email", "a@gmail.com", 100]
    },
    My_data.
