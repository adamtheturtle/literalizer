-module(fixture_call_no_params_erlang_call).
-export([x/0]).
process() -> ok.
x() ->
    process(),
    process().
