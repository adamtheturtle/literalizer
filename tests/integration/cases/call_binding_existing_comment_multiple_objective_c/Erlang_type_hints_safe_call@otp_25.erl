-module(fixture_call_binding_existing_comment_multiple_objective_c_erlang_type_hints_safe_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = 42,
    My_data = make_widget(My_data) // note
    // extra,
    make_widget(My_data).
