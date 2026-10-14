-module(fixture_call_binding_existing_seeded_erlang_type_hints_safe_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = make_widget(42),
    My_data = make_widget(My_data),
    make_widget(My_data).
