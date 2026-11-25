-module(fixture_yaml_partially_outdented_comment_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => #{
            "b" => [1],
            % Outdented from the sequence, so the inner mapping claims this.
            "c" => 2
        },
        % Outdented from the inner mapping too, so the root claims this.
        "d" => 3
    },
    My_data.
