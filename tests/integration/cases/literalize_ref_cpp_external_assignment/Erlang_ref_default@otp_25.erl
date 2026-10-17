-module(fixture_literalize_ref_cpp_external_assignment_erlang_ref_default).
-export([x/0]).
consume_widget(_) -> ok.
x() ->
    Ref_data = [
        1,
        2
    ],
    My_data = [
        0
    ],
    consume_widget(My_data),
    My_data = Ref_data,
    consume_widget(My_data).
