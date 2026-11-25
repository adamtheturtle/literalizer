-module(fixture_call_dotted_parameter_matches_root_erlang_call).
-export([x/0]).
'outer.inner'(_, _) -> ok.
x() ->
    'outer.inner'(1, 2).
