-module(fixture_call_quoted_atom_target_erlang_call).
-export([x/0]).
'DoThing'(_) -> ok.
x() ->
    'DoThing'(1),
    'DoThing'(2).
