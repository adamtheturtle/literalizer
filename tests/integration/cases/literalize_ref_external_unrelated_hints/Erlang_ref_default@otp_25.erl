-module(fixture_literalize_ref_external_unrelated_hints_erlang_ref_default).
-export([x/0]).
consume_widget(_) -> ok.
x() ->
    Missing = [
        1,
        2
    ],
    My_data = Missing,
    consume_widget(My_data).
