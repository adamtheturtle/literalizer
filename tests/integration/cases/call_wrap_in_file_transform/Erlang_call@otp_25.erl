-module(fixture_call_wrap_in_file_transform_erlang_call).
-export([x/0]).
process(_, _) -> undefined.
x() ->
    process(1, 2).
