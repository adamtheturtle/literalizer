-module(fixture_call_zip_opaque_omitted_erlang_call).
-export([x/0]).
process(_) -> undefined.
x() ->
    process(1).
