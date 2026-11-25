-module(fixture_call_wrapped_empty_list_erlang_call).
-export([x/0]).
make_widget(_) -> ok.
x() ->
    make_widget([]).
