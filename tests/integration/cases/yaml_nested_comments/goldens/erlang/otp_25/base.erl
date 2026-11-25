-module(fixture_yaml_nested_comments_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => #{
            % inner note
            "b" => 1  % inline b
        },
        "list" => [
            1,  % first
            2  % second
        ]
    },
    My_data.
