-module(fixture_tuple_record_field_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "call" => "send",
        "args" => [1, "email", "a@gmail.com", 100]
    },
    My_data.
