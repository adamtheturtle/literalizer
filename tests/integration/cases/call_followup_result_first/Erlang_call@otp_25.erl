-module(fixture_call_followup_result_first_erlang_call).
-export([x/0]).
make_widget(_, _) -> undefined.
consume(_, _) -> ok.
x() ->
    My_data = make_widget(42, 3),
    consume(My_data, 3).
