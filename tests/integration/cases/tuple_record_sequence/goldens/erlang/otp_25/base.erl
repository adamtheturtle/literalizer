-module(fixture_tuple_record_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"call" => "send", "args" => [1, "email", "a@gmail.com", 100]},
        #{"call" => "recv", "args" => [2, "sms", "b@example.com", 200]}
    ],
    My_data.
