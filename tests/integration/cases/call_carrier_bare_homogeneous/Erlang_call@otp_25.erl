-module(fixture_call_carrier_bare_homogeneous_erlang_call).
-export([x/0]).
make_widget(_, _) -> ok.
x() ->
    make_widget([1], [2]).
