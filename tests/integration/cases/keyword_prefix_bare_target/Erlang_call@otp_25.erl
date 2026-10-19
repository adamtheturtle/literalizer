-module(fixture_keyword_prefix_bare_target_erlang_call).
-export([x/0]).
first_value(_) -> ok.
x() ->
    first_value(1).
