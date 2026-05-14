-module(fixture_record_basic_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "id" => 1,
        "description" => "example",
        "is_done" => false,
        "blocks" => [1, 2, 3]
    },
    My_data.
