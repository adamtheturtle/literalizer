-module(fixture_uniform_mixed_num_dicts_in_seq_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"x" => 1, "y" => 2.5},
        #{"x" => 3, "y" => 4.0}
    ],
    My_data.
