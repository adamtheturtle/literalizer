-module(fixture_call_wrap_in_file_erlang_call).
-export([x/0]).
process(_, _) -> ok.
x() ->
    process(1, 2),
    process(3, 4).
