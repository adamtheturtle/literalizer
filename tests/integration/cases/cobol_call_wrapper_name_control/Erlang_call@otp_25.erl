-module(fixture_cobol_call_wrapper_name_control_erlang_call).
-export([x/0]).
check_wrapper(_) -> ok.
x() ->
    check_wrapper(42).
