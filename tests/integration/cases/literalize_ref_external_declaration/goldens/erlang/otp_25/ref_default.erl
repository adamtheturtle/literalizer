-module(fixture_literalize_ref_external_declaration_erlang_ref_default).
-export([x/0]).
consume_widget(_) -> ok.
x() ->
    Shared = [
        1,
        2
    ],
    My_data = Shared,
    consume_widget(My_data).
