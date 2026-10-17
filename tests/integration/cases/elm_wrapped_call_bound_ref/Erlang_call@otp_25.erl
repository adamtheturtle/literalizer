-module(fixture_elm_wrapped_call_bound_ref_erlang_call).
-export([x/0]).
make_widget(_) -> ok.
x() ->
    Value = 1,
    make_widget(Value).
