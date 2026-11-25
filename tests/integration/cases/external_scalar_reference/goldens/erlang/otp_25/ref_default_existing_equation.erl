-module(fixture_external_scalar_reference_erlang_ref_default_existing_equation).
-export([x/0]).
consume_widget(_) -> ok.
x() ->
    Shared = 1,
    My_data = Shared,
    consume_widget(My_data).
