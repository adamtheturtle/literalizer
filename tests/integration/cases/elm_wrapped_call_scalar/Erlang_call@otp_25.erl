-module(fixture_elm_wrapped_call_scalar_erlang_call).
-export([x/0]).
make_widget(_) -> ok.
x() ->
    make_widget(1).
