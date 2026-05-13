-module(fixture_call_variable_form_new_erlang_call).
-export([x/0]).
x() ->
    make_widget(_) -> undefined.
    Result = make_widget(42),
    Result.
