-module(fixture_systemverilog_keyword_case_parameter_erlang_call).
-export([x/0]).
make_widget(_) -> ok.
x() ->
    make_widget(1).
