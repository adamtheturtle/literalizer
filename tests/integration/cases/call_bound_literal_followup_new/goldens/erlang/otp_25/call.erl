-module(fixture_call_bound_literal_followup_new_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
consume(_) -> ok.
x() ->
    My_data = make_widget(42),
    consume(My_data).
