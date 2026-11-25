-module(fixture_literalize_ref_unresolved_unrelated_values_erlang_ref_default).
-export([x/0]).
consume_widget(_) -> ok.
x() ->
    A = 0,
    My_data = [
        A,
        1
    ],
    consume_widget(My_data).
