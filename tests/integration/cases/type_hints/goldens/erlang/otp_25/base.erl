-module(fixture_type_hints_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "name" => "Alice",
        "age" => 30,
        "active" => true,
        "score" => undefined,
        "joined" => "2024-01-15",
        "last_login" => "2024-01-15T12:30:00+00:00",
        "avatar" => <<72, 101, 108, 108, 111>>
    },
    My_data.
