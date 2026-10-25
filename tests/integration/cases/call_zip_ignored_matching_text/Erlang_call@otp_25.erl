-module(fixture_call_zip_ignored_matching_text_erlang_call).
-export([x/0]).
process(_) -> undefined.
x() ->
    process("time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC)").
