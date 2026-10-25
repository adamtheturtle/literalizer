-module(fixture_yaml_encoding_cookie_comment_erlang).
-export([x/0]).
x() ->
    % coding: ascii
    My_data = "café",
    My_data.
