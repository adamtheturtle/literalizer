-module(fixture_noncharacter_string_erlang_type_hints_safe).
-export([x/0]).
x() ->
    My_data = #{
        "fffe" => [65534],
        "ffff" => [65535]
    },
    My_data.
