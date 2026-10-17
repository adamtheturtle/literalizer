-module(fixture_elm_wrapped_call_empty_list_erlang_call).
-export([x/0]).
make_widget(_) -> ok.
x() ->
    make_widget([]).
