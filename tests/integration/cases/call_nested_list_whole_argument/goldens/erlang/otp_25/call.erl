-module(fixture_call_nested_list_whole_argument_erlang_call).
-export([x/0]).
f(_) -> ok.
x() ->
    f([[1, 2], [3]]).
