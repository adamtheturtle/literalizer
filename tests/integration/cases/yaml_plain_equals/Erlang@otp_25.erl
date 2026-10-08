-module(fixture_yaml_plain_equals_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "x" => "="
        % unrelated
    },
    My_data.
