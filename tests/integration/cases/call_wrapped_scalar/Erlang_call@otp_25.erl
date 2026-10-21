-module(fixture_call_wrapped_scalar_erlang_call).
-export([x/0]).
make_widget(_) -> ok.
x() ->
    make_widget(1).
