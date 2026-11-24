-module(fixture_call_trailing_underscore_parameter_erlang_call).
-export([x/0]).
do_thing(_) -> ok.
x() ->
    do_thing(1),
    do_thing(2).
