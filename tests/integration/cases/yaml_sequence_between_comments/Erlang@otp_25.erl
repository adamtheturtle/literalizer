-module(fixture_yaml_sequence_between_comments_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"item" => "existing"},
        % This comment describes the next item.
        #{"item" => "next"}
    ],
    My_data.
