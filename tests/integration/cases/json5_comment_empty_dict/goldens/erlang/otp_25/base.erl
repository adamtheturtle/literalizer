-module(fixture_json5_comment_empty_dict_erlang).
-export([x/0]).
x() ->
    % empty heading
    % empty body
    % after empty
    My_data = #{},
    My_data.
