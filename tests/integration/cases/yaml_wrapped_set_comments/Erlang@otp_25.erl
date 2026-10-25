-module(fixture_yaml_wrapped_set_comments_erlang).
-export([x/0]).
x() ->
    My_data = sets:from_list([
        10,  % comment for ten
        2  % comment for two
    ]),
    My_data.
