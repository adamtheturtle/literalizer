-module(fixture_systemverilog_keyword_case_bare_target_erlang_call).
-export([x/0]).
'Before'(_) -> ok.
x() ->
    'Before'(1).
