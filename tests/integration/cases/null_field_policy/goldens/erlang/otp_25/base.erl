-module(fixture_null_field_policy_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "drop" => undefined,
        "keep" => 1
    },
    My_data.
