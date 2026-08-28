-module(fixture_yaml_unread_comment_slots_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "flow" => [
            1,
            % After the first element.
            2
        ],
        % Between the key and its value.
        "gap" => 3,
        % On the block scalar header.
        "block" => "Text.\n",
        "anchored" => 4,
        "alias" => 4
        % On the alias.
    },
    My_data.
