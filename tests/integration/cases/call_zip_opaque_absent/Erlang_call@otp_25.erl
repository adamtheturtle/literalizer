-module(fixture_call_zip_opaque_absent_erlang_call).
-export([x/0]).
process(_) -> undefined.
x() ->
    process(1).
