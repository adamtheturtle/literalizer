-module(fixture_call_nim_empty_statement_erlang_call).
-export([x/0]).
make_widget(_) -> ok.
x() ->
    make_widget([]).
