-module(fixture_erlang_noncharacter_string_erlang_noncharacter_string).
-export([x/0]).
x() ->
    My_data = #{
        "fffe" => [65534],
        "ffff" => [65535]
    },
    My_data.
